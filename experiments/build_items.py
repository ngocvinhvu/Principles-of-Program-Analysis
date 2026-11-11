"""Build value-prediction items from a pure-Python library's doctests.

Pipeline (one item = one doctest expression with an expected output):
  1. doctest.DocTestFinder collects examples from each module of the library.
  2. Earlier examples without output in the same docstring are the item's setup code.
  3. The original example is re-executed; it must reproduce the doctest output (validity check).
  4. Integer / string literals are mutated with a consistent mapping (same old value -> same new
     value) so the answer is not the memorisable doctest output; the mutated code is executed
     twice and the repr of the result is the ground truth (interpreter = oracle).
  5. sys.setprofile records which library code ran; each code object is mapped to its enclosing
     *unit* (top-level function or top-level class).  The set of units is the function-level
     dynamic slice ("fragments") of the item.
  6. Every unit's source is stored with docstrings removed (doctests would leak answers).

Usage:
  .venv/bin/python experiments/build_items.py --lib toolz --out experiments/data/toolz
"""
import argparse
import ast
import builtins
import inspect
import doctest
import importlib
import io
import json
import os
import pkgutil
import random
import re
import sys
from contextlib import redirect_stdout

SKIP_MODULE_PARTS = {"tests", "curried", "_version", "compatibility"}
# Library plumbing that runs but carries no item-specific semantics (signature introspection
# behind `curry`, the dict-factory helper). Kept in `fragments`, excluded from `core_fragments`.
# This list is a manual, documented decision (threat to validity).
INFRA_UNITS = {
    "toolz": {"curry", "InstanceProperty", "instanceproperty", "_check_sigspec", "is_partial_args",
              "is_valid_args", "has_varargs", "has_keywords", "num_required_args", "is_arity",
              "signature_or_spec", "expand_sig", "_get_factory"},
}
MAX_ANSWER_CHARS = 200
WORDS = ["kiwi", "plum", "fig", "lime", "pear", "date", "yam", "okra", "leek", "kale",
         "mint", "sage", "dill", "rue", "tea", "oat"]


# ---------------------------------------------------------------- units (fragments)
class Unit:
    def __init__(self, uid, file, name, start, end, source):
        self.uid, self.file, self.name, self.start, self.end, self.source = (
            uid, file, name, start, end, source)

    def as_dict(self):
        return {"uid": self.uid, "file": self.file, "name": self.name,
                "start": self.start, "end": self.end, "source": self.source,
                "chars": len(self.source)}


def strip_docstrings(node, lines, start):
    """Return the unit's source text (lines start..end) with all docstrings removed."""
    keep = {i: l for i, l in enumerate(lines[start - 1: node.end_lineno], start)}
    for sub in ast.walk(node):
        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and sub.body:
            first = sub.body[0]
            if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                for i in range(first.lineno, first.end_lineno + 1):
                    keep.pop(i, None)
                if len(sub.body) == 1:  # body was only a docstring
                    indent = " " * first.col_offset
                    keep[first.lineno] = indent + "pass\n"
    text = "".join(keep[i] for i in sorted(keep))
    return re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"


def index_units(pkg_dir, rel_root):
    units = {}
    for root, dirs, files in os.walk(pkg_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_MODULE_PARTS and not d.startswith("__")]
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, rel_root)
            src = open(path, encoding="utf-8").read()
            lines = src.splitlines(keepends=True)
            tree = ast.parse(src)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    start = min([d.lineno for d in node.decorator_list] + [node.lineno])
                    uid = f"{rel}::{node.name}"
                    units[uid] = Unit(uid, rel, node.name, start, node.end_lineno,
                                      strip_docstrings(node, lines, start))
    return units


def unit_lookup(units):
    by_file = {}
    for u in units.values():
        by_file.setdefault(u.file, []).append(u)
    return by_file


