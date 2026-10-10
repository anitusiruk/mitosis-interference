#!/bin/bash
# Re-run an idempotent job script (skips existing outputs) until it reports no FAIL lines.
# Failures here are GPU out-of-memory under contention; runs are deterministic, so retries
# introduce no selection.  Usage: retry_until_done.sh <script> <log>
for i in $(seq 1 20); do
  PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True "$1" > "$2.try$i" 2>&1
  grep -q FAIL "$2.try$i" || { echo "clean after $i tries" >> "$2"; exit 0; }
  echo "try $i: $(grep -c FAIL $2.try$i) failures" >> "$2"; sleep 60
done
