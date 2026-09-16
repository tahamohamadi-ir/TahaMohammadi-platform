# Knowledge Atlas v1 Plan B: Admin Authoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the entire Atlas authorable, validatable, previewable and publishable from the admin panel — no code edits, no manual database writes — by adding `/api/v1/admin/atlas/*` to the existing admin API and the corresponding screens to the React admin SPA.

**Architecture:** A new `atlas_router` on the existing `admin_api` (same-origin session + CSRF + TOTP, shared `If-Match` gate, shared audit) exposes versions, nodes, relations, groups, taxonomy, layout, validation, publish and preview-mint operations. The admin SPA gains one API client module, one navigation entry, four pages (Versions, Editor, Taxonomy, Preview) and a deterministic 2D authoring graph that reads the stored layout coordinates — the same coordinates the public 3D Atlas consumes.

**Tech Stack:** Django 5.2 + django-ninja admin API (existing `AdminError` envelope, `_require_if_match`, `AuditLog`), pytest; React 19 + TypeScript + react-router-dom 7 + @tanstack/react-query 5 + Vite 7, vitest 4 + @testing-library/react (jsdom), Playwright.

**Spec:** Docs/05-delivery/knowledge-atlas/KNOWLEDGE-ATLAS-V1-DESIGN-SPEC.md

**Depends on:** Plan A (models, services, validation, payload contract). Plan B consumes those interfaces and MUST NOT re-implement any of them.

## Global Constraints

- **Admin is the source of Atlas authoring truth** (spec §9). Every production-authorable semantic — versions, nodes, relations, groups, taxonomy, translations, pins — has an admin path; nothing requires a shell.
- **Never mutate an active version.** Editing an active version is refused with `409 IMMUTABLE_ACTIVE`. Precondition semantics follow the existing graph admin API exactly (`428 PRECONDITION_REQUIRED`, `409 STALE_REVISION`, `409 VALIDATION_BLOCKED`, `409 ALREADY_ACTIVE`).
- **Options are data, never hard-coded lists.** Node types, relation types and their rules come from the API; the SPA contains no enumerated type or relation key.
- **No drag-to-connect in v1** (spec §25). Node drag writes pins only and never touches semantics.
- **The 3D preview is read-only** and is never the editing surface (spec §9.5).
- **Accessibility is part of done:** every authoring action reachable by keyboard alone, focus visible, ≥ 44 px targets, no canvas-only workflow (spec §18, card task 19).
- **No deployment steps in this plan.** Staging/production rollout belongs to Plan D.
- **Existing SPA conventions are binding:** pages in `src/pages/*.tsx` with co-located `*.test.tsx`, API clients in `src/lib/api/*.ts` with co-located tests, error normalisation through `src/lib/api/errors.ts`, `adminJson` from `src/lib/api/auth.ts`, route registration in `src/app/router.tsx` + `src/components/Nav.tsx`, e2e specs in `tests/e2e/*.e2e.ts`.

**Commands (Windows/MSYS, from the repository root):**

```bash
# Backend
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/test_admin_atlas_api.py -q
./.venv/Scripts/python.exe -m ruff check .

# Admin SPA
cd /d/Project/tahamohammadi-platform/Front-End/admin-panel
npm test -- src/lib/api/atlas.test.ts
npm run lint && npm run format:check && npm run build
npx playwright test tests/e2e/atlas-authoring.e2e.ts
```

## File Map

**Created — backend**

| Path | Responsibility |
|---|---|
| `Back-End/apps/atlas/api_admin.py` | `atlas_router` with every admin operation; no business rules (delegates to `services`, `validation`, `layout`, `projection`) |
| `Back-End/apps/atlas/admin_preview.py` | Staff preview token minting for a draft version (`kind="atlas-version"`) reusing `apps.content.preview_token` |
| `Back-End/tests/test_admin_atlas_api.py` | Endpoint behaviour, guards, precondition matrix, audit |
| `Back-End/tests/test_admin_atlas_preview.py` | Preview minting, TTL, staff-only, draft payload isolation |

**Created — admin SPA**

| Path | Responsibility |
|---|---|
| `src/lib/api/atlas.ts` (+ `atlas.test.ts`) | Typed client for every admin Atlas operation; generated types only |
| `src/pages/AtlasVersionsPage.tsx` (+ test) | Version list, create, clone, status, open editor |
| `src/pages/AtlasEditorPage.tsx` (+ test) | The editor shell: graph, node form, relation form, relation table, validation panel, publish |
| `src/pages/AtlasTaxonomyPage.tsx` (+ test) | Node types and relation types incl. localized copy and rules |
| `src/pages/AtlasPreviewPage.tsx` (+ test) | EN/FA switch and the read-only 3D final preview |
| `src/components/atlas/AuthoringGraph.tsx` (+ test) | Deterministic 2D authoring graph (stored coordinates, selection, highlight, pin drag) |
| `src/components/atlas/NodeForm.tsx` (+ test) | Node authoring form incl. overrides, mobile role, groups, pin |
| `src/components/atlas/RelationForm.tsx` (+ test) | Structured relation form |
| `src/components/atlas/RelationTable.tsx` (+ test) | Filterable relation table with edit/delete/inspect |
| `src/components/atlas/ValidationPanel.tsx` (+ test) | Blockers, warnings, source locations, actionable messages |
| `src/components/atlas/issue-labels.ts` (+ test) | Stable issue code/token → human label map (the only place UI copy for issues lives) |
| `tests/e2e/atlas-authoring.e2e.ts` | End-to-end authoring journey against the dev stack |

**Modified**

