"""Summarise compare_pilot.py results.

  .venv/bin/python experiments/summarize_compare.py experiments/results/compare_*.jsonl

Per (model, arm, length, layout): semantic exact-match accuracy, partial-match, lexical copy.
Middle drop D = mean(acc_start, acc_end) - acc_middle, paired by item, with a 95% bootstrap CI
(items resampled, 5000 draws). Amplitude A = max - min over the three positions (eq. 3 of the
group outline).
"""
import collections
import json
import random
import sys


def arm_name(r):
    return f"{r['arm']}{r['digits'] or ''}"


recs = []
for p in sys.argv[1:]:
    recs += [json.loads(l) for l in open(p, encoding="utf-8")]
ok = [r for r in recs if "error" not in r]
ok_keys = {(r["model"], r["item"], r["task"], r["layout"], r["length"]) for r in ok}
unresolved = [r for r in recs if "error" in r
              and (r["model"], r["item"], r["task"], r["layout"], r["length"]) not in ok_keys]
print(f"records {len(recs)}, errors {len(recs) - len(ok)} (unresolved after retry: {len(unresolved)}), "
      f"thinking leaked {sum(r.get('reasoning_chars', 0) > 0 for r in ok)}")
for m in sorted({r["model"] for r in ok}):
    rs = [r for r in ok if r["model"] == m and r["length"]]
    if rs:
        ratio = [r["usage"]["prompt_tokens"] / r["est_tokens"] for r in rs]
        print(f"  {m}: prompt tokens actual/estimated {min(ratio):.2f}-{max(ratio):.2f}, "
              f"max {max(r['usage']['prompt_tokens'] for r in rs):,}, "
              f"total {sum(r['usage']['prompt_tokens'] for r in ok if r['model'] == m):,}")

cells = collections.defaultdict(list)
for r in ok:
    cells[(r["model"], arm_name(r), r["length"], r["task"], r["layout"])].append(r)

print(f"\n{'model':18} {'arm':10} {'len':>6} {'task':8} {'layout':7} {'n':>3} {'acc':>5} {'part':>5} {'copy':>5}")
order = {"oracle": 0, "start": 1, "middle": 2, "end": 3}
for key in sorted(cells, key=lambda k: (k[0], k[1], k[2], k[3], order[k[4]])):
    rs = cells[key]
    acc = [r["correct"] for r in rs if "correct" in r]
    part = [r["partial"] for r in rs if "partial" in r]
    cp = [r["copy"] for r in rs if r.get("copy") is not None]
    f = lambda xs: f"{sum(xs)/len(xs):5.2f}" if xs else "    -"
    print(f"{key[0]:18} {key[1]:10} {key[2]:>6} {key[3]:8} {key[4]:7} {len(rs):>3} "
          f"{f(acc)} {f(part)} {f(cp)}")

print("\nMiddle drop D = mean(start,end) - middle (semantic, paired by item), 95% bootstrap CI")
print(f"{'model':18} {'arm':10} {'len':>6} {'n':>3} {'start':>5} {'mid':>5} {'end':>5} {'A':>5} {'D':>6}  CI95")
groups = collections.defaultdict(dict)
for r in ok:
    if r["task"] == "semantic" and r["length"]:
        groups[(r["model"], arm_name(r), r["length"])].setdefault(r["item"], {})[r["layout"]] = r["correct"]
rng = random.Random(0)
for key in sorted(groups):
    rows = [v for v in groups[key].values() if len(v) == 3]
    if not rows:
        continue
    d = [(v["start"] + v["end"]) / 2 - v["middle"] for v in rows]
    mean = lambda xs: sum(xs) / len(xs)
    boots = sorted(mean([rng.choice(d) for _ in d]) for _ in range(5000))
    s, mi, e = (mean([v[p] for v in rows]) for p in ("start", "middle", "end"))
    print(f"{key[0]:18} {key[1]:10} {key[2]:>6} {len(rows):>3} {s:5.2f} {mi:5.2f} {e:5.2f} "
          f"{max(s, mi, e) - min(s, mi, e):5.2f} {mean(d):+6.2f}  [{boots[124]:+.2f}, {boots[4874]:+.2f}]")
