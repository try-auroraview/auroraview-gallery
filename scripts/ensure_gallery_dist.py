from __future__ import annotations

import subprocess
from pathlib import Path


def main() -> int:
    # This repository *is* the Gallery app, so scripts/ -> <repo> is the app root.
    gallery_dir = Path(__file__).resolve().parent.parent
    dist_index = gallery_dir / "dist" / "index.html"

    if dist_index.exists():
        print(f"[OK] Reusing existing Gallery build: {dist_index}")
        return 0

    print("[INFO] dist/ not found; building frontend...")
    completed = subprocess.run(["npm", "run", "build"], cwd=gallery_dir)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
