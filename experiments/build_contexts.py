"""Build prompts: place an item's core fragments in a long static code context.

Factors
  layout  k_core == 1 : start | middle | end
          k_core >= 2 : cluster_start | cluster_middle | cluster_end | spread
  length  target prompt size in tokens (estimated as chars / CHARS_PER_TOKEN; the API's
          reported prompt_tokens is logged at run time and is the value used in analysis)
  task    semantic  - predict repr(result)
          lexical   - copy the named fragments verbatim
          rtt       - retrieve-then-trace: copy the named fragments, then predict
          nocontext - semantic question without any code (guessing / memorisation floor)

Filler = the library's other units first (same repository), then units from stdlib modules
(pure Python) when the library is too small for the target length. Units whose names collide
with library names or with names used by the item are never used as filler.
"""
import ast
import hashlib
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_items import strip_docstrings  # noqa: E402

CHARS_PER_TOKEN = 3.9  # pilot: 4.3 under-estimated DeepSeek-V4-Flash prompt_tokens by 7-16%
STDLIB_FILLER = ["textwrap", "difflib", "shlex", "calendar", "fractions", "statistics",
                 "configparser", "ipaddress", "pprint", "string", "tarfile", "zipfile",
                 "argparse", "dataclasses", "pathlib", "email/message", "http/cookiejar"]

LAYOUTS_K1 = {"start": [0.0], "middle": [0.5], "end": [1.0]}
LAYOUTS_KN = {"cluster_start": "c0.0", "cluster_middle": "c0.5", "cluster_end": "c1.0",
              "spread": "spread"}

INTRO = ("Below is Python source code (docstrings removed). Assume every function and class "
         "defined in it is already in scope.\n\n```python\n{ctx}```\n\n")
Q_SEMANTIC = ("Now this code is executed:\n\n```python\n{setup}result = {expr}\n```\n\n"
              "What would `print(repr(result))` output? Do not explain. Reply with exactly one "
              "line of the form `ANSWER: <output>`.")
Q_LEXICAL = ("Copy the complete source of {names} exactly as it appears in the code above. "
             "Output only the code, in one ```python block.")
Q_RTT = ("Now this code is executed:\n\n```python\n{setup}result = {expr}\n```\n\n"
         "First, copy the complete source of {names} exactly as it appears in the code above, in "
         "one ```python block. Then, on the last line, write what `print(repr(result))` would "
         "output, in the form `ANSWER: <output>`.")
Q_NOCONTEXT = ("The following code uses functions from the Python library `{lib}`. Assume they are "
               "in scope.\n\n```python\n{setup}result = {expr}\n```\n\n"
               "What would `print(repr(result))` output? Do not explain. Reply with exactly one "
              "line of the form `ANSWER: <output>`.")


def stdlib_units():
    base = os.path.dirname(os.__file__)
    out = []
    for mod in STDLIB_FILLER:
        path = os.path.join(base, mod + ".py")
        if not os.path.exists(path):
            continue
        src = open(path, encoding="utf-8").read()
        lines = src.splitlines(keepends=True)
        for node in ast.parse(src).body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                start = min([d.lineno for d in node.decorator_list] + [node.lineno])
                out.append({"uid": f"stdlib/{mod}.py::{node.name}", "file": f"stdlib/{mod}.py",
                            "name": node.name, "source": strip_docstrings(node, lines, start)})
    return out


def names_in(code):
    try:
        return {n.id for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Name)}
    except SyntaxError:
        return set()


def render(u):
    return f"# file: {u['file']}\n{u['source']}\n"


def name_list(units):
    names = [f"`{u['name']}`" for u in units]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