| Path | Change |
|---|---|
| `Back-End/apps/api/admin_api.py` | `admin_api.add_router("/atlas", atlas_router)` |
| `Back-End/docs/contracts/openapi/current/{admin-openapi.json,PROVENANCE.json,ACCEPTANCE.json,endpoint-inventory.md}` | Regenerated admin snapshot + re-pin (Task 11) |
| `Back-End/tests/test_admin_openapi.py`, `tests/test_admin_permission_matrix.py`, `tests/test_admin_openapi.py` fixtures | New routes registered in the permission/openapi assertions |
| `Front-End/admin-panel/src/app/router.tsx`, `src/components/Nav.tsx` | Atlas routes + navigation entry |
| `Front-End/admin-panel/src/generated/{admin-api.ts,openapi-hash.json}`, `src/lib/api/product-contract.test.ts` | Regenerated types + accepted-hash re-pin (Task 11) |

**Cross-plan interfaces**

| Interface | Direction | Note |
|---|---|---|
| `admin_api.add_router("/atlas", …)` | produces | Registered alongside `"/graph"`; single registration line |
| `services.{clone_version, activate_version, recompute_layout}`, `validation.validate_version`, `projection.build_locale_projection` | consumes | Plan A; never duplicated here |
| Atlas preview render mode in the public site (`?preview=<token>` on `/…/atlas/`) | **consumed, declared dependency** | Owned by Plan C (task C8). Until it lands, the preview page frames the public Atlas route and labels the shown projection `Active`; the admin-side preview screen ships independently. |
| `issue-labels.ts` code map | produces | Consumed by the editor's validation panel; codes come from Plan A's `ATLAS_ISSUE_CODES` |

---

### Task 1: Admin router skeleton, guards and precondition helper

**Files:**
- Create: `Back-End/apps/atlas/api_admin.py`
- Modify: `Back-End/apps/api/admin_api.py`
- Test: `Back-End/tests/test_admin_atlas_api.py`

**Interfaces:**
- Produces: `atlas_router = Router()`; `_require_current_revision(request, version)` (428/409 via `_require_if_match`); `_require_draft(version)` → `409 IMMUTABLE_ACTIVE`; every mutation writes `AuditLog(action="atlas.<verb>")` with `_client_ip(request)`
- Consumes: `apps.api.admin_common.{AdminError, _check_csrf, _client_ip, _require_admin_otp, _require_staff_session, _require_if_match}`, `PRECONDITION_REQUIRED`, `STALE_REVISION`, `IMMUTABLE_ACTIVE`

- [ ] **Step 1: Write the failing tests**

```python
def test_atlas_routes_require_staff_session(anonymous_client):
    assert anonymous_client.get("/api/v1/admin/atlas/versions").status_code in (401, 403)


def test_atlas_routes_require_otp(staff_client_without_otp):
    response = staff_client_without_otp.get("/api/v1/admin/atlas/versions")
    assert response.status_code == 403
    assert response.json()["code"] == "OTP_REQUIRED"


def test_mutations_require_csrf_and_if_match(admin_client, draft_version):
    assert admin_client.post(f"/api/v1/admin/atlas/versions/{draft_version.pk}/layout", {}).status_code == 403
    response = admin_client.post(f"/api/v1/admin/atlas/versions/{draft_version.pk}/layout", {},
                                HTTP_X_CSRFTOKEN=admin_client.csrf, content_type="application/json")
    assert response.status_code == 428
    assert response.json()["code"] == "PRECONDITION_REQUIRED"


def test_editing_an_active_version_is_refused(admin_client, active_version):
    response = admin_client.patch(
        f"/api/v1/admin/atlas/versions/{active_version.pk}/nodes/{active_version.first_key}",
        {"importance": 90},
        HTTP_X_CSRFTOKEN=admin_client.csrf,
        HTTP_IF_MATCH=version_revision(active_version),
        content_type="application/json",
    )
    assert response.status_code == 409
    assert response.json()["code"] == "IMMUTABLE_ACTIVE"


def test_mutations_are_audited(admin_client, draft_version):
    _patch_node(admin_client, draft_version, {"importance": 70})
    assert AuditLog.objects.filter(action="atlas.node.update").exists()
```

- [ ] **Step 2: Run — expect FAIL** (`404`: the router is not registered).
- [ ] **Step 3: Implement** the router module with the shared guards, then register it:

```python
# apps/atlas/api_admin.py
atlas_router = Router()


def _require_current_revision(request, version: AtlasVersion) -> None:
    _require_if_match(
        request,
        current=version.updated_at,
        missing_message="An If-Match revision is required. GET the Atlas version first.",
        stale_message="The Atlas version was modified by someone else.",
    )


def _require_draft(version: AtlasVersion) -> None:
    if version.status != "draft":
        raise AdminError(409, IMMUTABLE_ACTIVE, "An active Atlas version cannot be edited. Clone it first.")


def _audit(request, action: str, *, model_name: str, object_id: int, detail: str = "") -> None:
    AuditLog.objects.create(action=action, model_name=model_name, object_id=object_id,
                            ip=_client_ip(request), detail=detail)


@atlas_router.get("/versions", response=list[AtlasVersionRowOut])
def list_versions(request):
    _require_admin_otp(request)
    ...
```
```python
# apps/api/admin_api.py
from apps.atlas.api_admin import atlas_router
...
admin_api.add_router("/atlas", atlas_router)
```
- [ ] **Step 4: Migrate the permission matrix** — add the Atlas routes to `tests/test_admin_permission_matrix.py`'s expectations (they are staff+OTP like `/graph`).
- [ ] **Step 5: Run — expect `5 passed`** plus the permission matrix green:

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/test_admin_atlas_api.py tests/test_admin_permission_matrix.py -q
```
- [ ] **Step 6: Commit**

```bash
git add -- apps/atlas/api_admin.py apps/api/admin_api.py tests/test_admin_atlas_api.py tests/test_admin_permission_matrix.py
git commit -m "feat(atlas): add guarded admin router skeleton"
```

---

### Task 2: Version endpoints

**Files:**
- Modify: `Back-End/apps/atlas/api_admin.py`
- Test: `Back-End/tests/test_admin_atlas_api.py` (extend)

**Interfaces:**
- Produces: `GET /versions` → `[{id, label, status, nodeCount, relationCount, publishedAt, updatedAt}]`; `POST /versions {label}` → 201 draft; `GET /versions/{id}` → detail incl. `revision`; `POST /versions/{id}/clone {label}` → 201 new draft; `POST /versions/{id}/archive`

- [ ] **Step 1: Write the failing tests** — create returns `status="draft"` with a `revision`; clone returns a distinct id and identical node/relation keys; archiving a draft is `409`; listing shows counts that match the ORM.
- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** by delegating to `services.clone_version` and serialising through one `_serialize_version_row` helper (mirroring `admin_graph._serialize_version_row`).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add admin version endpoints"`