# ---------------------------------------------------------------- tracing
class Tracer:
    def __init__(self, pkg_dir, rel_root, by_file):
        self.pkg_dir = os.path.realpath(pkg_dir)
        self.rel_root = rel_root
        self.by_file = by_file
        self.hits = []

    def _profile(self, frame, event, arg):
        if event != "call":
            return
        co = frame.f_code
        fpath = os.path.realpath(co.co_filename)
        if not fpath.startswith(self.pkg_dir):
            return
        rel = os.path.relpath(fpath, self.rel_root)
        for u in self.by_file.get(rel, []):
            if u.start <= co.co_firstlineno <= u.end:
                if u.uid not in self.hits:
                    self.hits.append(u.uid)  # keep first-call order
                return

    def __enter__(self):
        self.hits = []
        sys.setprofile(self._profile)
        return self

    def __exit__(self, *exc):
        sys.setprofile(None)


# ---------------------------------------------------------------- mutation
class Mutator(ast.NodeTransformer):
    def __init__(self, rng):
        self.rng, self.map, self.count = rng, {}, 0

    def visit_Constant(self, node):
        v = node.value
        if isinstance(v, bool) or v is None:
            return node
        if isinstance(v, int):
            if v not in self.map:  # injective: never map two old values to one new value
                step = 1 if v >= 0 else -1
                cand = v + step * self.rng.choice([1, 2, 3])
                while cand in self.map.values():
                    cand += step
                self.map[v] = cand
            self.count += 1
            return ast.copy_location(ast.Constant(self.map[v]), node)
        if isinstance(v, str) and v.isalpha() and 2 <= len(v) <= 12:
            if v not in self.map:
                choices = [w for w in WORDS if w not in self.map.values() and w != v]
                new = self.rng.choice(choices)
                self.map[v] = new.capitalize() if v[0].isupper() else new
            self.count += 1
            return ast.copy_location(ast.Constant(self.map[v]), node)
        return node


def mutate(setup, expr, rng):
    """Apply one consistent literal mapping to setup and expr."""
    m = Mutator(rng)
    setup_tree = ast.parse(setup) if setup.strip() else None
    expr_tree = ast.parse(expr, mode="eval")
    if setup_tree is not None:
        setup_tree = ast.fix_missing_locations(m.visit(setup_tree))
    expr_tree = ast.fix_missing_locations(m.visit(expr_tree))
    new_setup = ast.unparse(setup_tree) + "\n" if setup_tree is not None else ""
    return new_setup, ast.unparse(expr_tree), m.count


# ---------------------------------------------------------------- static backward slice of setup
def defs_uses(stmt):
    """Names a top-level statement defines and names it reads (incl. inside nested bodies)."""
    defs, uses = set(), set()
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        defs.add(stmt.name)
    for n in ast.walk(stmt):
        if isinstance(n, ast.Name):
            (defs.add if isinstance(n.ctx, ast.Store) else uses.add)(n.id)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            defs.update((a.asname or a.name).split(".")[0] for a in n.names)
        elif isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store):
            root = n
            while isinstance(root, ast.Attribute):
                root = root.value
            if isinstance(root, ast.Name):
                defs.add(root.id)  # obj.attr = ... modifies obj
    return defs, uses


def slice_setup(setup, expr):
    """Keep setup statements the expression depends on (def-use backward slice).
    Expression statements (e.g. `log.append(x)`) are kept if they read a needed name,
    because they may mutate it (conservative). Returns list of kept statement sources."""
    if not setup.strip():
        return []
    stmts = ast.parse(setup).body
    needed = {n.id for n in ast.walk(ast.parse(expr, mode="eval")) if isinstance(n, ast.Name)}
    keep = []
    for st in reversed(stmts):
        d, u = defs_uses(st)
        mutating_expr = isinstance(st, ast.Expr) and (u & needed)
        if (d & needed) or mutating_expr:
            keep.append(st)
            needed |= u
    keep.reverse()
    return [ast.unparse(st) for st in keep]


