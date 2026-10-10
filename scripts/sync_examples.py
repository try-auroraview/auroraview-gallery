#!/usr/bin/env python3
"""Refresh the vendored examples/ copy from a local try-auroraview/auroraview checkout.

Usage:
    python scripts/sync_examples.py /path/to/auroraview [--dry-run]

The vendored copy is what makes a fresh clone work with no setup. This script
keeps it honest: it records the upstream commit it synced from, so drift between
this repository and the framework repository stays traceable.

To develop against upstream samples without syncing, point the host at them
instead:  AURORAVIEW_EXAMPLES_DIR=/path/to/auroraview/examples python main.py
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
MANIFEST_NAME = ".upstream-commit"

EXCLUDE = {"__pycache__", ".pytest_cache", ".venv", "node_modules"}


def upstream_commit(checkout: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def relative_files(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        return {}
    files: dict[str, Path] = {}
    for p in root.rglob("*"):
        if p.is_dir() or EXCLUDE & set(p.parts) or p.name == MANIFEST_NAME:
            continue
        files[str(p.relative_to(root))] = p
    return files


def sync(checkout: Path, dry_run: bool) -> int:
    upstream = checkout / "examples"
    if not upstream.is_dir():
        print(f"error: no examples/ directory under {checkout}", file=sys.stderr)
        return 1

    src = relative_files(upstream)
    dst = relative_files(EXAMPLES_DIR)

    added = sorted(set(src) - set(dst))
    removed = sorted(set(dst) - set(src))
    changed = sorted(
        name for name in set(src) & set(dst) if not filecmp.cmp(src[name], dst[name], shallow=False)
    )

    print(f"upstream : {checkout} @ {upstream_commit(checkout)}")
    print(f"added    : {len(added)}")
    print(f"changed  : {len(changed)}")
    print(f"removed  : {len(removed)}")
    for name in added:
        print(f"  + {name}")
    for name in changed:
        print(f"  ~ {name}")
    for name in removed:
        print(f"  - {name}")

    if dry_run:
        print("\n[dry-run] nothing written")
        return 0

    for name in removed:
        (EXAMPLES_DIR / name).unlink()
    for name in added + changed:
        target = EXAMPLES_DIR / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src[name], target)

    manifest = EXAMPLES_DIR / MANIFEST_NAME
    manifest.write_text(f"{upstream_commit(checkout)}\n", encoding="utf-8")
    print(f"\nwrote {manifest.relative_to(REPO_ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync vendored examples from an AuroraView checkout.")
    ap.add_argument("checkout", type=Path, help="path to a try-auroraview/auroraview checkout")
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = ap.parse_args()
    return sync(args.checkout.expanduser().resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
