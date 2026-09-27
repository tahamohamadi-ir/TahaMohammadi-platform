#!/usr/bin/env python3
"""Check that local documentation links resolve.

The execution-queue validator already checks links inside
`Docs/05-delivery/concept-alignment-v2/`, but that is the scope of the packet
allowlist, not of the documentation set. A link that rots in a tracking or
design document is invisible to it, and a reader following it gets a 404 in the
middle of a decision record.

Excluded by design, and why:
  * `Docs/references/` - historical evidence, not executable instructions.
  * `Docs/superpowers/` and `Docs/templates/` - archived plans and scaffolding.
  * External and anchor-only links - not resolvable from the filesystem.

Read-only: it reports and exits non-zero, and never rewrites a document.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
SKIP = ("references/", "superpowers/", "templates/")
LINK = re.compile(r"\]\(([^)\s]+)")
REMOTE = ("http:", "https:", "#", "mailto:", "tel:", "data:")


def main() -> int:
    if not DOCS.is_dir():
        print(f"error: {DOCS} does not exist", file=sys.stderr)
        return 1

    checked = 0
    broken = []
    scanned = 0

    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in rel for part in SKIP):
            continue
        scanned += 1
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            if target.startswith(REMOTE):
                continue
            checked += 1
            local = target.split("#", 1)[0]
            if not local:
                continue
            if not (path.parent / local).resolve().exists():
                broken.append(f"{rel} -> {target}")

    if broken:
        print(f"Broken local documentation links ({len(broken)}):", file=sys.stderr)
        for item in broken:
            print(f"  {item}", file=sys.stderr)
        return 1

    print(f"OK: {checked} local links across {scanned} documents resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
