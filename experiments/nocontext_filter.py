"""Ask every item WITHOUT code (3 repeats) to find guessable / memorised items.

  .venv/bin/python experiments/nocontext_filter.py --reps 3
Writes experiments/results/<lib>_nocontext.jsonl; items correct in >=1 repeat are 'guessable'.
"""
import argparse, concurrent.futures as cf, json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from build_contexts import ContextBuilder
from run_eval import ROOT, call, creds, score

ap = argparse.ArgumentParser()
ap.add_argument("--lib", default="toolz")
ap.add_argument("--data", default=None, help="dataset prefix, default experiments/data/<lib>")
ap.add_argument("--label", default=None, help="library name shown in the prompt")
ap.add_argument("--model", default="DeepSeek-V4-Flash")
ap.add_argument("--reps", type=int, default=3)
ap.add_argument("--workers", type=int, default=4)
args = ap.parse_args()
data = args.data or os.path.join(ROOT, f"experiments/data/{args.lib}")
items = [json.loads(l) for l in open(data + "_items.jsonl")]
cb = ContextBuilder(data + "_units.json", args.label or args.lib)
base, key = creds()
jobs = [(it, r) for it in items for r in range(args.reps)]

def work(job):
    it, r = job
    j = cb.nocontext(it)
    res = call(base, key, args.model, j["prompt"], 300)
    rec = {**{k: v for k, v in j.items() if k != "prompt"}, **res, "rep": r, "model": args.model,
           "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    return score(rec, it, cb.units) if "error" not in res else rec

out = os.path.join(ROOT, f"experiments/results/{os.path.basename(data)}_nocontext.jsonl")
with open(out, "w") as f, cf.ThreadPoolExecutor(args.workers) as ex:
    recs = list(ex.map(work, jobs))
    for rec in recs:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
by = {}
for rec in recs:
    by.setdefault(rec["item"], []).append(bool(rec.get("correct")))
guess = {i for i, v in by.items() if any(v)}
byid = {it["id"]: it for it in items}
print(f"errors {sum('error' in r for r in recs)}; items {len(by)}; guessable {len(guess)}; "
      f"unstable across reps {sum(len(set(v)) > 1 for v in by.values())}")
for grp, cond in [("k_core=1", lambda it: it["k_core"] == 1), ("k_core>=2", lambda it: it["k_core"] >= 2)]:
    usable = [i for i in by if cond(byid[i]) and byid[i]["mutated"] and i not in guess]
    print(f"{grp}: mutated & not guessable = {len(usable)}")
for src in ("doctest", "synth"):
    ids = [i for i in by if byid[i].get("source") == src]
    if ids:
        print(f"{src}: guessable {sum(i in guess for i in ids)}/{len(ids)}")
