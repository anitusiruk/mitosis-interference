"""Run a list of jobs (one JSON argv list per line) with N parallel workers; skip jobs whose
--out exists; print FAIL lines for failed jobs. No shell quoting involved."""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def run(args, module):
    out = Path(args[args.index("--out") + 1])
    if out.exists():
        return None
    out.parent.mkdir(parents=True, exist_ok=True)
    log = out.with_suffix(".log")
    with open(log, "w") as fh:
        rc = subprocess.call([sys.executable, "-m", module] + args, stdout=fh, stderr=subprocess.STDOUT)
    if rc == 0:
        log.unlink()
        return None
    return f"FAIL {' '.join(args)}"


def main():
    jobfile, workers, module = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    jobs = [json.loads(l) for l in open(jobfile) if l.strip()]
    with ThreadPoolExecutor(workers) as ex:
        for r in ex.map(lambda j: run(j, module), jobs):
            if r:
                print(r, flush=True)
    print("JOBS_DONE", flush=True)


if __name__ == "__main__":
    main()