---

### Task 3: Node endpoints

**Files:**
- Modify: `Back-End/apps/atlas/api_admin.py`
- Test: `Back-End/tests/test_admin_atlas_api.py` (extend)

**Interfaces:**
- Produces: `GET|POST /versions/{id}/nodes`, `GET|PATCH|DELETE /versions/{id}/nodes/{key}` with body fields `{nodeTypeKey, canonicalSource, canonicalTranslationKey, importance, visible, mobileOverview, groupKeys[], pin:{x,y,z}|null, overrides:{en:{label,summary,accessibleLabel,aliases},fa:{…}}}`
- Produces: `GET /canonical-candidates?source=method&q=…` → `[{translationKey, title, localeStatus:{en:bool, fa:bool}, publishable:{en:bool, fa:bool}}]` so the picker can never invent a record

- [ ] **Step 1: Write the failing tests**

```python
def test_create_node_validates_the_canonical_pair(admin_client, draft_version, method_pair):
    response = _create_node(admin_client, draft_version, {
        "nodeTypeKey": "method", "canonicalSource": "method",
        "canonicalTranslationKey": str(method_pair.translation_key), "importance": 45,
    })
    assert response.status_code == 201
    assert response.json()["publicKey"].startswith("method-")
    assert response.json()["localeStatus"] == {"en": True, "fa": True}


def test_create_node_rejects_an_unpublishable_canonical_record(admin_client, draft_version, draft_only_method):
    response = _create_node(admin_client, draft_version, {
        "nodeTypeKey": "method", "canonicalSource": "method",
        "canonicalTranslationKey": str(draft_only_method.translation_key),
    })
    assert response.status_code == 400
    assert response.json()["fields"]["canonicalTranslationKey"]


def test_pin_requires_both_coordinates(admin_client, draft_version, node_key):
    response = _patch_node(admin_client, draft_version, node_key, {"pin": {"x": 4.0}})
    assert response.status_code == 400
    assert "pin" in response.json()["fields"]


def test_node_public_key_is_never_editable(admin_client, draft_version, node_key):
    response = _patch_node(admin_client, draft_version, node_key, {"publicKey": "attacker-chosen"})
    assert response.status_code == 400


def test_canonical_candidates_are_publish_gated(admin_client, draft_only_method):
    rows = admin_client.get("/api/v1/admin/atlas/canonical-candidates?source=method").json()
    assert all(row["publishable"]["en"] or row["publishable"]["fa"] for row in rows)
    assert str(draft_only_method.translation_key) not in {row["translationKey"] for row in rows if row["publishable"]["en"]}
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** with a `NodeWriteIn` schema, `_require_draft`, `full_clean()` before save (so model `clean()` rules surface as `400 VALIDATION` with `fields`), overrides written through `AtlasNodeTranslation` upserts, group membership replaced transactionally, and the picker endpoint reading the allow-list from `canonical.CANONICAL_SOURCES`.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add admin node endpoints with canonical picker"`

---

### Task 4: Relation, group and taxonomy endpoints

**Files:**
- Modify: `Back-End/apps/atlas/api_admin.py`
- Test: `Back-End/tests/test_admin_atlas_api.py` (extend)

**Interfaces:**
- Produces: `GET|POST /versions/{id}/relations`, `PATCH|DELETE /versions/{id}/relations/{key}` (`key` = the composed public key); `GET|POST /versions/{id}/groups`, `PATCH|DELETE /versions/{id}/groups/{key}`, `PUT /versions/{id}/groups/{key}/members {nodeKeys[]}`; `GET|POST /node-types`, `PATCH|DELETE /node-types/{key}`, and the same for `/relation-types`

- [ ] **Step 1: Write the failing tests**

