#!/usr/bin/env python3
"""Publish THE DAILY ATLAS -- Thursday 19 November 2026.

Copies the entry image bundled next to this file to /output/entry.png.
Before copying, it checks that the bundled file exists and that its first
eight bytes are the PNG signature, so a missing or non-PNG file is refused
rather than published. Python 3.13, standard library only, no network.
"""
import hashlib
import shutil
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        raise SystemExit(f"missing entry image: {source}")
    header = source.read_bytes()[:8]
    if header != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a PNG file (bad signature)")
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    expected_size = source.stat().st_size
    expected_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    size = target.stat().st_size
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if size != expected_size or digest != expected_digest:
        raise SystemExit("copy verification failed: /output/entry.png differs from entry.png")
    print(f"published {target} ({size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
