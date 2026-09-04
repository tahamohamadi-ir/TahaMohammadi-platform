# OpenAPI Acceptance — scaffold foundation

Status: **accepted for frontend scaffold foundation only**.

This acceptance locks the reviewed, source-generated snapshot for type generation and API-adapter foundation work. It does not approve owner facts, promoted media, fonts, production deployment, or a future breaking API change.

## Locked evidence

| Item | Value |
|---|---|
| Backend commit | `82e3984520154b60146009ae4a0d21eb5c30373e` |
| Settings used to generate | `config.settings.development` |
| Public schema | `docs/contracts/openapi/current/public-openapi.json` — SHA-256 `0f672693de28ed33286789e5119eb3226c062693fb15168b1aba5513c257c0a5` — 40 paths — version `0.4.0` |
| Admin schema | `docs/contracts/openapi/current/admin-openapi.json` — SHA-256 `1328f8244c5541f225648082891a0a1244961c0dead6692488992ac8c7606f09` — 47 paths — version `0.1.0` |
| Endpoint inventory | `docs/contracts/openapi/current/endpoint-inventory.md` — SHA-256 `618ab18826875a5f27357ab87a3917082291d2e8610959b18aa2f936a7f3aa96` — 103 operations |
| Access evidence | `tests/test_public_openapi.py` and `tests/test_admin_openapi.py`: 9 passing checks for anonymous public and verified staff-plus-OTP admin access |

## Binding client scope

- Public client base remains `/api/`; it must use the canonical endpoint families in `API-CONTRACT.md`.
- Admin client base remains `/api/v1/admin/`; admin docs/schema remain staff-plus-OTP protected.
- About fetches only `/api/profiles/{locale}/about` and renders an unavailable state when no published record exists.
- Locale-sensitive site text never comes from unlocalized `/api/site`.
- Search remains local-index only; Rebuild/Health is excluded from admin v1.

## Change control

Any schema or backend-source change that changes one of these hashes immediately reopens PS-05. Regenerate the snapshots, run the public/admin OpenAPI access tests, update the review report, and create a new acceptance record before regenerated client types are adopted.

## Addendum 2026-09-02 — admin API additions (G-E, G-G) and ADR-0006 phase 1 envelope

Status: **accepted addendum** (owner decisions G-E and G-G recorded in `Docs/10-tracking/DECISION-LOG.md`, 2026-09-02). This addendum re-locks the regenerated artifacts after two additive admin API changes and the ADR-0006 phase-1 error-envelope step. Public schema content is unchanged (same hash); only the admin schema and the endpoint inventory moved.

### Owner decisions implemented

- **G-E — media deletion.** `DELETE /api/v1/admin/media/{media_id}` added with a usage guard (gap documented in `Back-End/docs/contracts/ADMIN-ROUTE-RECONCILIATION.md`).
- **G-G — profile sibling-locale creation.** The legacy `POST /api/admin/profiles/{locale}/{slug}/siblings/{target_locale}` behavior (`apps/content/admin_api.py:admin_profile_create_sibling`) is migrated onto the accepted admin API as `POST /api/v1/admin/content/profile/{id}/sibling-locale`. The legacy route stays in place untouched; its deprecation remains a BACKEND-151 decision.

### New paths (admin schema)