class ContextBuilder:
    def __init__(self, units_path, lib):
        self.units = json.load(open(units_path, encoding="utf-8"))
        self.lib = lib
        lib_names = {u["name"] for u in self.units.values()}
        self.extra = [u for u in stdlib_units() if u["name"] not in lib_names]
        self._fcache = {}

    def _filler(self, item, length, seed, ref_len):
        "Layout-INDEPENDENT filler: same (item,length,seed) => same filler; only fragment positions change."
        key = (item["id"], length, seed)
        if key in self._fcache:
            return self._fcache[key]
        frag_ids = set(item["core_fragments"])
        used = names_in(item["setup"] + "\n" + item["expr"])
        pool = [u for uid, u in self.units.items() if uid not in frag_ids]
        pool += [u for u in self.extra if u["name"] not in used]
        pool.sort(key=lambda u: u["uid"])
        random.Random(f"{item['id']}|filler|{seed}").shuffle(pool)  # seed EXCLUDES layout & length
        budget = 0 if length == 0 else int(length * CHARS_PER_TOKEN) - ref_len
        filler, size = [], 0
        for u in pool:
            r = len(render(u))
            if size + r > budget:
                continue
            filler.append(u)
            size += r
            if budget - size < 200:
                break
        self._fcache[key] = filler
        return filler

    def build(self, item, layout, length, task, seed=0):
        frags = [self.units[uid] for uid in item["core_fragments"]]
        random.Random(f"{item['id']}|frags|{seed}").shuffle(frags)  # same order in every layout
        names = name_list(frags)
        q_tmpl = {"semantic": Q_SEMANTIC, "lexical": Q_LEXICAL, "rtt": Q_RTT}[task]
        question = q_tmpl.format(setup=item["setup"], expr=item["expr"], names=names)
        frag_ids = set(item["core_fragments"])
        ref_q = Q_RTT.format(setup=item["setup"], expr=item["expr"], names=names)
        ref_len = len(INTRO) + len(ref_q) + sum(len(render(f)) for f in frags)
        filler = self._filler(item, length, seed, ref_len)
        seq = list(filler)
        sizes = [len(render(u)) for u in seq]
        total = sum(sizes)

        def idx_at(frac):  # insertion index whose preceding text is closest to frac * total
            cum, best, best_d = 0, 0, frac * total
            for i, sz in enumerate(sizes, 1):
                cum += sz
                d = abs(cum - frac * total)
                if d < best_d:
                    best, best_d = i, d
            return best

        if layout in LAYOUTS_K1:
            assert len(frags) == 1, "k_core==1 layouts need exactly one fragment"
            targets = [(idx_at(LAYOUTS_K1[layout][0]), [frags[0]])]
        elif LAYOUTS_KN[layout] == "spread":
            k = len(frags)
            targets = [(idx_at((i + 0.5) / k), [f]) for i, f in enumerate(frags)]
        else:
            targets = [(idx_at(float(LAYOUTS_KN[layout][1:])), frags)]
        for pos, fs in sorted(targets, key=lambda t: -t[0]):  # insert from the back
            seq[pos:pos] = fs
        ctx = "".join(render(u) for u in seq)

        # where each fragment ended up, as fraction of context characters (for analysis)
        offsets, cur = {}, 0
        for u in seq:
            if u["uid"] in frag_ids:
                offsets[u["uid"]] = round(cur / max(1, len(ctx)), 3)
            cur += len(render(u))

        prompt = INTRO.format(ctx=ctx) + question
        return {"item": item["id"], "task": task, "layout": layout, "length": length,
                "prompt": prompt, "est_tokens": round(len(prompt) / CHARS_PER_TOKEN),
                "fragment_offsets": offsets, "requested": [f["uid"] for f in frags],
                "n_filler_lib": sum(1 for u in filler if not u["file"].startswith("stdlib/")),
                "n_filler_ext": sum(1 for u in filler if u["file"].startswith("stdlib/")),
                "filler_hash": hashlib.md5("|".join(u["uid"] for u in filler).encode()).hexdigest()[:10]}

    def nocontext(self, item):
        prompt = Q_NOCONTEXT.format(lib=self.lib, setup=item["setup"], expr=item["expr"])
        return {"item": item["id"], "task": "nocontext", "layout": "none", "length": 0,
                "prompt": prompt, "est_tokens": round(len(prompt) / CHARS_PER_TOKEN),
                "fragment_offsets": {}, "requested": [], "n_filler_lib": 0, "n_filler_ext": 0}


def layouts_for(item):
    return list(LAYOUTS_K1) if item["k_core"] == 1 else list(LAYOUTS_KN)
