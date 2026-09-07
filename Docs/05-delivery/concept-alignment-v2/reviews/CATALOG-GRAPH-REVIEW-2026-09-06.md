# Catalog and graph coordinator review — 2026-09-06

Decision: **PU-04-catalog REVISE; CA-02 REVISE**. Neither packet receives local acceptance from this review. Existing acceptance manifests are preserved; no product code, schema, commit or deployment was changed. This review adds concrete reproduction evidence and reconciles queue state.

## Independent checks

- `uv run pytest tests/test_product_story_blocks.py tests/test_product_localized_settings.py -q`: **24 passed** (7 catalog, 17 settings).
- `npm.cmd test -- src/lib/hero-graph-content.test.ts src/lib/hero-graph-resolve.test.ts src/lib/product-resolver.contract.test.ts`: **42 passed** (23 + 10 + 9).
- Plan validator before review: PASS; both packets were ready_for_review.
- Additional backend probes used a disposable Django test database, created/destroyed by setup_databases/teardown_databases. Synthetic Media metadata used bulk_create so no file or real upload was written; the probe measures URL projection, not actual file retrieval.
- Additional PUBLIC probes loaded the actual TypeScript module through Vite SSR and evaluated the returned URL with the standard URL parser. No public fixture or production output was published.

Passing existing tests does not cover the following reproduced cases.

## C1 — restricted download URL exposed by file block (P1)

`Back-End/apps/composition/projection.py:109` checks download.status and media.is_active, but does not enforce `Download.public_media_is_downloadable()`, exact locale, or published_at. It emits the direct storage URL instead of preserving the existing download endpoint's access checks.

Reproduction: a synthetic published Download, locale fa, access_state restricted, with active media:

```json
{"public_download_allowed":false,"projected_file":{"1":{"id":1,"title":"Synthetic restricted","slug":"synthetic","url":"/media/audit/synthetic.pdf","mime":"application/pdf","size":0}}}
```

The normal download endpoint in apps/api/api.py explicitly rejects this record through public_media_is_downloadable. The block projection bypasses that guard. This proves disallowed URL disclosure; no claim is made that the synthetic nonexistent file was downloadable.

Required correction, owner PU-04-catalog:
- Resolve downloads with the same publication/access policy as the existing endpoint, exact story locale, and current published-snapshot policy.
- Preserve gated file delivery; do not place direct storage URLs in the public story when the download is restricted, metadata-only, inactive, future-dated or otherwise ineligible.
- Test actual public story responses, both live and snapshot-backed, for public/restricted/metadata-only/draft/future/inactive/wrong-locale records. Include approved positive cases and preserve no-JS consumers.

## C2 — related block copies unresolved references verbatim (P2)

`_project_settings` copies `records` without public resolution. Actual call:

```json
{"unresolved_related_projection":{"records":[{"family":"article","id":"999999"}]}}
```

I03 requires exact-locale published references and omission of unpublished/missing references. Syntax validation alone is insufficient. Resolve through the shared published-record policy, preserve order, and omit ineligible references. Test missing, private/draft, archived, other-locale and valid references in the returned story. Do not invent slugs. Confirm the final block shape with renderer/editor consumers before changing the public interface.

## C3 — file ID conversion can raise ValueError (P2)

`Back-End/apps/composition/blocks.py:499` uses isdigit then int. Actual call to `validate_block_settings('file', {'downloadId': '\u00b2'}, kind=KIND_STORY)` raises **ValueError**, not BlockValidationError. The same parsing pattern exists in media IDs; inspect shared parsing before altering legacy behavior.

Require bounded canonical ASCII ID validation before conversion/query, matching actual model storage range. Add Unicode, overlong, zero/negative and overflow tests at validation and HTTP boundaries; malformed input must not become an internal error.

## G1 — unsafe slug segments change the link destination (P2)

Actual `workRefToHref` results from src/lib/hero-graph-content.ts:

