# ADR-0006 — Error envelope normalization plan (non-breaking)

Status: Accepted (2026-09-02)

> Accepted by owner delegation: the owner directed the agent to review this
> plan and take the best decision (session instruction, 2026-09-02); review
> verified the inventory against source and fixtures and found the plan
> consistent with `ERROR-CONTRACT.md` and the stable-code registry. Per
> `AUTHORITY-ORDER.md` this acceptance is recorded here and in
> `Docs/10-tracking/DECISION-LOG.md`. The plan itself still changes no wire
> behavior by itself: phases below remain evidence-gated, and any artifact
> hash change still reopens PS-05 under `OPENAPI-ACCEPTANCE.md` change
> control.

## Context

### Problem

The workspace has one documented target error envelope
(`Docs/03-contracts/ERROR-CONTRACT.md`) but several concurrently served error
shapes across the backend's surfaces. Clients (public-site, admin-panel) must
currently normalize every shape themselves, per the client rules in
`ERROR-COMPATIBILITY-MATRIX.md`. A normalization path is needed that never
breaks an existing consumer and never silently changes an accepted artifact.

### Constraints

- Stable admin error-code strings are wire contract and must never be renamed
  (`Back-End/apps/api/admin_common.py`, "declare once, never rename" registry).
- Any schema or backend-source change that alters an accepted OpenAPI artifact
  hash reopens PS-05 and requires regeneration, access tests, a review report,
  and a new acceptance record (`Docs/03-contracts/OPENAPI-ACCEPTANCE.md`,
  "Change control").
- Public messages must never expose stack traces, filesystem paths,
  credentials, database details, or internal identifiers
  (`ERROR-CONTRACT.md`).
- Clients must map unknown errors to a safe generic state and may preserve a
  request identifier only when the server actually provides one
  (`ERROR-CONTRACT.md`). No server-side request-id generation exists in the
  current source, so this plan must not fabricate one.
- Backend behavior is preserved until a tested task explicitly changes it
  (`Back-End/AGENTS.md`).

### Inventory of current error-envelope shapes (verified in source and fixtures)

| # | Surface | Routes | Source of truth | Observed shape | Status codes |
|---|---|---|---|---|---|
| 1 | Admin API `AdminError` (Problem-Details-style) | `/api/v1/admin/**` | `apps/api/admin_common.py` (`AdminError`, `_api_error_handler`) | `{ "code", "message", "fields"? }` — `fields` omitted when empty | Per `AdminError.status`; includes 401/403/428/409/400 and 429 login rate limit (`RATE_LIMITED`, `apps/api/admin_api.py`) |
| 2 | Admin API conflict extension | `/api/v1/admin/**` conflict handlers | e.g. `apps/api/admin_content.py` (`AdminConflictError`, `_admin_conflict_handler`) | `{ "code": "CONFLICT", "message", "currentUpdatedAt" }` — extension key on the base shape | 409 |
| 3 | Legacy admin profile API | `/api/admin/profiles/{locale}/{slug}` (GET/PUT), `.../siblings/{target_locale}` (POST) | `apps/content/admin_api.py` (`_json_error`) | `{ "code", "detail", **extras }` — extras seen: `currentRevision`, `editorUrl`; PUT validation: `{ "code": "VALIDATION_ERROR", "detail": <dict\|list> }` | 400/401/403/404/409/428 |
| 4 | Public Ninja API `HttpError` | `/api/**` (e.g. `/api/profiles/{locale}/{slug}`) | `apps/api/api.py` (`raise HttpError(404, ...)`); fixture `tests/fixtures/contracts/errors/profile-not-found.404.json` | `{ "detail": "<message>" }` | 404 (documented instance) |
| 5 | Ninja request-validation errors | `/api/**` | framework default; fixture `tests/fixtures/contracts/errors/framework-validation.unhandled.json` (`/api/articles/en?page=not-a-number`) | `{ "detail": [ { "type", "loc", "msg" } ] }` | 422 |
| 6 | Contact JSON failure | `POST /api/contact` (non-form content types) | `apps/api/public_contact.py` (`fail` → `_json_response`); fixture `tests/fixtures/contracts/errors/contact.post.error.json` | `{ "ok": false, "error": "<safe message>" }` (success: `{ "ok": true }`) | 400 (cross-origin, invalid JSON, invalid email, empty message), 404 (form disabled), 429 (rate limit), 503 (inbox/delivery not configured) |
| 7 | Contact HTML failure page | `POST /api/contact` (form posts, no-JS progressive path) | `apps/api/public_contact.py` (`_html_response`); fixture `tests/fixtures/contracts/errors/contact.post.validation.html` | Styled HTML page (`text/html`), heading "Message not sent" / "پیام ارسال نشد", `noindex`, back-link to `/{locale}/` | Always 422 on failure regardless of underlying reason (`200 if ok else 422`); success is 200 HTML |
| 8 | Profile translation-unavailable 404 | `GET /api/profiles/{locale}/{slug}` (slug published in another locale only) | `apps/content/profile_api.py` (`build_translation_unavailable`), `apps/content/public_api.py` | `{ "code": "TRANSLATION_UNAVAILABLE", "detail", "locale", "slug", "availableLocales" }` — uses `detail`, not `message` | 404 |
| 9 | Framework defaults outside routers | Unresolved paths; CSRF-protected Django views | No custom `handler404`/`handler403` configured in `config/` | Django default HTML 404/403 pages | 404/403 |

