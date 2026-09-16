# Knowledge Atlas v1 Plan D: Migration, About Preview, Retirement and Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the real Research Universe data (4 nodes / 3 relations) into the Atlas with provable semantic, link and locale parity; make About a lightweight 2D preview; retire the About Three.js scene and the obsolete graph paths only after the gates pass; and roll the whole change out — staging first, production only through the owner-gated host procedure — with a rehearsed rollback.

**Architecture:** An idempotent, dry-run-first Django management command adapts `GraphVersion` rows into an `AtlasVersion` (identity system node + one `research-area` per `ResearchTopic` + `research-focus` relations), resolving canonical references through `translation_key`. A parity harness compares the old and new payloads per locale and blocks every downstream step until it is green. About then consumes the same active version through Plan C's `about-preview` 2D projection, the Three.js mount is removed, and the obsolete Home/RU code is retired in separate commits. Production promotion follows the documented host-side runbook; nothing here enables a new pipeline or a production auto-deploy.

**Tech Stack:** Django management commands + pytest, Astro 7 + vitest + Playwright, PostgreSQL, Docker Compose on `taha-nl`, the existing `Deploy staging` workflow, the documented §8 host procedures in `PROJECT-STATUS.md`.

**Spec:** Docs/05-delivery/knowledge-atlas/KNOWLEDGE-ATLAS-V1-DESIGN-SPEC.md

**Depends on:** Plan A (models, services, fixtures) and Plan C (Atlas route, 2D `about-preview` mode, README-level verification). Plan B is required for **owner authoring acceptance** but not for the migration itself; the migration command writes rows directly and is the only sanctioned path that does.

## Global Constraints

- **The current graph storage is never modified.** `GraphVersion`, `GraphNode`, `GraphEdge`, `GraphNodeRelated`, `GraphGroup` and `/api/graph/{locale}` are read-only for this entire plan; their removal is a separate approved change (spec §23.6, §25).
- **Dry-run first, always.** Every mutating command has `--dry-run` and prints what it would write; the real run is a separate, explicit, recorded command.
- **No invented content.** Nothing is authored to "make the Atlas look populated": no Method or Technology rows, no relations that are not in the current published graph, no copy the owner did not write.
- **Parity is a gate, not a report.** The About 3D mount is removed only after the parity record exists (spec §23.4).
- **Hero v2 and Home are untouched.** No file under `src/components/home/**`, `src/components/hero/**` except the explicitly retired Home-graph modules of Task 11, and never `src/lib/visual/hero-sequence.ts`.
- **Retirement is separate from migration.** Cleanup that increases rollback risk gets its own commit boundary and, where the card requires it, its own task.
- **Production is owner-gated.** No task in this plan performs a production promotion; the plan produces the runbook, the evidence, and the explicit owner decision point.
- **Staging deploys through the existing workflow only** — push to the public-site `main`, then watch `Deploy staging`. No new pipeline.

**Commands:**

```bash
# Backend
cd /d/Project/tahamohammadi-platform/Back-End
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/ apps/ -q

# Frontend
cd ../Front-End/public-site
npm test && npm run lint && npm run build
npx playwright test tests/e2e/product-atlas.e2e.ts tests/e2e/product-about.e2e.ts
```

## File Map

**Created — backend**

| Path | Responsibility |
|---|---|
| `Back-End/apps/atlas/management/commands/atlas_seed_taxonomy.py` | Idempotent seed of the v1 node-type and relation-type vocabulary (including `research-focus`) |
| `Back-End/apps/atlas/management/commands/atlas_migrate_graph.py` | Dry-run-first migration of the current `GraphVersion` into an `AtlasVersion` |
| `Back-End/apps/atlas/migration_parity.py` | Pure parity comparison: old semantic model vs new projection, per locale |
| `Back-End/apps/atlas/tests/test_seed_taxonomy.py`, `test_migrate_graph.py`, `test_migration_parity.py` | Coverage for the three modules above |
| `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-D-MIGRATION.md` | Inventory, dry-run output, migration record, parity table, rollback rehearsal |

