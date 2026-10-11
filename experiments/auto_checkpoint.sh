#!/bin/bash
# Hourly checkpoint of results to GitHub (the only persistent storage).
cd /workspace/mitosis-interference
while true; do
  git add -A results/tfcl results/sema_x notes paper experiments src >/dev/null 2>&1
  git -c user.name=anitusiruk -c user.email=samdwu12@gmail.com commit -qm "Checkpoint: pipeline results $(date -u +%Y-%m-%dT%H:%MZ)" >/dev/null 2>&1 && git push -q origin tmlr-reframe >/dev/null 2>&1
  sleep 3600
done