Codes in the stable registry (surface 1), which must never be renamed:
`AUTH_REQUIRED`, `FORBIDDEN`, `OTP_REQUIRED`, `CSRF_FAILED`, `VALIDATION`,
`NOT_FOUND`, `PRECONDITION_REQUIRED`, `STALE_REVISION`, `UNKNOWN_KEY`,
`DUPLICATE_KEY`, `DUPLICATE_ORDER`, `BAD_ENUM`, `TOO_LONG`, `BAD_TYPE`,
`INVALID_DETAIL_URL`, `BAD_WEIGHT`, `UNKNOWN_ID`, `UNKNOWN_FIELD`,
`OUT_OF_RANGE`, `UNKNOWN_LICENSE`, `IMMUTABLE_ACTIVE`, `ALREADY_ACTIVE`,
`VALIDATION_BLOCKED`, `UNKNOWN_EDGE_ENDPOINT`, `DUPLICATE_RELATED`,
`UNKNOWN_GROUP_MEMBER`, `DUPLICATE_GROUP_MEMBER`, plus `RATE_LIMITED` emitted
by the admin login flow. The legacy profile API (surface 3) emits codes that
are not in this registry (`REVISION_CONFLICT`, `INVALID_TARGET_LOCALE`,
`PROFILE_LOCALE_EXISTS`, `SLUG_CONFLICT`, `VALIDATION_ERROR`); they are
consumer-visible strings today and are not renamed by this plan either.

The error-shape fixtures above are the BACKEND-130 deliverables and are
asserted by `Back-End/tests/test_contract_fixtures.py`.

## Decision

Proposed: adopt a single normalized JSON error envelope for machine clients,
introduced only additively, and retire divergent shapes only after consumer
evidence exists. Specifically:

### Normalized envelope (target, unchanged from `ERROR-CONTRACT.md`)

```json
{
  "code": "stable_machine_code",
  "message": "Safe human-readable message",
  "field_errors": {},
  "request_id": "optional-server-generated-id"
}
```

Rules:

- `code` carries the existing stable admin codes verbatim; new codes may be
  registered, never renamed.
- `message` is the safe human-readable text (the key the admin API already
  uses today).
- `field_errors` is an object mapping a field path to a list of messages. On
  surfaces that adopt the envelope it is always present (empty object when
  there are no field errors), for deterministic client handling.
- `request_id` appears only when the server actually provides one. The
  backend has no request-id generation today; introducing one is a separate
  decision. No surface fabricates this field.
- HTTP status codes are unchanged by normalization.
- The contact HTML failure page (surface 7) stays HTML. It serves the no-JS
  progressive form path, not a machine client, and is out of scope for JSON
  normalization.

### Compatibility mapping (current shape → normalized)

