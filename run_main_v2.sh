#!/bin/bash
# Corrected main benchmark (claude-code design): per-length invocations, rate-limit-aware.
# Hermes executes; claude-code interprets.
cd /Users/Nhym/vinh-work/Ky-thuat-phan-tich-chuong-trinh/Detai5.Chapter13 || exit 1
P=".venv/bin/python experiments/run_eval.py"
C="--tasks semantic --k-groups 1,3 --filler-seed 0 --seed 7 --n 40 --data experiments/data/toolz_final_clean"

echo "==== DeepSeek-V4-Flash ===="
$P $C --model DeepSeek-V4-Flash --lengths 0    --workers 2 --out experiments/results/main_ds_0.jsonl
$P $C --model DeepSeek-V4-Flash --lengths 4000 --workers 4 --out experiments/results/main_ds_4k.jsonl
$P $C --model DeepSeek-V4-Flash --lengths 16000 --workers 4 --out experiments/results/main_ds_16k.jsonl
$P $C --model DeepSeek-V4-Flash --lengths 32000 --workers 3 --out experiments/results/main_ds_32k.jsonl

echo "==== Qwen3.6-27B ===="
$P $C --model Qwen3.6-27B --lengths 0    --workers 2 --out experiments/results/main_qw_0.jsonl
$P $C --model Qwen3.6-27B --lengths 4000 --workers 2 --out experiments/results/main_qw_4k.jsonl
$P $C --model Qwen3.6-27B --lengths 16000 --workers 2 --out experiments/results/main_qw_16k.jsonl
$P $C --model Qwen3.6-27B --lengths 32000 --workers 1 --out experiments/results/main_qw_32k.jsonl

echo "MAIN_V2_ALL_DONE"
