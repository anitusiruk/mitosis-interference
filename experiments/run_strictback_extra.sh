#!/usr/bin/env bash
set -euo pipefail

cd /workspace/mitosis-interference
mkdir -p logs

export PYTHONPATH=/workspace/mitosis-interference

echo "=== STRICT ALTORDER ==="
python -u experiments/day2_predictor_strict_backward.py \
  --seed 1337 \
  --class-order-seed 7331 \
  --tag strictback_altorder \
  2>&1 | tee logs/strictback_altorder.txt

echo "=== STRICT RUN 3 ==="
python -u experiments/day2_predictor_strict_backward.py \
  --seed 17 \
  --class-order-seed 1701 \
  --tag strictback_r3 \
  2>&1 | tee logs/strictback_r3.txt

echo "=== STRICT RUN 4 ==="
python -u experiments/day2_predictor_strict_backward.py \
  --seed 31415 \
  --class-order-seed 27182 \
  --tag strictback_r4 \
  2>&1 | tee logs/strictback_r4.txt

echo "=== STRICT RUN 5 ==="
python -u experiments/day2_predictor_strict_backward.py \
  --seed 4242 \
  --class-order-seed 5150 \
  --tag strictback_r5 \
  2>&1 | tee logs/strictback_r5.txt

echo
echo "ALL STRICT-BACKWARD REPLICATIONS COMPLETE"