# ---------------------------------------------------------------- execution
def run(setup, expr, base_globs, tracer=None, stmt_traces=None):
    """Execute setup then evaluate expr; return repr(result).
    With a tracer, each setup statement and the expression are traced separately and the
    hits are stored in stmt_traces (list aligned with statements, last entry = expression)."""
    ns = dict(base_globs)
    buf = io.StringIO()
    stmts = [ast.unparse(st) for st in ast.parse(setup).body] if setup.strip() else []
    with redirect_stdout(buf):
        for st in stmts:
            if tracer:
                with tracer:
                    exec(compile(st, "<item>", "exec"), ns)
                stmt_traces.append(list(tracer.hits))
            else:
                exec(compile(st, "<item>", "exec"), ns)
        if tracer:
            with tracer:
                result = eval(compile(expr, "<item>", "eval"), ns)
            stmt_traces.append(list(tracer.hits))
        else:
            result = eval(compile(expr, "<item>", "eval"), ns)
    return repr(result)


def norm(s):
    return " ".join(s.split())


def usable_answer(ans):
    return len(ans) <= MAX_ANSWER_CHARS and " at 0x" not in ans and "object>" not in ans


# ---------------------------------------------------------------- fresh namespace check
def unit_namespace(units, lib):
    """Names the model is told are in scope: every unit shown in the context."""
    ns = {}
    for u in units.values():
        modname = u.file[:-3].replace("/", ".")
        if modname.endswith(".__init__"):
            modname = modname[: -len(".__init__")]
        try:
            ns[u.name] = getattr(importlib.import_module(modname), u.name)
        except Exception:
            pass
    return ns


def prelude_for(setup, expr, globs, unit_ns, lib):
    """Import lines for names the doctest took from its module's globals (not shown to model)."""
    trees = [ast.parse(expr, mode="eval")] + ([ast.parse(setup)] if setup.strip() else [])
    assigned, loaded = set(), []
    for t in trees:
        for n in ast.walk(t):
            if isinstance(n, ast.Name):
                (assigned.add if isinstance(n.ctx, ast.Store) else loaded.append)(n.id)
            elif isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                assigned.add(n.name)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                assigned.update((a.asname or a.name).split(".")[0] for a in n.names)
            elif isinstance(n, ast.arg):
                assigned.add(n.arg)
    lines = []
    for name in dict.fromkeys(loaded):
        if name in assigned or name in unit_ns or hasattr(builtins, name) or name not in globs:
            continue
        obj = globs[name]
        if inspect.ismodule(obj):
            lines.append(f"import {obj.__name__}" if obj.__name__ == name
                         else f"import {obj.__name__} as {name}")
            continue
        mod = getattr(obj, "__module__", None)
        if not mod:
            return None  # a plain data global: cannot be recreated honestly -> drop item
        mod = {"_operator": "operator", "_functools": "functools", "_collections": "collections"}.get(mod, mod)
        if mod.split(".")[0] == lib:
            return None  # library object that is not a context unit
        real = getattr(obj, "__name__", name)
        lines.append(f"from {mod} import {real}" + (f" as {name}" if real != name else ""))
    return "".join(l + "\n" for l in lines)


# ---------------------------------------------------------------- main
def iter_modules(pkg):
    yield pkg.__name__
    for info in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        if not any(p in SKIP_MODULE_PARTS for p in info.name.split(".")):
            yield info.name


class Pipeline:
    """Shared tail of the pipeline: slice setup, execute+trace, filter, fresh-namespace check."""

    def __init__(self, lib, units, tracer, unit_ns, stats):
        self.lib, self.units, self.tracer, self.unit_ns, self.stats = lib, units, tracer, unit_ns, stats
        self.infra = INFRA_UNITS.get(lib, set())

    def skip(self, why):
        self.stats[why] = self.stats.get(why, 0) + 1

    def finalize(self, setup, expr, globs):
        """Return dict(setup, expr, answer, trace, core) or None (reason counted in stats)."""
        try:
            kept = slice_setup(setup, expr)
            setup = "".join(k + "\n" for k in kept)
            per_stmt = []
            ans1 = run(setup, expr, globs, self.tracer, per_stmt)
            trace = list(dict.fromkeys(u for hits in per_stmt for u in hits))
            ans2 = run(setup, expr, globs)
        except Exception:
            return self.skip("skip_exec_error")
        if ans1 != ans2:
            return self.skip("skip_nondeterministic")
        if not usable_answer(ans1):
            return self.skip("skip_answer_unusable")
        core = [u for u in trace if self.units[u].name not in self.infra]
        if not core:
            return self.skip("skip_no_library_code")
        prelude = prelude_for(setup, expr, globs, self.unit_ns, self.lib)
        if prelude is None:
            return self.skip("skip_hidden_global")
        try:  # what the model sees: only context units + prelude + setup
            fresh = run(prelude + setup, expr, self.unit_ns)
        except Exception:
            fresh = None
        if fresh != ans1:
            return self.skip("skip_fresh_ns_mismatch")
        return {"setup": prelude + setup, "expr": expr, "answer": ans1, "trace": trace, "core": core}


