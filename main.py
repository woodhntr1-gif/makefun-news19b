#!/usr/bin/env python3
"""Entry point for the make.fun bounty news-image-20261119.

The repository holds entry.png, the one-image summary of the world news
of Thursday 19 November 2026 (drawn by render.py). This program's whole
job is to place those exact bytes at the output location the grader
names, so the two grading runs produce identical files.

Standard library only; no network.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.png")


def main():
    dest = output_path()
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    with open(SOURCE, "rb") as a, open(dest, "rb") as b:
        if a.read() != b.read():
            print("copy mismatch", file=sys.stderr)
            return 1
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
