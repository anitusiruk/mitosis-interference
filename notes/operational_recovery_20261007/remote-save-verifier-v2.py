"""Push the preserved study and verify independently downloaded GitHub LFS objects.

Run from the authoritative checkout after authenticating GitHub CLI.
All command output stays outside Git; the committed receipt contains no credentials.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import shutil


ROOT = Path.cwd()
BRANCH = "day5-causal-audit"
WORKSPACE = ROOT.parent
ENV = os.environ.copy()
ENV.update(GIT_TERMINAL_PROMPT="0", GH_PROMPT_DISABLED="1", GCM_INTERACTIVE="never")


def now():
    return datetime.now(timezone.utc).isoformat()


def run(args, timeout=7200):
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


def lfs_map(commit=None):
    args = ["git", "lfs", "ls-files", "--long"]
    if commit:
        args.append(commit)
    return {line.split(" ", 2)[2]: line.split()[0]
            for line in read(args).splitlines()}


def seed_verified_remote_objects(storage, current_oids):
    """Reuse only immutable objects covered by a saved independent-download receipt.

    Every source object is rehashed before linking. Ordinary local LFS storage
    is never a source. Missing or discrepant historical storage fails closed.
    The receipt explicitly distinguishes reuse from a new empty-cache download.
    """
    sources, seeded = [], set()
    plans = [
        ("notes/github_save_verification.json", "all_current_lfs_sha256_verified",
         None, "mitosis-lfs-verify-*"),
        ("notes/day17_github_save_verification.json", "all_day17_lfs_sha256_verified",
         "results/day17_", "mitosis-day17-lfs-verify-*"),
        ("notes/day19_github_save_verification.json", "all_day19_lfs_sha256_verified",
         "results/day19_", "mitosis-day19-lfs-verify-*"),
    ]
    for name, flag, prefix, pattern in plans:
        receipt_path = Path(name)
        if not receipt_path.exists():
            continue
        receipt = json.loads(receipt_path.read_text())
        assert receipt[flag] and receipt["repository"] == "anitusiruk/mitosis-interference"
        paths = lfs_map(receipt["preserved_snapshot_commit"])
        source_oids = {oid for path, oid in paths.items()
                       if prefix is None or (path.startswith(prefix) and "checkpoint" in Path(path).parts)}
        assert len(source_oids) == receipt["unique_lfs_objects_verified"], name
        candidates = ([Path(receipt["verification_storage"])] if receipt.get("verification_storage")
                      else sorted(WORKSPACE.glob(pattern)))
        # A storage path is accepted only when it covers the complete receipt scope.
        candidates = [p for p in candidates if p != storage and all(
            (p / "objects" / oid[:2] / oid[2:4] / oid).is_file() for oid in source_oids)]
        assert candidates, "Historical independent-download cache unavailable: " + name
        source = candidates[-1]
        for oid in source_oids:
            obj = source / "objects" / oid[:2] / oid[2:4] / oid
            assert file_hash(obj) == oid, "Historical remote object changed: " + oid
            if oid in current_oids:
                target = storage / "objects" / oid[:2] / oid[2:4] / oid
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    try:
                        os.link(obj, target)
                    except OSError:
                        shutil.copyfile(obj, target)
                assert file_hash(target) == oid
                seeded.add(oid)
        sources.append({"receipt_path": name, "receipt_sha256": file_hash(receipt_path),
                        "snapshot_commit": receipt["preserved_snapshot_commit"],
                        "independent_download_storage": str(source),
                        "receipt_scope_objects_rehashed": len(source_oids),
                        "objects_in_current_snapshot": len(source_oids & current_oids)})
    return sources, seeded


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
    assert file_hash(Path(name)) == expected["sha256"], name
by_path = lfs_map()
for name in tensor_paths:
    assert manifest[name]["sha256"] == by_path[name], "Local checkpoint is not its Git LFS object: " + name
run(["git", "lfs", "fsck"])
run(["git", "push", "--set-upstream", "origin", BRANCH])
assert remote_head() == snapshot, "GitHub ref does not match preserved state"
run(["git", "lfs", "push", "--all", "origin", BRANCH])

fresh_storage = WORKSPACE / ("mitosis-lfs-verify-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
assert not fresh_storage.exists(), "Verification must use a new empty storage directory"
unique_oids = set(by_path.values())
sources, seeded_oids = seed_verified_remote_objects(fresh_storage, unique_oids)
run(["git", "-c", f"lfs.storage={fresh_storage}", "lfs", "fetch", "--include=*", "--exclude=", "origin", BRANCH])
run(["git", "-c", f"lfs.storage={fresh_storage}", "lfs", "fsck"])
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
    "verification_mode": "incremental_independent_remote_download_with_rehashed_immutable_objects",
    "verification_storage": str(fresh_storage),
    "previous_independent_download_sources": sources,
    "previously_downloaded_objects_rehashed_and_reused": len(seeded_oids),
    "new_objects_downloaded_from_github": len(unique_oids - seeded_oids),
    "incremental_remote_lfs_fetch_returncode": 0,
    "complete_snapshot_lfs_fsck_returncode": 0,
    "all_current_lfs_sha256_verified": True,
    "lfs_files": len(lfs_lines),
    "unique_lfs_objects_verified": len(unique_oids),
    "checkpoint_files": len(manifest),
    "checkpoint_bytes": sum(item["bytes"] for item in manifest.values()),
    "earlier_failed_push_log": "logs/wrap_github_push.txt",
}
prior = Path("notes/github_save_verification.json")
prior_data = json.loads(prior.read_text())
history = Path("notes/github_save_verification_history")
history.mkdir(exist_ok=True)
archive = history / (prior_data["preserved_snapshot_commit"] + ".json")
if archive.exists():
    assert archive.read_bytes() == prior.read_bytes()
else:
    archive.write_bytes(prior.read_bytes())
Path("notes/github_save_verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
run(["git", "add", "notes/github_save_verification.json", str(archive)])
run(["git", "commit", "-m", "Record authenticated GitHub save and independently verified checkpoint downloads"])
run(["git", "push", "origin", BRANCH])
final_head = head()
assert remote_head() == final_head
assert not read(["git", "status", "--porcelain"])
print("GITHUB_SAVE_VERIFIED", final_head, flush=True)

print("SAVE_COMPLETE", final_head, "CHECKPOINTS", len(manifest), "REMOTE_LFS_VERIFIED", True, flush=True)