```python
def test_relation_create_enforces_allowed_pairs(admin_client, draft_version, node_keys):
    response = _create_relation(admin_client, draft_version, {
        "sourceKey": node_keys["publication"], "relationTypeKey": "uses", "targetKey": node_keys["method"],
    })
    assert response.status_code == 409
    assert response.json()["issues"][0]["code"] == "RELATION_TYPE_NOT_ALLOWED"


def test_relation_key_is_the_composed_public_key(admin_client, draft_version, node_keys):
    created = _create_relation(admin_client, draft_version, {
        "sourceKey": node_keys["project"], "relationTypeKey": "uses", "targetKey": node_keys["method"],
    }).json()
    assert created["key"] == f"{node_keys['project']}~uses~{node_keys['method']}"


def test_directed_override_is_refused_when_the_type_forbids_it(admin_client, draft_version, node_keys):
    response = _create_relation(admin_client, draft_version, {
        "sourceKey": node_keys["project"], "relationTypeKey": "uses", "targetKey": node_keys["method"],
        "directed": False,
    })
    assert response.status_code == 400
    assert response.json()["fields"]["directed"]


def test_deleting_an_in_use_node_type_is_blocked(admin_client, draft_version):
    response = admin_client.delete("/api/v1/admin/atlas/node-types/project",
                                   HTTP_X_CSRFTOKEN=admin_client.csrf)
    assert response.status_code == 409
    assert response.json()["code"] == "TAXONOMY_IN_USE"


def test_inactive_taxonomy_cannot_be_referenced(admin_client, draft_version, node_keys):
    _patch_node_type(admin_client, "method", {"active": False})
    response = _create_relation(admin_client, draft_version, {
        "sourceKey": node_keys["project"], "relationTypeKey": "uses", "targetKey": node_keys["method"],
    })
    assert response.status_code == 400
    assert response.json()["fields"]["targetKey"]
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement**, mapping `ProtectedError`/in-use checks to `409 TAXONOMY_IN_USE` (add that code to `admin_common`'s stable code list next to `IMMUTABLE_ACTIVE`), and returning `409 VALIDATION_BLOCKED` with the Plan A issue array when a write would leave the graph invalid.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add admin relation, group and taxonomy endpoints"`

---

### Task 5: Layout, bulk graph, validation and publish endpoints

**Files:**
- Modify: `Back-End/apps/atlas/api_admin.py`
- Test: `Back-End/tests/test_admin_atlas_api.py` (extend)

**Interfaces:**
- Produces: `POST /versions/{id}/layout` → `{layoutRevision, coordinates:{key:[x,y,z]}}`; `PUT /versions/{id}/graph` (transactional bulk replace of nodes+relations+groups, `If-Match`, `400 {issues}`); `GET /versions/{id}/validate` → `{blocking:[Issue], warnings:[Issue]}`; `POST /versions/{id}/activate` → `{id, status:"active", publishedAt, enqueuedPublicationJob}`; `GET /versions/{id}/status` → post-publish status (active/archived, job id)

- [ ] **Step 1: Write the failing tests**

```python
def test_layout_endpoint_is_deterministic_and_revisioned(admin_client, draft_version):
    first = _post(admin_client, draft_version, "layout", {}).json()
    second = _post(admin_client, draft_version, "layout", {}).json()
    assert first["coordinates"] == second["coordinates"]
    assert second["layoutRevision"] == first["layoutRevision"] + 1


def test_bulk_graph_put_is_transactional(admin_client, draft_version):
    body = _graph_body(draft_version, break_one_relation=True)   # dangling target
    response = _put_graph(admin_client, draft_version, body)
    assert response.status_code == 400
    assert response.json()["issues"][0]["code"] == "DANGLING_RELATION_ENDPOINT"
    assert draft_version.nodes.count() == _initial_node_count(draft_version)   # nothing written


def test_activate_requires_a_clean_report_and_enqueues_a_job(admin_client, draft_version):
    blocked = _post(admin_client, draft_version, "activate", {})
    assert blocked.status_code == 409 and blocked.json()["code"] == "VALIDATION_BLOCKED"

    _fix_projection(admin_client, draft_version)
    activated = _post(admin_client, draft_version, "activate", {})
    assert activated.status_code == 200
    assert activated.json()["status"] == "active"
    assert activated.json()["enqueuedPublicationJob"] is not None


def test_activate_on_an_active_version_is_already_active(admin_client, active_version):
    response = _post(admin_client, active_version, "activate", {})
    assert response.status_code == 409 and response.json()["code"] == "ALREADY_ACTIVE"
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** by delegating: `recompute_layout`, the bulk replace inside `transaction.atomic` (delete-then-create only for the rows the body owns, preserving ids where the public key matches), `validate_version(...).to_dict()`, `activate_version(...)` + `enqueue_publication_job(affected_paths=["/en/atlas/", "/fa/atlas/", "/en/about/", "/fa/about/"])` from `apps.rebuild.services`, and mapping `ValidationFailed`→`409 VALIDATION_BLOCKED`, `AlreadyActive`→`409 ALREADY_ACTIVE`, `PreconditionFailed`→`409 STALE_REVISION`.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add layout, bulk graph, validate and publish endpoints"`

---

### Task 6: Preview minting for a draft version

**Files:**
- Create: `Back-End/apps/atlas/admin_preview.py`
- Modify: `Back-End/apps/atlas/api_admin.py`
- Test: `Back-End/tests/test_admin_atlas_preview.py`

**Interfaces:**
- Produces: `POST /versions/{id}/preview-link {locale}` → `{url, expiresAt}` where `url = f"{PUBLIC_SITE_BASE}/%s/atlas/?preview={token}"`; token minted with `apps.content.preview_token.build_preview_token("atlas-version", version_id, ttl_seconds=…)`; staff-only, noindex, never a public URL
- Consumes (does **not** implement): `GET /api/atlas/preview/{token}` — the token-gated draft projection endpoint is **Plan A task 15**'s public surface. This task only mints the staff token that endpoint validates, so Plans B and C stay independent of each other.

- [ ] **Step 1: Write the failing tests**

