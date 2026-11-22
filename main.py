"""Copy the bundled news image to the grader's output directory.

The image is drawn once, offline, and stored in this repository as
entry.png. This program only copies those exact bytes to
$MAKEFUN_OUTPUT_DIR/entry.png, so every run is byte-identical and
needs nothing beyond the standard library: no fonts, no image
libraries, no network.
"""

import hashlib
import os
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
IMAGE_NAME = "entry.png"


def repo_dir() -> Path:
    return Path(__file__).resolve().parent


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> int:
    source = repo_dir() / IMAGE_NAME
    data = source.read_bytes()

    if not data.startswith(PNG_SIGNATURE):
        print(f"entry.png is not a PNG file: {source}", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1

    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    target.write_bytes(data)

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
