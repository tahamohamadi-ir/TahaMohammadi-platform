# Frontend Reference Consolidation Migration Report

## Baseline

Generated from `Front-End/Assets` on 2026-08-29 by `generate-inventory.ps1`.

| Measure | Value |
|---|---:|
| Incoming files | 172 |
| Incoming unique SHA-256 values | 105 |
| Incoming bytes | 174,809,510 |
| Verified deletion candidates | 65 |
| Unique unmanaged `others/` files retained locally | 14 |
| Tracked canonical binary files | 30 |
| Tracked canonical aliases | 3 |
| Component definitions | 24 |
| Template definitions | 6 |

## Classification

- `verified-duplicate`: candidate is byte-identical to a retained tracked authority or legacy-planning evidence file. `DELETION-MAP.json` records the retained path.
- `retained-local-source`: source master remains in the local input tree after its canonical tracked copy was created.
- `unmanaged-unique`: local-only evidence preserved under the local archive and explicitly excluded from implementation authority.
- `history`: planning/history evidence retained locally or in `Docs/references/legacy-planning`; not active authority.
- `needs-review`: top-level package documentation to be moved into local provenance or mapped to an existing tracked document before cleanup.

## Destructive-action guard

No candidate may be removed solely because its name looks duplicated. The cleanup command reads `DELETION-MAP.json`, recalculates the candidate SHA-256, recalculates the retained file SHA-256, and stops if they differ. Local unique archive moves are not deletions and preserve the original bytes.

## Authority result

`Docs/references/frontend-design-authority` is the active tracked visual reference. The old `site-redesign` tree was retired after active-path search and validation; its prior state remains recoverable through Git history. The ignored `Front-End/Assets` tree remains a local incoming source and cannot be used as a routine implementation dependency.

## Local cleanup evidence

The incoming inventory recorded 172 files, 105 unique SHA-256 values, and 65 safe deletion candidates. The cleanup script validated the tracked authority before mutation, removed exactly those 65 hash-proven duplicates, retained 30 unique local files in `Front-End/Assets/archive/`, normalized the two requested concept variants, and removed the now-empty legacy duplicate folders. The 166-file, 174,749,215-byte former tracked tree was then retired from the working tree; Git history remains its recovery path.
