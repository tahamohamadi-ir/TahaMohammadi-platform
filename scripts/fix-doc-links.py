#!/usr/bin/env python3
"""One-off: repair the three classes of broken local link found by
`check-doc-links.py` on 2026-09-27.

Each rewrite is mechanical and path-preserving:
  1. `](../PUBLIC-190-asset-prompts/...)` -> `](./PUBLIC-190-asset-prompts/...)`
     The document lives in `Docs/10-tracking/`, so `../` climbed to `Docs/` and
     missed the sibling directory.
  2. `](file:///d:/Project/...)` -> the workspace-relative path.
     An absolute path from one developer's machine is broken everywhere else.
  3. `](<uuid>)` in WORK-LOG -> plain code span. The parenthesised seed UUID
     was prose, not a link; markdown rendered it as one and pointed it at a
     file that never existed.

Idempotent, and it reports what it changed rather than silently rewriting.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Byte-level replacements. Read/write as BYTES, never as decoded text: these
# documents contain em dashes and section signs, and a text round-trip through a
# mis-guessed codec silently corrupts every one of them into mojibake. That is
# exactly what happened on the first attempt at this repair.
REPAIRS = [
    (
        b"Docs/10-tracking/PUBLIC-190-VISUAL-REMEDIATION-PLAN.md",
        b"](../PUBLIC-190-asset-prompts/",
        b"](./PUBLIC-190-asset-prompts/",
    ),
    (
        b"Docs/10-tracking/product-v2/PU-01-HANDOFF.md",
        b"](../PUBLIC-190-asset-prompts/",
        b"](./PUBLIC-190-asset-prompts/",
    ),
    (
        b"Docs/10-tracking/product-v2/PU-01-HANDOFF.md",
        b"](file:///d:/Project/tahamohammadi-platform/Docs/05-delivery/concept-alignment-v2/",
        b"](../../05-delivery/concept-alignment-v2/",
    ),
    (
        b"Docs/10-tracking/WORK-LOG.md",
        b"](b6bf1fce-8a04-40a3-8ef5-eb106256cd51)",
        b" (b6bf1fce-8a04-40a3-8ef5-eb106256cd51)",
    ),
]


def main() -> int:
    total = 0
    for raw_rel, pattern, replacement in REPAIRS:
        path = ROOT / raw_rel.decode("ascii")
        if not path.is_file():
            print(f"skip (absent): {raw_rel.decode('ascii')}")
            continue
        before = path.read_bytes()
        after, count = before.replace(pattern, replacement), before.count(pattern)
        if count:
            path.write_bytes(after)
        print(f"{raw_rel.decode('ascii')}: {count} replacement(s)")
        total += count
    print(f"total replacements: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
