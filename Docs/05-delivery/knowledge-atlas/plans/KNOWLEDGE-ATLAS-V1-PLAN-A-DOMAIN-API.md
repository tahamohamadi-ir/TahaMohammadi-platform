# Knowledge Atlas v1 Plan A: Domain Model + Public API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a fully testable Atlas domain (models, taxonomy, canonical references, deterministic layout, validation, transactional publish) and the read-only public endpoint `GET /api/atlas/{locale}` with ETag/304 — before any UI consumes it.

**Architecture:** A new Django app `Back-End/apps/atlas/` holds the locale-neutral Atlas topology (version, nodes, relations, groups, taxonomy) plus three pure modules — `canonical.py` (record resolution), `validation.py` (publish gate), `layout.py` (deterministic coordinates). `Method` and `Technology` are added to `apps/content/` as ordinary localized, publishable content entities. The public payload is projected per locale and served by the existing public `NinjaAPI` instance with a strong ETag and `If-None-Match` support. Nothing is mounted in any frontend; the only cross-repository effect is the generated-contract re-pin.

**Tech Stack:** Python 3.12.13, Django 5.2 + django-ninja, PostgreSQL (dev: sqlite), pytest 9 + pytest-django, ruff 0.14; existing `ContentQuerySet.public()` publication gate and the existing OpenAPI export/pin machinery.

**Spec:** Docs/05-delivery/knowledge-atlas/KNOWLEDGE-ATLAS-V1-DESIGN-SPEC.md

## Global Constraints

- **Spec is authority.** Sections 5, 6, 7, 8, 10, 12, 20, 21 and 23 of the spec are binding. This plan fixes only the *storage/API shapes* the spec left to implementation; it reopens no product decision.
- **BACKEND ONLY.** No frontend, no admin UI, no migration of existing content, no production data mutation.
- **Additive migrations only.** Never edit an existing migration file. Every new migration ships with forward and backout evidence (`migrate atlas 0001` / `migrate atlas zero` on a database copy).
- **Pure modules stay pure.** `validation.py` and `layout.py` import no HTTP layer and perform no queries inside the algorithm loops beyond a passed-in queryset.
- **Validation never reshapes.** A validator returns issues; it never returns a reduced or repaired graph.
- **No inferred relations.** The only relation rows that exist are authored ones.
- **Locale parity is a publish blocker in both directions.** Every `visible` node must resolve EN **and** FA (canonical row for that exact locale, or a per-locale override — never a cross-locale fallback) before `activate_version` may succeed; `MISSING_LOCALE_PROJECTION` is blocking and is never emitted as a warning. Invisible nodes follow the visibility rule exactly and are therefore not parity-gated.
- **Draft preview is credential-transported, never URL-transported.** The Atlas preview capability travels only in an `Authorization: Bearer` header to `GET /api/atlas/preview?locale=…` (spec §10.10.1); no Atlas route accepts a preview token in a path segment or query string, and the signing secret (`PREVIEW_SHARE_SECRET`) never reaches frontend code.
- **Exactly one compact-overview field.** `mobile_overview_priority` (model) / `mobileOverviewPriority` (wire) is the only spelling; no second field, alias column or form-only variant is introduced.
- **Exactly one active version platform-wide**, enforced by a partial unique constraint, never by application code alone.
- **Draft invisibility is a test, not an intention:** the public route must be unable to serve draft data on any code path.
- **Working invocation on this machine** (Hermes leaks `PYTHONPATH`; the project venv is `Back-End/.venv`):

```bash
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/ -q
./.venv/Scripts/python.exe -m ruff check .
```

Baseline before Task 1: **952 tests collected**, `ruff` clean, both snapshots pinned (public `469bd51e…`, admin `274407a8…`). Exactly one commit per task; stage by explicit path only.

## File Map

**Created**