# ---------------------------------------------------------------- C: synthetic compositions
# Chains of real library functions over a random int list. Only used for libraries listed here.
SYNTH_SEQ = {  # seq of ints -> iterable of ints
    "toolz": [
        lambda r, s: f"take({r.randint(2, 6)}, {s})",
        lambda r, s: f"drop({r.randint(1, 3)}, {s})",
        lambda r, s: f"take_nth({r.randint(2, 3)}, {s})",
        lambda r, s: f"tail({r.randint(2, 5)}, {s})",
        lambda r, s: f"unique({s})",
        lambda r, s: (lambda m: f"remove(lambda x: x % {m} == {r.randrange(m)}, {s})")(r.randint(2, 4)),
        lambda r, s: f"accumulate(add, {s})",
        lambda r, s: f"interpose({r.randint(0, 9)}, {s})",
        lambda r, s: f"topk({r.randint(2, 5)}, {s})",
        lambda r, s: f"merge_sorted({s}, {sorted(r.sample(range(20), 3))})",
        lambda r, s: (lambda n: f"pluck({r.randrange(n)}, sliding_window({n}, {s}))")(r.randint(2, 3)),
        lambda r, s: f"concat(partition_all({r.randint(2, 3)}, {s}))",
        lambda r, s: f"mapcat(lambda x: [x, x + {r.randint(1, 5)}], {s})",
        lambda r, s: f"cons({r.randint(0, 9)}, {s})",
    ]}
SYNTH_FINAL = {  # iterable of ints -> printable value
    "toolz": [
        lambda r, s: f"list({s})",
        lambda r, s: f"frequencies({s})",
        lambda r, s: f"valmap(len, groupby(lambda x: x % {r.randint(2, 4)}, {s}))",
        lambda r, s: f"keyfilter(lambda k: k > {r.randint(3, 12)}, frequencies({s}))",
        lambda r, s: f"last({s})",
        lambda r, s: f"nth({r.randint(1, 3)}, {s})",
        lambda r, s: f"count({s})",
        lambda r, s: f"reduceby(lambda x: x % {r.randint(2, 3)}, add, {s})",
        lambda r, s: f"countby(lambda x: x > {r.randint(4, 12)}, {s})",
    ]}


def synth_candidates(lib, rng, n):
    out, seen = [], set()
    for _ in range(n * 20):
        if len(out) >= n or lib not in SYNTH_SEQ:
            break
        expr = "xs"
        for _ in range(rng.choice([1, 2, 3])):
            expr = rng.choice(SYNTH_SEQ[lib])(rng, expr)
        expr = rng.choice(SYNTH_FINAL[lib])(rng, expr)
        if expr in seen:
            continue
        seen.add(expr)
        xs = [rng.randint(0, 20) for _ in range(rng.randint(6, 10))]
        out.append(("from operator import add\n" + f"xs = {xs}\n", expr))
    return out


# ------------------------------------------------------- C-easy: controllable k_core==3 chains
# Easy, predictable multi-function (k_core==3) items so a non-thinking model can solve them at
# oracle. Small inputs + self-contained functions (take/drop/tail/unique are itertools-only; they
# do NOT pull in other toolz units), one printable final (last/first/count/nth). We keep only
# candidates whose traced core is EXACTLY 3 distinct toolz units (finalize() measures it).
# Each entry: (unit_name, fn(rng, expr) -> expr_string). expr_string invokes exactly that one unit.
EASY_STEPS = [
    ("take",   lambda r, s: f"take({r.randint(2, 4)}, {s})"),
    ("drop",   lambda r, s: f"drop({r.randint(1, 3)}, {s})"),
    ("tail",   lambda r, s: f"tail({r.randint(2, 4)}, {s})"),
    ("unique", lambda r, s: f"unique({s})"),
]
EASY_FINALS = [
    ("last",  lambda r, s: f"last({s})"),
    ("first", lambda r, s: f"first({s})"),
    ("count", lambda r, s: f"count({s})"),
    ("nth",   lambda r, s: f"nth({r.randint(1, 2)}, {s})"),
]


