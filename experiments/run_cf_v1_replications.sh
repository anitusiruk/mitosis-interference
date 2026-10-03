#!/usr/bin/env bash
set -euo pipefail

cd /workspace/mitosis-interference
export PYTHONPATH=/workspace/mitosis-interference

mkdir -p logs

seeds=(1337 17 31415 4242)

for seed in "${seeds[@]}"; do

    echo
    echo "=============================================="
    echo "CF-v1 CONFIDENT seed=$seed"
    echo "=============================================="

    out="results/controller_recurrence_counterfactual_confident_seed${seed}/routing.csv"

    if [ -s "$out" ]; then
        echo "SKIP existing $out"
        continue
    fi

    python -u \
      experiments/controller_recurrence_counterfactual_confident.py \
      --seed "$seed" \
      2>&1 | tee \
      "logs/controller_recurrence_counterfactual_confident_${seed}.txt"

done

echo
echo "ALL CF-v1 REPLICATIONS COMPLETE"
