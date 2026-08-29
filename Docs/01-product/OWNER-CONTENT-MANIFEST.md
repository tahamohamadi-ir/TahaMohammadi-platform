# Owner Content Manifest

Status: **Seed v1.1 ingested** — candidate + supplement records exist; **zero production-published** entries.

Canonical seed package: `Docs/01-product/owner-content-seed-v1/`

Nothing in Seed v1/v1.1 is production-published until the owner explicitly approves wording, source evidence, and publication state per record.

## Publication gate

```text
approval_state == approved
publication_state == published
visibility == public
```

## Seed summary (2026-08-29)

| Package | Records | Published | Import file |
|---|---|---|---|
| v1.0.0 base | 66 | 0 | `cms-package/content-records.json` |
| v1.1 supplement | +19 (85 total) | 0 | `cms-package/content-records.v1.1-seed.json` |

Supplement adds: bilingual empty states (creative, teaching, CV) and admin-only verification rows (academic evidence, IP clearance, legal dependency, writing checklists, seed defaults).

## Required record fields

| Field | Meaning |
|---|---|
| `content_id` | Stable internal manifest identifier |
| `surface` | Public route or admin setting that may consume the value |
| `locale` | `fa`, `en`, or locale-independent |
| `source_path` | Owner-provided file or approved backend record path |
| `source_hash` | SHA-256 when the source is a file |
| `approval_state` | `approved`, `needs-owner-input`, `private`, `unavailable`, or `superseded` |
| `publication_state` | `not-public`, `draft`, `published`, or `retired` |
| `translation_state` | `not-needed`, `approved`, `untranslated`, or `not-authorized` |
| `notes` | Scope and restrictions, not a substitute for the value itself |

## Where to work

| Task | Document |
|---|---|
| Read/edit owner prose | `owner-content-seed-v1/source/owner-public-content.md` |
| See what is still missing | `owner-content-seed-v1/source/owner-content-gaps.md` |
| Review candidate rows | `owner-content-seed-v1/manifest/candidate-records.md` |
| Import/backend seed | `owner-content-seed-v1/cms-package/content-records.v1.1-seed.json` |
| Supplement registry | `owner-content-seed-v1/cms-package/supplement/supplement-registry.csv` |
| Dev defaults | `owner-content-seed-v1/cms-package/supplement/seed-settings.json` |
| Owner approval queue | `owner-content-seed-v1/cms-package/owner-approval-queue.json` |

## Source file integrity

| File | SHA-256 |
|---|---|
| `source/owner-public-content.md` | `0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770` |
| `manifest/candidate-records.md` | `bda76664a61453abe25dcc1a116765f306f91700d3dda2a2e9c4798bfcda73c7` |
| `source/owner-content-gaps.md` | `4146b7cc5be7e122a1d699fc84057e93128a75a97e7cb5dd30854e6503e32caa` |

## Production approval

Until a record is individually marked `approved` + `published`, the UI uses an honest unavailable/empty state or omits the module; it never falls back to concept art copy.
