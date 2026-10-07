"""Push the preserved study and verify a fresh GitHub LFS download.

Run from the authoritative checkout after authenticating GitHub CLI.
All command output stays outside Git; the committed receipt contains no credentials.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess


ROOT = Path.cwd()
BRANCH = "day5-causal-audit"
WORKSPACE = ROOT.parent
ENV = os.environ.copy()
ENV.update(GIT_TERMINAL_PROMPT="0", GH_PROMPT_DISABLED="1", GCM_INTERACTIVE="never")


def now():
    return datetime.now(timezone.utc).isoformat()


def run(args, timeout=1800):
    print("RUN", " ".join(args), flush=True)
    result = subprocess.run(args, env=ENV, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"Command failed with exit {result.returncode}: {args[:3]}")


def read(args):
    return subprocess.check_output(args, env=ENV, text=True, timeout=90).strip()


def head():
    return read(["git", "rev-parse", "HEAD"])


def remote_head():
    result = read(["git", "ls-remote", "origin", f"refs/heads/{BRANCH}"])
    assert result, "Remote branch missing"
    return result.split()[0]


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


assert (ROOT / ".git").is_dir()
assert read(["git", "branch", "--show-current"]) == BRANCH
assert not read(["git", "status", "--porcelain"]), "Commit the verification script first"
account = read(["gh", "api", "user", "--jq", ".login"])
repo = json.loads(read(["gh", "api", "repos/anitusiruk/mitosis-interference"]))
assert repo["full_name"] == "anitusiruk/mitosis-interference"
assert repo["permissions"]["push"], "Authenticated account cannot push"
assert read(["git", "remote", "get-url", "origin"]) == "https://github.com/anitusiruk/mitosis-interference.git"
run(["git", "config", "--local", "credential.https://github.com.helper", ""])
run(["git", "config", "--local", "--add", "credential.https://github.com.helper", "!gh auth git-credential"])

snapshot = head()
manifest = json.loads(Path("results/checkpoint_preservation_manifest.json").read_text())
lfs_lines = read(["git", "lfs", "ls-files", "--long"]).splitlines()
lfs_paths = {line.split(" ", 2)[2] for line in lfs_lines}
tensor_paths = {name for name in manifest if Path(name).suffix in {".pt", ".safetensors"}}
assert tensor_paths <= lfs_paths, "Some checkpoint tensors are not tracked through LFS"
for name, expected in manifest.items():
    assert Path(name).stat().st_size == expected["bytes"], name
run(["git", "lfs", "fsck"])
run(["git", "push", "--set-upstream", "origin", BRANCH])
assert remote_head() == snapshot, "GitHub ref does not match preserved state"
run(["git", "lfs", "push", "--all", "origin", BRANCH])

fresh_storage = WORKSPACE / ("mitosis-lfs-verify-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
assert not fresh_storage.exists(), "Verification must use a new empty storage directory"
run(["git", "-c", f"lfs.storage={fresh_storage}", "lfs", "fetch", "origin", BRANCH])
run(["git", "-c", f"lfs.storage={fresh_storage}", "lfs", "fsck"])
unique_oids = {line.split()[0] for line in lfs_lines}
for oid in unique_oids:
    obj = fresh_storage / "objects" / oid[:2] / oid[2:4] / oid
    assert obj.is_file(), "A remotely fetched LFS object is missing"
    assert file_hash(obj) == oid, "A remotely fetched LFS object failed SHA256 verification"
print("REMOTE_LFS_ROUNDTRIP_PASS", len(unique_oids), "unique objects", flush=True)

receipt = {
    "verified_utc": now(),
    "repository": repo["full_name"],
    "branch": BRANCH,
    "authenticated_account": account,
    "preserved_snapshot_commit": snapshot,
    "github_snapshot_commit_verified": remote_head() == snapshot,
    "github_push_returncode": 0,
    "lfs_push_all_returncode": 0,
    "fresh_remote_lfs_fetch_returncode": 0,
    "fresh_remote_lfs_fsck_returncode": 0,
    "all_current_lfs_sha256_verified": True,
    "lfs_files": len(lfs_lines),
    "unique_lfs_objects_verified": len(unique_oids),
    "checkpoint_files": len(manifest),
    "checkpoint_bytes": sum(item["bytes"] for item in manifest.values()),
    "earlier_failed_push_log": "logs/wrap_github_push.txt",
}
Path("notes/github_save_verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
run(["git", "add", "notes/github_save_verification.json"])
run(["git", "commit", "-m", "Record authenticated GitHub save and independently verified checkpoint downloads"])
run(["git", "push", "origin", BRANCH])
final_head = head()
assert remote_head() == final_head
assert not read(["git", "status", "--porcelain"])
print("GITHUB_SAVE_VERIFIED", final_head, flush=True)

print("SAVE_COMPLETE", final_head, "CHECKPOINTS", len(manifest), "REMOTE_LFS_VERIFIED", True, flush=True)
