#!/usr/bin/env python3
"""
Pilot for IT5440 topic 5-KH: SemTrace-Dep (small) + context conditions C0-C3.

Pure standard library. Talks to a local Ollama server (http://localhost:11434).

  python3 pilot.py --dry-run --n 5           # build items, check answers, show one prompt
  python3 pilot.py --model qwen2.5-coder:7b --n 20
  python3 pilot.py --model qwen2.5-coder:7b --n 20 --tokens 8000 --conds C0,C1,C2,C3

Output: results/<model>_<time>.jsonl (one line per query) and an accuracy table.

Differences from the draft's Appendix A (on purpose):
  * Each helper mixes +c, -c, *k and an if-branch, so it does NOT collapse to
    "x + constant" (the shortcut the draft itself flags).
  * Distractors come in two kinds: "similar" (same template, other constants,
    never called) and "generic" (small utility functions written here, so no
    licence question).
"""
import argparse, ast, json, os, random, re, string, sys, time, urllib.request
from collections import defaultdict

# ---------------------------------------------------------------- generator
def rand_name(rng):
    return "fn_" + "".join(rng.choice("0123456789abcdef") for _ in range(4))

def arith_body(rng, call=None, m=3):
    """Lines computing from x; optional call to helper `call`. Returns list of lines."""
    lines, cur = [], "x"
    if call:
        lines.append(f"    a = {call}(x {rng.choice('+-')} {rng.randint(10, 99)})")
        cur = "a"
    for i in range(m):
        v = "bcdefg"[i]
        op = rng.choice(["+", "-", "*"])
        c = rng.randint(2, 3) if op == "*" else rng.randint(100, 999)
        lines.append(f"    {v} = {cur} {op} {c}")
        cur = v
    t = rng.randint(100, 999)
    c1, c2 = rng.randint(10, 99), rng.randint(10, 99)
    lines.append(f"    if {cur} > {t}:")
    lines.append(f"        {cur} = {cur} - {c1}")
    lines.append(f"    else:")
    lines.append(f"        {cur} = {cur} + {c2}")
    lines.append(f"    return {cur}")
    return lines

def make_func(name, body):
    return f"def {name}(x):\n" + "\n".join(body) + "\n"

GENERIC = [
    "def {n}(s):\n    words = [w for w in s.split() if w]\n    return ' '.join(reversed(words))\n",
    "def {n}(xs):\n    seen = set()\n    out = []\n    for v in xs:\n        if v not in seen:\n            seen.add(v)\n            out.append(v)\n    return out\n",
    "def {n}(d, key, default=None):\n    if key in d:\n        return d[key]\n    return default\n",
    "def {n}(path):\n    parts = path.strip('/').split('/')\n    return parts[-1] if parts else ''\n",
    "def {n}(xs, k):\n    return [xs[i:i + k] for i in range(0, len(xs), k)]\n",
    "def {n}(s):\n    return sum(1 for ch in s if ch in 'aeiou')\n",
    "def {n}(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n",
    "def {n}(xs):\n    if not xs:\n        return 0\n    return sum(xs) / len(xs)\n",
]

def make_item(rng, k=3, depth=2):
    """Target f -> h1 -> h2 (chain of `depth`) plus extra direct helpers up to k."""
    names = [rand_name(rng) for _ in range(k + 1)]
    target, helpers = names[0], names[1:]
    funcs = {}
    # chain: helpers[0] calls helpers[1] ... up to depth
    chain = helpers[:depth]
    for i in range(len(chain) - 1, -1, -1):
        callee = chain[i + 1] if i + 1 < len(chain) else None
        funcs[chain[i]] = make_func(chain[i], arith_body(rng, call=callee))
    extra = helpers[depth:]
    for h in extra:
        funcs[h] = make_func(h, arith_body(rng))
    # target: calls chain head and each extra helper, returns a list
    body = [f"    r = {chain[0]}(x + {rng.randint(10, 99)})"]
    outs = ["r"]
    for j, h in enumerate(extra):
        v = f"s{j}"
        body.append(f"    {v} = {h}(r {rng.choice('+-')} {rng.randint(10, 99)})")
        outs.append(v)
    body.append(f"    return [{', '.join(outs)}]")
    funcs[target] = make_func(target, body)
    order = list(reversed(chain)) + extra + [target]          # callee before caller
    needed = [funcs[n] for n in order]
    x = rng.randint(10, 99)
    ns = {}
    exec("\n".join(needed), ns)
    y = ns[target](x)
    # independent check: re-evaluate with a fresh namespace in reverse definition order
    ns2 = {}
    for src in reversed(needed):
        exec(src, ns2)
    assert ns2[target](x) == y, "answer cross-check failed"
    return {"target": target, "x": x, "y": y, "needed": needed, "needed_names": order}

def distractors(rng, count, frac_similar=0.5):
    out = []
    for _ in range(count):
        n = rand_name(rng)
        if rng.random() < frac_similar:
            out.append(make_func(n, arith_body(rng, call=rand_name(rng) if rng.random() < .5 else None)))
        else:
            out.append(rng.choice(GENERIC).format(n=n))
    return out

def approx_tokens(s):
    return len(s) // 4

