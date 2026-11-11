"""Run prompts against an OpenAI-compatible endpoint and score them.

Reads LLM_BASE_URL / LLM_API_KEY from the environment, else from .claude/settings.local.json.
Thinking is explicitly DISABLED (it is ON by default for DeepSeek-V4-Flash on this endpoint and
would turn every semantic call into an implicit retrieve-then-trace).

Pilot (default): N items with k_core == 1 and N with k_core >= 2 (mutated items only),
all layouts, one length, tasks semantic + lexical (+ rtt for k>=2) + nocontext.

  .venv/bin/python experiments/run_eval.py --n 5 --lengths 16000 --out experiments/results/pilot.jsonl
"""
import argparse
import ast
import concurrent.futures as cf
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from build_contexts import ContextBuilder, layouts_for  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def creds():
    base, key = os.environ.get("LLM_BASE_URL"), os.environ.get("LLM_API_KEY")
    if not (base and key):
        env = json.load(open(os.path.join(ROOT, ".claude/settings.local.json")))["env"]
        base, key = env["LLM_BASE_URL"], env["LLM_API_KEY"]
    return base.rstrip("/"), key


def call(base, key, model, prompt, max_tokens, retries=4):
    body = {"model": model, "temperature": 0, "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "thinking": {"type": "disabled"}}
    data = json.dumps(body).encode()
    for attempt in range(retries):
        req = urllib.request.Request(base + "/chat/completions", data=data, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json"})
        t = time.time()
        try:
            r = json.load(urllib.request.urlopen(req, timeout=600))
            m = r["choices"][0]["message"]
            return {"output": m.get("content") or "", "usage": r.get("usage", {}),
                    "latency": round(time.time() - t, 2), "model_returned": r.get("model"),
                    "reasoning_chars": len(m.get("reasoning_content") or "")}
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}: {e.read()[:200]!r}"
            if e.code not in (429, 500, 502, 503, 504, 520, 522, 524):
                return {"error": err}
        except Exception as e:  # timeouts, connection resets
            err = repr(e)
        time.sleep(2 ** attempt * 3)
    return {"error": err}


# ---------------------------------------------------------------- scoring
def strip_fences(s):
    return re.sub(r"```[a-zA-Z]*", "", s)


def same_value(pred, gold):
    pred = pred.strip().strip("`").strip()
    if " ".join(pred.split()) == " ".join(gold.split()):
        return True
    try:
        return ast.literal_eval(pred) == ast.literal_eval(gold)
    except Exception:
        return False


def semantic_pred(output, task):
    m = re.findall(r"ANSWER:\s*(.+)", output)
    if m:
        return m[-1].strip()
    if task == "rtt":
        return ""
    lines = [l for l in strip_fences(output).splitlines() if l.strip()]
    return lines[-1] if lines else ""


def norm_code(s):
    return "\n".join(l.rstrip() for l in strip_fences(s).splitlines() if l.strip())


def copy_score(output, requested, units):
    """Fraction of requested fragments reproduced verbatim (modulo blank lines/trailing space)."""
    out = norm_code(output)
    hits = sum(norm_code(units[uid]["source"]) in out for uid in requested)
    return hits / len(requested) if requested else None


def score(rec, item, units):
    out = rec.get("output", "")
    if rec["task"] in ("semantic", "nocontext", "rtt"):
        rec["pred"] = semantic_pred(out, rec["task"])
        rec["correct"] = same_value(rec["pred"], item["answer"])
        orig = item.get("orig_answer")
        rec["memorised_orig"] = bool(orig) and orig != item["answer"] and same_value(rec["pred"], orig)
    if rec["task"] in ("lexical", "rtt"):
        rec["copy"] = copy_score(out, rec["requested"], units)
    return rec


# ---------------------------------------------------------------- main
def pick_items(items, n, seed, k_groups=("1", "2+"), exclude=()):
    """n mutated, non-guessable items per k-group: "3" means k_core == 3, "2+" means k_core >= 2."""
    rng = random.Random(seed)
    pool = [it for it in items if it["mutated"] and it["id"] not in exclude]
    chosen = []
    for g in k_groups:
        lo = int(g.rstrip("+"))
        grp = [it for it in pool if (it["k_core"] >= lo if g.endswith("+") else it["k_core"] == lo)]
        rng.shuffle(grp)
        chosen += grp[:n]
    return chosen


def guessable_ids(path):
    """Items answered correctly without code in any repeat (from nocontext_filter.py)."""
    if not path:
        return set()
    return {r["item"] for r in map(json.loads, open(path, encoding="utf-8")) if r.get("correct")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(ROOT, "experiments/data/toolz"))
    ap.add_argument("--lib", default="toolz")
    ap.add_argument("--model", default="DeepSeek-V4-Flash")
    ap.add_argument("--n", type=int, default=5, help="items per k-group")
    ap.add_argument("--lengths", default="16000")
    ap.add_argument("--tasks", default="semantic,lexical,rtt,nocontext")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default=os.path.join(ROOT, "experiments/results/pilot.jsonl"))
    ap.add_argument("--k-groups", default="1,2+", help='e.g. "1,3" (exact) or "1,2+" (>=2)')
    ap.add_argument("--exclude-guessable", default=None, help="*_nocontext.jsonl from nocontext_filter.py")
    ap.add_argument("--drop-degenerate", action="store_true", help="drop items flagged degenerate in the data")
    ap.add_argument("--filler-seed", type=int, default=0, help="layout-independent filler seed (replication dimension)")
    ap.add_argument("--dry-run", action="store_true", help="build prompts only, no API calls")
    args = ap.parse_args()

    items = [json.loads(l) for l in open(args.data + "_items.jsonl", encoding="utf-8")]
    if args.drop_degenerate:
        items = [i for i in items if not i.get("degenerate")]
    chosen = pick_items(items, args.n, args.seed, tuple(args.k_groups.split(",")),
                        guessable_ids(args.exclude_guessable))
    by_id = {it["id"]: it for it in items}
    cb = ContextBuilder(args.data + "_units.json", args.lib)
    tasks = args.tasks.split(",")

    jobs = []
    for it in chosen:
        if "nocontext" in tasks:
            jobs.append(cb.nocontext(it))
        for length in map(int, args.lengths.split(",")):
            # length 0 = "oracle": only the item's fragments, no filler (intrinsic difficulty)
            for layout in (layouts_for(it)[:1] if length == 0 else layouts_for(it)):
                for task in tasks:
                    if task == "nocontext" or (task == "rtt" and it["k_core"] == 1):
                        continue
                    job = cb.build(it, layout, length, task, seed=args.filler_seed)
                    if length == 0:
                        job["layout"] = "oracle"
                    jobs.append(job)
    print(f"{len(chosen)} items, {len(jobs)} calls, "
          f"~{sum(j['est_tokens'] for j in jobs)/1e6:.2f}M input tokens (estimated)")
    if args.dry_run:
        return

    base, key = creds()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    max_tok = {"semantic": 300, "nocontext": 300, "lexical": 4000, "rtt": 5000}

    def work(job):
        res = call(base, key, args.model, job["prompt"], max_tok[job["task"]])
        rec = {**{k: v for k, v in job.items() if k != "prompt"}, **res, "model": args.model,
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
        if "error" not in res:
            score(rec, by_id[job["item"]], cb.units)
        return rec

    done = 0
    with open(args.out, "a", encoding="utf-8") as f, cf.ThreadPoolExecutor(args.workers) as ex:
        for rec in ex.map(work, jobs):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            done += 1
            if "error" in rec:
                print("ERROR", rec["item"], rec["task"], rec["error"])
    print(f"done {done} -> {args.out}")


if __name__ == "__main__":
    main()
