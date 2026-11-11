#!/bin/bash
# Sequential continuation of the main first-pass experiment (reps 2 and 3).
# Run AFTER rep1 completes, so we stay under the 150 RPM endpoint cap.
cd /Users/Nhym/vinh-work/Ky-thuat-phan-tich-chuong-trinh/Detai5.Chapter13 || exit 1
.venv/bin/python experiments/run_eval.py --data experiments/data/toolz_final_clean \
  --k-groups "1,3" --n 200 --lengths 16000 --tasks semantic,rtt --workers 4 \
  --out experiments/results/main16k_r2.jsonl
.venv/bin/python experiments/run_eval.py --data experiments/data/toolz_final_clean \
  --k-groups "1,3" --n 200 --lengths 16000 --tasks semantic,rtt --workers 4 \
  --out experiments/results/main16k_r3.jsonl
echo REPS23_ALL_DONE
