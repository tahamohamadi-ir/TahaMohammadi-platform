# Taha Site CMS Content Package

This directory is an import-neutral content seed generated from the owner-review draft package.

## What this package is

It converts the owner content into a structured CMS/backend contract with:

- stable IDs
- content types
- locale-specific records
- slugs and routes
- title / excerpt / body
- publication and approval state
- visibility
- dates
- external links
- evidence and source hashes
- restrictions
- SEO fields
- route composition
- owner-approval queue

It is intentionally **not** a publish action.

## Safety gate

A public API or frontend should expose a record only when all three conditions are true:

```text
approval_state == approved
publication_state == published
visibility == public
```

The seed records currently remain `draft` unless an existing restriction requires `not-public`.

## Locale policy

Persian and English are independent content records.

- No automatic locale fallback.
- Do not show an English record on a Persian route unless that behavior is explicitly approved later.
- Missing translations should produce an omitted module or honest unavailable state.

## Files

- `content-model.schema.json` — JSON Schema for a content record.
- `content-records.json` — base seed package **v1.0.0** (66 records).
- `content-records.v1.1-seed.json` — **import target** merged seed (85 records).
- `content-records.ndjson` — one record per line for batch import (v1.0.0 baseline).
- `route-composition.json` — page/slot composition **v1.0.0**.
- `route-composition.v1.1-seed.json` — composition with creative/teaching/CV empty states.
- `supplement/` — v1.1 supplement registry, dev settings, validation (`supplement/README.md`).
- `content-id-registry.csv` — flat registry useful for CMS migration planning.
- `owner-approval-queue.json` — records that still need owner review or publication action.
- `link-registry.json` — canonical public destinations and intentionally private/missing links.
- `validate_content.py` — local validation script.
- `VALIDATION-REPORT.md` — generated QA summary.

## Recommended CMS field mapping

| Package field | CMS field type |
|---|---|
| `content_id` | immutable unique string |
| `content_type` | enum / collection type |
| `slug` | slug |
| `locale` | enum (`en`, `fa`, `und`) |
| `title` | short text |
| `excerpt` | medium text |
| `body_markdown` | long text / Markdown |
| `route` | short text |
| `status.*` | enums |
| `dates.*` | date/datetime or null |
| `sort_order` | integer |
| `tags` | list of strings |
| `links` | repeatable component |
| `data` | structured JSON |
| `evidence` | repeatable component / audit trail |
| `restrictions` | repeatable text / admin only |
| `seo` | structured SEO component |
| `relations` | references / relation component |

## Public rendering rules

1. Query only records that pass the safety gate.
2. Filter by exact locale.
3. Order by `sort_order`.
4. Never treat `restrictions` as public prose.
5. Never synthesize missing fields from another locale.
6. `private` and `admin-only` records must never be returned from published-only APIs.
7. Writing records must display their real `data.work_status`.

## Current known blockers

- Owner approval for all public copy.
- Academic CV/resume files are not yet approved as public downloads.
- Education values still need final verification against official records before publication.
- Stanford credential source must be attached before publication.
- Employer/IP-sensitive behavioral platform content remains private.
- Creative work, teaching, legal/privacy copy, and public location remain intentionally incomplete.

## Source integrity

Parent seed: `../README.md`

- `../source/owner-public-content.md`: `0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770`
- `../manifest/candidate-records.md`: `bda76664a61453abe25dcc1a116765f306f91700d3dda2a2e9c4798bfcda73c7`
- `../source/owner-content-gaps.md`: `4146b7cc5be7e122a1d699fc84057e93128a75a97e7cb5dd30854e6503e32caa`