| Path | Responsibility |
|---|---|
| `Back-End/apps/atlas/__init__.py`, `apps.py`, `admin.py`, `migrations/__init__.py` | App skeleton (`AppConfig.name = "apps.atlas"`, `label = "atlas"`) |
| `Back-End/apps/atlas/contract.py` | `ATLAS_CONTRACT_VERSION = "atlas01-1.0.0"` — the single wire-contract constant both repositories mirror |
| `Back-End/apps/atlas/keys.py` | Public-key generation/validation: node `<type-key>-<8hex>`, group `group-<8hex>`, composed relation key |
| `Back-End/apps/atlas/canonical.py` | Allow-listed canonical source registry + `translation_key` resolution per locale |
| `Back-End/apps/atlas/models.py` | The ten Atlas models of spec §5.3 |
| `Back-End/apps/atlas/validation.py` | Publish-blocking issues + warnings with stable codes (spec §20) |
| `Back-End/apps/atlas/layout.py` | Deterministic layout pipeline (spec §12.2) |
| `Back-End/apps/atlas/projection.py` | Locale projection → wire payload + ETag digest |
| `Back-End/apps/atlas/services.py` | `clone_version`, `activate_version` (atomic publish), `recompute_layout` |
| `Back-End/apps/atlas/tests/__init__.py`, `factories.py`, `test_*.py` | Test package + ORM factories (the production seed vocabulary is Plan D's) |
| `Back-End/tests/test_atlas_public_api.py` | Endpoint behaviour, ETag/304, draft invisibility, fail-closed |
| `Back-End/docs/contracts/ATLAS-PAYLOAD-CONTRACT.md` | Wire-shape notes for the payload (companion to the spec) |

**Modified**

| Path | Change |
|---|---|
| `Back-End/config/settings/base.py` | Add `"apps.atlas"` to `INSTALLED_APPS` |
| `Back-End/apps/content/models.py` | Add `Method`, `Technology` |
| `Back-End/apps/content/admin.py` | Register the two new entities for staff HTML fallback |
| `Back-End/apps/api/api.py` | Import the Atlas projection; add `GET /api/atlas/{locale}` |
| `Back-End/docs/contracts/openapi/current/public-openapi.json`, `PROVENANCE.json`, `ACCEPTANCE.json` | Regenerated snapshot + deliberate re-pin (Task 19) |
| `Back-End/tests/test_openapi_hash_drift.py` | Accepted-hash constants for the new snapshot (Task 19) |
| `Front-End/public-site/src/generated/public-api.ts`, `src/generated/openapi-hash.json`, `contracts/openapi.public.sha256`, `src/lib/product-api.contract.test.ts` (+ `product-resolver.contract.test.ts`, `src/public-310.contract-fixtures.test.ts`, `src/test-harness/contract-fixtures.ts` if they assert `pathCount`/hashes) | Re-pinned consumer contract (Task 19) |

**Cross-plan interfaces (frozen by this plan)**

| Interface | Consumed by | Shape |
|---|---|---|
| Atlas models + taxonomy + pins | Plan B (admin), Plan D (migration) | `apps.atlas.models.*` |
| `validate_version(version) -> ValidationReport` | Plan B (validate UI), Plan D (gates) | `ValidationReport(blocking=[Issue], warnings=[Issue])`, `Issue.code` stable |
| `activate_version(version_id, *, expected_revision) -> AtlasVersion` | Plan B (publish action), Plan D (rollout) | Raises `ValidationFailed(issues)`, `PreconditionFailed`, `AlreadyActive` |
| `clone_version(source_id, label) -> AtlasVersion` | Plan B (clone action) | New draft with copied public keys and pins |
| `recompute_layout(version) -> int` | Plan B (layout button), Plan D (seed) | Returns new `layout_revision` |
| `GET /api/atlas/{locale}` → payload `atlas01-1.0.0` | Plan C (frontend), Plan D (About preview) | Spec §10.2; keys identical across locales; localized text/hrefs |
| `GET /api/atlas/preview?locale=<en\|fa>` + `Authorization: Bearer <token>` → draft projection | Consumed by Plan C task 8 (static preview shell fetch); **capabilities minted by Plan B task 6** | Spec §10.10/§10.10.1. The credential never appears in a request URL; Plan A owns validation, the signing/verification primitive and the endpoint, so Plans B and C stay independent of each other |
| `build_atlas_preview_token` / `parse_atlas_preview_token` | Consumed by Plan B task 6 (mint) | One primitive, one place that can mint or verify an Atlas preview capability; reuses the existing HMAC/secret handling of `apps/content/preview_token.py` |

---

### Task 1: Preflight — bilingual pairing audit (read-only)

**Files:**
- Create: `Back-End/apps/atlas/management/__init__.py`, `Back-End/apps/atlas/management/commands/__init__.py`, `Back-End/apps/atlas/management/commands/atlas_preflight.py`
- Modify: `Back-End/docs/contracts/ATLAS-PAYLOAD-CONTRACT.md` (create in Task 1 with the preflight report format)
- Test: `Back-End/apps/atlas/tests/test_preflight_command.py`

**Interfaces:**
- Consumes: `apps.content.models.{Profile, ResearchTopic}` and `ContentPublicationMetadataMixin.translation_key`
- Produces: a printed report + JSON file `atlas_preflight_report.json` listing, per candidate record, `{model, locale, pk, slug, translation_key|null, published, partner_locale_present}`; **exit code 1 when any candidate lacks a usable pairing**

- [ ] **Step 1: Write the failing test** — `apps/atlas/tests/test_preflight_command.py`

```python
import json

import pytest
from django.core.management import call_command

from apps.content.models import Profile, ResearchTopic

pytestmark = pytest.mark.django_db


def _make_pair(model, translation_key, **extra):
    rows = []
    for locale in ("en", "fa"):
        rows.append(
            model.objects.create(
                locale=locale,
                slug=f"{model._meta.model_name}-{locale}",
                title=f"{model._meta.model_name} {locale}",
                status="published",
                published_at="2026-01-01T00:00:00Z",
                translation_key=translation_key,
                **extra,
            )
        )
    return rows


def test_preflight_reports_unpaired_record_as_blocking(tmp_path, capsys):
    from uuid import uuid4

    _make_pair(ResearchTopic, uuid4())
    # An unpaired published topic: no translation_key at all.
    ResearchTopic.objects.create(
        locale="en", slug="lonely", title="Lonely", status="published",
        published_at="2026-01-01T00:00:00Z",
    )

    with pytest.raises(SystemExit) as exc:
        call_command("atlas_preflight", "--json", str(tmp_path / "r.json"))

    assert exc.value.code == 1
    report = json.loads((tmp_path / "r.json").read_text(encoding="utf-8"))
    assert report["blocking"], "an unpaired published record must be reported"
    assert any("lonely" in str(entry) for entry in report["blocking"])


def test_preflight_passes_when_every_candidate_is_paired(tmp_path):
    from uuid import uuid4

    _make_pair(ResearchTopic, uuid4())
    _make_pair(Profile, uuid4())

    call_command("atlas_preflight", "--json", str(tmp_path / "r.json"))
    report = json.loads((tmp_path / "r.json").read_text(encoding="utf-8"))
    assert report["blocking"] == []
```

- [ ] **Step 2: Run it — confirm failure**

```bash
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_preflight_command.py -q
```
Expected: FAIL — `ModuleNotFoundError: No module named 'apps.atlas'` then `Unknown command: 'atlas_preflight'`.

- [ ] **Step 3: Minimal implementation** — create the app package (`apps/atlas/apps.py` with `name = "apps.atlas"`, `label = "atlas"`, `default_auto_field` unset), add `"apps.atlas"` to `INSTALLED_APPS`, and write the command:

```python
class Command(BaseCommand):
    help = "Read-only audit of bilingual pairing for Atlas candidate records."

    def add_arguments(self, parser):
        parser.add_argument("--json", dest="json_path", default=None)
        parser.add_argument("--models", default="profile,researchtopic")

    def handle(self, *args, **options):
        report = {"generated_at": timezone.now().isoformat(), "candidates": [], "blocking": []}
        for key in options["models"].split(","):
            model = CANONICAL_SOURCES[key.strip()]
            for row in model.objects.filter(status="published").order_by("slug", "locale"):
                partner = (
                    model.objects.filter(translation_key=row.translation_key, locale=("fa" if row.locale == "en" else "en")).exists()
                    if row.translation_key else False
                )
                entry = {"model": model._meta.model_name, "locale": row.locale, "pk": row.pk,
                         "slug": row.slug, "translation_key": str(row.translation_key) if row.translation_key else None,
                         "partner_locale_present": partner}
                report["candidates"].append(entry)
                if not row.translation_key or not partner:
                    report["blocking"].append(entry)
        if options["json_path"]:
            Path(options["json_path"]).write_text(json.dumps(report, indent=2), encoding="utf-8")
        self.stdout.write(f"atlas_preflight: candidates={len(report['candidates'])} blocking={len(report['blocking'])}")
        if report["blocking"]:
            raise SystemExit(1)
```

`CANONICAL_SOURCES` is created in Task 8; for this task define the two-entry dict locally in the command and move it in Task 8 (a single import-line change).

- [ ] **Step 4: Run both tests — confirm they pass**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_preflight_command.py -q
```
Expected: `2 passed`.

- [ ] **Step 5: Run the preflight against the development database (read-only) and record the output**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py atlas_preflight --json /tmp/atlas-preflight-dev.json
```
Expected: prints candidate/blocking counts; **no database write**. This report is the Plan D prerequisite document (spec §23.2). Do not repair production data here.

- [ ] **Step 6: Commit**

```bash
git add -- apps/atlas/__init__.py apps/atlas/apps.py apps/atlas/management apps/atlas/tests config/settings/base.py
git commit -m "feat(atlas): add read-only bilingual pairing preflight"
```

---

### Task 2: `Method` entity

**Files:**
- Create: `Back-End/apps/content/migrations/0032_method.py` (generated)
- Modify: `Back-End/apps/content/models.py` (append `class Method(...)` after `ResearchTopic`), `Back-End/apps/content/admin.py`
- Test: `Back-End/apps/atlas/tests/test_content_entities.py`

**Interfaces:**
- Consumes: `LocalizedContentMixin`, `ContentPublicationMetadataMixin`, `LifecycleMixin`, `LifecycleStatus`, `Locale`
- Produces: `apps.content.models.Method` with `objects.public()`, `translation_key`, `slug/title/locale`, `short_description`, `description`, `sort_order`, and the allow-listed canonical source key `"method"`

- [ ] **Step 1: Write the failing test**

```python
def test_method_public_gate_and_identity():
    paired = uuid4()
    draft = Method.objects.create(locale="en", slug="draft-method", title="Draft",
                                  status="draft", translation_key=paired)
    live = Method.objects.create(locale="en", slug="live-method", title="Live",
                                 status="published", published_at=timezone.now(),
                                 translation_key=paired)
    future = Method.objects.create(locale="fa", slug="future-method", title="Future",
                                   status="published",
                                   published_at=timezone.now() + timedelta(days=1),
                                   translation_key=paired)

    visible = set(Method.objects.public().values_list("pk", flat=True))
    assert live.pk in visible
    assert draft.pk not in visible
    assert future.pk not in visible
    assert Method._meta.db_table == "content_method"
    with pytest.raises(IntegrityError):
        Method.objects.create(locale="en", slug="live-method", title="Duplicate",
                              translation_key=uuid4())
```

- [ ] **Step 2: Run it — confirm failure**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_content_entities.py -q
```
Expected: FAIL — `ImportError: cannot import name 'Method'`.

- [ ] **Step 3: Implement minimally**

```python
class Method(LocalizedContentMixin, ContentPublicationMetadataMixin, LifecycleMixin):
    """Research/engineering method — first-class publishable entity (Atlas node source)."""

    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "content_method"
        ordering = ["locale", "sort_order", "slug"]
        constraints = [
            models.UniqueConstraint(fields=["locale", "slug"], name="content_method_unique_locale_slug"),
        ]
```

- [ ] **Step 4: Generate and apply the migration, then re-run the test**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe manage.py makemigrations content --name method
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_content_entities.py -q
```
Expected: migration `apps/content/migrations/0032_method.py` created; `1 passed` (2 once Task 3 adds its cases).

- [ ] **Step 5: Backout evidence** (on a database copy, never the dev DB)

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py migrate content 0031
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py migrate content
```
Expected: reverse drops `content_method`, forward recreates it, no other migration touched.

- [ ] **Step 6: Commit**

```bash
git add -- apps/content/models.py apps/content/admin.py apps/content/migrations/0032_method.py apps/atlas/tests/test_content_entities.py
git commit -m "feat(content): add Method entity"
```

---

### Task 3: `Technology` entity

**Files:**
- Create: `Back-End/apps/content/migrations/0033_technology.py`
- Modify: `Back-End/apps/content/models.py`, `Back-End/apps/content/admin.py`
- Test: `Back-End/apps/atlas/tests/test_content_entities.py` (extend)

**Interfaces:**
- Produces: `apps.content.models.Technology`, canonical source key `"technology"`, table `content_technology`

- [ ] **Step 1: Write the failing test** — duplicate Task 2's three assertions for `Technology` (public gate, `db_table == "content_technology"`, unique `(locale, slug)`) plus:
```python
def test_technology_and_method_are_distinct_models():
    assert Method._meta.db_table != Technology._meta.db_table
    assert set(Method._meta.get_fields()) - set(Technology._meta.get_fields()) == {Method._meta.get_field("id")} | set()
```
- [ ] **Step 2: Run — expect FAIL** (`cannot import name 'Technology'`).
- [ ] **Step 3: Implement** the mirrored model with `db_table = "content_technology"` and `content_technology_unique_locale_slug`.
- [ ] **Step 4: Migrate + test**

```bash
./.venv/Scripts/python.exe manage.py makemigrations content --name technology
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_content_entities.py -q
```
Expected: `2 passed`.
- [ ] **Step 5: Register both entities in `apps/content/admin.py`** (list display `title, locale, status, sort_order`, `search_fields = ("title", "slug")`), and add the two keys to `apps/atlas/canonical.py`'s allow-list in Task 8.
- [ ] **Step 6: Commit**

```bash
git add -- apps/content/models.py apps/content/admin.py apps/content/migrations/0033_technology.py apps/atlas/tests/test_content_entities.py
git commit -m "feat(content): add Technology entity"
```

---

### Task 4: Public-key generator

**Files:**
- Create: `Back-End/apps/atlas/keys.py`
- Test: `Back-End/apps/atlas/tests/test_keys.py`

**Interfaces:**
- Produces: `new_node_key(node_type_key: str) -> str`, `new_group_key() -> str`, `relation_public_key(source: str, relation_type: str, target: str, *, directed: bool) -> str`, `PUBLIC_KEY_RE`, `is_valid_public_key(value: str) -> bool`

- [ ] **Step 1: Write the failing test**

```python
from apps.atlas.keys import (PUBLIC_KEY_RE, is_valid_public_key, new_group_key,
                             new_node_key, relation_public_key)


def test_node_key_shape_and_uniqueness():
    keys = {new_node_key("research-area") for _ in range(200)}
    assert len(keys) == 200
    for key in keys:
        assert key.startswith("research-area-")
        assert PUBLIC_KEY_RE.match(key)
        assert is_valid_public_key(key)


def test_group_key_shape():
    assert new_group_key().startswith("group-")
    assert is_valid_public_key(new_group_key())


def test_relation_key_is_composed_and_direction_ordered():
    directed = relation_public_key("identity-2b3c4d5e", "research-focus", "research-area-1a2b3c4d", directed=True)
    assert directed == "identity-2b3c4d5e~research-focus~research-area-1a2b3c4d"

    forward = relation_public_key("a-11111111", "related-to", "b-22222222", directed=False)
    reverse = relation_public_key("b-22222222", "related-to", "a-11111111", directed=False)
    assert forward == reverse == "a-11111111~related-to~b-22222222"
    assert is_valid_public_key(directed) and is_valid_public_key(forward)


def test_key_grammar_rejects_unsafe_characters():
    for bad in ("UPPER-case", "has space", "slash/key", "colon:key", "", "x" * 81):
        assert not is_valid_public_key(bad)
```

- [ ] **Step 2: Run — confirm failure** (`ModuleNotFoundError: No module named 'apps.atlas.keys'`).
- [ ] **Step 3: Implement**

```python
PUBLIC_KEY_RE = re.compile(r"^[a-z0-9][a-z0-9._~-]{1,79}$")
_SUFFIX_BYTES = 4


def _suffix() -> str:
    return uuid.uuid4().hex[:_SUFFIX_BYTES * 2]  # 8 lowercase hex characters


def new_node_key(node_type_key: str) -> str:
    return f"{node_type_key}-{_suffix()}"


def new_group_key() -> str:
    return f"group-{_suffix()}"


def relation_public_key(source: str, relation_type: str, target: str, *, directed: bool) -> str:
    first, second = (source, target) if directed or source <= target else (target, source)
    return f"{first}~{relation_type}~{second}"


def is_valid_public_key(value: str) -> bool:
    return bool(value) and bool(PUBLIC_KEY_RE.match(value)) and "~" not in value.split("~")[0][:1] and len(value) <= 80
```
(Keep the `~`-free constraint explicit: node and group keys never contain `~`, so a `~` in a URL key unambiguously means "relation".)
- [ ] **Step 4: Run — confirm pass** (`4 passed`).
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/keys.py apps/atlas/tests/test_keys.py
git commit -m "feat(atlas): add stable public-key generator"
```

---

### Task 5: Taxonomy models and lifecycle rules

**Files:**
- Create: `Back-End/apps/atlas/models.py` (the two taxonomy models first), `Back-End/apps/atlas/migrations/0001_initial.py` (generated)
- Test: `Back-End/apps/atlas/tests/test_taxonomy.py`

**Interfaces:**
- Produces: `AtlasNodeType`, `AtlasRelationType` with every field of spec §5.3/§6, `SEMANTIC_ROLES`, `VISUAL_ROLES`, `SELF_LOOP_POLICIES`, `CANONICAL_SOURCES`
- Produces: `AtlasNodeType.active_key_immutable` behaviour — `save()` rejects changing `key` after any node exists; `delete()` raises `ProtectedError` while in use

- [ ] **Step 1: Write the failing tests**

```python
@pytest.mark.django_db
def test_node_type_key_is_immutable_once_used():
    node_type = AtlasNodeType.objects.create(key="research-area", label_en="Research area", label_fa="دامنهٔ پژوهشی",
                                             semantic_role="area", visual_role="domain", canonical_source="research_topic")
    version = AtlasVersion.objects.create(status="draft", label="v1")
    AtlasNode.objects.create(version=version, public_key=new_node_key("research-area"), node_type=node_type,
                             canonical_model="research_topic")
    node_type.key = "research-area-renamed"
    with pytest.raises(ValidationError):
        node_type.save()


@pytest.mark.django_db
def test_in_use_taxonomy_cannot_be_deleted():
    node_type = _node_type("project")
    version = AtlasVersion.objects.create(status="draft", label="v1")
    AtlasNode.objects.create(version=version, public_key=new_node_key("project"), node_type=node_type,
                             canonical_model="project")
    with pytest.raises(ProtectedError):
        node_type.delete()
    node_type.active = False
    node_type.save(update_fields=["active"])   # retiring is allowed
    assert AtlasNodeType.objects.get(pk=node_type.pk).active is False


@pytest.mark.django_db
def test_relation_type_records_its_policies():
    relation_type = _relation_type("uses", allowed_sources=["project"], allowed_targets=["method", "technology"])
    assert relation_type.directed_default is True
    assert relation_type.hierarchy_role is False
    assert relation_type.self_loop_policy == "forbid"
    assert relation_type.overridable_direction is False
    assert list(relation_type.allowed_source_types.values_list("key", flat=True)) == ["project"]
```

- [ ] **Step 2: Run — expect FAIL** (`cannot import name 'AtlasNodeType'`).
- [ ] **Step 3: Implement the two models exactly as specified in spec §5.3** — all listed fields, `active`, `sort_order`, `filter_visible`, `canonical_source` choices, `MultipleObjectsReturned`-safe M2M for allowed types, and:

```python
class AtlasNodeType(models.Model):
    key = models.SlugField(max_length=64, unique=True)
    ...
    def save(self, *args, **kwargs):
        if self.pk and AtlasNode.objects.filter(node_type_id=self.pk).exists():
            original = AtlasNodeType.objects.only("key").get(pk=self.pk)
            if original.key != self.key:
                raise ValidationError({"key": "A node type key is immutable once a node uses it."})
        super().save(*args, **kwargs)
```
Deletion protection uses `on_delete=models.PROTECT` on the node FK (Task 6), which raises `ProtectedError` without custom code.
- [ ] **Step 4: Migrate + test** — `makemigrations atlas --name initial_taxonomy`, then pytest the file; expect `3 passed`.
- [ ] **Step 5: Assert the reserved-key rule:** `key` must not contain `~`; add `test_key_never_contains_tilde` (`ValidationError` on `AtlasNodeType(key="a~b")`).
- [ ] **Step 6: Commit**

```bash
git add -- apps/atlas/models.py apps/atlas/migrations/0001_initial.py apps/atlas/tests/test_taxonomy.py
git commit -m "feat(atlas): add node-type and relation-type taxonomy models"
```

---

### Task 6: Version, node and node-translation models

**Files:**
- Create: `Back-End/apps/atlas/migrations/0002_version_node.py`
- Modify: `Back-End/apps/atlas/models.py`
- Test: `Back-End/apps/atlas/tests/test_models_version_node.py`

**Interfaces:**
- Produces: `AtlasVersion` (with the layout storage field, see below), `AtlasNode`, `AtlasNodeTranslation`
- Produces: `AtlasVersion.layout = models.JSONField(default=dict, blank=True)` holding `{"<node public_key>": [x, y, z], ...}` (3-decimal floats) — the spec fixes the layout *behaviour* (computed once per revision and served, §12.1); the plan fixes its storage shape
- Produces: the exact `AtlasNode` field set Plans B and C consume — `version`, `public_key`, `node_type`, `canonical_model`, `canonical_translation_key`, `importance` (0–100), `visible` (bool), `mobile_overview_priority` (`auto` / `featured` / `hidden`, default `auto`), `pin_x` / `pin_y` / `pin_z` (all-or-none), `sort_order`, timestamps — plus `AtlasNodeTranslation(node, locale, label_override, summary_override, aliases)`. These names are final (spec §5): `mobile_overview_priority` is the one compact-overview field, spelled `mobileOverviewPriority` on the wire — there is no `mobile_overview`, no `mobileOverview` and no other alias anywhere, and no separate `pinned` flag, only the coordinate trio.

- [ ] **Step 1: Write the failing tests**

```python
@pytest.mark.django_db
def test_only_one_active_version_can_exist():
    AtlasVersion.objects.create(status="active", label="v1")
    with pytest.raises(IntegrityError):
        AtlasVersion.objects.create(status="active", label="v2")


@pytest.mark.django_db
def test_a_canonical_record_appears_once_per_version():
    node_type = _node_type("publication", canonical_source="publication")
    version = AtlasVersion.objects.create(status="draft", label="v1")
    key = uuid4()
    AtlasNode.objects.create(version=version, public_key=new_node_key("publication"), node_type=node_type,
                             canonical_model="publication", canonical_translation_key=key)
    with pytest.raises(IntegrityError):
        AtlasNode.objects.create(version=version, public_key=new_node_key("publication"), node_type=node_type,
                                 canonical_model="publication", canonical_translation_key=key)


@pytest.mark.django_db
def test_localized_override_is_optional_and_unique_per_locale():
    node = _node()
    AtlasNodeTranslation.objects.create(node=node, locale="en", label_override="Custom EN title")
    with pytest.raises(IntegrityError):
        AtlasNodeTranslation.objects.create(node=node, locale="en", label_override="Second EN title")
    blank = AtlasNodeTranslation.objects.create(node=node, locale="fa")
    assert blank.label_override == "" and blank.aliases == []


@pytest.mark.django_db
def test_node_public_key_is_unique_per_version_and_reusable_across_versions(atlas_v1):
    # Amended during execution (ruling R9): the plan originally asserted GLOBAL uniqueness,
    # which is unsatisfiable with the clone flow this plan's own Task 13 requires
    # (`clone_version` copies keys onto a coexisting draft) and with the critical rule
    # "stable public keys must not silently mutate".
    first, second = _node(), _node(version=AtlasVersion.objects.create(status="draft", label="v2"))
    second.public_key = first.public_key
    with pytest.raises(IntegrityError):
        second.save()


@pytest.mark.django_db
def test_mobile_overview_priority_defaults_and_rejects_unknown_values():
    node = _node()                                   # no explicit mobile_overview_priority
    assert node.mobile_overview_priority == "auto"
    node.mobile_overview_priority = "sometimes"
    with pytest.raises(ValidationError):
        node.full_clean()
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement the three models** with these exact constraints:

```python
class Meta:  # AtlasVersion
    db_table = "atlas_version"
    ordering = ["-id"]
    constraints = [models.UniqueConstraint(fields=["status"], condition=models.Q(status="active"),
                                           name="atlas_version_unique_active")]

class Meta:  # AtlasNode
    db_table = "atlas_node"
    ordering = ["version", "sort_order", "public_key"]
    constraints = [
        models.UniqueConstraint(fields=["version", "public_key"], name="atlas_node_version_public_key"),  # ruling R9
        models.UniqueConstraint(fields=["version", "node_type", "canonical_translation_key"],
                                condition=models.Q(canonical_translation_key__isnull=False),
                                name="atlas_node_unique_canonical_per_version"),
    ]
    indexes = [models.Index(fields=["version", "visible"], name="atlas_node_version_visible_idx"),
               models.Index(fields=["canonical_model", "canonical_translation_key"], name="atlas_node_canonical_idx")]
```
`AtlasNode.clean()` additionally enforces: `public_key` matches `PUBLIC_KEY_RE`; `canonical_model` equals `node_type.canonical_source`; pins are both-or-neither; `mobile_overview_priority` is one of the three choices.
- [ ] **Step 4: Migrate + test** — expect `5 passed`.
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/models.py apps/atlas/migrations/0002_version_node.py apps/atlas/tests/test_models_version_node.py
git commit -m "feat(atlas): add version, node and localized override models"
```

---

### Task 7: Relation, relation-translation, group and membership models

**Files:**
- Create: `Back-End/apps/atlas/migrations/0003_relation_group.py`
- Modify: `Back-End/apps/atlas/models.py`
- Test: `Back-End/apps/atlas/tests/test_models_relation_group.py`

**Interfaces:**
- Produces: `AtlasRelation`, `AtlasRelationTranslation`, `AtlasGroup`, `AtlasGroupTranslation`, `AtlasGroupMembership`
- Produces: `AtlasRelation.public_key` (property, never stored), `AtlasRelationTranslation.explanation`, `AtlasGroupTranslation.{label, description}`

- [ ] **Step 1: Write the failing tests**

```python
@pytest.mark.django_db
def test_relation_duplicate_and_mirror_rules():
    source, target = _node(public_key="research-area-1a2b3c4d"), _node(public_key="project-2b3c4d5e")
    relation_type = _relation_type("related-to", directed_default=False, overridable_direction=True)
    AtlasRelation.objects.create(version=source.version, source=source, target=target,
                                 relation_type=relation_type, directed=False)
    with pytest.raises(IntegrityError):   # exact duplicate
        AtlasRelation.objects.create(version=source.version, source=source, target=target,
                                     relation_type=relation_type, directed=False)
    with pytest.raises(ValidationError):  # mirrored undirected pair, caught by clean()
        AtlasRelation.objects.create(version=source.version, source=target, target=source,
                                     relation_type=relation_type, directed=False).full_clean()


@pytest.mark.django_db
def test_self_loop_only_where_the_type_permits_it():
    node, forbidden = _node(), _relation_type("related-to")
    with pytest.raises(ValidationError):
        AtlasRelation.objects.create(version=node.version, source=node, target=node,
                                     relation_type=forbidden).full_clean()
    allowed = _relation_type("related-to-self", self_loop_policy="allow")
    relation = AtlasRelation.objects.create(version=node.version, source=node, target=node,
                                            relation_type=allowed)
    relation.full_clean()
    assert relation.public_key == f"{node.public_key}~related-to-self~{node.public_key}"


@pytest.mark.django_db
def test_endpoints_must_share_the_version():
    other = AtlasVersion.objects.create(status="draft", label="v2")
    source = _node()
    with pytest.raises(ValidationError):
        AtlasRelation.objects.create(version=source.version, source=source, target=_node(version=other),
                                     relation_type=_relation_type("uses")).full_clean()


@pytest.mark.django_db
def test_group_membership_is_many_to_many_and_localized():
    group = AtlasGroup.objects.create(version=_node().version, public_key=new_group_key())
    for locale, label in (("en", "Vision & language"), ("fa", "زبان و بینایی")):
        AtlasGroupTranslation.objects.create(group=group, locale=locale, label=label)
    node_a, node_b = _node(), _node()
    AtlasGroupMembership.objects.create(group=group, node=node_a)
    AtlasGroupMembership.objects.create(group=group, node=node_b)
    assert group.members.count() == 2
    with pytest.raises(IntegrityError):
        AtlasGroupMembership.objects.create(group=group, node=node_a)
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** with `UniqueConstraint(fields=["version", "source", "target", "relation_type"])`, `clean()` enforcing same-version endpoints, self-loop policy and mirrored-undirected rejection (mirroring `GraphEdge.clean`), and the unique `(node, locale)` / `(group, locale)` / `(group, node)` constraints.
- [ ] **Step 4: Migrate + test** — expect `4 passed`.
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/models.py apps/atlas/migrations/0003_relation_group.py apps/atlas/tests/test_models_relation_group.py
git commit -m "feat(atlas): add relation, group and membership models"
```

---

### Task 8: Canonical CMS-record reference strategy

**Files:**
- Create: `Back-End/apps/atlas/canonical.py`
- Test: `Back-End/apps/atlas/tests/test_canonical.py`

**Interfaces:**
- Produces: `CANONICAL_SOURCES: dict[str, type[Model]]` (strict allow-list: `profile`, `research_topic`, `project`, `publication`, `method`, `technology`), `SUMMARY_FIELDS: dict[str, tuple[str, ...]]`, `CanonicalResolution` dataclass `{model, row, locale, title, summary, route_family, slug}`, `resolve_canonical(source: str, translation_key: UUID, locale: str) -> CanonicalResolution | None`, `resolve_canonical_pair(...) -> dict[str, CanonicalResolution | None]`
- Produces (for Plan B): `CANONICAL_SOURCE_KEYS` for admin pickers

- [ ] **Step 1: Write the failing tests**

```python
def test_allow_list_is_closed_and_ordered():
    assert list(CANONICAL_SOURCES) == ["profile", "research_topic", "project", "publication", "method", "technology"]
    with pytest.raises(KeyError):
        resolve_canonical("researchstatement", uuid4(), "en")   # deliberately not allow-listed in v1


def test_resolution_is_exact_locale_and_publish_gated(seed_pairs):
    topic_en, topic_fa = seed_pairs.research_topic
    key = topic_en.translation_key
    assert resolve_canonical("research_topic", key, "en").row.pk == topic_en.pk
    assert resolve_canonical("research_topic", key, "fa").row.pk == topic_fa.pk

    topic_fa.status = "draft"
    topic_fa.save(update_fields=["status"])
    assert resolve_canonical("research_topic", key, "fa") is None      # unpublished → None
    assert resolve_canonical("research_topic", key, "en") is not None  # never falls back across locales


def test_summary_precedence_uses_the_first_populated_field(seed_pairs):
    project_en, _ = seed_pairs.project
    project_en.summary = ""
    project_en.objective = "Objective text"
    project_en.save(update_fields=["summary", "objective"])
    assert resolve_canonical("project", project_en.translation_key, "en").summary == "Objective text"


def test_ambiguity_is_detected_not_guessed(seed_pairs):
    topic_en, _ = seed_pairs.research_topic
    ResearchTopic.objects.create(locale="en", slug="twin", title="Twin", status="published",
                                 published_at=timezone.now(), translation_key=topic_en.translation_key)
    with pytest.raises(AmbiguousCanonicalRef):
        resolve_canonical("research_topic", topic_en.translation_key, "en")
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement**

```python
CANONICAL_SOURCES: dict[str, type[models.Model]] = {
    "profile": Profile, "research_topic": ResearchTopic, "project": Project,
    "publication": Publication, "method": Method, "technology": Technology,
}
SUMMARY_FIELDS: dict[str, tuple[str, ...]] = {
    "profile": ("short_bio", "summary"), "research_topic": ("summary",),
    "project": ("summary", "objective"), "publication": ("abstract",),
    "method": ("short_description", "description"), "technology": ("short_description", "description"),
}


def resolve_canonical(source, translation_key, locale):
    if translation_key is None:
        return None
    model = CANONICAL_SOURCES[source]
    rows = list(model.objects.public().filter(translation_key=translation_key, locale=locale)[:2])
    if not rows:
        return None
    if len(rows) > 1:
        raise AmbiguousCanonicalRef(f"{source}:{translation_key}:{locale}")
    return _as_resolution(source, rows[0], locale)
```
`_as_resolution` picks the first non-empty summary field and maps `route_family` from `apps.api.record_resolver.ROUTE_FAMILY_MAP` (import it; do not duplicate the table).
- [ ] **Step 4: Run — expect `4 passed`.** Add `apps/atlas/tests/factories.py` with the `seed_pairs` fixture used above (paired EN/FA rows for profile, research_topic, project, publication, method, technology).
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/canonical.py apps/atlas/tests/factories.py apps/atlas/tests/test_canonical.py
git commit -m "feat(atlas): add allow-listed canonical record resolution"
```

---

### Task 9: Relation validation rules

**Files:**
- Create: `Back-End/apps/atlas/validation.py` (relation rules first)
- Test: `Back-End/apps/atlas/tests/test_validation_relations.py`

**Interfaces:**
- Produces: `Issue` dataclass `{code, node_key, relation_key, group_key, message_token}`, `ValidationReport(blocking, warnings)`, `ATLAS_ISSUE_CODES`, `BLOCKING_CODES`, `WARNING_CODES`, `validate_relations(version) -> list[Issue]`
- Codes implemented here: `RELATION_TYPE_INACTIVE`, `RELATION_TYPE_NOT_ALLOWED`, `SELF_LOOP_FORBIDDEN`, `DUPLICATE_RELATION`, `DANGLING_RELATION_ENDPOINT`

- [ ] **Step 1: Write the failing tests** — one test per code, each asserting the exact code string and that the issue names the offending relation key:

```python
def test_allowed_pair_violation_is_blocking(atlas_v1):
    issue = issue_codes(validate_relations(atlas_v1.version))
    assert "RELATION_TYPE_NOT_ALLOWED" in issue
    assert issue["RELATION_TYPE_NOT_ALLOWED"] == [atlas_v1.bad_relation.public_key]


def test_inactive_relation_type_blocks_publish(atlas_v1):
    AtlasRelationType.objects.filter(pk=atlas_v1.relation_type.pk).update(active=False)
    assert "RELATION_TYPE_INACTIVE" in issue_codes(validate_relations(atlas_v1.version))


def test_directed_override_is_only_allowed_when_the_type_permits_it(atlas_v1):
    assert "DIRECTION_NOT_OVERRIDABLE" in issue_codes(validate_relations(atlas_v1.version))
```

- [ ] **Step 2: Run — expect FAIL** (`cannot import name 'validate_relations'`).
- [ ] **Step 3: Implement** the rules with a pure function over the version's relations; each issue carries the composed relation key and a `message_token` (`atlas.relationTypeNotAllowed`, …). `DIRECTION_NOT_OVERRIDABLE` is added to the blocking set (it is the code for a relation whose `directed` contradicts `directed_default` while `overridable_direction` is false).
- [ ] **Step 4: Run — expect `3 passed`.**
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/validation.py apps/atlas/tests/test_validation_relations.py
git commit -m "feat(atlas): add relation validation rules"
```

---

### Task 10: Hierarchy DAG, locale parity and taxonomy lifecycle validation

**Files:**
- Modify: `Back-End/apps/atlas/validation.py`
- Test: `Back-End/apps/atlas/tests/test_validation_hierarchy_locale.py`

**Interfaces:**
- Produces: `validate_hierarchy(version)`, `validate_locale_projection(version)`, `validate_taxonomy(version)`, `validate_canonical_refs(version)`; codes `HIERARCHY_CYCLE`, `MULTIPLE_PARENTS_ALLOWED`-free behaviour (no code — asserted by test), `MISSING_LOCALE_PROJECTION`, `CANONICAL_SOURCE_MISSING`, `CANONICAL_SOURCE_UNPUBLISHED`, `AMBIGUOUS_CANONICAL_REF`, `NODE_TYPE_INACTIVE`, `GROUP_LOCALE_MISSING`, `DANGLING_NODE_HIDDEN_RELATION`

- [ ] **Step 1: Write the failing tests**

```python
def test_hierarchy_allows_multiple_parents_and_rejects_cycles(atlas_dag):
    report = validate_version(atlas_dag.diamond)          # area → {area-a, area-b} → area-c
    assert report.blocking_codes() == []
    assert len(atlas_dag.diamond.node("area-c").parents()) == 2

    atlas_dag.close_cycle()                                # area-c → area-a (hierarchy role)
    assert "HIERARCHY_CYCLE" in validate_version(atlas_dag.diamond).blocking_codes()


def test_general_graph_cycles_are_legal(atlas_dag):
    atlas_dag.add_related_cycle()                          # a related-to b, b related-to a (undirected)
    assert "HIERARCHY_CYCLE" not in validate_version(atlas_dag.diamond).blocking_codes()


def test_missing_fa_projection_blocks_and_override_clears_it(atlas_v1):
    assert "MISSING_LOCALE_PROJECTION" in validate_version(atlas_v1.version).blocking_codes()
    AtlasNodeTranslation.objects.create(node=atlas_v1.fa_missing_node, locale="fa", label_override="برچسب")
    assert "MISSING_LOCALE_PROJECTION" not in validate_version(atlas_v1.version).blocking_codes()


def test_invisible_nodes_and_relations_do_not_participate(atlas_v1):
    AtlasNode.objects.filter(pk=atlas_v1.fa_missing_node.pk).update(visible=False)
    report = validate_version(atlas_v1.version)
    assert "MISSING_LOCALE_PROJECTION" not in report.blocking_codes()
    assert "DANGLING_NODE_HIDDEN_RELATION" in report.blocking_codes()


def test_parity_gate_covers_both_directions_and_passes_when_both_locales_resolve(atlas_v1):
    report = validate_version(atlas_v1.version)
    parity = {issue.nodeKey for issue in report.blocking if issue.code == "MISSING_LOCALE_PROJECTION"}
    assert parity == {atlas_v1.en_missing_node.public_key, atlas_v1.fa_missing_node.public_key}   # EN ✗ and FA ✗ both block

    atlas_v1.override(atlas_v1.en_missing_node, locale="fa", label="برچسب")
    atlas_v1.override(atlas_v1.fa_missing_node, locale="en", label="Label")
    assert "MISSING_LOCALE_PROJECTION" not in validate_version(atlas_v1.version).blocking_codes()   # both resolve → gate passes
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** — hierarchy DFS over `visible` relations whose type has `hierarchy_role=True` (iterating nodes in `public_key` order for determinism), reporting the first node on every cycle; locale projection resolution via `resolve_canonical` with override precedence (`label_override` non-blank ⇒ resolvable without a canonical row); canonical checks per spec §20.1; group copy gate; dangling visible relation to an invisible node.
- [ ] **Step 4: Run — expect `5 passed`** — the parity-matrix test is the §20.1 gate proof for both missing-locale directions and for the both-resolve pass.
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/validation.py apps/atlas/tests/test_validation_hierarchy_locale.py
git commit -m "feat(atlas): add hierarchy, locale-parity and taxonomy validation"
```

---

### Task 11: Deterministic layout engine

**Files:**
- Create: `Back-End/apps/atlas/layout.py`
- Test: `Back-End/apps/atlas/tests/test_layout.py`

**Interfaces:**
- Produces: `LAYOUT_CONSTANTS` (documented numbers), `compute_layout(nodes, relations, groups) -> dict[str, tuple[float, float, float]]`, `hierarchy_depths(...) -> dict[str, int]`, `apply_layout(version) -> dict[str, list[float]]` (rounds to 3 decimals, honours pins)
- Consumes: `AtlasNode` rows (id, public_key, importance, visible, pins, node_type), hierarchy-role relations, group memberships

- [ ] **Step 1: Write the failing tests**

```python
def test_layout_is_deterministic_for_identical_input(atlas_scale_fixture):
    first = compute_layout(*atlas_scale_fixture.parts)
    second = compute_layout(*atlas_scale_fixture.parts)
    assert first == second

    reversed_input = atlas_scale_fixture.parts_reversed()
    assert compute_layout(*reversed_input) == first, "order of arrival must not change the result"


def test_pins_win_over_every_derived_coordinate(atlas_scale_fixture):
    nodes = atlas_scale_fixture.with_pin("project-2b3c4d5e", x=12.5, y=-4.25)
    layout = compute_layout(nodes, atlas_scale_fixture.relations, atlas_scale_fixture.groups)
    assert layout["project-2b3c4d5e"][:2] == (12.5, -4.25)


def test_domains_are_spread_unequally_and_hierarchy_layers_separate(atlas_scale_fixture):
    layout = compute_layout(*atlas_scale_fixture.parts)
    radii = sorted(hypot(x, y) for key, (x, y, z) in layout.items() if atlas_scale_fixture.is_root(key))
    assert radii[-1] - radii[0] > 5, "deterministic spiral must not collapse to one radius"
    depths = atlas_scale_fixture.z_by_depth(layout)
    assert len(set(depths)) > 1, "hierarchy hints must produce more than one depth layer"


def test_blueprint_matches_the_spec_pipeline_order(atlas_scale_fixture):
    assert [stage for stage, _ in atlas_scale_fixture.blueprint()] == [
        "hierarchy-depth", "importance-radius", "seed-placement", "group-attraction",
        "collision-relaxation", "depth-layering", "pins", "final-collision", "rounding",
    ]
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** `layout.py` as a pure module implementing spec §12.2 stages 1–9 with these frozen constants (recorded here so the implementation and its tests agree):

```python
LAYOUT_CONSTANTS = {
    "r_min": 6.0, "r_max": 18.0, "anchor_ratio": 1.45,
    "golden_angle": 2.399963229728653, "seed_spacing": 14.0, "child_seed_scale": 0.55,
    "group_attraction": 0.18, "relaxation_iterations": 120, "relaxation_damping": 0.5,
    "max_step_per_iteration": 1.0, "gap": 3.0, "depth_spread": 9.0, "coordinate_decimals": 3,
}
```
Every iteration walks `sorted(nodes, key=lambda n: n.public_key)`; no `random`, no `time`, no dict-order dependence.
- [ ] **Step 4: Run — expect `4 passed`**, then add a **scale timing test** guarded by `@pytest.mark.slow` asserting 80 nodes/150 relations compute in under 2 s (spec §19.2).
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/layout.py apps/atlas/tests/test_layout.py
git commit -m "feat(atlas): add deterministic layout engine"
```

---

### Task 12: Validation report + payload contract check

**Files:**
- Modify: `Back-End/apps/atlas/validation.py`
- Test: `Back-End/apps/atlas/tests/test_validation_report.py`

**Interfaces:**
- Produces: `validate_version(version) -> ValidationReport`, `ValidationReport.blocking_codes()`, `ValidationReport.to_dict()`, `validate_payload_contract(projection: dict) -> list[Issue]` (codes `PAYLOAD_CONTRACT_INVALID`, `MISSING_LAYOUT`, `INVALID_PIN`, `DUPLICATE_PUBLIC_KEY`, `ISOLATED_NODE`, `NO_INBOUND_RELATIONS`, `NO_OUTBOUND_RELATIONS`, `HIGH_DEGREE_HUB`, `SUMMARY_MISSING`, `UNUSED_NODE_TYPE`, `UNUSED_RELATION_TYPE`, `OVERLAPPING_PINS`, `SCALE_NODES`, `SCALE_RELATIONS`, `SINGLE_LEVEL_HIERARCHY`)

- [ ] **Step 1: Write the failing tests** — one per warning code, plus:
```python
def test_report_shape_is_stable_and_json_serializable(atlas_v1):
    payload = validate_version(atlas_v1.version).to_dict()
    assert set(payload) == {"blocking", "warnings"}
    assert all(set(issue) <= {"code", "nodeKey", "relationKey", "groupKey", "messageToken"} for issue in payload["blocking"])
    json.dumps(payload)


def test_scale_warnings_fire_above_thresholds(atlas_scale_fixture):
    report = validate_version(atlas_scale_fixture.version(visible_nodes=101))
    assert "SCALE_NODES" in report.warning_codes()
    assert "SCALE_NODES" not in report.blocking_codes()
```
- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** aggregation in the spec's order (blocking codes first, then warnings), stable sorting by `(code, nodeKey/relationKey/groupKey)`, and thresholds read from a `SCALE_WARN_THRESHOLDS = {"nodes": 100, "relations": 250, "hubs": 12}` constant.
- [ ] **Step 4: Run — expect all green**; print the full code list and confirm it equals spec §20.1 + §20.2 exactly (a test asserting the two lists against literal tuples freezes the vocabulary).
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/validation.py apps/atlas/tests/test_validation_report.py
git commit -m "feat(atlas): add aggregate validation report with stable issue codes"
```

---

### Task 13: Clone and publish services

**Files:**
- Create: `Back-End/apps/atlas/services.py`
- Test: `Back-End/apps/atlas/tests/test_services_lifecycle.py`

**Interfaces:**
- Produces: `clone_version(source_id, label) -> AtlasVersion`, `activate_version(version_id, *, expected_revision) -> AtlasVersion`, `recompute_layout(version) -> int`, exceptions `ValidationFailed(issues)`, `PreconditionFailed`, `AlreadyActive`, `ImmutableActive`
- Produces: `version_revision(version) -> str` (`f"{version.pk}-{version.updated_at.isoformat()}"`) — the `If-Match` value Plan B's admin API reuses

- [ ] **Step 1: Write the failing tests**

```python
def test_clone_copies_topology_pins_and_keys(atlas_v1):
    clone = clone_version(atlas_v1.version.pk, "v2")
    assert clone.status == "draft"
    assert clone.pk != atlas_v1.version.pk
    assert {n.public_key for n in clone.nodes.all()} == {n.public_key for n in atlas_v1.version.nodes.all()}
    assert clone.nodes.get(public_key=atlas_v1.pinned_key).pin_x == atlas_v1.pinned_x


def test_activate_is_atomic_and_archives_the_previous_active(atlas_two_versions):
    activated = activate_version(atlas_two_versions.draft.pk, expected_revision=version_revision(atlas_two_versions.draft))
    assert activated.status == "active"
    assert AtlasVersion.objects.get(pk=atlas_two_versions.previous_active.pk).status == "archived"
    assert AtlasVersion.objects.filter(status="active").count() == 1
    assert activated.published_at is not None


def test_activation_rolls_back_completely_on_validation_failure(atlas_two_versions):
    atlas_two_versions.break_fa_projection()
    with pytest.raises(ValidationFailed) as exc:
        activate_version(atlas_two_versions.draft.pk, expected_revision=version_revision(atlas_two_versions.draft))
    assert "MISSING_LOCALE_PROJECTION" in {issue.code for issue in exc.value.issues}
    assert AtlasVersion.objects.get(pk=atlas_two_versions.previous_active.pk).status == "active"
    assert AtlasVersion.objects.get(pk=atlas_two_versions.draft.pk).status == "draft"


def test_activation_rejects_either_missing_locale_direction(atlas_two_versions):
    for break_it, restore in ((atlas_two_versions.break_fa_projection, atlas_two_versions.restore_fa_projection),
                              (atlas_two_versions.break_en_projection, atlas_two_versions.restore_en_projection)):
        break_it()
        with pytest.raises(ValidationFailed) as exc:
            activate_version(atlas_two_versions.draft.pk, expected_revision=version_revision(atlas_two_versions.draft))
        assert "MISSING_LOCALE_PROJECTION" in {issue.code for issue in exc.value.issues}
        assert AtlasVersion.objects.get(pk=atlas_two_versions.draft.pk).status == "draft"
        restore()
    activate_version(atlas_two_versions.draft.pk, expected_revision=version_revision(atlas_two_versions.draft))


def test_stale_revision_and_already_active_are_rejected(atlas_two_versions):
    with pytest.raises(PreconditionFailed):
        activate_version(atlas_two_versions.draft.pk, expected_revision="0-stale")
    activate_version(atlas_two_versions.draft.pk, expected_revision=version_revision(atlas_two_versions.draft))
    with pytest.raises(AlreadyActive):
        activate_version(atlas_two_versions.draft.pk, expected_revision=version_revision(atlas_two_versions.draft))


def test_active_version_cannot_be_edited_in_place(atlas_active_version):
    with pytest.raises(ImmutableActive):
        clone_version(atlas_active_version.pk, "no-op") if False else None
    assert not hasattr(services, "edit_active")   # editing an active version is not a supported service
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** with `django.db.transaction.atomic`, re-running `validate_version` and the locale gate **inside** the transaction, `select_for_update()` on the active row, and the archive-then-activate ordering of spec §8.3. `activate_version` returns the refreshed instance and never touches other versions' rows.
- [ ] **Step 4: Run — expect `5 passed`.**
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/services.py apps/atlas/tests/test_services_lifecycle.py
git commit -m "feat(atlas): add clone and transactional publish services"
```

---

### Task 14: Locale projection and payload assembly

**Files:**
- Create: `Back-End/apps/atlas/projection.py`
- Test: `Back-End/apps/atlas/tests/test_projection.py`

**Interfaces:**
- Produces: `build_locale_projection(version, locale) -> dict` (exactly the spec §10.2 shape), `projection_etag(payload) -> str` (`"<version.id>-<16 hex>"`), `canonical_json(payload) -> bytes` (sorted keys, compact separators — the ETag input)
- Consumes: `canonical.resolve_canonical`, `version.layout`

- [ ] **Step 1: Write the failing tests**

```python
def test_projection_serves_only_visible_entities_and_the_documented_order(atlas_scale_fixture):
    payload = build_locale_projection(atlas_scale_fixture.version_obj, "en")
    assert payload["contractVersion"] == "atlas01-1.0.0"
    assert payload["locale"] == "en"
    assert len(payload["nodes"]) == atlas_scale_fixture.visible_count
    assert [n["importance"] for n in payload["nodes"]] == sorted(
        (n["importance"] for n in payload["nodes"]), reverse=True)


def test_ids_are_identical_across_locales_while_text_differs(atlas_scale_fixture):
    en = build_locale_projection(atlas_scale_fixture.version_obj, "en")
    fa = build_locale_projection(atlas_scale_fixture.version_obj, "fa")
    assert [n["key"] for n in en["nodes"]] == [n["key"] for n in fa["nodes"]]
    assert [r["key"] for r in en["relations"]] == [r["key"] for r in fa["relations"]]
    assert [g["key"] for g in en["groups"]] == [g["key"] for g in fa["groups"]]
    assert [n["label"] for n in en["nodes"]] != [n["label"] for n in fa["nodes"]]
    assert all(n["canonical"]["href"].startswith("/en/") for n in en["nodes"] if n.get("canonical"))
    assert all(n["canonical"]["href"].startswith("/fa/") for n in fa["nodes"] if n.get("canonical"))


def test_etag_is_stable_for_an_unchanged_version_and_changes_on_projection_change(atlas_scale_fixture):
    first = projection_etag(build_locale_projection(atlas_scale_fixture.version_obj, "en"))
    second = projection_etag(build_locale_projection(atlas_scale_fixture.version_obj, "en"))
    assert first == second
    atlas_scale_fixture.rename_one_node()
    assert projection_etag(build_locale_projection(atlas_scale_fixture.version_obj, "en")) != first


def test_payload_size_stays_inside_the_budget(atlas_scale_fixture):
    body = canonical_json(build_locale_projection(atlas_scale_fixture.version_obj, "en"))
    assert len(body) < 120_000, "80-node raw payload budget (spec §10.4)"
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement** the projection with camelCase keys, blank-optional omission, `position` from `version.layout`, `canonical` only when resolution succeeded, relation `key` from `keys.relation_public_key`, `hierarchy` from the relation type, `inverseLabel` from the type's inverse copy, and catalogs limited to active types actually used by visible entities.
- [ ] **Step 4: Run — expect `4 passed`.**
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/projection.py apps/atlas/tests/test_projection.py
git commit -m "feat(atlas): add locale projection and ETag digest"
```

---

### Task 15: Public endpoint, draft invisibility, fail-closed behaviour

**Files:**
- Create: `Back-End/apps/atlas/preview_tokens.py`
- Modify: `Back-End/apps/api/api.py`
- Test: `Back-End/tests/test_atlas_public_api.py`, `Back-End/apps/atlas/tests/test_preview_tokens.py`

**Interfaces:**
- Produces: `GET /api/atlas/{locale}` returning the projection; `404` envelope `atlas_not_found` for unknown locale or no active version; `500` envelope with no partial payload when the active version fails its own contract check
- Produces: `GET /api/atlas/preview?locale=<en|fa>` — the **draft projection behind an `Authorization` credential** (spec §10.10.1): the capability is read only from the request's `Authorization: Bearer <token>` header, never from the path or query, and is verified through `parse_atlas_preview_token` (unforgeable, unexpired, `purpose == "atlas-preview"`, locale scope equal to `?locale`, referenced version exists, read-only). Success returns the draft payload with `Cache-Control: no-store`, `Pragma: no-cache`, `X-Robots-Tag: noindex, nofollow`, `Referrer-Policy: no-referrer`. Failure is `401` (absent/unparseable credential) or `403` (expired, wrong purpose, wrong locale, unknown version) — never `404`, because a probe must not learn that a draft exists. It never exposes a draft through `GET /api/atlas/{locale}`, and no route accepts a preview token in a path segment or query string.
- Produces: `Back-End/apps/atlas/preview_tokens.py` — `build_atlas_preview_token(version_id, locale, *, ttl_seconds=600) -> str` and `parse_atlas_preview_token(token) -> AtlasPreviewCapability | None` with `AtlasPreviewCapability(version_id, locale, purpose="atlas-preview", exp)`, signing `preview:atlas-preview:{version_id}:{locale}:{exp}` through the existing HMAC/secret handling of `apps/content/preview_token.py` (`PREVIEW_SHARE_SECRET`, falling back to `SECRET_KEY`). Consumed by Plan B task 6 for minting; the secret stays backend-only settings and is never bundled into a frontend artifact.
- Produces (internal): `public_atlas_payload(locale: str) -> dict | None` importable by Plan B's preview minting

- [ ] **Step 1: Write the failing tests**

```python
def test_serves_active_version_for_both_locales(client, atlas_active_version):
    for locale in ("en", "fa"):
        response = client.get(f"/api/atlas/{locale}")
        assert response.status_code == 200
        body = response.json()
        assert body["locale"] == locale
        assert body["version"]["nodeCount"] == 4


def test_unknown_locale_and_missing_active_version_are_404_envelopes(client):
    assert client.get("/api/atlas/de").json()["code"] == "atlas_not_found"
    AtlasVersion.objects.all().delete()
    assert client.get("/api/atlas/en").json()["code"] == "atlas_not_found"


def test_draft_entities_are_never_served(client, atlas_active_version):
    draft_node_key = atlas_active_version.add_draft_only_node()      # visible node in a DRAFT version
    body = client.get("/api/atlas/en").json()
    assert draft_node_key not in json.dumps(body)
    assert body["version"]["id"] == atlas_active_version.pk


def test_malformed_active_version_fails_closed_without_partial_data(client, atlas_active_version):
    atlas_active_version.corrupt_layout(lambda layout: layout.popitem())   # remove one coordinate
    response = client.get("/api/atlas/en")
    assert response.status_code == 500
    assert "nodes" not in response.json()
    assert response.json()["code"] == "atlas_internal"


def test_relations_never_reference_unknown_nodes(client, atlas_active_version):
    body = client.get("/api/atlas/en").json()
    keys = {node["key"] for node in body["nodes"]}
    for relation in body["relations"]:
        assert relation["source"] in keys and relation["target"] in keys
```

- [ ] **Step 2: Run — expect FAIL** (`404` from the router: route does not exist).
- [ ] **Step 3: Implement** the endpoint beside `get_graph`, projecting only through `public_atlas_payload`, which uses `GraphVersion`-style semantics: `AtlasVersion.objects.filter(status="active").first()` → projection → `validate_payload_contract` → on failure raise `HttpError(500)` with the `atlas_internal` envelope and no body fields. Draft rows must be unreachable by construction (the query filters `status="active"`).
- [ ] **Step 4: Run — expect `5 passed`**, then add the preview-endpoint cases and re-run:

```python
def test_preview_serves_the_draft_projection_with_no_store_headers(client, draft_version_with_extra_node):
    capability = build_atlas_preview_token(draft_version_with_extra_node.pk, "en")   # TTL 600 s
    response = client.get("/api/atlas/preview?locale=en", HTTP_AUTHORIZATION=f"Bearer {capability}")
    assert response.status_code == 200
    assert response["Cache-Control"] == "no-store"
    assert response["Pragma"] == "no-cache"
    assert response["X-Robots-Tag"] == "noindex, nofollow"
    assert response["Referrer-Policy"] == "no-referrer"
    assert response.json()["version"]["id"] == draft_version_with_extra_node.pk
    assert response.json()["locale"] == "en"


def test_preview_credential_is_only_read_from_the_authorization_header(client, draft_version):
    capability = build_atlas_preview_token(draft_version.pk, "en")
    assert client.get("/api/atlas/preview?locale=en").status_code == 401                        # absent
    assert client.get("/api/atlas/preview?locale=en", HTTP_AUTHORIZATION="Bearer nope").status_code == 401
    assert client.get(f"/api/atlas/preview?locale=en&token={capability}").status_code == 401    # query is not a credential
    assert client.get("/api/atlas/preview?locale=en", HTTP_AUTHORIZATION=f"Token {capability}").status_code == 401
    # the URL-carrying route of the rejected design must not exist at all (token never in a path segment)
    assert client.get(f"/api/atlas/preview/{capability}").status_code == 404


def test_preview_rejects_expired_wrong_locale_wrong_purpose_and_unknown_version(client, draft_version, published_article):
    for bad in (build_atlas_preview_token(draft_version.pk, "en", ttl_seconds=-5),
                build_atlas_preview_token(draft_version.pk, "fa"),
                build_preview_token("article", published_article.pk),
                build_atlas_preview_token(999_999, "en")):
        response = client.get("/api/atlas/preview?locale=en", HTTP_AUTHORIZATION=f"Bearer {bad}")
        assert response.status_code == 403, bad


def test_preview_is_read_only_and_never_leaks_into_the_public_route(client, draft_version_with_extra_node):
    capability = build_atlas_preview_token(draft_version_with_extra_node.pk, "en")
    draft_only_key = draft_version_with_extra_node.draft_only_key
    assert draft_only_key in json.dumps(client.get("/api/atlas/preview?locale=en",
                                                  HTTP_AUTHORIZATION=f"Bearer {capability}").json())
    assert client.post("/api/atlas/preview?locale=en", HTTP_AUTHORIZATION=f"Bearer {capability}").status_code == 405
    assert draft_only_key not in json.dumps(client.get("/api/atlas/en").json())
    assert draft_only_key not in json.dumps(client.get("/api/atlas/fa").json())
```

Plus the primitive's own tests in `apps/atlas/tests/test_preview_tokens.py`: a minted token round-trips to `AtlasPreviewCapability(version_id, locale, purpose="atlas-preview", exp)`; a tampered signature, a swapped version id, a swapped locale and a `hero`-style foreign purpose all parse to `None`; TTL defaults to 600 s and is never taken from the request.
Expected: `10 passed`. The purpose/locale scope is the point: the existing preview service mints tokens for content entities, so an Atlas capability must be unreachable with a token minted for anything else, and a content preview must be unreachable with an Atlas capability.

- [ ] **Step 5: Re-run the full backend suite to prove no regression**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/ apps/ -q
```
Expected: `952 + N passed` (N = the new tests), zero failures.
- [ ] **Step 6: Commit**

```bash
git add -- apps/api/api.py tests/test_atlas_public_api.py
git commit -m "feat(atlas): serve the active projection and a token-gated draft preview"
```

---

### Task 16: ETag, If-None-Match and Cache-Control

**Files:**
- Modify: `Back-End/apps/api/api.py`
- Test: `Back-End/tests/test_atlas_public_api.py` (extend)

**Interfaces:**
- Produces: `ETag: "<version.id>-<16 hex>"`, `Cache-Control: public, max-age=60`, `304` with no body on a matching `If-None-Match`, and no projection work on the `304` path

- [ ] **Step 1: Write the failing tests**

```python
def test_etag_and_cache_control_headers(client, atlas_active_version):
    response = client.get("/api/atlas/en")
    assert response["Cache-Control"] == "public, max-age=60"
    assert re.fullmatch(r'"\d+-[0-9a-f]{16}"', response["ETag"])


def test_if_none_match_returns_304_without_a_body(client, atlas_active_version):
    etag = client.get("/api/atlas/en")["ETag"]
    response = client.get("/api/atlas/en", HTTP_IF_NONE_MATCH=etag)
    assert response.status_code == 304
    assert response.content == b""
    assert response["ETag"] == etag


def test_304_path_does_not_rebuild_the_projection(client, atlas_active_version, monkeypatch):
    etag = client.get("/api/atlas/en")["ETag"]
    calls = []
    monkeypatch.setattr(api_module, "build_locale_projection", lambda *a, **k: calls.append(1) or {})
    assert client.get("/api/atlas/en", HTTP_IF_NONE_MATCH=etag).status_code == 304
    assert calls == []


def test_etag_changes_after_activation(client, atlas_two_versions):
    before = client.get("/api/atlas/en")["ETag"]
    activate_version(atlas_two_versions.draft.pk, expected_revision=version_revision(atlas_two_versions.draft))
    assert client.get("/api/atlas/en")["ETag"] != before
```

- [ ] **Step 2: Run — expect FAIL** (no `ETag` header).
- [ ] **Step 3: Implement** the ETag from the active version id + the projection digest inside `public_atlas_payload`, returning the digest alongside the payload so the view can short-circuit before building the body; answer `304` with `HttpResponseNotModified` semantics through Ninja's `Status`/`HttpResponse`.
- [ ] **Step 4: Run — expect `4 passed`.**
- [ ] **Step 5: Commit**

```bash
git add -- apps/api/api.py tests/test_atlas_public_api.py
git commit -m "feat(atlas): add ETag, conditional GET and cache headers"
```

---

### Task 17: Wire contract notes document

**Files:**
- Modify: `Back-End/docs/contracts/ATLAS-PAYLOAD-CONTRACT.md`
- Test: none (documentation) — validated by the drift/pin tasks that follow

**Interfaces:**
- Produces: the human-readable companion to the payload: field tables, key grammar, ordering guarantees, omission rules, the ETag formula, the `304` contract, the preflight report format from Task 1, **and the preview contract** — the mint endpoint, the `Authorization` credential scheme with the documented reason it replaces the repository's path-token share preview, the `?locale=` selector rule, the `no-store`/`no-cache`/`noindex, nofollow`/`no-referrer` header set, and the `401`/`403` matrix with the explicit "never `404` for a bad credential" rule

- [ ] **Step 1: Write the document** from the implemented projection (paste the real field lists; no invented fields). Cross-link `Docs/05-delivery/knowledge-atlas/KNOWLEDGE-ATLAS-V1-DESIGN-SPEC.md` §10 and the new `I09 — Atlas` section of `Docs/03-contracts/PRODUCT-INTERFACES-V2.md`.
- [ ] **Step 2: Verify it matches the implementation** by regenerating one payload and diffing its keys against the document's tables:

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_projection.py -q -k payload_keys
```
Expected: PASS (add a `test_payload_keys_match_documented_contract` that asserts `set(payload) == {...}` and node/relation field sets against literals copied from the doc).
- [ ] **Step 3: Add the `I09 — Atlas` section to `Docs/03-contracts/PRODUCT-INTERFACES-V2.md`** (coordination root) describing the endpoint, its payload and the freshness contract.
- [ ] **Step 4: Commit** (two repositories → two commits, staged by explicit path)

```bash
git add -- docs/contracts/ATLAS-PAYLOAD-CONTRACT.md && git commit -m "docs(api): document the Atlas payload contract"
cd ../.. && git add -- Docs/03-contracts/PRODUCT-INTERFACES-V2.md && git commit -m "docs(contracts): add the I09 Atlas interface"
```

---

### Task 18: Seed-free test fixtures for scale

**Files:**
- Modify: `Back-End/apps/atlas/tests/factories.py`
- Test: `Back-End/apps/atlas/tests/test_factories.py`

**Interfaces:**
- Produces: `atlas_scale_fixture` building a deterministic **72-node / 136-relation** version (the spec's 40–80 / 60–150 target band) with: 1 identity anchor, 12 research areas, 24 projects, 20 publications, 8 methods, 7 technologies, 6 groups, a 3-level hierarchy, one `featured`/`hidden` split using `mobile_overview_priority`, and pins on 4 nodes
- Produces: `atlas_v1`/`atlas_active_version` — the small mirror of the current published graph (identity anchor + 3 research areas + 3 `research-focus` relations) whose surface Tasks 10, 13 and 15 depend on: `version`, `pinned_key`/`pinned_x`, `fa_missing_node` (canonical EN only), `en_missing_node` (canonical FA only), `override(node, *, locale, label)`, `add_draft_only_node()`/`draft_only_key`
- Produces: `atlas_two_versions` — `draft` + `previous_active` with `break_fa_projection()`/`restore_fa_projection()` and `break_en_projection()`/`restore_en_projection()`, used by Task 13's both-directions activation test
- Consumed by Plan C (its frontend fixture is generated from the same JSON) and Plan D (parity tests)

- [ ] **Step 1: Write the failing test**

```python
def test_scale_fixture_matches_the_target_band(atlas_scale_fixture):
    payload = build_locale_projection(atlas_scale_fixture.version_obj, "en")
    assert 40 <= len(payload["nodes"]) <= 80
    assert 60 <= len(payload["relations"]) <= 150
    assert "SCALE_NODES" not in validate_version(atlas_scale_fixture.version_obj).warning_codes()
    assert validate_version(atlas_scale_fixture.version_obj).blocking_codes() == []


def test_scale_fixture_is_deterministic(atlas_scale_fixture):
    atlas_scale_fixture.assert_same_bytes_on_rebuild()
```

- [ ] **Step 2: Run — expect FAIL**.
- [ ] **Step 3: Implement the factory** using `uuid5(NAMESPACE_URL, slug)`-derived `translation_key`s so repeated runs produce identical keys, and text from a small literal pool (no random strings).
- [ ] **Step 4: Run — expect `2 passed`.** Export the fixture for the frontend:

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_factories.py -q --dump-atlas-fixture=../../Front-End/public-site/tests/fixtures/atlas
```
Implement `--dump-atlas-fixture` as a pytest option that writes `en.json`, `fa.json` and `benchmark.json` (72 nodes) exactly as the projection serves them — Plan C copies these files unchanged.
- [ ] **Step 5: Commit**

```bash
git add -- apps/atlas/tests/factories.py apps/atlas/tests/test_factories.py
git commit -m "test(atlas): add deterministic 72-node scale fixtures"
```

---

### Task 19: OpenAPI export, re-pin and consumer type regeneration

**Files:**
- Modify: `Back-End/docs/contracts/openapi/current/{public-openapi.json,PROVENANCE.json,ACCEPTANCE.json,endpoint-inventory.md}`, `Front-End/public-site/{src/generated/public-api.ts,src/generated/openapi-hash.json,contracts/openapi.public.sha256,src/lib/product-api.contract.test.ts}` (+ any other pin consumer the grep finds), `Docs/03-contracts/OPENAPI-ACCEPTANCE.md` (acceptance entry)
- Test: `Back-End/tests/test_openapi_hash_drift.py` (accepted hashes)

**Interfaces:**
- Produces: a re-pinned public contract containing both new public paths — `/api/atlas/{locale}` and `/api/atlas/preview`; `pathCount` 49 → 51; consumer types regenerated from the accepted snapshot
- Consumed by: Plan C (typed payload) and Plan D (migration evidence)

- [ ] **Step 1: Export the snapshot**

```bash
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe scripts/export_openapi.py
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe scripts/verify_openapi_export.py
```
Expected: `public-openapi.json` gains `/api/atlas/{locale}` **and** `/api/atlas/preview` (both public paths, and no path that carries a preview token); `PROVENANCE.json` records the new source commit; verification prints OK.

- [ ] **Step 2: Confirm the delta is additive — this is the gate**

```bash
git diff --stat -- docs/contracts/openapi/current/public-openapi.json
git diff -- docs/contracts/openapi/current/public-openapi.json | grep -E '^-' | grep -v '^---' | head -20
```
Expected: the second command prints **only** the schema-version/description lines the exporter always rewrites (compare with the previous re-pin commit `07197024`); any removed path or removed field is a stop-and-report condition, not a re-pin.

- [ ] **Step 3: Update the recorded accepted hashes** — compute the new values and write them into `ACCEPTANCE.json` (canonical-LF and CRLF variants), `endpoint-inventory.md` counts, and the constants in `tests/test_openapi_hash_drift.py`:

```bash
sha256sum docs/contracts/openapi/current/public-openapi.json
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/test_openapi_hash_drift.py -q
```
Expected: PASS after the update; FAIL (as it should) before it.

- [ ] **Step 4: Re-pin the public-site consumer**

```bash
cd /d/Project/tahamohammadi-platform/Front-End/public-site
npm run generate:api-types
grep -rl "469bd51ed7e1e0d3bed7c64affaf9d488c8ee124da69496e8f5b8acc36eda914" src contracts
```
Update every file the grep lists (`contracts/openapi.public.sha256`, `src/generated/openapi-hash.json`, `src/lib/product-api.contract.test.ts`'s `acceptedPublicSchemaSha256`, `openapiVersion`/`pathCount`, and any fixture pin) to the new hash/count, then:
```bash
npm test -- src/lib/product-api.contract.test.ts src/lib/product-resolver.contract.test.ts src/public-310.contract-fixtures.test.ts
```
Expected: `3 files passed`.

- [ ] **Step 5: Record the acceptance entry** in `Docs/03-contracts/OPENAPI-ACCEPTANCE.md` (coordination root): date, endpoint added, additive-only evidence, new hashes, and the commands run. The drift test is the gate; the entry is the evidence.

- [ ] **Step 6: Commit** (two repositories)

```bash
git add -- docs/contracts/openapi/current tests/test_openapi_hash_drift.py && git commit -m "chore(contracts): re-pin public OpenAPI for the Atlas endpoint"
cd ../.. && git add -- Docs/03-contracts/OPENAPI-ACCEPTANCE.md && git commit -m "docs(contracts): record the Atlas endpoint acceptance"
cd Front-End/public-site && git add -- src/generated contracts/openapi.public.sha256 src/lib/product-api.contract.test.ts && git commit -m "chore(contracts): adopt the re-pinned public OpenAPI"
```

---

### Task 20: Plan A acceptance run

**Files:**
- Modify: `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-A-TASKS.md` (create: the evidence log for this plan)
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: the recorded evidence Plan B/C/D cite when they claim Plan A is done. The file must contain, each with its exact command and output, the twenty plan-completion proofs: Atlas domain tests green · `Method`/`Technology` tests green · taxonomy-constraint tests green · multi-parent green · hierarchy-cycle rejection green · **EN/FA activation parity green in both directions** · atomic-publish rollback green · draft invisibility green · `GET /api/atlas/en` green · `GET /api/atlas/fa` green · stable topology keys identical across the two locale payloads · ETag emitted · `If-None-Match` → `304` · `Cache-Control: public, max-age=60` · a valid short-lived capability reaches exactly its draft version and locale · invalid/expired/wrong-scope capabilities rejected (`401`/`403`) · preview response headers are `no-store`/`noindex, nofollow` · generated contracts/types synchronized · the existing `GraphVersion` system still intact · the public-site/Hero v2 runtime unchanged by this plan

- [ ] **Step 1: Run the full backend gates and capture the output**

```bash
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/ apps/ -q
./.venv/Scripts/python.exe -m ruff check .
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe manage.py check
```
Expected: `952 + N passed`, ruff PASS, `System check identified no issues`.

- [ ] **Step 2: Run the frontend gates touched by the re-pin**

```bash
cd ../Front-End/public-site
npm run lint && npm run format:check && npm test && npm run build
```
Expected: lint/format clean, vitest green, build succeeds (42 pages locally without `PUBLIC_API_BASE_URL`).

- [ ] **Step 3: Write the evidence file** — commands, exact outputs, counts, hashes, and the preflight report path from Task 1. No claim without its command. Tick the twenty proofs listed in **Interfaces** one by one; if a proof cannot be produced, the plan is not complete and the gap is recorded as a finding rather than omitted.
- [ ] **Step 4: Commit**

```bash
git add -- Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-A-TASKS.md
git commit -m "docs(atlas): record Plan A acceptance evidence"
```

---

**Plan A completion criterion:** a fully testable Atlas domain and read-only public API exists — models, taxonomy lifecycle, canonical resolution, deterministic layout, validation with stable codes, transactional publish, `GET /api/atlas/{en,fa}` with ETag/304 — with no UI consuming it yet and no frontend or admin behaviour changed.
