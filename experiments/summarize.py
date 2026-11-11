"""Summarise a results file: accuracy / copy score per task x layout, plus sanity checks.

  .venv/bin/python experiments/summarize.py experiments/results/pilot_16k.jsonl
"""
import collections
import json
import sys

recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
ok = [r for r in recs if "error" not in r]
print(f"records {len(recs)}, errors {len(recs) - len(ok)}")
print(f"thinking leaked (reasoning_chars>0): {sum(r.get('reasoning_chars', 0) > 0 for r in ok)}")
pt = [r["usage"].get("prompt_tokens", 0) for r in ok if r["length"]]
ratio = [r["usage"]["prompt_tokens"] / r["est_tokens"] for r in ok if r["length"]]
if pt:
    print(f"prompt_tokens min/mean/max: {min(pt)}/{sum(pt)//len(pt)}/{max(pt)}; "
          f"actual/estimated: {min(ratio):.2f}-{max(ratio):.2f}")
    print(f"total prompt tokens {sum(r['usage'].get('prompt_tokens', 0) for r in ok):,}, "
          f"cached {sum((r['usage'].get('prompt_tokens_details') or {}).get('cached_tokens', 0) for r in ok):,}, "
          f"completion {sum(r['usage'].get('completion_tokens', 0) for r in ok):,}")

cells = collections.defaultdict(list)
for r in ok:
    kgrp = "none" if r["layout"] == "none" else (
        "k1" if r["requested"] and len(r["requested"]) == 1 else f"k{len(r['requested'])}")
    key = (r["length"], kgrp, r["task"], r["layout"])
    cells[key].append(r)

print(f"\n{'len':>6} {'k':4} {'task':10} {'layout':15} {'n':>3} {'acc':>6} {'copy':>6} {'mem':>4}")
for key in sorted(cells):
    rs = cells[key]
    acc = [r["correct"] for r in rs if "correct" in r]
    cp = [r["copy"] for r in rs if r.get("copy") is not None]
    mem = sum(r.get("memorised_orig", False) for r in rs)
    print(f"{key[0]:>6} {key[1]:4} {key[2]:10} {key[3]:15} {len(rs):>3} "
          f"{(sum(acc)/len(acc) if acc else float('nan')):6.2f} "
          f"{(sum(cp)/len(cp) if cp else float('nan')):6.2f} {mem:>4}")
