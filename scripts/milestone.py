"""Open and close a milestone with one command each.

    make start M=02    switch to an up-to-date main and create the milestone branch
    make close M=02    import the downloaded chapter and log, rebuild the handbook index,
                       commit, run the pre-publish check, push, open the pull request,
                       merge it and return to an up-to-date main
    make fetch F="el/load_raw.py"
                       move a file downloaded from the chat to its place in the repo

The branch name, commit message and pull request title are read from docs/MILESTONES.md,
so they are never typed by hand. Every step stops the script if it fails.
"""
import glob
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PREPUBLISH = r"""
git ls-files --cached | grep -iE "AI_OPERATING_BRIEF|WALKTHROUGH|SESSION_PROTOCOL|PROJECT_INSTRUCTIONS|(^|/)\.env$|\.duckdb$|\.pem$|credentials|key\.json$" \
  && echo "STOP: private file tracked" || echo "OK: no private files tracked"
git grep --cached -nIE "(api[_-]?key|secret|password|token)[[:space:]]*[:=]" -- . ':!*.example' | grep -v "env_var" \
  && echo "STOP: possible secret in code" || echo "OK: no secret patterns"
"""


def fail(message: str) -> None:
    sys.exit(f"\nSTOPPED: {message}")


def run(*cmd: str, check: bool = True, capture: bool = False) -> str:
    print(f"$ {shlex.join(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=REPO, text=True,
                            stdout=subprocess.PIPE if capture else None)
    if check and result.returncode != 0:
        fail(f"'{shlex.join(cmd)}' exited with code {result.returncode}")
    return (result.stdout or "").strip()


def quiet(*cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)


def milestone(number: str) -> tuple[str, str, str]:
    """Return (branch, commit message, pull request title) for milestone NN."""
    text = (REPO / "docs" / "MILESTONES.md").read_text(encoding="utf-8")
    text = re.sub(r"(?ms)^[ \t]*(`{3,})[^\n]*\n.*?^[ \t]*\1[ \t]*$", "", text)
    head = re.search(rf"^## (M{number} — .+)$", text, re.M)
    if not head:
        fail(f"no heading '## M{number} — ...' in docs/MILESTONES.md")
    body = text[head.end():].split("\n## ", 1)[0]
    commit = re.search(rf"\*\*Commit\.\*\* `(m{number}-[a-z0-9-]+)` → `(.+?)`", body)
    if not commit:
        fail(f"no '**Commit.**' line for M{number} in docs/MILESTONES.md")
    return commit.group(1), commit.group(2), head.group(1)


def newest_download(pattern: str) -> Path | None:
    folders = [os.environ["DOWNLOADS"]] if os.environ.get("DOWNLOADS") else \
        glob.glob("/mnt/c/Users/*/Downloads")
    matches = [Path(p) for f in folders for p in glob.glob(os.path.join(f, pattern))]
    return max(matches, key=lambda p: p.stat().st_mtime) if matches else None


def fetch(paths: list[str]) -> None:
    """Move the newest download of each file to its path in the repository."""
    for rel in paths:
        target = REPO / rel
        found = newest_download(f"{target.stem}*{target.suffix}")
        if not found:
            fail(f"{target.name} is not in your Downloads folder; download it from the chat")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(found.read_bytes())
        found.unlink()
        print(f"moved {found} -> {rel} ({target.stat().st_size} bytes)")


def start(number: str) -> None:
    branch, _, title = milestone(number)
    if quiet("git", "status", "--porcelain").stdout.strip():
        fail("the working tree has uncommitted changes; close the previous milestone first")
    run("git", "switch", "main")
    run("git", "pull", "--ff-only")
    run("git", "switch", "-c", branch)
    print(f"\nReady: {title}\nBranch: {branch}")


def close(number: str) -> None:
    branch, message, title = milestone(number)
    print(f"Closing {title}\n")

    print("[1/8] Branch")
    current = run("git", "branch", "--show-current", capture=True)
    if current == "main":
        exists = quiet("git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}")
        run("git", "switch", branch) if exists.returncode == 0 else \
            run("git", "switch", "-c", branch)
    elif current != branch:
        fail(f"you are on '{current}', expected '{branch}' or 'main'")

    print("\n[2/8] Import the downloaded chapter and log")
    targets = [(f"{branch}*.md", REPO / "docs" / "handbook" / f"{branch}.md"),
               ("PROJECT_LOG*.md", REPO / "docs" / "PROJECT_LOG.md")]
    for pattern, target in targets:
        found = newest_download(pattern)
        if found:
            target.write_bytes(found.read_bytes())
            found.unlink()
            print(f"moved {found} -> {target.relative_to(REPO)}")
        elif target.name.startswith(f"m{number}-") and target.exists():
            print(f"no download found; using the existing {target.relative_to(REPO)}")
        elif target.name == "PROJECT_LOG.md" and quiet(
                "git", "diff", "--quiet", "--", str(target)).returncode == 1:
            print("no download found; docs/PROJECT_LOG.md is already modified")
        else:
            fail(f"download {target.name} from the chat into your Downloads folder first")

    print("\n[3/8] Handbook index")
    run(sys.executable, "scripts/build_handbook_index.py")

    print("\n[4/8] Stage and check")
    run("git", "add", "-A")
    run("git", "status", "--short")
    check = subprocess.run(["bash", "-c", PREPUBLISH], cwd=REPO, text=True,
                           capture_output=True).stdout
    print(check.strip())
    if "STOP" in check:
        fail("the pre-publish check found a private file or a secret; nothing was committed")

    print("\n[5/8] Commit")
    if quiet("git", "diff", "--cached", "--quiet").returncode == 1:
        run("git", "commit", "-q", "-m", message)
    run("git", "log", "--oneline", "-1")
    run("git", "fetch", "-q", "origin", "main")
    if run("git", "rev-list", "--count", "origin/main..HEAD", capture=True) == "0":
        fail("this branch has no commits that main does not already have")

    print("\n[6/8] Push and open the pull request")
    run("git", "push", "-u", "origin", branch)
    if quiet("gh", "pr", "view", branch).returncode != 0:
        run("gh", "pr", "create", "--base", "main", "--head", branch, "--title", title,
            "--body", f"Milestone {title}. Chapter: docs/handbook/{branch}.md")

    print("\n[7/8] Checks and merge")
    if (REPO / ".github" / "workflows").is_dir():
        run("gh", "pr", "checks", branch, "--watch", "--fail-fast")
    run("gh", "pr", "merge", branch, "--squash", "--delete-branch")

    print("\n[8/8] Back to main")
    run("git", "switch", "main", check=False)
    run("git", "pull", "--ff-only", "--prune")
    run("git", "log", "--oneline", "-3")
    run("git", "status", "--short", "--branch")
    print(f"\nDone: {title} is merged into main.")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "fetch":
        fetch(sys.argv[2:])
    elif len(sys.argv) == 3 and sys.argv[1] in ("start", "close") \
            and re.fullmatch(r"\d\d", sys.argv[2]):
        {"start": start, "close": close}[sys.argv[1]](sys.argv[2])
    else:
        fail("usage: make start M=NN | make close M=NN | make fetch F=\"path ...\"")