```python
def test_preview_link_is_staff_only_and_short_lived(admin_client, draft_version):
    response = _post(admin_client, draft_version, "preview-link", {"locale": "fa"})
    assert response.status_code == 200
    url = response.json()["url"]
    assert "/fa/atlas/?preview=" in url
    payload = parse_preview_token(url.split("preview=")[1])
    assert payload.kind == "atlas-version" and payload.pk == draft_version.pk
    assert 0 < payload.exp - int(time.time()) <= 900


def test_preview_link_is_refused_for_an_active_version(admin_client, active_version):
    response = _post(admin_client, active_version, "preview-link", {"locale": "en"})
    assert response.status_code == 409
    assert response.json()["code"] == "IMMUTABLE_ACTIVE"


def test_preview_link_targets_the_locale_asked_for(admin_client, draft_version):
    for locale, expected in (("en", "/en/atlas/?preview="), ("fa", "/fa/atlas/?preview=")):
        response = _post(admin_client, draft_version, "preview-link", {"locale": locale})
        assert expected in response.json()["url"]
```

Endpoint-side cases (tampered tokens, expiry, foreign `kind`, draft invisibility on the public route) belong to **Plan A task 15** and are deliberately not duplicated here.

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** `admin_preview.py` — token minting only, plus the `POST /versions/{id}/preview-link` route on `atlas_router` (staff + OTP + CSRF, `_require_draft`). It does not register anything on the public API.
- [ ] **Step 4: Run — expect `3 passed`.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add staff preview minting for draft versions"`

---

### Task 7: Admin OpenAPI export, re-pin and admin type regeneration

**Files:**
- Modify: `Back-End/docs/contracts/openapi/current/{admin-openapi.json,PROVENANCE.json,ACCEPTANCE.json,endpoint-inventory.md}`, `Front-End/admin-panel/src/generated/{admin-api.ts,openapi-hash.json}`
- Test: `Back-End/tests/test_admin_openapi.py` (route inventory assertions), `src/lib/api/product-contract.test.ts`

**Interfaces:**
- Produces: the accepted admin snapshot containing the Atlas operations (`pathCount` 57 → 57 + number of new path templates); consumer types regenerated
- Consumed by: Tasks 8–11 (typed client)

- [ ] **Step 1: Export and verify**

```bash
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe scripts/export_openapi.py
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe scripts/verify_openapi_export.py
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/test_admin_openapi.py -q
```
Expected: export OK; `test_admin_openapi.py` FAILS until its route expectations include the new Atlas operations (that failure is the check working).

- [ ] **Step 2: Additive check** — `git diff -- docs/contracts/openapi/current/admin-openapi.json | grep -E '^-' | grep -v '^---'` must print only the always-rewritten header lines. Stop and report otherwise.
- [ ] **Step 3: Re-pin** — new sha256 into `ACCEPTANCE.json` (both variants), the counts in `endpoint-inventory.md`, and the constants in `tests/test_admin_openapi.py` / `tests/test_openapi_hash_drift.py` as applicable:

```bash
sha256sum docs/contracts/openapi/current/admin-openapi.json
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/test_openapi_hash_drift.py tests/test_admin_openapi.py tests/test_admin_permission_matrix.py -q
```
Expected: PASS after the update.

- [ ] **Step 4: Regenerate the admin consumer** and re-pin its own guard:

```bash
cd /d/Project/tahamohammadi-platform/Front-End/admin-panel
npm run generate:api-types
grep -rl "135f14e5c7f03ba1aaee50fca76a54e55e0ed5a2e0360050a8939e837859208c" src
```
Update `src/generated/openapi-hash.json` (sha256, `pathCount`, `openapiVersion`) and `acceptedAdminSchemaSha256` in `src/lib/api/product-contract.test.ts`, then:
```bash
npm test -- src/lib/api/product-contract.test.ts
```
Expected: PASS.

- [ ] **Step 5: Record the acceptance entry** in `Docs/03-contracts/OPENAPI-ACCEPTANCE.md` (coordination root).
- [ ] **Step 6: Commit** (two repositories, explicit paths)

```bash
git add -- docs/contracts/openapi/current tests/test_openapi_hash_drift.py tests/test_admin_openapi.py && git commit -m "chore(contracts): re-pin admin OpenAPI for Atlas operations"
cd ../Front-End/admin-panel && git add -- src/generated src/lib/api/product-contract.test.ts && git commit -m "chore(contracts): adopt the re-pinned admin OpenAPI"
```

---

### Task 8: Admin API client

**Files:**
- Create: `Front-End/admin-panel/src/lib/api/atlas.ts`
- Test: `src/lib/api/atlas.test.ts`

**Interfaces:**
- Produces: `fetchAtlasVersions()`, `createAtlasVersion(label)`, `cloneAtlasVersion(id, label)`, `fetchAtlasVersion(id)`, `fetchAtlasGraph(id)`, `saveAtlasGraph(id, body, revision)`, `createAtlasNode(id, body)`, `updateAtlasNode(id, key, body, revision)`, `deleteAtlasNode(id, key, revision)`, `createAtlasRelation(...)`, `updateAtlasRelation(...)`, `deleteAtlasRelation(...)`, `saveGroups(...)`, `listTaxonomy()`, `saveNodeType(...)`, `saveRelationType(...)`, `recomputeLayout(id, revision)`, `validateAtlasVersion(id)`, `activateAtlasVersion(id, revision)`, `fetchAtlasPreviewLink(id, locale)`, `fetchCanonicalCandidates(source, query)`
- Types: all from `@/generated/admin-api` (`AtlasVersionRowOut`, `AtlasNodeOut`, `AtlasValidationOut`, …) — no hand-written duplicates

- [ ] **Step 1: Write the failing tests** — model them on `src/lib/api/graph.test.ts`: each function asserts method, path, `If-Match` header presence, and 201/409/400 handling through `adminJson`.

