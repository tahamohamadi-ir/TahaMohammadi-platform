# Owner Content Manifest

Status: **Seed v1 ingested** — candidate records exist; **zero production-approved** entries.

Canonical seed package: `Docs/01-product/owner-content-seed-v1/`

Nothing in Seed v1 is published until the owner explicitly approves wording, source evidence, and publication state per record.

## Publication gate

```text
approval_state == approved
publication_state == published
visibility == public
```

## Seed v1 summary (2026-08-29)

| Metric | Value |
|---|---|
| Structured CMS records | 66 |
| Flat manifest candidates | 39 |
| Published | 0 |
| Private by default | 2 (`project.behavior-platform`, `contact.phone`) |
| Validation | PASS (`owner-content-seed-v1/cms-package/validate_content.py`) |

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
| Import/backend seed | `owner-content-seed-v1/cms-package/content-records.json` |
| Owner approval queue | `owner-content-seed-v1/cms-package/owner-approval-queue.json` |

## Source file integrity (Seed v1)

| File | SHA-256 |
|---|---|
| `source/owner-public-content.md` | `0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770` |
| `manifest/candidate-records.md` | `bda76664a61453abe25dcc1a116765f306f91700d3dda2a2e9c4798bfcda73c7` |
| `source/owner-content-gaps.md` | `4146b7cc5be7e122a1d699fc84057e93128a75a97e7cb5dd30854e6503e32caa` |

## Production approval

Until a record is individually marked `approved` + `published`, the UI uses an honest unavailable state or omits the module; it never falls back to concept art copy.
