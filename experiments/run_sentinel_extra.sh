#!/usr/bin/env bash
set -euo pipefail

cd /workspace/mitosis-interference
mkdir -p logs

export PYTHONPATH=/workspace/mitosis-interference

echo "=== SENTINEL ALTORDER ==="
python -u experiments/day2_predictor_fixed_sentinel.py \
  --seed 1337 \
  --class-order-seed 7331 \
  --tag sentinel_altorder \
  2>&1 | tee logs/sentinel_altorder.txt

echo "=== SENTINEL RUN 3 ==="
python -u experiments/day2_predictor_fixed_sentinel.py \
  --seed 17 \
  --class-order-seed 1701 \
  --tag sentinel_r3 \
  2>&1 | tee logs/sentinel_r3.txt

echo "=== SENTINEL RUN 4 ==="
python -u experiments/day2_predictor_fixed_sentinel.py \
  --seed 31415 \
  --class-order-seed 27182 \
  --tag sentinel_r4 \
  2>&1 | tee logs/sentinel_r4.txt

echo "=== SENTINEL RUN 5 ==="
python -u experiments/day2_predictor_fixed_sentinel.py \
  --seed 4242 \
  --class-order-seed 5150 \
  --tag sentinel_r5 \
  2>&1 | tee logs/sentinel_r5.txt

echo
echo "ALL SENTINEL REPLICATIONS COMPLETE"