| Operation | Guards | Response codes |
|---|---|---|
| `DELETE /api/v1/admin/media/{media_id}` | staff session + verified OTP (`401 AUTH_REQUIRED`, `403 FORBIDDEN`, `403 OTP_REQUIRED`), same-origin CSRF (`403 CSRF_FAILED`) | `200 {ok, id}`; `404 NOT_FOUND`; `409 MEDIA_IN_USE` (body extension key `usageCount`) when the row is referenced by any `MEDIA_REFERENCE_FIELDS` FK or composition-block JSON setting; deletion removes the DB row and the stored file and writes an audit row (`action="media.delete"`, `model_name="media"`) |
| `POST /api/v1/admin/content/profile/{id}/sibling-locale` | staff session + verified OTP, CSRF | `201 {editorUrl, profile}` (legacy projection: empty draft inheriting the source's slug, `translation_key`, and `updated_at`, `status=draft`); `404 NOT_FOUND` (unknown profile); `400 VALIDATION` (invalid target locale / same-locale target); `409 DUPLICATE` (sibling already exists for the translation family / slug conflict in the target locale); audit row `action="admin.profile.sibling_created"` (same action string as the legacy route) |

Stable-code registry: no existing code was renamed. `MEDIA_IN_USE` was **added** to the declare-once registry in `Back-End/apps/api/admin_common.py`. The legacy local codes (`INVALID_TARGET_LOCALE`, `PROFILE_LOCALE_EXISTS`, `SLUG_CONFLICT`) are **not** emitted on the new `/api/v1/` surface; the registry codes above replace them there. Deviation note: the legacy 409 `PROFILE_LOCALE_EXISTS` response carried an `editorUrl` extension key; the new-surface 409 uses the normalized envelope (`code`, `message`, `field_errors`) without `editorUrl`, because the AdminError handler does not carry surface extras and no consumer exists for the new endpoint yet. Success responses keep `editorUrl` exactly as the legacy route returned it.

### Regenerated artifacts (SHA-256)

Hashes are computed over CRLF-encoded bytes (same rule as the original acceptance; see `OPENAPI-ARTIFACT-CONTRACT.md` for the LF/CRLF provenance note). `scripts/verify_openapi_export.py` exits 0 with 3/3 MATCH against these values.

| Artifact | Old → New SHA-256 (CRLF) | Count |
|---|---|---|
| `public-openapi.json` | `0f672693de28ed33286789e5119eb3226c062693fb15168b1aba5513c257c0a5` (unchanged) | 40 paths, version `0.4.0` |
| `admin-openapi.json` | `1328f8244c5541f225648082891a0a1244961c0dead6692488992ac8c7606f09` → `60e5aba0e19426ced2b0386aad23cef388f5909c22294fd5799aea533cf13bfc` | 47 → 48 paths, version `0.1.0` |
| `endpoint-inventory.md` | `618ab18826875a5f27357ab87a3917082291d2e8610959b18aa2f936a7f3aa96` → `df2d1921d7fda90169dd5e1926a94c5d3e229be245ed6cac3a3abdb19fb70605` | 103 → 105 operations |

`PROVENANCE.json` records `scaffold-accepted`, source commit `edecc10188c207df88a3c7bceaf31dcd6fcfc5ec`, settings `config.settings.development`, generated 2026-09-02. `Back-End/tests/test_openapi_hash_drift.py` (which pins the accepted hashes) was updated to the new values.

### Access-test evidence

New tests (all written failing first, then passing):

- `tests/test_admin_media_api.py`: `test_delete_media_requires_auth`, `test_delete_media_requires_otp`, `test_delete_media_requires_csrf`, `test_delete_media_404`, `test_delete_media_in_use_409`, `test_delete_media_success_removes_row_file_and_audits`.
- `tests/test_admin_content_api.py`: `test_sibling_locale_requires_auth`, `test_sibling_locale_requires_otp`, `test_sibling_locale_requires_csrf`, `test_sibling_locale_unknown_profile_404`, `test_sibling_locale_invalid_target_locale_400`, `test_sibling_locale_same_locale_400`, `test_sibling_locale_creates_draft_sibling_201`, `test_sibling_locale_existing_sibling_409`, `test_sibling_locale_slug_conflict_409`.
- `tests/test_admin_api_auth.py` (ADR-0006 phase 1): `test_admin_error_envelope_includes_empty_field_errors`, `test_admin_error_envelope_keeps_fields_dual_key`.
- Pre-existing gate evidence still passing: `tests/test_public_openapi.py` + `tests/test_admin_openapi.py` (anonymous public / verified staff+OTP admin access) and `tests/test_openapi_hash_drift.py`.

### ADR-0006 phase-1 note (`field_errors` on AdminError responses)

Per ADR-0006 phase 1 (additive-key changes on existing endpoints), `_api_error_handler` in `apps/api/admin_common.py` now emits `field_errors` (always present; `{}` when empty; same dict-of-lists structure as `fields`) on every `AdminError` response, while `fields` continues to be emitted exactly as before (dual-key safety, ADR mapping row 1). The 409 `CONFLICT` conflict-extension handlers (`apps/api/admin_media.py`, `apps/api/admin_content.py`) also gained additive `field_errors: {}` (mapping row 2), and the new 409 `MEDIA_IN_USE` response includes it. No `request_id` is emitted or fabricated. Error responses are not documented in `admin-openapi.json` (no documented error schemas existed), so this step alone would not have changed artifact hashes; the hash movement in this addendum comes from the two new operations. No existing error fixture was edited.

### Compatibility / frontend impact / migration notes

- **Compatibility:** additive only. Existing admin operations keep their shapes, status codes, and stable codes verbatim; the success/error keys listed above are new or legacy-preserving. `DELETE` on `/api/v1/admin/media/{media_id}` and the new sibling-locale POST do not collide with existing routes.
- **admin-panel (ADMIN repo):** the media delete UX (workflow-map row 3) is now implementable against `DELETE /api/v1/admin/media/{id}` — the client must render the `409 MEDIA_IN_USE` + `usageCount` state and pass the CSRF header. The profile translation flow may target the new sibling-locale endpoint; `editorUrl` on 409 is not available there (see deviation note). New-surface error handling should read `field_errors` per ADR-0006.
- **public-site (PUBLIC repo):** no impact; the public schema and `/api/` surface are untouched (hash unchanged).
- **Migration notes:** no schema/data migration. The legacy sibling route remains functional until BACKEND-151 retires it; both surfaces write the same `admin.profile.sibling_created` audit action during the dual-surface period. Media deletion is permanent (row + stored file); the `usageCount` guard is the only protection — clients must confirm before calling.

## Addendum 2026-09-04 - owner approval queue surface and publication gate (BACKEND-210)

Status: **accepted addendum** (owner decisions recorded 2026-09-04 in the admin-panel workspace conversation: approval queue served from backend data - not a bundled static JSON - and the publication gate enforced on the server). This addendum re-locks the regenerated artifacts after one additive admin read endpoint, one additive response field pair, and one new stable error code on an existing operation. Public schema content is unchanged (same hash).

### Changes implemented

- **GET /api/v1/admin/approval-queue** (new path, admin read surface). Serves the owner approval queue from ContentSeedRecord rows imported by BACKEND-070 (per-content_id seed provenance: pproval_state, publication_state, isibility, derived isPublicationAllowed). Query state in {all, approved, not-approved}, default 
ot-approved; response {items, counts:{total, approved, notApproved}} where counts always cover every seed record. Guards: staff session + verified OTP. Read-only by design - approving is an owner decision, not a staff toggle.
- **Publication gate (ADMIN-280 / BACKEND-210).** POST /api/v1/admin/content/{entity}/{id}/transition with 	o=published now returns 409 APPROVAL_REQUIRED when a linked ContentSeedRecord exists and its three-part is_publication_allowed triple is not satisfied. Rows without seed provenance (admin-created content) publish without the gate: they are owner-authored through this admin. The same gate is enforced inside publish_scheduled_content (blocked rows are reported and skipped with a nonzero exit) so the scheduler cannot bypass it.
- **pprovalState projection (additive).** ContentListItemOut and ContentDetailOut gained pprovalState: string | null - the linked seed record's pproval_state, or 
ull for admin-created rows. List lookups are batched (one query per list page).

Stable-code registry: APPROVAL_REQUIRED **added** to the declare-once registry usage on the transition operation. No existing code renamed.

### Regenerated artifacts (SHA-256, CRLF rule)

| Artifact | Old -> New SHA-256 (CRLF) | Count |
|---|---|---|
| public-openapi.json |  f672693de28ed33286789e5119eb3226c062693fb15168b1aba5513c257c0a5 (unchanged) | 40 paths, version  .4.0 |
| dmin-openapi.json | 60e5aba0e19426ced2b0386aad23cef388f5909c22294fd5799aea533cf13bfc -> 5856a37dbefbae60ea5e27ed48a1a2ab37767c9352800fe389371ab94a94b49a | 48 -> 49 paths, version  .1.0 |
| endpoint-inventory.md | df2d1921d7fda90169dd5e1926a94c5d3e229be245ed6cac3a3abdb19fb70605 -> 452de5ab13f5e0b9ea57bf22cd7687ef04cadad96edb0fd2057918f7d8ffd7ef | 105 -> 106 operations |

PROVENANCE.json records scaffold-accepted, settings config.settings.development, generated 2026-09-04. Back-End/tests/test_openapi_hash_drift.py was updated to the new values.

### Tests (written failing first, then passing)

- 	ests/test_admin_approvals.py: 	est_approval_queue_requires_admin_otp, 	est_approval_queue_counts_and_default_filter, 	est_publish_blocked_without_owner_approval, 	est_publish_allowed_once_owner_triple_cleared, 	est_publish_allowed_without_seed_provenance, 	est_approval_state_exposed_in_list_and_detail, 	est_scheduled_publish_command_honors_gate.
- Pre-existing gate evidence still passing: 	ests/test_admin_content_api.py, 	ests/test_admin_content_write.py, 	ests/test_admin_revisions_schedule.py, 	ests/test_admin_bulk_archive.py, 	ests/test_admin_openapi.py, 	ests/test_openapi_hash_drift.py.

### Compatibility / frontend impact

- **Compatibility:** additive only; existing operations keep shapes and codes. The transition 	o=published on seed-linked rows changes behavior exactly as decided (was: always allowed).
- **admin-panel:** regenerates src/generated/admin-api.ts; the editor renders pprovalState, disables publish while it is not pproved, and maps APPROVAL_REQUIRED to the conflict kind; a new Approval queue page consumes the read endpoint.
- **public-site:** no impact (public schema unchanged).

## Addendum 2026-09-04b - seed policy projection (BACKEND-211 / ADMIN-281)

Status: **accepted addendum** (owner decision recorded 2026-09-04: the seed policy is persisted server-side and surfaced to the admin, not bundled statically). One additive response field on GET /api/v1/admin/site; no new path. Public schema unchanged (same hash).

### Changes implemented

- SiteSettings.seed_policy JSONField added (migration siteconfig.0004), written only by pply_seed_settings during the seed import; the admin PUT schema does not include it (verified by test).
- SiteSettingsOut gained seedPolicy: object | null - the raw supplement/seed-settings.json payload, so the site settings admin can label seed-managed surfaces (phone, city/country, CV/resume slots) instead of guessing.

### Regenerated artifacts (SHA-256, CRLF rule)

| Artifact | Old -> New SHA-256 (CRLF) | Count |
|---|---|---|
| public-openapi.json |  f672693de28ed33286789e5119eb3226c062693fb15168b1aba5513c257c0a5 (unchanged) | 40 paths |
| dmin-openapi.json | 5856a37dbefbae60ea5e27ed48a1a2ab37767c9352800fe389371ab94a94b49a -> 38ff4d81d454287bd0e6c437ad84bfada41255e8fa6acc13704144223014fd7a | 49 paths (unchanged count), version  .1.0 |
| endpoint-inventory.md | 452de5ab13f5e0b9ea57bf22cd7687ef04cadad96edb0fd2057918f7d8ffd7ef (unchanged) | 106 operations |

### Tests (written failing first, then passing)

- 	ests/test_admin_seed_policy.py: 	est_apply_seed_settings_persists_policy, 	est_missing_policy_file_leaves_seed_policy_empty, 	est_admin_site_response_carries_seed_policy, 	est_seed_policy_is_not_writable_via_update.
- 	ests/test_openapi_hash_drift.py re-pinned to the new admin hash.
