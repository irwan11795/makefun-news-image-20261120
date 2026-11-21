#!/usr/bin/env python3
"""Entry point for news-image-20261120 (stdlib only).

Copies the pre-rendered entry.png into the output directory and prints its
SHA-256. Verifies the file against the expected hash and fails loudly on any
mismatch. No network, no Pillow, no code generation.
"""
import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path

EXPECTED_SHA256 = "6b96202a53b7977db527e38a76562ec07349ede0c58a45f872949067e4e90662"
ENTRY_NAME = "entry.png"


def output_dir():
    for candidate in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        "./output",
    ):
        if candidate:
            try:
                Path(candidate).mkdir(parents=True, exist_ok=True)
                probe = Path(candidate) / ".write-test"
                probe.write_bytes(b"ok")
                probe.unlink()
                return Path(candidate)
            except OSError:
                continue
    return Path(tempfile.mkdtemp(prefix="makefun-output-"))


def main():
    here = Path(__file__).resolve().parent
    src = here / ENTRY_NAME
    if not src.is_file():
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print("error: entry.png sha256 mismatch", file=sys.stderr)
        print("  expected: " + EXPECTED_SHA256, file=sys.stderr)
        print("  actual:   " + digest, file=sys.stderr)
        return 1
    out = output_dir()
    dest = out / ENTRY_NAME
    shutil.copyfile(src, dest)
    if dest.read_bytes() != data:
        print("error: copied file differs from source", file=sys.stderr)
        return 1
    print(digest)
    print(str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
