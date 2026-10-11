"""Scheduling helper (no effect on results): like run_jobs.py, but with a configurable GPU-memory
gate, optional job filter and reverse order, so extra workers can share a frozen job list.
Usage: run_jobs_lowmem.py <jobs.jsonl> <workers> <module> <need_mb> [--reverse] [--exclude SUBSTR]"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor

import experiments.run_jobs as R


def main():
    jobfile, workers, module, need = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    jobs = [json.loads(l) for l in open(jobfile) if l.strip()]
    if "--exclude" in sys.argv:
        sub = sys.argv[sys.argv.index("--exclude") + 1]
        jobs = [j for j in jobs if not any(sub in a for a in j)]
    if "--reverse" in sys.argv:
        jobs = jobs[::-1]
    with ThreadPoolExecutor(workers) as ex:
        for r in ex.map(lambda j: R.run(j, module, need_mb=need), jobs):
            if r:
                print(r, flush=True)
    print("JOBS_DONE", flush=True)


if __name__ == "__main__":
    main()