def easy_synth_candidates(lib, rng, n):
    """Generate controllable easy chains aiming at exactly 3 distinct toolz units over a small xs."""
    if lib not in ("toolz",):
        return []
    out, seen = [], set()
    for _ in range(n * 30):
        if len(out) >= n:
            break
        steps = rng.sample(EASY_STEPS, 2)
        expr = "xs"
        names = []
        for name, fn in steps:
            expr = fn(rng, expr)
            names.append(name)
        fname, ffn = rng.choice(EASY_FINALS)
        expr = ffn(rng, expr)
        names.append(fname)
        if len(set(names)) != 3 or expr in seen:
            continue
        xs = [rng.randint(0, 9) for _ in range(rng.randint(5, 6))]
        if rng.random() < 0.5:
            xs[rng.randrange(len(xs))] = xs[rng.randrange(len(xs))]
        try:
            ns = {"xs": xs}
            exec("from toolz import take,drop,tail,unique,last,first,count,nth", ns)
            eval(expr, {"__builtins__": __builtins__}, ns)
        except Exception:
            continue
        seen.add(expr)
        out.append(("from operator import add\n" + "xs = " + repr(xs) + "\n", expr))
    return out



EASY1 = [  # exactly ONE toolz unit (wrapped by builtin list) -> k_core==1, easy to compute
    ("take",   lambda r, s: f"list(take({r.randint(2, 4)}, {s}))"),
    ("drop",   lambda r, s: f"list(drop({r.randint(1, 3)}, {s}))"),
    ("tail",   lambda r, s: f"list(tail({r.randint(2, 4)}, {s}))"),
    ("unique", lambda r, s: f"list(unique({s}))"),
]


