"""Comparison pilot: does semantic recall still degrade with position for current models?

Two arms under the SAME prompt template, filler and scoring, so they can be compared directly:

  semtrace  - arm A (group outline, D1): SemTrace re-implemented from the description of
              2505.13353 (Listing 1): f(x) builds a list of k in [4,10] slots, each slot assigned
              x +/- y with |y| of `digits` digits, assignment lines in random order.
              digits = 2 (as in [2]) and 4 (group's H1).
  toolz     - arm B (workspace, C1'-mini): anonymised toolz items with k_core == 1 that the model
              solved 3/3 in the oracle calibration (results/toolz_anon_oracle_calib.jsonl).

Lengths: 0 = oracle (only the target function, no filler) and the given long lengths.
Layouts: start / middle / end. Tasks: semantic (all) + lexical (middle only, sanity check).
Filler: anonymised toolz units, then stdlib (ContextBuilder). Thinking explicitly disabled.

  .venv/bin/python experiments/compare_pilot.py --model gemma-3-27b-it --lengths 0,16000 \
      --out experiments/results/compare_gemma.jsonl
"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from build_contexts import ContextBuilder  # noqa: E402
from run_eval import call, creds, score, same_value  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "experiments/data/toolz_anon")
CALIB = os.path.join(ROOT, "experiments/results/toolz_anon_oracle_calib.jsonl")


def semtrace_item(i, digits, seed):
    rng = random.Random(f"semtrace|{digits}|{i}|{seed}")
    k = rng.randint(4, 10)
    name = "fn_" + "".join(rng.choice("0123456789abcdef") for _ in range(6))
    x = rng.randint(10, 99) if digits == 2 else rng.randint(1000, 9999)
    lo, hi = (-100, 99) if digits == 2 else (-10000, 9999)
    ys = [rng.randint(lo, hi) for _ in range(k)]
    lines = [f"    arr[{j}] = x {'+' if y >= 0 else '-'} {abs(y)}\n" for j, y in enumerate(ys)]
    rng.shuffle(lines)
    src = f"def {name}(x):\n    arr = [0] * {k}\n" + "".join(lines) + "    return arr\n"
    ns = {}
    exec(src, ns)
    answer = repr(ns[name](x))
    uid = f"semtrace/gen.py::{name}"
    unit = {"uid": uid, "file": "semtrace/gen.py", "name": name, "source": src}
    item = {"id": f"semtrace{digits}-{i:03d}", "k_core": 1, "core_fragments": [uid], "setup": "",
            "expr": f"{name}({x})", "answer": answer, "mutated": True, "digits": digits, "k": k}
    return item, unit


def toolz_solvable(n):
    items = {it["id"]: it for it in map(json.loads, open(DATA + "_items.jsonl", encoding="utf-8"))}
    hits = {}
    for r in map(json.loads, open(CALIB, encoding="utf-8")):
        if r.get("task") == "semantic" and len(r["requested"]) == 1:
            hits.setdefault(r["item"], []).append(bool(r.get("correct")))
    ids = sorted(i for i, h in hits.items() if len(h) >= 3 and all(h) and items[i]["k_core"] == 1)
    return [items[i] for i in ids][:n]


def partial(pred, gold):
    import ast
    try:
        p, g = ast.literal_eval(pred), ast.literal_eval(gold)
    except Exception:
        return 0.0
    if not isinstance(p, list) or not isinstance(g, list):
        return float(p == g)
    return sum(a == b for a, b in zip(p, g)) / len(g)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--lengths", default="0,16000")
    ap.add_argument("--n-semtrace", type=int, default=30, help="items per digit setting")
    ap.add_argument("--n-toolz", type=int, default=36)
    ap.add_argument("--arms", default="semtrace,toolz")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cb = ContextBuilder(DATA + "_units.json", "toolz")
    jobs = []  # (job, item, extra_unit)
    arms = args.arms.split(",")
    pool = []
    if "semtrace" in arms:
        for d in (2, 4):
            pool += [("semtrace",) + semtrace_item(i, d, args.seed) for i in range(args.n_semtrace)]
    if "toolz" in arms:
        pool += [("toolz", it, None) for it in toolz_solvable(args.n_toolz)]

    for arm, it, unit in pool:
        if unit:
            cb.units[unit["uid"]] = unit
        for length in map(int, args.lengths.split(",")):
            for layout in (["middle"] if length == 0 else ["start", "middle", "end"]):
                tasks = ["semantic"] + (["lexical"] if layout == "middle" and length else [])
                for task in tasks:
                    j = cb.build(it, layout, length, task)
                    j.update(arm=arm, layout="oracle" if length == 0 else layout,
                             digits=it.get("digits"))
                    jobs.append((j, it, unit))
        if unit:
            del cb.units[unit["uid"]]

    # resume: skip cells already answered without error in --out (re-runs only failed/missing calls)
    if os.path.exists(args.out):
        done = {(r["item"], r["task"], r["layout"], r["length"])
                for r in map(json.loads, open(args.out, encoding="utf-8")) if "error" not in r}
        jobs = [t for t in jobs if (t[0]["item"], t[0]["task"], t[0]["layout"], t[0]["length"]) not in done]

    print(f"{len(pool)} items, {len(jobs)} calls, "
          f"~{sum(j['est_tokens'] for j, _, _ in jobs)/1e6:.2f}M input tokens (estimated)")
    if args.dry_run:
        return

    base, key = creds()
    max_tok = {"semantic": 300, "lexical": 2000}

    def work(arg):
        job, it, unit = arg
        res = call(base, key, args.model, job["prompt"], max_tok[job["task"]])
        rec = {**{k: v for k, v in job.items() if k != "prompt"}, **res, "model": args.model,
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
        if "error" not in res:
            units = dict(cb.units)
            if unit:
                units[unit["uid"]] = unit
            score(rec, it, units)
            if job["task"] == "semantic":
                rec["partial"] = partial(rec["pred"], it["answer"])
        return rec

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "a", encoding="utf-8") as f, cf.ThreadPoolExecutor(args.workers) as ex:
        for rec in ex.map(work, jobs):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if "error" in rec:
                print("ERROR", rec["item"], rec["task"], rec["error"][:120])
    print("done ->", args.out)


if __name__ == "__main__":
    main()