**Created — frontend**

| Path | Responsibility |
|---|---|
| `src/components/about/AboutAtlasPreview.astro` (+ test) | The About mini preview: 6–10 nodes, active Atlas data, CTA, deep links, no Three.js |
| `tests/e2e/product-about.e2e.ts` | About suite rewritten for the preview (replacing the retired scene assertions) |

**Modified — frontend**

| Path | Change |
|---|---|
| `src/components/about/AboutPageContent.astro` | Render the preview instead of `ResearchUniverse` |
| `src/pages/{en,fa}/about/index.astro` | Load the Atlas snapshot instead of `loadHeroGraph` for the preview slot |
| `src/components/about/ResearchUniverse.astro` | Removed (Task 8) after the gates |
| `src/lib/atlas/preview.ts`, `projection-2d.ts` consumers | Unchanged; the About preview uses the existing `about-preview` mode |
| `tests/e2e/ru-about.e2e.ts` | Retired/replaced (Task 9) |
| `tests/e2e/ru-home.e2e.ts` | Retired or rewritten (Task 10), per the Hero v2 reality |
| `playwright.research.config.ts` | `testMatch` updated to the surviving spec names |

**Modified — workspace**

| Path | Change |
|---|---|
| `PROJECT-STATUS.md` | §5 releases, §6 changelog entry, §7 owner queue |
| `Docs/10-tracking/WORK-LOG.md` | Dated entry for the migration and rollout |
| `Docs/10-tracking/DECISION-LOG.md` | The retirement decisions with their evidence pointers |

**Cross-plan interfaces**

| Interface | Direction | Note |
|---|---|---|
| `AtlasProjection2d` `about-preview` mode | consumes | Plan C task 13 |
| `about-preview` node selection (6–10) | consumes | Plan C task 13 |
| `GET /api/atlas/{locale}` + preview token | consumes | Plan A task 15/16, Plan C task 8 |
| Parity evidence document | produces | Cited by the rollout gate and the WORK-LOG entry |

---

### Task 1: Legacy graph inventory

**Files:**
- Create: `Back-End/apps/atlas/management/commands/atlas_graph_inventory.py`, `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-D-MIGRATION.md` (start it here)
- Test: `Back-End/apps/atlas/tests/test_graph_inventory.py`

**Interfaces:**
- Produces: `manage.py atlas_graph_inventory --json <path>` printing per-locale `{versionId, status, nodes:[{nodeId,type,label,position,relatedRecords}], edges:[{id,source,target,relationType,directed,weight}], groups:[…]}` — read-only, zero writes

- [ ] **Step 1: Write the failing test** — against the test database seeded with a 4-node/3-edge graph, the command's JSON contains every node and edge, `groups` is present (empty is expected), and the command performs no writes (assert row counts before/after are identical).
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the read-only command.
- [ ] **Step 4: Run against the development database and record the output path** in the evidence file:
```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py atlas_graph_inventory --json /tmp/atlas-graph-inventory.json
```
Expected: prints per-locale counts; the JSON is the migration input contract.
- [ ] **Step 5: Commit** — `git commit -m "chore(atlas): add the read-only legacy graph inventory"`

---

### Task 2: Parity fixture from the live published payloads

**Files:**
- Create: `Back-End/apps/atlas/tests/fixtures/legacy-graph/{en,fa}.json`
- Modify: `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-D-MIGRATION.md`
- Test: `Back-End/apps/atlas/tests/test_legacy_parity_fixture.py`

**Interfaces:**
- Produces: the frozen "before" contract — the exact bytes the live public API serves today, captured as test fixtures with the capture command and timestamp recorded

- [ ] **Step 1: Capture the payloads**