```ts
it('updates a node with If-Match and returns the new revision', async () => {
  fetchMock.mockResponseOnce(JSON.stringify({ publicKey: 'method-1a2b3c4d', revision: '17-2026-09-16T12:00:00+00:00' }))
  const result = await updateAtlasNode(3, 'method-1a2b3c4d', { importance: 70 }, '16-2026-09-16T11:00:00+00:00')
  const [url, init] = fetchMock.mock.calls[0]
  expect(url).toBe('/api/v1/admin/atlas/versions/3/nodes/method-1a2b3c4d')
  expect(init?.method).toBe('PATCH')
  expect((init?.headers as Record<string, string>)['If-Match']).toBe('16-2026-09-16T11:00:00+00:00')
  expect(result.revision).toBe('17-2026-09-16T12:00:00+00:00')
})


it('surfaces a stale revision as a conflict', async () => {
  fetchMock.mockResponseOnce(JSON.stringify({ code: 'STALE_REVISION', message: 'stale' }), { status: 409 })
  await expect(updateAtlasNode(3, 'x', { importance: 1 }, 'stale')).rejects.toMatchObject({ kind: 'conflict' })
})
```

- [ ] **Step 2: Run — expect FAIL** (`Cannot find module '@/lib/api/atlas'`).
- [ ] **Step 3: Implement** the client using `adminJson` and the existing error normalisation (never a second fetch wrapper).
- [ ] **Step 4: Run — expect green** (`npm test -- src/lib/api/atlas.test.ts`).
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add the Atlas API client"`

---

### Task 9: Navigation and routes

**Files:**
- Modify: `Front-End/admin-panel/src/components/Nav.tsx`, `src/app/router.tsx`
- Test: `src/components/Nav.test.tsx` (extend), `src/app/router.test.tsx` (extend)

**Interfaces:**
- Produces: nav entry `{ to: '/atlas', label: 'Atlas', requiresStaff: true }`; routes `/atlas`, `/atlas/:versionId`, `/atlas/taxonomy`, `/atlas/:versionId/preview`, each wrapped in `<ProtectedRoute requireStaff>`

- [ ] **Step 1: Write the failing tests** — the nav renders the Atlas link for staff; the router resolves each of the four paths to its page component; an unknown version id renders the page's error state rather than crashing.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the entries (one nav line, four route blocks mirroring the `/graph` blocks).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add Atlas navigation and routes"`

---

### Task 10: Versions page and draft status

**Files:**
- Create: `src/pages/AtlasVersionsPage.tsx`
- Modify: `src/app/router.tsx` (wire the page)
- Test: `src/pages/AtlasVersionsPage.test.tsx`

**Interfaces:**
- Consumes: `fetchAtlasVersions`, `createAtlasVersion`, `cloneAtlasVersion`
- Produces: a table of `{label, status, nodeCount, relationCount, publishedAt, updatedAt}` with `Open editor`, `Clone to draft`, `Create draft`; the active row is visibly marked and its actions are limited to `Clone` and `Open preview`

- [ ] **Step 1: Write the failing tests** — the table renders one row per version; `Clone to draft` calls the API with the source id and navigates to the new version's editor; `Create draft` posts a label; the active version offers no edit control.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with react-query (`useQuery`/`useMutation`) and the existing table/button primitives in `src/components/ui/`.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add the Atlas versions page"`

---

### Task 11: Node form

**Files:**
- Create: `src/components/atlas/NodeForm.tsx`
- Modify: `src/pages/AtlasEditorPage.tsx` (host it)
- Test: `src/components/atlas/NodeForm.test.tsx`

**Interfaces:**
- Produces: a form over one node — canonical record picker (async search through `fetchCanonicalCandidates`, publish-gated), node type select (active types only), importance (0–100 numeric with the band hint), visible toggle, `mobile_overview` radio (`auto`/`featured`/`hidden`), EN/FA override fields with a `blank = canonical copy` hint, alias list, group multi-select, pin controls (`Pin to current position`, `Clear pin`, numeric x/y), and a delete action
- Consumes: `createAtlasNode`, `updateAtlasNode`, `deleteAtlasNode`

- [ ] **Step 1: Write the failing tests**

```tsx
it('shows the canonical record and never lets a key be edited', async () => {
  render(<NodeForm node={node({ canonical: { family: 'researchtopic', id: '1', title: 'PARS-SQL / VTD-Edge' } })} />)
  expect(screen.getByText('PARS-SQL / VTD-Edge')).toBeInTheDocument()
  expect(screen.queryByLabelText(/public key/i)).toBeNull()
})


it('blocks saving a pin with only one coordinate', async () => {
  render(<NodeForm node={node()} />)
  await userEvent.type(screen.getByLabelText(/pin x/i), '12')
  await userEvent.click(screen.getByRole('button', { name: /save/i }))
  expect(await screen.findByText(/both pin coordinates/i)).toBeInTheDocument()
})


it('warns when an override is blank and the canonical locale is missing', async () => {
  render(<NodeForm node={node({ localeStatus: { en: true, fa: false } })} />)
  expect(screen.getByText(/no Persian canonical copy/i)).toBeInTheDocument()
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with labelled controls, `aria-describedby` hints, `role="alert"` for field errors coming from `NormalizedAdminError.fieldErrors`, and a keyboard path for every action.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add the Atlas node form"`

---

### Task 12: Relation form and relation table

**Files:**
- Create: `src/components/atlas/RelationForm.tsx`, `src/components/atlas/RelationTable.tsx`
- Modify: `src/pages/AtlasEditorPage.tsx`
- Test: `src/components/atlas/RelationForm.test.tsx`, `src/components/atlas/RelationTable.test.tsx`

