#!/usr/bin/env bash
set -euo pipefail

cd /workspace/mitosis-interference

echo "=== RUN 3 ==="
python -u experiments/day2_predictor_cable.py \
  --seed 17 \
  --class-order-seed 1701 \
  --tag cable_r3 \
  2>&1 | tee logs/cable_r3.txt

echo "=== RUN 4 ==="
python -u experiments/day2_predictor_cable.py \
  --seed 31415 \
  --class-order-seed 27182 \
  --tag cable_r4 \
  2>&1 | tee logs/cable_r4.txt

echo "=== RUN 5 ==="
python -u experiments/day2_predictor_cable.py \
  --seed 4242 \
  --class-order-seed 5150 \
  --tag cable_r5 \
  2>&1 | tee logs/cable_r5.txt

echo
echo "ALL THREE EXTRA RUNS COMPLETE"
