# PU-03-resolver — coordinator review R1

Decision: **REVISE**, uncommitted. PU-SYNC-graph remains dependency-blocked pending accepted resolver revision.

## Verified evidence

The supplied attachment reports this backend packet, separately from the user's CA-01 message. Current source and handoff were inspected. The original test command was independently rerun: **25 passed**. Passing those cases is not acceptance of unchecked input handling.

Direct calls to the actual resolver with `article:` followed by U+00B2 (superscript two), or 5000 ASCII nines, raised **ValueError**, not the required controlled HTTP 400. `str.isdigit()` admits characters that `int()` does not parse, and unbounded conversion can exceed Python's integer-string limit. No database access is needed to reproduce these failures.

## Required revision — keep original BACKEND allowlist

1. Validate ASCII decimal ID syntax and length/range before integer conversion. Reject noncanonical leading zeros with 400 (IDs must match `[1-9][0-9]*` and fit the record-key storage range). This also prevents accepted `article:0001` from being incorrectly reported unresolved despite existing record 1. Do not use permissive isdigit as the conversion guard.
2. Return the new-endpoint error envelope from PRODUCT-INTERFACES-V2 I08 / ERROR-CONTRACT: code, safe message, field_errors, server-generated request_id. Current HttpError responses use the legacy detail-only shape. Add explicit 400/404 response schema without globally changing legacy API errors. Do not echo full attacker-supplied refs into messages.
3. Add HTTP-level regression tests for U+00B2, non-ASCII digits, leading zeros, overlong/out-of-range IDs and malformed refs; assert controlled status/envelope and no unhandled exception. Retain order/deduplication, 50-reference bound and private/draft/locale exclusion tests.
4. Source-export both schemas and update provenance/hash/inventory after tests. Append revision results to the existing handoff; retain its original record. Do not manually edit generated schema bodies.

## Acceptance

Run `uv run pytest tests/test_product_record_resolver.py`, `uv run ruff check .`, and source schema export. Show failing-before/passing-after evidence for new boundary cases and exact changed paths. No migration, publication or frontend type sync belongs to this revision.

Return `PU-03-resolver_R1_HANDOFF_READY`. No next packet, commit, push or deploy is requested here.