| Current surface / shape | Normalized target | Mapping rules | Breaking risk |
|---|---|---|---|
| 1. Admin `AdminError` `{code, message, fields?}` | `{code, message, field_errors}` | `field_errors` carries the same dict-of-lists structure `fields` carries today. Legacy responses keep emitting `fields`; new `/api/v1/` surfaces emit `field_errors`. Code strings unchanged. | None if legacy key kept during dual-shape period; dropping `fields` requires consumer evidence (phase 3) |
| 2. Conflict extension `{code, message, currentUpdatedAt}` | `{code, message, field_errors: {}, currentUpdatedAt}` | `currentUpdatedAt` is a surface-specific extension key; it is preserved alongside the envelope, not folded into it. | Additive only |
| 3. Legacy profile API `{code, detail, **extras}` | `{code, message, field_errors, **extras}` | `detail` maps to `message`. `VALIDATION_ERROR` validation payloads map `detail` (dict/list) into `field_errors`. Codes are kept verbatim (not remapped to registry codes) — remapping would be a consumer-visible rename and is out of scope. Extras (`currentRevision`, `editorUrl`) preserved as extension keys. | Key changes (`detail`→`message`) are breaking → opt-in (phase 2) only |
| 4. Public `HttpError` `{detail}` | `{code, message}` (plus `field_errors: {}`) | Adding `code`/`message` alongside `detail` is additive; removing `detail` requires consumer evidence. Public codes do not exist today; any new public code set must be registered like the admin registry. | Additive phase 1 is safe for tolerant readers but changes accepted artifact hashes → PS-05 reopening required |
| 5. Ninja validation `{detail: [{type, loc, msg}]}` | `{code: "VALIDATION", message, field_errors}` | Framework shape stays on existing surfaces (matrix row: "treat as unknown safe failure"); normalized mapping only on adopting surfaces. `loc` path joins into `field_errors` keys; exact join rule fixed in the acceptance packet. | Framework shape removal is breaking → phase 3 with evidence |
| 6. Contact JSON `{ok: false, error}` | `{ok, error, code, message, field_errors}` during opt-in | `ok`/`error` keys preserved; `code` (new contact code set) is additive. Full-envelope-only responses require consumer evidence. Success shape `{ok: true}` untouched. | Additive safe; removal phase 3 |
| 7. Contact HTML 422 page | No change | Not a machine envelope; no-JS progressive path depends on it. | None (out of scope) |
| 8. Translation-unavailable `{code, detail, locale, slug, availableLocales}` | `{code, message, field_errors, locale, slug, availableLocales}` | `detail`→`message` on adopting surfaces. `locale`, `slug`, `availableLocales` are extension keys; the registry fallback rule ("show the distinct untranslated state", PUBLIC-ROUTE-RECONCILIATION Gap B) depends on this body, so keys may not be dropped without a registry decision. | Key rename breaking → opt-in; extension-key removal needs Gap B owner decision |
| 9. Framework HTML 404/403 | No change | Browser-facing default pages; out of JSON-envelope scope. | None (out of scope) |

No stable admin error code is renamed in any phase. Extension keys
(`currentUpdatedAt`, `currentRevision`, `editorUrl`, `locale`, `slug`,
`availableLocales`) are preserved, never silently folded into the envelope.

### Rollout plan (non-breaking, evidence-gated, no dates)

- **Phase 1 — additive fields / new `/api/v1/` surfaces only.**
  Every new public or admin surface under `/api/v1/` emits the normalized
  envelope for all error responses from its first commit. Existing endpoints
  do not change shape except by adding keys (e.g. additive `code` on contact
  JSON failures). Any addition that changes an accepted OpenAPI artifact hash
  is executed only together with artifact regeneration, the OpenAPI access
  tests, and a new PS-05 acceptance record, per
  `OPENAPI-ACCEPTANCE.md` change control.
- **Phase 2 — opt-in dual shape.**
  Existing endpoints may serve the normalized envelope when the client
  explicitly asks for it (negotiation mechanism — e.g. a request header or
  query flag — is chosen in the acceptance packet; the plan deliberately does
  not fix it here). Both shapes are served and fixture-tested during this
  period. Legacy keys (`fields`, `detail`, `ok`/`error`) are never removed
  while any phase-2 consumer remains.
- **Phase 3 — retire legacy shapes, only with consumer evidence.**
  Removing a legacy shape requires: (a) adapter/fixture evidence from
  public-site and admin-panel that no consumer reads the legacy keys,
  (b) regenerated and re-accepted OpenAPI artifacts, and (c) a separate
  accepted decision record. This ADR does not authorize removal.

