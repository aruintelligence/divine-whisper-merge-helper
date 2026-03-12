#!/usr/bin/env python
"""
merge_four_branches.py

Automates the “merge all four branches” step:

    repo-ecos  -> main
    post-launch
    spec-v7
    ray-poc

If any conflict occurs the script aborts and prints a hint.
Run from an empty tmp dir or pass --workspace.
"""

import subprocess as sp
import argparse
from pathlib import Path
import sys

REPO = "git@github.com:<org>/divine-whisper-ecosystem.git"
BRANCHES = ["repo-ecos", "post-launch", "spec-v7", "ray-poc"]  # merge order


def sh(cmd, cwd=None, check=True):
    """run shell command and stream stdout"""
    print("▶", cmd)
    return sp.run(cmd, shell=True, cwd=cwd, check=check)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=Path, default=Path("./dw-merge-ws"))
    args = ap.parse_args()

    ws = args.workspace
    ws.mkdir(parents=True, exist_ok=True)

    # 1. clone
    if not (ws / "divine-whisper-ecosystem").exists():
        sh(f"git clone {REPO}", cwd=ws)
    repo = ws / "divine-whisper-ecosystem"

    # 2. fetch all remote branches
    sh("git fetch --all --prune", cwd=repo)

    # 3. checkout main fresh
    sh("git checkout main", cwd=repo)
    sh("git pull origin main", cwd=repo)

    # 4. merge branches sequentially
    for br in BRANCHES:
        # ensure branch exists
        res = sp.run(f"git rev-parse --verify origin/{br}", shell=True, cwd=repo)
        if res.returncode != 0:
            sys.exit(f"❌ Branch {br} not found on remote")
        print(f"🔀  merging {br} → main")
        try:
            sh(f"git merge --no-ff origin/{br} -m 'merge: {br} into main'", cwd=repo)
        except sp.CalledProcessError:
            print("❌ merge conflict — resolve manually; aborting")
            sys.exit(1)

    # 5. push
    sh("git push origin main", cwd=repo)
    print("✅  all four branches merged and pushed to main")


if __name__ == "__main__":
    main()