```bash
curl -s https://tahamohamadi.ir/api/graph/en -o Back-End/apps/atlas/tests/fixtures/legacy-graph/en.json
curl -s https://tahamohamadi.ir/api/graph/fa -o Back-End/apps/atlas/tests/fixtures/legacy-graph/fa.json
```
- [ ] **Step 2: Write the test that freezes the shape** — 4 nodes and 3 edges per locale, the three labels of each locale verbatim, the relation type `research-focus`, the identity node's `relatedRecords` family `profile`, and the three topic nodes' family `researchtopic`. Record the `sha256` of both files in the evidence document; a later change to the live graph must fail this test loudly rather than silently re-baseline.
- [ ] **Step 3: Run — expect PASS on the captured bytes.**
- [ ] **Step 4: Commit** — `git commit -m "test(atlas): freeze the legacy graph payloads for parity"`

---

### Task 3: Seed the v1 taxonomy vocabulary

**Files:**
- Create: `Back-End/apps/atlas/management/commands/atlas_seed_taxonomy.py`
- Test: `Back-End/apps/atlas/tests/test_seed_taxonomy.py`

**Interfaces:**
- Produces: idempotent creation/update of the six node types (`identity`, `research-area`, `project`, `publication`, `method`, `technology`) and the eleven relation types of spec §6.2 (including `research-focus`), with localized labels, inverse labels, hierarchy roles, allowed type sets and self-loop policies exactly as tabulated
- Produces: `--dry-run` printing a diff of what would change; re-running with no spec change writes nothing

- [ ] **Step 1: Write the failing tests** — a fresh run creates all 17 rows with the spec's values; a second run reports `created=0 updated=0`; changing a label in the command's table updates exactly that row; `research-focus` exists with `directed_default=True`, `hierarchy_role=False`, allowed pair `identity → research-area`; no node type named `experience` exists.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with the vocabulary as a literal table in the command (single source for the seed) and `update_or_create` keyed by `key`.
- [ ] **Step 4: Run the seed against the development database, then prove idempotency**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py atlas_seed_taxonomy --dry-run
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py atlas_seed_taxonomy
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py atlas_seed_taxonomy
```
Expected: dry-run lists the 17 planned rows; the first real run creates them; the second prints `created=0 updated=0`.
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): seed the v1 taxonomy vocabulary"`

---

### Task 4: Migration dry-run utility

**Files:**
- Create: `Back-End/apps/atlas/management/commands/atlas_migrate_graph.py`, `Back-End/apps/atlas/migration_parity.py`
- Test: `Back-End/apps/atlas/tests/test_migrate_graph.py`, `Back-End/apps/atlas/tests/test_migration_parity.py`

**Interfaces:**
- Produces: `manage.py atlas_migrate_graph [--dry-run] [--label "Research Universe v1"]` that reads the legacy graph, maps it into a draft `AtlasVersion`, and prints the full plan (nodes, relations, canonical resolutions per locale, every unresolved reference)
- Produces the **locale-pairing** step the dry run reports: for each candidate canonical record the command resolves the shared `translation_key` and checks that a published EN **and** FA row exist; an unpaired record is reported as a blocking prerequisite and is never paired by guesswork inside this command
- Produces: `compare_parity(legacy_payloads, atlas_projection) -> ParityReport` with `{nodes, edges, labels, links, localeParity}` checks and a `ok` flag

- [ ] **Step 1: Write the failing tests**

