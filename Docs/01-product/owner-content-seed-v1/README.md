# Owner content — Seed v1

Status: **seed only** — not approved for production publication.

This package holds the first owner-authored factual draft. Agents and importers may use it for backend seeding, CMS migration planning, and scaffold development. Nothing here is published until each record passes the three-part gate:

```text
approval_state == approved
publication_state == published
visibility == public
```

## Layout

| Path | Purpose |
|---|---|
| `source/owner-public-content.md` | Human-readable owner draft (identity, bio, projects, writing, contact) |
| `source/owner-content-gaps.md` | Checklist of items still needing owner decision or evidence |
| `manifest/candidate-records.md` | Flat manifest table (39 candidate rows; all draft or private) |
| `cms-package/` | Machine-readable seed: 66 structured records, route composition, approval queue |

## Seed v1 stats (2026-08-29)

- Structured records: **66** (35 `en`, 26 `fa`, 5 locale-independent)
- Published records: **0**
- Private records: **2** (`project.behavior-platform`, sensitive contact fields)
- Validation: `python cms-package/validate_content.py` → PASS

## Source integrity

| File | SHA-256 |
|---|---|
| `source/owner-public-content.md` | `0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770` |
| `manifest/candidate-records.md` | `bda76664a61453abe25dcc1a116765f306f91700d3dda2a2e9c4798bfcda73c7` |
| `source/owner-content-gaps.md` | `4146b7cc5be7e122a1d699fc84057e93128a75a97e7cb5dd30854e6503e32caa` |

## Canonical registry

The workspace-level registry is `Docs/01-product/OWNER-CONTENT-MANIFEST.md`. It points here until records are individually approved for production.

## Locale policy

Persian and English are independent. No automatic fallback between locales.