def easy_synth_k1(lib, rng, n):
    """Single-function easy items: list(<self-contained step(xs)>) => exactly one toolz unit."""
    if lib not in ("toolz",):
        return []
    out, seen = [], set()
    for _ in range(n * 20):
        if len(out) >= n:
            break
        name, fn = rng.choice(EASY1)
        xs = [rng.randint(0, 9) for _ in range(rng.randint(4, 5))]
        if rng.random() < 0.5:
            xs[rng.randrange(len(xs))] = xs[rng.randrange(len(xs))]
        expr = fn(rng, "xs")
        key = (expr, tuple(xs))          # k=1 items differ by the DATA, not the expr
        if key in seen:
            continue
        try:
            ns = {"xs": xs}
            exec("from toolz import take,drop,tail,unique", ns)
            eval(expr, {"__builtins__": __builtins__}, ns)
        except Exception:
            continue
        seen.add(key)
        out.append(("from operator import add\n" + "xs = " + repr(xs) + "\n", expr))
    return out


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lib", default="toolz")
    ap.add_argument("--out", default="experiments/data/toolz")
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--synth", type=int, default=0, help="number of synthetic chain candidates (C)")
    ap.add_argument("--easy", type=int, default=0, help="number of easy k_core==3 synthetic chain candidates")
    ap.add_argument("--easy1", type=int, default=0, help="number of easy k_core==1 synthetic chain candidates")
    args = ap.parse_args()

    pkg = importlib.import_module(args.lib)
    pkg_dir = os.path.dirname(pkg.__file__)
    rel_root = os.path.dirname(pkg_dir)
    units = index_units(pkg_dir, rel_root)
    tracer = Tracer(pkg_dir, rel_root, unit_lookup(units))
    unit_ns = unit_namespace(units, args.lib)
    rng = random.Random(args.seed)
    items, stats, seen = [], {}, set()
    pipe = Pipeline(args.lib, units, tracer, unit_ns, stats)

    def add_item(res, source, extra):
        items.append({
            "id": f"{args.lib}-{len(items):04d}", "source": source, **extra,
            "setup": res["setup"], "expr": res["expr"], "answer": res["answer"],
            "fragments": res["trace"], "k": len(res["trace"]),
            "core_fragments": res["core"], "k_core": len(res["core"]),
            "files": sorted({units[u].file for u in res["trace"]}),
        })

    # --- doctest items
    finder = doctest.DocTestFinder(recurse=True)
    for modname in iter_modules(pkg):
        try:
            mod = importlib.import_module(modname)
        except Exception as e:  # optional deps missing etc.
            stats[f"import_error:{modname}"] = repr(e)
            continue
        for test in finder.find(mod):
            if test.name in seen or not test.examples:
                continue
            seen.add(test.name)
            setup_parts = []
            for ex in test.examples:
                src = ex.source.strip()
                if not ex.want.strip():
                    setup_parts.append(src)
                    continue
                stats["candidates"] = stats.get("candidates", 0) + 1
                try:
                    ast.parse(src, mode="eval")
                except SyntaxError:
                    pipe.skip("skip_not_expression")
                    continue
                setup = "\n".join(setup_parts) + ("\n" if setup_parts else "")
                try:
                    orig = run(setup, src, test.globs)
                except Exception:
                    pipe.skip("skip_orig_error")
                    continue
                if norm(orig) != norm(ex.want):
                    pipe.skip("skip_orig_mismatch")
                    continue
                try:
                    m_setup, m_expr, n_mut = mutate(setup, src, rng)
                except Exception:
                    pipe.skip("skip_mutation_error")
                    continue
                res = pipe.finalize(m_setup, m_expr, test.globs)
                if res:
                    add_item(res, "doctest", {
                        "doctest": test.name, "orig_setup": setup, "orig_expr": src,
                        "orig_answer": orig, "mutated": n_mut > 0 and res["answer"] != orig})

    # --- C: synthetic chains of real library functions (fresh random data = "mutated")
    for setup, expr in synth_candidates(args.lib, rng, args.synth):
        stats["synth_candidates"] = stats.get("synth_candidates", 0) + 1
        res = pipe.finalize(setup, expr, unit_ns)
        if res:
            add_item(res, "synth", {"doctest": None, "orig_setup": None, "orig_expr": None,
                                    "orig_answer": None, "mutated": True})

    # --- C-easy: controllable k_core==3 chains
    for setup, expr in easy_synth_candidates(args.lib, rng, args.easy):
        stats["easy_candidates"] = stats.get("easy_candidates", 0) + 1
        res = pipe.finalize(setup, expr, unit_ns)
        if res:
            add_item(res, "synth", {"doctest": None, "orig_setup": None, "orig_expr": None,
                                    "orig_answer": None, "mutated": True})

    # --- C-easy: controllable k_core==1 chains
    for setup, expr in easy_synth_k1(args.lib, rng, args.easy1):
        stats["easy1_candidates"] = stats.get("easy1_candidates", 0) + 1
        res = pipe.finalize(setup, expr, unit_ns)
        if res:
            add_item(res, "synth", {"doctest": None, "orig_setup": None, "orig_expr": None,
                                    "orig_answer": None, "mutated": True})

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out + "_items.jsonl", "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    with open(args.out + "_units.json", "w", encoding="utf-8") as f:
        json.dump({u.uid: u.as_dict() for u in units.values()}, f, ensure_ascii=False, indent=1)

    stats["items"] = len(items)
    stats["units"] = len(units)
    for src in ("doctest", "synth"):
        sub = [it for it in items if it["source"] == src and it["mutated"]]
        ks = {}
        for it in sub:
            ks[it["k_core"]] = ks.get(it["k_core"], 0) + 1
        stats[f"{src}_mutated_k_core"] = dict(sorted(ks.items()))
    stats["multi_file_core_items"] = sum(
        len({units[u].file for u in it["core_fragments"]}) > 1 for it in items)
    stats["lib_version"] = getattr(pkg, "__version__", "?")
    print(json.dumps(stats, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