```python
def test_dry_run_writes_nothing(legacy_graph, django_assert_num_queries):
    AtlasVersion.objects.all().delete()
    call_command("atlas_migrate_graph", "--dry-run")
    assert AtlasVersion.objects.count() == 0


def test_mapping_is_exactly_the_published_graph(legacy_graph):
    call_command("atlas_migrate_graph", "--label", "Research Universe v1")
    version = AtlasVersion.objects.get(status="draft")
    assert version.nodes.count() == 4
    assert version.relations.count() == 3
    assert set(version.nodes.values_list("node_type__key", flat=True)) == {"identity", "research-area"}
    assert set(version.relations.values_list("relation_type__key", flat=True)) == {"research-focus"}


def test_unresolvable_canonical_reference_is_reported_not_guessed(legacy_graph_without_translation_key):
    result = call_command("atlas_migrate_graph", "--dry-run")
    assert "profile(identity): translation_key missing" in result


def test_migration_is_idempotent(legacy_graph):
    call_command("atlas_migrate_graph", "--label", "A")
    call_command("atlas_migrate_graph", "--label", "B")
    assert AtlasVersion.objects.count() == 1, "a second run must update the existing migrated draft, not duplicate it"
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the mapping of spec §23.3 (identity → `identity` node referencing the `Profile` `translation_key`; each `research-topic-N` → `research-area` referencing that `ResearchTopic`'s `translation_key`, `importance = 80`; each edge → `research-focus`; published `position.x/y` offered as **optional** pins behind `--carry-positions`), plus `compare_parity` implementing spec §23.4's five checks.
- [ ] **Step 4: Run the dry run against development and record it**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py atlas_migrate_graph --dry-run
```
Expected: prints 4 nodes / 3 relations, the canonical resolution for each per locale, and **zero** unresolved references. If the preflight report from Plan A Task 1 still lists unpaired records, stop here: the pairing repair is a separate, owner-visible step and must not be improvised inside this command.
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the dry-run graph migration and parity comparator"`

---

### Task 5: Execute the migration

**Files:**
- Modify: `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-D-MIGRATION.md`
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: one draft `AtlasVersion` in the development database containing exactly the published graph; its id recorded as evidence

