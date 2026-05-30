#!/usr/bin/env python3
"""Fail if any public HTML page contains invalid JSON-LD."""
import glob
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ("/archive/", "/mockups/")


def main():
    errors = []
    for path in glob.glob(os.path.join(BASE, "**/*.html"), recursive=True):
        if any(part in path for part in SKIP):
            continue
        rel = os.path.relpath(path, BASE)
        html = open(path, encoding="utf-8").read()
        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        )
        for idx, block in enumerate(blocks, 1):
            raw = block.strip()
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel} block {idx}: {exc.msg} (line {exc.lineno})")
    if errors:
        print("Invalid JSON-LD found:")
        for err in errors:
            print(" -", err)
        return 1
    print("JSON-LD OK on all public HTML pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