### Gap D / Gap E references (candidates only — require their own acceptance)

- **Gap D** (`Back-End/docs/contracts/PUBLIC-ROUTE-RECONCILIATION.md`,
  "cross-locale availability probing outside profiles"): a per-record
  cross-locale availability field is a candidate additive field for the
  normalization program, because it could serve the registry alternate-link
  rule without list-probing. It is a data-shape decision, not an error
  decision, and is **not** accepted here; it requires its own contract
  change, artifact regeneration, and owner acceptance.
- **Gap E** ("locale parameter strictness is uneven"): normalizing list
  endpoints to a uniform 404 for non-`fa`/`en` locales is a *behavior*
  change (200-with-empty-collection → 404) and is therefore **breaking** for
  any consumer treating the empty collection as valid. It cannot ride a
  non-breaking normalization plan. It is referenced here only so the
  normalized 404 envelope (with a stable code) is the shape such a change
  would adopt if separately accepted.

## Consequences

Positive:

- One machine envelope for new surfaces, with the stable admin code registry
  untouched.
- Clients can converge on a single adapter instead of per-surface shape
  handling, per the client rules in `ERROR-COMPATIBILITY-MATRIX.md`.
- Every legacy-key removal is blocked until consumer evidence exists.

Negative / risks:

- A dual-shape period increases the surfaces tests and clients must cover.
- Additive keys on existing public endpoints reopen PS-05 (artifact hashes),
  which has coordination cost with frontend type generation.
- Extension keys and non-registry codes (surface 3) remain unnormalized for
  a long time; the plan accepts this to avoid breaking the legacy admin
  profile consumers.

### Frontend impact notes

- **public-site (Astro, static-first, no-JS readable):**
  The contact form's no-JS path must keep receiving the styled HTML page
  (surface 7); nothing in this plan touches it. A JSON adapter path, if
  adopted per the matrix, may opt in during phase 2. Profile
  unavailable/not-found rendering maps from surfaces 4 and 8; during any
  dual-shape period both mappings must work. Unknown errors continue to map
  to a safe generic state; the site must never depend on a field the server
  does not guarantee (no `request_id` assumptions).
- **admin-panel (React 19 SPA):**
  The admin client consumes surfaces 1–3. On legacy `/api/v1/admin/` routes
  it keeps reading `fields`; on new surfaces it reads `field_errors`. A
  single adapter should centralize this so the phase-3 transition is a
  one-place change. The client must not assume `request_id` and must treat
  unknown codes as a safe generic failure state per `ERROR-CONTRACT.md`.

## Verification

The plan is adopted — not merely proposed — when the following observable
evidence exists at each step:

- Phase 1: new `/api/v1/` endpoints ship golden normalized-envelope fixtures
  (error responses only) in `Back-End/tests/fixtures/contracts/errors/`,
  asserted by `tests/test_contract_fixtures.py`-style tests; additive-key
  changes on existing endpoints come with regenerated artifact hashes, the
  public/admin OpenAPI access tests passing, a review report, and a new
  acceptance record (PS-05 control).
- Phase 2: per-endpoint dual-shape tests prove both the legacy and normalized
  responses (key-superset assertions: legacy keys present, values unchanged);
  public-site and admin-panel consumer fixtures demonstrate both mappings.
- Phase 3: consumer evidence (adapter code + fixtures) from both frontend
  repositories, a separate accepted decision record, regenerated artifacts,
  and the OpenAPI access tests — before any legacy key is removed.
- Continuous: a stability test asserts the stable admin code registry strings
  appear verbatim on the wire (no renames), and the existing
  `tests/test_openapi_hash_drift.py` gate keeps uncoordinated envelope
  changes out of accepted artifacts.

Test strategy additions implied by this plan (to be written when a phase is
scheduled, not before): golden fixtures per new surface, key-superset
compatibility tests per dual-shape endpoint, opt-in negotiation tests both
ways (with and without the opt-in), registry-string stability tests, and
cross-repo consumer fixtures. No existing fixture may be edited to match a
new shape during phase 1; new fixtures are added alongside.