```json
{"slug":"..","href":"/en/blog/../","browserPath":"/en/"}
{"slug":"%2e%2e","href":"/en/blog/%2e%2e/","browserPath":"/en/"}
{"slug":"normal","href":"/en/blog/normal/","browserPath":"/en/blog/normal/"}
```

`SAFE_SLUG_RE` allows dot segments, percent-encoded navigation segments and backslashes. The route-family regex checks shape, not the allowed mapping for a content family. These break the packet's no-guessed/incorrect-link requirement even without script execution.

Required correction, owner CA-02: use one authoritative family-to-canonical-route mapping and validated/encoded path segments. Reject dot traversal, encoded separators/dot navigation and malformed non-string response values without throwing. Handle singleton Home/About according to the actual route contract. Test the browser-normalized pathname and correct Persian slug handling, not just string interpolation.

## G2 — frontend ID bound differs from backend (P2)

`isValidRelatedRecordId('2147483648')` returns false. PUBLIC caps IDs at 2147483647; backend resolver accepts signed 64-bit positive IDs, and DEFAULT_AUTO_FIELD is BigAutoField. The catalog related validator also uses the smaller bound.

Use bounded decimal-string comparison or BigInt without lossy Number conversion, aligned with backend signed64 limits. Test boundary, maximum, overflow and canonical spelling. Preserve IDs as strings on the wire.

## G3 — unsupported family can invalidate a mixed resolver batch (P2)

PUBLIC's eligible list includes lesson and collection. Backend RESOLVER_FAMILIES currently has 13 families and excludes both; an unknown family returns 400 for the entire batch. Thus a graph containing an unsupported ref alongside a valid article can suppress the valid article link. Existing tests verify lesson-400 and isolated frontend eligibility separately, not the mixed round trip.

Immediate CA-02 correction: distinguish adapter-visible families from families supported by the current resolver. Unsupported references must remain non-links without poisoning supported batches. Add a mixed article+lesson+collection test against the actual resolver contract.

Contract clarification: I03 explicitly says to extend collection/lesson registries when their projections exist. Projections and generic admin entities now exist in the implementation, though their owning packets remain unaccepted. This is planned implementation/integration work to track under PU-05-lessons/PU-06-collection and resolver synchronization, not automatically a new product decision. Future support must include published parent-course and exact-locale guards. Do not advertise lesson support before that work is reviewed.

## Settings publish concurrency — bounded conclusion

The current POST /site/{locale}/publish locks the row and publishes its latest draft. It does not read If-Match, including a supplied stale value. This serializes database writes but does **not** prove the published draft is the version the operator previously reviewed.

I04 explicitly specifies If-Match for GET/PUT and describes POST publish separately. Therefore this review does not silently rewrite the accepted POST contract or revoke settings acceptance based solely on absence of a publish precondition. The earlier phrase “race is benign” is not substantiated for editor intent.

Before a publishing UI promises “publish the version you reviewed”, define and test its precondition: editor A reads version 1, editor B commits version 2, editor A publishes version 1. Either reject the stale publication with the documented envelope or explicitly present “publish latest saved draft” semantics. Record the decision in the publishing/editor contract; no real concurrent-request test was run in this review, and row-lock inspection is not reported as such.

## Dispatch and stop

Both reviewed packets are REVISE with this evidence path. CA-01, PU-03-resolver, PU-03-settings and PU-SYNC-graph acceptance remains scoped to their pinned artifacts. No new acceptance was granted. The validator additionally exposes ready_for_revision so an empty ready_to_start cannot be mistaken for a prohibition on fixing these packets.

Next action: correct C1–C3 within PU-04-catalog and G1–G3 within CA-02, add the regressions above, run focused and affected integration tests, and return new revision handoffs. Any shared accepted-file changes require explicit impact review and updated hash evidence; do not blindly refresh manifests. Real ingress, visual acceptance and rollout remain OPEN.
