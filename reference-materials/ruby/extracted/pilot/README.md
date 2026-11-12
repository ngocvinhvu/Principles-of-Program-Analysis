# Pilot: SemTrace-Dep + context conditions C0–C3

Small pilot for the 5-KH plan (step 4 of II.9.1). Python 3 standard library only, using a free local model through Ollama.

## Setup (once)
1. Install Ollama: https://ollama.com/download
2. Pull a model:
       ollama pull qwen2.5-coder:7b      # ~4.7 GB, in the model family used by [2]
       ollama pull llama3.2:3b           # smaller and faster

## Run
    python3 pilot.py --dry-run --n 5                       # no model: check generator + contexts
    python3 pilot.py --model qwen2.5-coder:7b --n 20       # ~120 queries at ~4k tokens
    python3 pilot.py --model qwen2.5-coder:7b --n 20 --tokens 16000

## Conditions
- C0: only the needed functions (upper bound)
- C1: needed functions scattered among distractors at position p = 0 / 0.5 / 1
- C2: same content as C1, needed block moved to the end
- C3: static call-graph closure (Python ast) from the target

## What to look for
- Is C1@p=0.5 lower than C1@p=0 and p=1? That is the effect from [2] (RQ1 / K1).
- Does C2 or C3 bring accuracy back toward C0? (RQ2 / K2–K5)
- C3 is always exact on this synthetic code (risk R4 in the plan). Indirect calls are needed later.

Each query is logged in results/*.jsonl (raw answer, parsed answer, tokens).