- [ ] **Step 1: Run the migration for real (development, not production)**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py atlas_migrate_graph --label "Research Universe v1"
```
- [ ] **Step 2: Recompute the layout so every visible node has coordinates (the migration leaves layout unset on purpose)**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py shell -c "from apps.atlas.models import AtlasVersion; from apps.atlas.services import recompute_layout; v=AtlasVersion.objects.get(status='draft'); print(recompute_layout(v))"
```
Expected: prints `1` (the new `layout_revision`).
- [ ] **Step 3: Validate and record the report**

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.development ./.venv/Scripts/python.exe manage.py shell -c "from apps.atlas.models import AtlasVersion; from apps.atlas.validation import validate_version; print(validate_version(AtlasVersion.objects.get(status='draft')).to_dict())"
```
Expected: `blocking: []`; warnings may include `SINGLE_LEVEL_HIERARCHY` and `NO_INBOUND_RELATIONS` — both honest for a 4-node graph and both acceptable.
- [ ] **Step 4: Commit the evidence** (the draft itself lives in the database, not in git)
```bash
git add -- Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-D-MIGRATION.md
git commit -m "docs(atlas): record the executed graph migration"
```

---

### Task 6: Parity proof

**Files:**
- Create: plus an opt-in live check)
- Modify: `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-D-MIGRATION.md`
- Test: `Back-End/apps/atlas/tests/test_migration_parity_live.py` (fixture-backed

**Interfaces:**
- Produces: the parity table required by spec §23.4 — node count, relation count, per-locale labels, canonical targets, relation display copy — with an explicit PASS per row

- [ ] **Step 1: Write the failing test** — build the Atlas projection from the migrated draft and compare it against `tests/fixtures/legacy-graph/*.json` through `compare_parity`; assert `report.ok is True` and that every check is individually reported.
- [ ] **Step 2: Run — expect PASS**; if any label differs by a character, fix the mapping (never the fixture).
- [ ] **Step 3: Record the parity table** in the evidence document with the exact command and both payload hashes.
- [ ] **Step 4: Commit** — `git commit -m "test(atlas): prove migration parity against the frozen payloads"`

---

### Task 7: About mini 2D preview

**Files:**
- Create: `src/components/about/AboutAtlasPreview.astro`
- Modify: `src/components/about/AboutPageContent.astro`, `src/pages/{en,fa}/about/index.astro`
- Test: `src/components/about/about-atlas-preview.test.ts`
- Consumes (see Interfaces): `AtlasProjection2d` (`about-preview` mode, Plan C task 13), `fetchAtlasSnapshot` (Plan C task 3)

**Interfaces:**
- Produces: an About section that renders 6–10 important nodes from the **active** Atlas version, each linking to `/…/atlas/?focus=node:<key>`, with a CTA to `/…/atlas/`, an honest unavailable state when no version is active, and **no canvas, no Three.js import, no scene module in the About bundle**

- [ ] **Step 1: Write the failing tests** — the ready render contains between 6 and 10 preview nodes (or exactly the visible count when fewer exist), every node links to the correct locale's Atlas focus URL, the anchor is always present, the CTA href is `/{locale}/atlas/`, the unavailable render shows the honest state with the CTA still present, and the component's module graph contains no import from `src/lib/visual/**`.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** by composing the existing 2D projection; do not add a second projection implementation and do not add markup that duplicates the Atlas index.
- [ ] **Step 4: Run — expect green**, then build and verify About ships no canvas:

```bash
npm run build && grep -c "<canvas" dist/en/about/index.html dist/fa/about/index.html
```
Expected: `0` for both files.
- [ ] **Step 5: Commit** — `git commit -m "feat(about): preview the active Atlas in 2D"`

---

### Task 8: Remove the About Three.js mount (gated)

**Files:**
- Modify: `src/components/about/AboutPageContent.astro`, `src/components/about/ResearchUniverse.astro` (remove), `src/components/about/AboutPageContent.astro` imports, `src/styles/research-universe.css` (keep the rules the preview reuses; delete the now-unused About-stage rules)
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: an About route with zero canvas elements, zero scene imports and a smaller client bundle; **only executed after** the three gates below are recorded

- [ ] **Step 1: Confirm every gate is green and recorded**

| Gate | Evidence |
|---|---|
| Full Atlas route green (Plan C Task 24 evidence) | `EVIDENCE-C-TASKS.md` |
| About preview green (Task 7) | this plan's evidence file |
| Migration parity proven (Task 6) | this plan's evidence file |

If any gate is missing, stop and report — do not remove the mount.
- [ ] **Step 2: Remove the mount and the component** in one commit; keep the section position, heading and lead copy unchanged (they belong to the About narrative, not to the retired scene).
- [ ] **Step 3: Verify the removal**

```bash
npm run build
grep -c "<canvas" dist/en/about/index.html dist/fa/about/index.html      # expect 0 0
grep -rn "research-universe/enhancement" src/pages src/components/about   # expect no match
```
- [ ] **Step 4: Commit** — `git commit -m "refactor(about): retire the full Three.js research universe"`

---

### Task 9: Preserve About semantics and rewrite the About tests

**Files:**
- Modify: `src/components/about/AboutPageContent.astro` (prose sections untouched — assert this), `playwright.research.config.ts` (`testMatch` → the surviving spec names)
- Delete: `tests/e2e/ru-about.e2e.ts`
- Test: `tests/e2e/product-about.e2e.ts` (the replacement spec this task creates)

**Interfaces:**
- Produces: About coverage for the preview (deep links, CTA, 6–10 nodes, EN/FA, no canvas, reduced motion, axe) that **replaces** the retired scene assertions rather than dropping them

- [ ] **Step 1: Write the replacement spec** — for both locales: exactly one link per preview node with the right `focus` parameter, the CTA target, no `<canvas>`, the semantic About prose sections still present with their headings, reduced-motion stability, and an axe scan.
- [ ] **Step 2: Run the replacement against the fixture-backed build**

```bash
npx playwright test tests/e2e/product-about.e2e.ts
```
Expected: green.
- [ ] **Step 3: Delete the obsolete spec and update the research config's `testMatch`**, then prove nothing else referenced it:

```bash
grep -rn "ru-about" tests src scripts playwright*.config.ts
```
Expected: no match after the deletion.
- [ ] **Step 4: Commit** — `git commit -m "test(about): cover the Atlas preview and retire the scene spec"`

---

### Task 10: Resolve the stale Home Research Universe spec

**Files:**
- Modify: `playwright.research.config.ts` (`testMatch`), `Docs/10-tracking/DECISION-LOG.md` (the decision and its reasoning)
- Delete: `tests/e2e/ru-home.e2e.ts` (or rewrite it — Step 1's evidence decides; a rewrite is the `Modify` case and the staleness must not survive either way)
- Test: none (this task retires a spec whose subject no longer exists; surviving coverage is `tests/e2e/product-atlas.e2e.ts` plus the existing Hero v2 specs, named in Step 3)

**Interfaces:**
- Produces: a decision recorded with evidence — Home's current presentation is Hero v2 (image sequence, `data-hero-*`, zero canvases), so the Home-RU expectations cannot pass and must not be left red

- [ ] **Step 1: Prove the current Home reality before deciding**

```bash
curl -s https://tahamohammadi.ir/en/ | grep -c "data-universe-region"      # expect 0
curl -s https://tahamohammadi.ir/en/ | grep -oE 'data-hero-[a-z-]+' | sort -u | head
```
Expected: zero universe markers; Hero v2 markers present. Record the output in the decision entry.
- [ ] **Step 2: Check for any remaining consumer of the Home graph components before deleting anything**

```bash
grep -rn "HeroGraph.astro\|GraphNodeList\|home-preset\|createHomeScene" src tests
```
Expected: only test files and the retired modules themselves. If a production import exists, stop and report instead of deleting.
- [ ] **Step 3: Delete the stale spec** (its subject no longer exists) and note where the surviving coverage lives: Atlas behaviours → `tests/e2e/product-atlas.e2e.ts`; Home's actual presentation → the existing Hero v2 specs. Do **not** modify Hero v2 runtime or its specs.
- [ ] **Step 4: Record the decision** in `Docs/10-tracking/DECISION-LOG.md` with the evidence from Step 1 and the coverage mapping from Step 3.
- [ ] **Step 5: Commit** — `git commit -m "test(home): retire the stale research-universe home spec"`

---

### Task 11: Inventory and retire dead Home/RU legacy code (separate boundary)

**Files:**
- Create: `Docs/05-delivery/knowledge-atlas/plans/DEAD-CODE-INVENTORY.md`
- Modify: `Docs/10-tracking/DEBT-REGISTER.md` for anything left deliberately
- Delete: the Home-graph modules and their tests
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: an evidence-backed list with, per file, `imports outside tests`, `production consumer`, `replacement coverage`, `verdict`

- [ ] **Step 1: Build the inventory** for at least: `src/components/hero/HeroGraph.astro`, `GraphNodeList.astro`, `src/lib/research-universe/home-preset.ts`, `src/lib/visual/research-universe/{home-scene,home-motion,core-object}.ts`, `src/lib/visual/hero-enhancement.ts`, and the legacy engine `src/lib/visual/{graph-scene,graph-controller,graph-layout,graph-motion}.ts`.
- [ ] **Step 2: Apply the three-part test to each** (card item 15): no production import, no dependency of the `DESIGN_ATLAS` specimen build, and replacement test coverage. A file failing **any** of the three stays and is recorded as deliberately kept with its reason.
- [ ] **Step 3: Delete only the proven-dead files in their own commit** — and never in the same commit as the migration or the About removal.
- [ ] **Step 4: Re-run the gates** and confirm the `DESIGN_ATLAS` build still succeeds:

```bash
npm run build && npm run build:atlas 2>/dev/null || DESIGN_ATLAS=1 npx astro build
npm test && npx playwright test tests/e2e/product-atlas.e2e.ts tests/e2e/product-about.e2e.ts
```
Expected: green; the design atlas build still produces its pages (it may legitimately lose a specimen if that specimen was the deleted module — in that case the inventory must say so and the atlas section is removed in the same commit).
- [ ] **Step 5: Commit** — `git commit -m "chore(atlas): retire proven-dead home graph modules"`

---

### Task 12: Retired GLB handling

**Files:**
- Modify: `public/research-universe/models/*.glb` (move out of the public shipping path, if the evidence permits), `Docs/10-tracking/DEBT-REGISTER.md` or `Docs/10-tracking/DECISION-LOG.md` (the record)
- Test: `src/lib/visual/research-universe/runtime-purity.test.ts` (its scan must follow the relocated files; never weakened to make the move pass)

**Interfaces:**
- Produces: proof that nothing fetches the two retired GLBs at runtime, and — only then — their removal from the shipped build

- [ ] **Step 1: Prove no runtime consumer**

```bash
grep -rn "research-universe/models\|signature-v1\|signature-v3" src tests scripts docs 2>/dev/null | grep -v "runtime-purity.test.ts"
ls -la public/research-universe/models/
```
Expected: no runtime reference; the purity test is the only mention (it asserts the absence). Record both.
- [ ] **Step 2: Prove the production build ships them today** (`ls dist/research-universe/models/`) and measure the weight — this is the justification for the move.
- [ ] **Step 3: Move the artefacts out of `public/`** into a non-shipping location that preserves history (for example `Design-Assets/research-universe/models/`, which is tracked in the coordination workspace), **and** update the purity test's path expectation so the ban stays enforced from the new location.
- [ ] **Step 4: Verify the build no longer ships them**

```bash
npm run build && ls dist/research-universe/models/ 2>&1 | tail -1
```
Expected: no such directory.
- [ ] **Step 5: Commit** (two repositories: the workspace copy and the public-site removal, staged by explicit path).

---

### Task 13: Rollout sequence

**Files:**
- Create: `Docs/05-delivery/knowledge-atlas/plans/ROLLOUT.md` (the executable runbook, owner-gated)
- Modify: `PROJECT-STATUS.md` §5/§6/§7
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: the ordered, evidence-gated rollout — local → backend tests → admin validation → frontend build/tests → staging → owner visual acceptance → production (owner-gated, host-side)

- [ ] **Step 1: Local gates (all three repositories)** — record the commands and outputs:

```bash
cd Back-End && env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest tests/ apps/ -q && ./.venv/Scripts/python.exe -m ruff check .
cd ../Front-End/public-site && npm run lint && npm run format:check && npm test && npm run build
cd ../admin-panel && npm run lint && npm run format:check && npm test && npm run build
```
- [ ] **Step 2: Admin validation** — with the dev stack running, complete the Plan B journey once on the migrated version (validate → preview EN/FA → publish against the development database) and record the version id and counts.
- [ ] **Step 3: Frontend build + browser gates** — the Atlas and About suites plus the untouched-surface proof:

```bash
git diff --stat origin/main...HEAD -- src/components/home src/components/hero src/styles/hero-sequence.css
```
Expected: empty (Hero v2/Home untouched).
- [ ] **Step 4: Staging** — land on `main` through the repository's own gates and let the existing workflow deploy:

```bash
gh run list --limit 5 --json workflowName,status,conclusion,headBranch
gh run watch <run-id> --exit-status
```
Expected: `Deploy staging` succeeds. Then verify the **deployed artifact**, not just the workflow:

```bash
curl -s https://staging.tahamohamadi.ir/en/atlas/ | grep -o 'data-atlas-status="[a-z]*"' | head -1
curl -s https://staging.tahamohamadi.ir/en/about/ | grep -c "<canvas"        # expect 0
curl -s -D - https://staging.tahamohamadi.ir/api/atlas/en -o /dev/null | grep -iE "etag|cache-control"
```
Expected: `data-atlas-status="ready"`, zero canvases on About, ETag + `public, max-age=60`.

The backend part of the staging deploy must run the additive migrations; record the migration command actually used (`manage.py migrate atlas content`) and its output. Never enable `CMS_CD_AUTO_MIGRATE`.

- [ ] **Step 5: Owner visual acceptance** — the owner reviews the staging Atlas (desktop 3D, compact 2D, both locales, the About preview, deep links) and records acceptance in this repository's tracking register. Nothing proceeds without it.
- [ ] **Step 6: Production (owner-gated, host-side, **not performed by an agent without an explicit owner instruction**)** — the documented §8 pattern in `PROJECT-STATUS.md`, extended to the CMS service this change also needs:

```bash
# on taha-nl, after the owner's go-ahead, with a fresh RELEASE_ID in .env.prod
# 1) pre-flight backup (dump + restore-verified into an isolated probe database)
# 2) build the CMS and web images from the accepted staging SHA
# 3) run the additive migrations explicitly:  manage.py migrate atlas content
# 4) sync the static payload into taha-cms-prod_prod_public_html
# 5) docker compose -p taha-cms-prod --env-file .env.prod \
#      -f deploy/docker-compose.prod.yml up -d --force-recreate cms web
# 6) verify the served artifact: /en/atlas/ ready, About canvas count 0, /api/atlas/en ETag
```
Record the previous image tags and the pre-change backup path — they are the rollback.
- [ ] **Step 7: Update `PROJECT-STATUS.md`** (§5 releases, §6 dated changelog, §7 owner queue) and commit.
- [ ] **Step 8: Commit** — `git commit -m "docs(atlas): record the rollout runbook and status"`

---

### Task 14: Rollback plan and rehearsal

**Files:**
- Modify: `Docs/05-delivery/knowledge-atlas/plans/ROLLOUT.md`
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: four rehearsed rollback levels with the exact command and the expected observable state

- [ ] **Step 1: Rehearse the Atlas-version rollback (no deploy needed)** — re-activate the previous version through the admin publish path and verify the public payload's ETag changes back and the About preview follows. Record the before/after ETags.
- [ ] **Step 2: Rehearse the frontend route rollback** — the previous static payload is restored by rebuilding the previous image tag and re-syncing the volume (the documented §8 procedure); record the exact commands and confirm the Atlas route then serves the pre-Atlas build (no `/atlas/`).
- [ ] **Step 3: Rehearse the About rollback** — because the About change is a frontend rebuild, rolling back the web image restores the previous About presentation without any database action. Confirm by inspection that the retired scene's removal is entirely in the frontend (no schema dependency).
- [ ] **Step 4: State the data rollback property explicitly** — the Atlas migrations are additive; the previous CMS image and the previous web image keep working against a database that also contains the Atlas tables, and `GraphVersion` remains untouched and readable throughout (spec §23.6). A rollback therefore never requires dropping a table; dropping one is a separate, deliberate cleanup.
- [ ] **Step 5: Commit** — `git commit -m "docs(atlas): record the rollback plan and rehearsal"`

---

### Task 15: Final evidence package

**Files:**
- Modify: `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-D-MIGRATION.md`, `Docs/10-tracking/WORK-LOG.md`, `Docs/10-tracking/DECISION-LOG.md`
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: the closure record other agents and the owner read: inventory hashes, dry-run output, migration record, parity table, gate results per phase, staging verification, owner acceptance, production promotion (when performed), rollback rehearsal, and every deferred item with its register entry

- [ ] **Step 1: Assemble the evidence file** — every claim carries its command and its captured output; any unverified claim is labelled as such rather than asserted.
- [ ] **Step 2: Add the dated `WORK-LOG.md` entry** and the `DECISION-LOG.md` entries (retirement decisions, the Home-spec retirement, the GLB relocation).
- [ ] **Step 3: Confirm the deferral registers** — anything not done (for example a Method/Technology content set, an owner-authored group, a second hierarchy level) is in `DEBT-REGISTER.md` or `Docs/10-tracking/DEFERRED-VALIDATION.md` with an owner.
- [ ] **Step 4: Commit** — `git commit -m "docs(atlas): close the migration and rollout evidence"`

---

**Plan D completion criterion:** the site's existing Research Universe data is migrated with proven semantic, link and locale parity; About is a lightweight 2D preview of the active Atlas; the Atlas is the canonical research-graph route; the obsolete About scene and the proven-dead Home/RU modules are retired after their gates; and the change reached staging with an owner-gated production runbook and a rehearsed rollback — with no semantic loss and no modification of the legacy graph storage.