# ---------------------------------------------------------------- contexts
def callgraph_closure(source, target):
    """C3: static call graph by name (ast), closure from target, callee first."""
    tree = ast.parse(source)
    defs = {f.name: f for f in tree.body if isinstance(f, ast.FunctionDef)}
    calls = {n: {c.func.id for c in ast.walk(f) if isinstance(c, ast.Call)
                 and isinstance(c.func, ast.Name) and c.func.id in defs}
             for n, f in defs.items()}
    seen, order = set(), []
    def visit(n):
        if n in seen:
            return
        seen.add(n)
        for m in sorted(calls[n]):
            visit(m)
        order.append(n)
    visit(target)
    return "\n".join(ast.unparse(defs[n]) + "\n" for n in order), order

def build_contexts(item, rng, tokens, pos):
    needed = item["needed"]
    pool, total = [], approx_tokens("\n".join(needed))
    while total < tokens:
        d = distractors(rng, 1)[0]
        pool.append(d)
        total += approx_tokens(d)
    ctx = {"C0": "\n".join(needed)}
    # C1: needed functions scattered around relative position pos
    c1 = list(pool)
    centre = int(pos * len(c1))
    spread = max(1, len(c1) // 10)
    for i, f in enumerate(needed):
        at = min(len(c1), max(0, centre + rng.randint(-spread, spread)))
        c1.insert(at, f)
    ctx["C1"] = "\n".join(c1)
    # C2: same content, needed block contiguous at the end (dependency order)
    ctx["C2"] = "\n".join(pool + needed)
    # C3: static closure computed from C1 (not from generator ground truth)
    ctx["C3"], c3_names = callgraph_closure(ctx["C1"], item["target"])
    item["c3_exact"] = set(c3_names) == set(item["needed_names"])
    return ctx

PROMPT = ("You are given Python source code. Read it carefully and answer the question.\n"
          "Question: What does {f}({x}) return? Answer with the Python literal only.\n"
          "<code>\n{code}\n</code>\n"
          "Question (repeated): What does {f}({x}) return? Answer with the Python literal only.\n")

# ---------------------------------------------------------------- model
def ask_ollama(model, prompt, host, num_ctx):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0, "num_ctx": num_ctx}}).encode()
    req = urllib.request.Request(host + "/api/generate", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.loads(r.read())
    return d.get("response", ""), d.get("prompt_eval_count"), d.get("eval_count")

def parse_answer(text):
    text = re.sub(r"```(?:python)?", "", text).strip()
    m = re.search(r"\[[^\[\]]*\]", text)
    cand = m.group(0) if m else text.splitlines()[0] if text else ""
    try:
        return ast.literal_eval(cand)
    except Exception:
        return None

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5-coder:7b")
    ap.add_argument("--n", type=int, default=20, help="items per cell")
    ap.add_argument("--tokens", type=int, default=4000, help="approx. context length for C1/C2")
    ap.add_argument("--positions", default="0,0.5,1")
    ap.add_argument("--conds", default="C0,C1,C2,C3")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--host", default="http://localhost:11434")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rng = random.Random(a.seed)
    conds = a.conds.split(",")
    positions = [float(p) for p in a.positions.split(",")]
    num_ctx = max(8192, int(a.tokens * 1.6))
    os.makedirs("results", exist_ok=True)
    out = f"results/{a.model.replace(':', '_').replace('/', '_')}_{time.strftime('%Y%m%d_%H%M%S')}.jsonl"
    acc = defaultdict(lambda: [0, 0])
    c3_ok = 0
    t0 = time.time()
    with open(out, "w") as fh:
        for i in range(a.n):
            item = make_item(rng, a.k, a.depth)
            for pos in positions:
                ctx = build_contexts(item, rng, a.tokens, pos)
                c3_ok += item["c3_exact"]
                for c in conds:
                    if c in ("C0", "C2", "C3") and pos != positions[0]:
                        continue  # position only matters for C1
                    prompt = PROMPT.format(f=item["target"], x=item["x"], code=ctx[c])
                    if a.dry_run:
                        if i == 0 and c == "C0":
                            print(prompt)
                            print("expected:", item["y"])
                        continue
                    resp, pin, pout = ask_ollama(a.model, prompt, a.host, num_ctx)
                    pred = parse_answer(resp)
                    ok = pred == item["y"]
                    key = f"{c}@p={pos}" if c == "C1" else c
                    acc[key][0] += ok
                    acc[key][1] += 1
                    fh.write(json.dumps({"i": i, "cond": c, "pos": pos, "target": item["target"],
                                         "x": item["x"], "expected": item["y"], "raw": resp,
                                         "pred": repr(pred), "correct": ok,
                                         "prompt_tokens": pin, "output_tokens": pout}) + "\n")
                    fh.flush()
            print(f"item {i + 1}/{a.n} done ({time.time() - t0:.0f}s)", file=sys.stderr)
    cells = a.n * len(positions)
    print(f"\nC3 closure exact on {c3_ok}/{cells} contexts")
    if a.dry_run:
        print("dry run OK: items generated, answers cross-checked, contexts built")
        return
    print(f"\nModel {a.model}, ~{a.tokens} tokens, n={a.n}\n{'condition':<12}{'acc':>8}{'n':>6}")
    for key in sorted(acc):
        c, t = acc[key]
        print(f"{key:<12}{c / t:>8.2%}{t:>6}")
    print(f"\nlog: {out}")

if __name__ == "__main__":
    main()
