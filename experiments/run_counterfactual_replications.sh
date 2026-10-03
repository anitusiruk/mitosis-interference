#!/usr/bin/env bash
set -euo pipefail

cd /workspace/mitosis-interference
export PYTHONPATH=/workspace/mitosis-interference

mkdir -p logs

seeds=(1337 17 31415 4242)

for seed in "${seeds[@]}"; do

    echo
    echo "=================================================="
    echo "V3 BALANCED BASELINE seed=$seed"
    echo "=================================================="

    baseline_out="results/controller_recurrence_balanced_eval_seed${seed}/routing.csv"

    if [ -s "$baseline_out" ]; then
        echo "SKIP existing $baseline_out"
    else
        python -u \
          experiments/controller_recurrence_balanced_eval.py \
          --seed "$seed" \
          2>&1 | tee \
          "logs/controller_recurrence_balanced_eval_${seed}.txt"
    fi

    echo
    echo "=================================================="
    echo "COUNTERFACTUAL seed=$seed"
    echo "=================================================="

    cf_out="results/controller_recurrence_counterfactual_seed${seed}/routing.csv"

    if [ -s "$cf_out" ]; then
        echo "SKIP existing $cf_out"
    else
        python -u \
          experiments/controller_recurrence_counterfactual.py \
          --seed "$seed" \
          2>&1 | tee \
          "logs/controller_recurrence_counterfactual_${seed}.txt"
    fi

done

echo
echo "ALL COUNTERFACTUAL REPLICATIONS COMPLETE"