**Interfaces:**
- Produces: the structured relation form (`Source`, `Relation Type`, `Target`, `Directed` only when the type allows it, `Weight`, localized `Explanation`, `Visibility`) with allowed-pair filtering from the taxonomy; and a table with filter (relation type, source type, target type, visibility, hierarchy), edit, delete (confirm), inspect (selects the relation in the graph)
- Consumes: `createAtlasRelation`, `updateAtlasRelation`, `deleteAtlasRelation`

- [ ] **Step 1: Write the failing tests** — the form hides `Directed` for a non-overridable type; it filters the target picker to allowed types; a server `RELATION_TYPE_NOT_ALLOWED` issue renders inline on the target field; the table filters to hierarchy relations only when asked and deleting asks for confirmation first.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with the same error-normalisation path as the node form; the relation key is displayed read-only as the stable identity.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add relation authoring form and table"`

---

### Task 13: Taxonomy pages

**Files:**
- Create: `src/pages/AtlasTaxonomyPage.tsx`, `src/components/atlas/TaxonomyForms.tsx`  for the node-type and relation-type forms
- Modify: `src/app/router.tsx`
- Test: `src/pages/AtlasTaxonomyPage.test.tsx`, `src/components/atlas/TaxonomyForms.test.tsx`

**Interfaces:**
- Produces: node-type CRUD (key, labels EN/FA, descriptions, semantic role, visual role, default importance, allow-as-root, allow-children, canonical source, filter-visible, active, sort order) and relation-type CRUD (key, labels + inverse labels EN/FA, descriptions, directed default, overridable direction, semantic role, hierarchy role, default weight, visual priority, allowed source/target types, self-loop policy, active, sort order)
- Produces: the key field is disabled once the type is in use, with the reason stated inline; delete is disabled when `inUse` is true and shows `TAXONOMY_IN_USE` when attempted

- [ ] **Step 1: Write the failing tests** — key input is disabled with an explanation for an in-use type; the allowed source/target multi-selects reflect saved values; `active: false` is savable and the row renders as retired; deleting an in-use type surfaces the server conflict.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add Atlas taxonomy management"`

---

### Task 14: Deterministic 2D authoring graph

**Files:**
- Create: `src/components/atlas/AuthoringGraph.tsx`
- Modify: `src/pages/AtlasEditorPage.tsx`
- Test: `src/components/atlas/AuthoringGraph.test.tsx`

**Interfaces:**
- Consumes: the stored `coordinates` from `GET /versions/{id}`
- Produces: an SVG authoring plane that renders nodes at their stored coordinates through one deterministic affine transform, selects a node, highlights its incident relations, selects a relation, shows hierarchy-role relations with a distinct stroke, and writes a pin (`pin:{x,y}`) on drag-end only; pan/zoom is local view state and is never persisted

- [ ] **Step 1: Write the failing tests**

```tsx
it('renders every visible node at its stored coordinate transform', () => {
  render(<AuthoringGraph graph={graphFixture} selectedKey={null} onSelect={vi.fn()} onPin={vi.fn()} />)
  expect(screen.getAllByRole('graphics-symbol')).toHaveLength(graphFixture.nodes.length)
  expect(nodeCentre('research-area-1a2b3c4d')).toEqual(project(graphFixture.coordinates['research-area-1a2b3c4d']))
})


it('writes a pin on drag-end and never on drag-move', async () => {
  const onPin = vi.fn()
  render(<AuthoringGraph graph={graphFixture} selectedKey={null} onSelect={vi.fn()} onPin={onPin} />)
  await dragNode('project-2b3c4d5e', { dx: 40, dy: -10 })
  expect(onPin).toHaveBeenCalledTimes(1)
  expect(onPin).toHaveBeenCalledWith('project-2b3c4d5e', expect.objectContaining({ x: expect.any(Number), y: expect.any(Number) }))
})


it('highlights incident relations for the selected node', () => {
  const { container } = render(<AuthoringGraph graph={graphFixture} selectedKey="project-2b3c4d5e" onSelect={vi.fn()} onPin={vi.fn()} />)
  expect(container.querySelectorAll('[data-incident="true"]').length).toBe(graphFixture.incidentCount('project-2b3c4d5e'))
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with `role="graphics-document"`/`graphics-symbol` semantics, a keyboard path (arrow keys move the selection between neighbouring nodes, `P` pins the focused node), and a visible focus ring on the focused node.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add the deterministic 2D authoring graph"`

---

### Task 15: Validation panel and publish gating

**Files:**
- Create: `src/components/atlas/ValidationPanel.tsx`, `src/components/atlas/issue-labels.ts`
- Modify: `src/pages/AtlasEditorPage.tsx`
- Test: `src/components/atlas/ValidationPanel.test.tsx`, `src/components/atlas/issue-labels.test.ts`

**Interfaces:**
- Consumes: `validateAtlasVersion(id)` → `{blocking, warnings}` with `{code, nodeKey, relationKey, groupKey, messageToken}`
- Produces: a panel listing blockers (each with a `Go to <entity>` action that selects it in the graph and opens its form) and warnings (with counts); a `Publish` button that is **disabled** while any blocker exists, with the blocking count and the reason stated next to it; `issue-labels.ts` maps each stable code to a human sentence (the only UI copy for issues)

- [ ] **Step 1: Write the failing tests** — publish is disabled with a blocker and the reason is announced; after the last blocker clears, publish becomes enabled; each blocker's `Go to` selects the right entity; every code in `ATLAS_ISSUE_CODES` (imported from a generated list or asserted against a literal array copied from the spec) has a label — a test fails if a code has no copy.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add Atlas validation panel and publish gating"`

---

### Task 16: Publish confirmation and post-publish status

