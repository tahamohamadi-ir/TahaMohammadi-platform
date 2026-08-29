# Owner content — Seed v1

Status: **seed only** — not approved for production publication.

This package holds owner-authored factual drafts plus a **v1.1 seed supplement** for safe empty states and admin-only verification records. Agents may use it for backend seeding, CMS migration planning, and scaffold development. Nothing is published until each record passes the three-part gate:

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
| `manifest/candidate-records.md` | Flat manifest table (39 candidate rows from base draft) |
| `cms-package/content-records.json` | Base machine seed **v1.0.0** — 66 records |
| `cms-package/content-records.v1.1-seed.json` | **Import target** — 85 records (base + supplement) |
| `cms-package/route-composition.v1.1-seed.json` | Route slots including creative/teaching/CV empty states |
| `cms-package/supplement/` | Supplement metadata, settings, registry, validation |

## Seed versions

| Version | Records | Notes |
|---|---|---|
| v1.0.0 | 66 | Owner draft package; 0 published |
| v1.1-seed | 85 | Adds 19 records: 6 public empty-state copies, 13 admin-only verification rows |

Supplement details: `cms-package/supplement/README.md`

Default dev settings: `cms-package/supplement/seed-settings.json` (email public, phone private, no locale fallback, CV download disabled).

## Source integrity

| File | SHA-256 |
|---|---|
| `source/owner-public-content.md` | `0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770` |
| `manifest/candidate-records.md` | `bda76664a61453abe25dcc1a116765f306f91700d3dda2a2e9c4798bfcda73c7` |
| `source/owner-content-gaps.md` | `4146b7cc5be7e122a1d699fc84057e93128a75a97e7cb5dd30854e6503e32caa` |

## Import rule

Backend seed importers must use **`content-records.v1.1-seed.json`** unless a task explicitly tests the v1.0.0 baseline. All imported records remain `draft` or `not-public` unless individually promoted.

## Canonical registry

`Docs/01-product/OWNER-CONTENT-MANIFEST.md`

## Locale policy

Persian and English are independent. No automatic fallback between locales.