**Files:**
- Create: `src/components/atlas/PublishDialog.tsx` — a plain confirmation region, **not** a modal dialog
- Modify: `src/pages/AtlasEditorPage.tsx`
- Test: `src/components/atlas/PublishDialog.test.tsx`, `src/pages/AtlasEditorPage.test.tsx`

**Interfaces:**
- Consumes: `activateAtlasVersion(id, revision)` → `{id, status, publishedAt, enqueuedPublicationJob}`
- Produces: a confirmation step that names the version, the node/relation counts and the warning count; after success, a persistent status line reading `Published <date>` plus the job id, and the version becomes read-only in the UI; on `409 VALIDATION_BLOCKED` the panel switches to the returned issues; on `409 STALE_REVISION` a `Reload` action is offered

- [ ] **Step 1: Write the failing tests** — confirmation is required before the call; a successful publish shows the status line and disables editing; `VALIDATION_BLOCKED` renders the returned issues; `STALE_REVISION` renders the reload affordance and does not claim success.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** (inline confirmation, `role="status"` for the outcome, no focus trap).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add publish confirmation and status"`

---

### Task 17: EN/FA preview switch and read-only 3D preview

**Files:**
- Create: `src/pages/AtlasPreviewPage.tsx`
- Modify: `src/app/router.tsx`, `src/lib/api/atlas.ts` (`fetchAtlasPreviewLink` already declared in Task 8)
- Test: `src/pages/AtlasPreviewPage.test.tsx`

**Interfaces:**
- Consumes: `fetchAtlasPreviewLink(versionId, locale)` → `{url, expiresAt}`
- Produces: a locale switch (EN/FA) that re-mints the link, and a framed preview of the real public renderer. **Declared cross-plan dependency:** the framed content requires Plan C's `?preview=<token>` render mode (task C8). Until that lands, the frame loads `/…/atlas/` and the page labels the projection shown as `Active`; the label is derived from the URL used, never hard-coded.

- [ ] **Step 1: Write the failing tests** — switching locale requests a new link (`/preview-link` called with `fa`); the frame `src` equals the returned URL; the page never renders the 3D graph itself (no canvas in this page: `expect(container.querySelector('canvas')).toBeNull()`); the read-only notice is present.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with `<iframe title="Atlas 3D preview" src={url} />` and a visible note stating that this is a read-only preview of the payload the public Atlas will serve.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): add locale preview switch and read-only 3D preview"`

---

### Task 18: Authoring accessibility pass

**Files:**
- Modify: `src/pages/AtlasEditorPage.tsx`, `src/components/atlas/*.tsx`
- Test: `src/pages/AtlasEditorPage.a11y.test.tsx`

**Interfaces:**
- Produces: a documented keyboard-only authoring path: navigate → select node → edit → save → create relation → validate → publish, with no pointer-only step; ≥ 44 px hit areas on every interactive control; visible focus on every control; no canvas-only operation

- [ ] **Step 1: Write the failing tests**

```tsx
it('completes the authoring journey with the keyboard only', async () => {
  render(<AtlasEditorPage />)
  await userEvent.tab()                                  // nav entry
  await keyboardSelectNode('project-2b3c4d5e')           // arrow keys inside AuthoringGraph
  await userEvent.tab({ shift: false })                  // to the node form
  await userEvent.keyboard('{Tab}70')                    // importance
  await userEvent.keyboard('{Enter}')                    // save
  expect(await screen.findByRole('status')).toHaveTextContent(/saved/i)
})


it('keeps every authoring control at least 44px tall', () => {
  render(<AtlasEditorPage />)
  for (const control of screen.getAllByRole('button')) {
    expect(control.getBoundingClientRect().height).toBeGreaterThanOrEqual(44)
  }
})
```

- [ ] **Step 2: Run — expect FAIL** (either the journey breaks or a control measures below 44 px).
- [ ] **Step 3: Fix the components** — increase hit areas via padding (never by scaling text), ensure DOM order equals focus order, add `:focus-visible` styles.
- [ ] **Step 4: Run — expect green**, then the e2e authoring journey:

```bash
npx playwright test tests/e2e/atlas-authoring.e2e.ts
```
Expected: one end-to-end spec creating a draft, adding a node and a relation, pinning a node, validating, and publishing — green against the dev stack (`npm run dev` + backend at `:8000`).
- [ ] **Step 5: Commit** — `git commit -m "feat(admin): meet the Atlas authoring accessibility contract"`

---

### Task 19: Plan B acceptance run

**Files:**
- Modify: `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-B-TASKS.md` (create)
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: the evidence Plan D cites before owner authoring acceptance

- [ ] **Step 1: Backend gates**

```bash
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/ apps/ -q
./.venv/Scripts/python.exe -m ruff check .
```
Expected: all green; test count recorded.

- [ ] **Step 2: Admin gates**

```bash
cd ../Front-End/admin-panel
npm run lint && npm run format:check && npm test && npm run build
npx playwright test tests/e2e/atlas-authoring.e2e.ts
```
Expected: lint/format clean, vitest green, `tsc -b && vite build` succeeds, e2e green.

- [ ] **Step 3: Prove the completion criterion by doing it once** — with the app running, create a draft, add a node, add a relation, pin a node, validate, resolve every blocker, preview EN and FA, publish. Record the version id, the counts, and the resulting `enqueuedPublicationJob` id.
- [ ] **Step 4: Write `EVIDENCE-B-TASKS.md`** with the commands, the outputs and the manual journey record.
- [ ] **Step 5: Commit** — `git commit -m "docs(atlas): record Plan B acceptance evidence"`

---

**Plan B completion criterion:** an editor can construct, validate, preview and publish the entire Atlas from the admin panel — no code edits, no manual database access — while an active version remains immutable and every mutation is guarded, audited and precondition-checked.
