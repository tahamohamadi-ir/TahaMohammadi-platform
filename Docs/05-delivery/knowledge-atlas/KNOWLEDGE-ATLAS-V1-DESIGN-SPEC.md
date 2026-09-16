# Knowledge Atlas v1 — Design Specification

| Field | Value |
|---|---|
| Document | Knowledge Atlas v1 design specification |
| Path | `Docs/05-delivery/knowledge-atlas/KNOWLEDGE-ATLAS-V1-DESIGN-SPEC.md` |
| Status | **APPROVED — DESIGN SPEC (owner decisions final 2026-09-16; no runtime change by this document)** |
| Date | 2026-09-16 |
| Owning repository | Coordination root for the design; implementation spans `Back-End`, `Front-End/public-site`, `Front-End/admin-panel` |
| Reads with | `Docs/09-decisions/ADR-0008`, `Docs/09-decisions/ADR-0010`, `Docs/03-contracts/PRODUCT-INTERFACES-V2.md`, `Docs/04-design/DESIGN-AUTHORITY.md`, `Docs/04-design/DESIGN-DNA.md`, `Docs/05-delivery/concept-alignment-v2/EXECUTION.md` |
| Supersedes | Nothing. The Research Universe renderer lineage is reused, not replaced. |

**Normative language.** `must`, `must not`, `shall` and `is required to` are binding on implementation. Every number stated as a budget is a ceiling that must be verified by the named measurement before the phase that depends on it is accepted.

**Implementation scope of this document.** This document specifies a system. It changes no runtime code, no model, no migration, no test and no deployment. It is the authority a future implementation program builds against.

---

## 1. Executive summary

The Knowledge Atlas is the site's research-graph product: one authored property graph of research areas, projects, publications, methods and technologies, published as a single bilingual topology, and presented four ways from that one topology — a full 3D interactive Atlas on desktop, a deterministic 2D SVG Atlas on mobile and on WebGL-less desktops, a lightweight 2D preview inside About, and a semantic HTML index that works with no JavaScript at all.

What makes it a product rather than a visualisation:

- **The graph is authored data, not inferred decoration.** Every node and every relation is an explicit editorial act in the admin panel. Nothing is derived from co-occurrence, similarity, titles or "AI".
- **Nodes are references, never copies.** A node points at a canonical published CMS record and borrows its content. Presentation overrides exist but are blank by default; the canonical record stays the source of truth.
- **One topology, two language projections.** EN and FA share the same node, relation and group identities. Only copy, links and explanations are localized. There is no per-locale graph.
- **Selection is addressable.** `?focus=node:<key>` and `?focus=relation:<key>` make any semantic selection a shareable, restorable, back/forward-safe URL.
- **Delivery is hybrid.** The Astro build embeds a validated snapshot so the first paint is complete without a network call; the runtime then revalidates cheaply against `GET /api/atlas/{locale}` and adopts a newer published version only when one exists. Publishing never requires a frontend deploy.
- **The renderer is the current Research Universe lineage**, extended for this scale: lazy dynamic import, one canvas per route, render-on-demand with zero idle RAF, DPR and drawing-buffer ceilings, offscreen pause, full disposal and a semantic fallback on every failure path.

The Atlas is additive. The existing `GraphVersion` graph, the existing About Research Universe and Hero v2 on Home keep working untouched until the migration phases retire them deliberately, after parity is proven.

---

## 2. Product goals and non-goals

### 2.1 Goals

| # | Goal | Measured by |
|---|---|---|
| G1 | Communicate "researcher who builds systems" — a body of work with structure, not a technology showcase | Preview + Atlas render against real published data only; zero decorative nodes |
| G2 | Make 40–80 research entities explorable without reading a list | Every node selectable and every selection addressable by URL |
| G3 | Show relationships as first-class, authored facts | Relations are selectable objects with their own inspector state and deep link |
| G4 | Keep the site's editorial/scientific character | Palette, type and material language come from the existing token authority (`Docs/04-design/DESIGN-AUTHORITY.md`, `Docs/04-design/DESIGN-DNA.md`, `contracts/design-authority/tokens.json`); no new visual system |
| G5 | Work for every visitor | Four presentations from one topology: desktop 3D, 2D SVG, About preview, no-JS semantic index |
| G6 | Stay inside the existing performance and accessibility contracts | Existing scene ceilings + Atlas budgets in §19, WCAG 2.2 AA evidence per §22 |
| G7 | Be editable by the owner without engineering | 100% of production-authorable semantics managed from admin (§9) |
| G8 | Publish without a deploy | Runtime API serves a newly activated version immediately (§8, §11) |

### 2.2 Non-goals

The Atlas is explicitly **not**:

- a generic AI network visualisation, or an illustration of "AI";
- a WebGL demo, a shader showcase, or a visual effect;
- a portfolio-only graph whose nodes are just links to pages;
- a second CMS, or a second home for content that already has a canonical record;
- a force-directed screensaver — no permanent browser physics, no idle simulation;
- a cyberpunk visualisation — no neon glow, no volumetric mist, no holographic chrome;
- a knowledge base with generated or inferred claims — **no inferred semantic edges**;
- a replacement for page-level navigation, search or the CV.

---

## 3. Current-state constraints

Each constraint below is verified against the current repositories and is binding on the design. File paths are relative to `Front-End/public-site` unless a repository is named.

| # | Constraint | Evidence | Consequence for the Atlas |
|---|---|---|---|
| C1 | The public site is static-first Astro 7 with **no SSR adapter**; all content is fetched at build time | `astro.config.mjs`; no adapter; `src/pages/**` use top-level `await` | The first paint comes from a build-time snapshot; runtime freshness is an enhancement layer, never a prerequisite |
| C2 | **One canvas per route** is a contract constant | `SCENE_PERFORMANCE_CEILINGS.maxActiveCanvasesPerRoute = 1` in `src/lib/visual/scene-contract.ts` | The Atlas route owns exactly one canvas; About must own none after extraction |
| C3 | Home is canvas-free and Hero v2 is frozen | Live `https://tahamohamadi.ir/en/` serves zero `<canvas>` and zero `data-universe-*` markers; Home renders `HeroSequence.astro` image frames | The Atlas must not add anything to Home; Hero v2 is not touched by this program |
| C4 | The current published graph is **4 nodes / 3 relations**, authored as a CMS `GraphVersion` per locale | Live `GET /api/graph/en` and `/api/graph/fa`; `Back-End/apps/api/api.py::public_graph_payload` | Migration is a small, fully verifiable parity exercise (§23) |
| C5 | The graph stores **one active version per locale**, and node ids differ by locale (`research-topic-1..3` vs `..4..6`) | `GraphVersion` partial unique constraint; live payloads | The Atlas replaces this with one locale-neutral version; locale-neutral identity is a hard requirement |
| C6 | The CMS pairs the EN and FA rows of one logical record through `translation_key` (UUID, nullable) | `ContentPublicationMetadataMixin.translation_key`; `apps/admin/views.py` sibling lookup; odd value of `translationKey` in the admin API | The canonical-record reference is `(model, translation_key)`, not a row id (§5.4) |
| C7 | Public reads are gated by `objects.public()` (published + `published_at <= now`) and by the publication-snapshot fallback | `apps/content/models.py::ContentQuerySet.public`; `apps/content/published.py` | A node is publishable only when the referenced record is publicly resolvable in **both** locales at publish time (§20) |
| C8 | The renderer already provides: lazy dynamic import, one coalesced rAF frame, no idle loop, `IntersectionObserver` visibility pause, ledger-based disposal, context-loss fallback, DPR caps (1.5 desktop / 1.0 mobile) and a 1.5 M-pixel drawing-buffer cap | `src/lib/visual/research-universe/{enhancement,scene-core,dispose}.ts`; idle-draw evidence in `docs/quality/RESEARCH-UNIVERSE-RU2-EVIDENCE.md` | The Atlas inherits these; it must not regress any of them |
| C9 | Triangles are capped at 50,000 and draw calls at 60 for a scene | `SCENE_PERFORMANCE_CEILINGS` | 80 nodes cannot use one tessellation tier; see the tier arithmetic in §13.7 |
| C10 | Picking and label projection are O(n) with 26 curve samples per relation edge, with no spatial-index dependency installed | `src/lib/visual/research-universe/hit-testing.ts`, `layout.ts` | §19 defines the benchmark gate and the dependency-free broad-phase plan |
| C11 | The public API sends **no CORS headers** and the site declares `connect-src 'self'` (report-only today) | Live `GET /api/graph/en` with an `Origin` header returns no `access-control-allow-*`; CSP header on the same response | Runtime Atlas reads must be same-origin (`/api/atlas/{locale}`), never a cross-origin API host |
| C12 | The existing public graph response sets `Cache-Control: public, max-age=60` and is served `cf-cache-status: DYNAMIC` | Live response headers | The freshness contract accepts a bounded staleness window and uses conditional requests (§11.3) |
| C13 | Two graph engines exist: the live Research Universe lineage (`src/lib/visual/research-universe/*`) and a legacy CA-03/04/05 engine (`graph-scene.ts`, `graph-controller.ts`, `graph-layout.ts`, `graph-motion.ts`, `hero-enhancement.ts`) reachable only from the `DESIGN_ATLAS=1` specimen build and unit tests | Import graph scan; `docs/quality/concept-alignment-v2/CA-0*-HANDOFF.md` | The legacy engine is **never** part of Atlas architecture |
| C14 | The Home Research Universe path is unwired: `HeroGraph.astro` is rendered by no page, and `tests/e2e/ru-home.e2e.ts` still targets its region | No page imports `HeroGraph.astro`; live Home has no `data-universe-region` | Home's dead graph path is out of scope here and is explicitly handled separately (§23.7) |
| C15 | Contract pins are explicit and CI-checked: `contracts/openapi.public.sha256`, `src/generated/openapi-hash.json`, generated `src/generated/public-api.ts` | Repo files + `npm run generate:api-types` | The Atlas endpoint must re-pin through the existing synchronization procedure (§10.9) |
| C16 | Route registration is explicit in several places: `src/pages/{locale}/…`, `src/lib/seo-route-registry.ts`, `scripts/seo-route-registry.mjs`, `src/lib/navigation.ts`, sitemap filter in `astro.config.mjs` | Repo files | A new `/atlas/` route must be registered in all of them in one change |
| C17 | Retired Blender GLB artefacts are still published under `public/research-universe/models/` with no runtime consumer, and a source-scan test forbids runtime references to them | `public/research-universe/models/*.glb`; `src/lib/visual/research-universe/runtime-purity.test.ts` | The Atlas adds no authored-asset path; the retired files are not migrated or referenced |
| C18 | The root coordination repo runs no CI and holds no formatter config; the two frontend/backend repos carry their own gates | No `.github/workflows/` at the root; per-repo workflows | Documentation changes are validated by review; code phases must pass each repository's own gates |

---

## 4. Information architecture

### 4.1 Routes

| Route | Presentation | Data | Notes |
|---|---|---|---|
| `/en/about/`, `/fa/about/` | **2D SVG mini Atlas preview** (6–10 important nodes) + CTA | Same active Atlas version as the full Atlas | No Three.js on About after extraction. No separate About graph exists in CMS. |
| `/en/atlas/`, `/fa/atlas/` | **Desktop (≥ 1024 px):** full 3D Atlas · **Mobile / compact (< 1024 px):** deterministic 2D SVG Atlas · **No WebGL:** 2D SVG Atlas · **No JS:** semantic HTML index | One locale projection of the active Atlas version | The only route that may own a canvas |
| `/en/atlas/preview/`, `/fa/atlas/preview/` | The same presentation as `/…/atlas/`, driven by a short-lived draft-preview capability carried in the URL **fragment** | The draft projection fetched with an `Authorization` header (§10.10), or the honest active framing when no valid token is present | `noindex, nofollow`, never in the sitemap, never canonicalised, never a nav entry. Not an authoring surface. |

`atlas` is a new canonical index route in both locales. It is registered in `src/lib/seo-route-registry.ts`, `scripts/seo-route-registry.mjs`, the sitemap `filter` in `astro.config.mjs` (no exclusion) and, once the owner asks for it, `src/lib/navigation.ts`.

### 4.2 Presentation matrix

For presentation purposes `desktop` means **≥ 1024 px** CSS width and `compact` means **< 1024 px**. The inherited DPR rule (1.5 desktop / 1.0 at mobile widths) still applies inside a running 3D scene regardless of this boundary.

| Condition | Desktop ≥ 1024 px | Compact < 1024 px |
|---|---|---|
| WebGL available, motion allowed | 3D Atlas, orbit + zoom + focus | **2D SVG Atlas** |
| WebGL unavailable | 2D SVG Atlas | 2D SVG Atlas |
| `prefers-reduced-motion: reduce` | 3D Atlas, static pose, instant selection, no transitions | 2D SVG Atlas (no motion by construction) |
| JavaScript disabled | Semantic HTML index | Semantic HTML index |

Rules:

- The 3D presentation requires **both** an available WebGL context and a viewport of at least 1024 px CSS width. Below that width the 2D projection is used, not a shrunken 3D scene — a 3D Atlas squeezed into a phone viewport is the presentation this design rejects. The 2D presentation has no orbit, no physics and no pinch-to-explore requirement.
- The inspector is stacked below the graph in the compact presentation, and beside the scene in the desktop presentation (§17.1). The scene's effective viewport (§17.2) is therefore full-width in the compact presentation.
- The presentation decision is made once per page load from capabilities, then published to the DOM as `data-atlas-presentation="3d" | "2d" | "list"` on the region element so tests and CSS read one fact.
- The 2D projection is the same topology in the same order, laid out deterministically from the same published coordinates (§12, §14). Switching presentation never changes the selected entity, the URL or the inspector content.

### 4.3 Entry points and navigation

- The About preview CTA is the primary editorial entry to `/…/atlas/`.
- Deep links enter the Atlas with a focused node or relation.
- v1 introduces **no primary-navigation change**. Promoting the Atlas into the main navigation is deferred (§25) and would be a one-line change in `src/lib/navigation.ts` when requested.

### 4.4 SEO and indexability

- `/en/atlas/` and `/fa/atlas/` are canonical, indexable, exact-locale pages with mutual `alternate` links from the existing route contract.
- `/en/atlas/preview/` and `/fa/atlas/preview/` are **not** indexable: `noindex, nofollow`, excluded from the sitemap, no canonical link that advertises them, and never reachable from the public navigation or the About preview. A draft capability must never be crawlable or shareable as a page.
- The canonical URL never contains a query string. `?focus=…` is a view state and is not canonicalised, indexed, or emitted in the sitemap.
- The no-JS semantic index carries the same published facts for crawlers and assistive technology: node list with type, title, summary and canonical link, plus the relation list with labelled endpoints.
- Pagefind keeps indexing the built page; the Atlas nodes themselves are HTML, so they are searchable by the site search as content, independent of the Atlas search UI (§16).

---

## 5. Domain model

### 5.1 Placement

| Concern | Location | Rationale |
|---|---|---|
| Atlas topology, taxonomy, layout, validation, admin API, public projection | New Django app **`Back-End/apps/atlas/`** | A distinct subsystem with its own validation, layout and admin surface; mirrors the existing `composition`, `siteconfig`, `analytics` app split |
| `Method`, `Technology` | **`Back-End/apps/content/models.py`** | They are localized, publishable CMS content entities: they reuse `LocalizedContentMixin`, `ContentPublicationMetadataMixin`, `LifecycleMixin` and the `objects.public()` gate, exactly like `ResearchTopic` |
| Public Atlas endpoint | `Back-End/apps/api/api.py` (alongside `/graph/{locale}`) | The public API is one NinjaAPI instance mounted at `path("api/", api.urls)` |
| Admin Atlas endpoints | `Back-End/apps/atlas/api_admin.py`, registered on the existing `admin_api` at `/api/v1/admin/atlas` | Mirrors `/api/v1/admin/graph` |

`apps.atlas` is added to `INSTALLED_APPS` after `apps.content`. `DEFAULT_AUTO_FIELD` is `BigAutoField`; no primary key is exposed publicly.

### 5.2 Method and Technology (first-class CMS entities)

Both models are identical in shape and are **not tags**. `Method` and `Technology` do not have public detail routes in v1; they are published entities that exist to be Atlas nodes (and future detail pages when the owner asks for them).

```python
class Method(LocalizedContentMixin, ContentPublicationMetadataMixin, LifecycleMixin):
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    # db_table = "content_method"; unique (locale, slug); ordering ["locale", "sort_order", "slug"]

class Technology(LocalizedContentMixin, ContentPublicationMetadataMixin, LifecycleMixin):
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    # db_table = "content_technology"; unique (locale, slug); ordering ["locale", "sort_order", "slug"]
```

Field roles:

| Requirement | Field |
|---|---|
| Stable identity | `translation_key` (from `ContentPublicationMetadataMixin`), unique per logical record across locales |
| Locale-aware content | `locale` + `slug` unique together; one row per locale, exactly like every other content entity |
| Name / title | `title` (from `LocalizedContentMixin`) |
| Short description | `short_description` |
| Longer description | `description` (plain text; sanitized rich text only if the owner later requests it) |
| Publish state | `status`, `published_at`, `scheduled_for` (from `LifecycleMixin`) + `objects.public()` |
| Sort order | `sort_order` |
| Timestamps | `created_at`, `updated_at` (from `LifecycleMixin`) |

Deliberately **not modeled in v1**: vendor, category, logo/icon, external identifier, external documentation URL, maturity, version. None is required by a specified behaviour. Adding any of them later is an additive migration driven by a named product need.

Admin exposure uses the existing generic content machinery: `method` and `technology` become registered entities in the generic content API/editor, with the same lifecycle, revision, preview and publication behaviour as `research-topic`.

### 5.3 Atlas models

All tables are declared explicitly (`db_table`) to match the `content_*` precedent style. All FKs use `on_delete=models.CASCADE` unless stated. Migrations are **additive** and never edit an existing migration file.

#### `AtlasNodeType` — `atlas_node_type` (admin-managed taxonomy)

| Field | Type | Rules |
|---|---|---|
| `key` | `SlugField(max_length=64, unique=True)` | Stable public type key; `[a-z0-9-]` only; **immutable once a node has used it** |
| `label_en`, `label_fa` | `CharField(max_length=120)` | Required; the canonical display copy for filters, inspector type line and legend |
| `description_en`, `description_fa` | `TextField(blank=True)` | Authoring/help copy |
| `semantic_role` | `CharField(choices=SEMANTIC_ROLES)` | One of `anchor`, `area`, `record`, `utility` — drives inspector grouping and defaults |
| `visual_role` | `CharField(choices=VISUAL_ROLES)` | One of `anchor`, `domain`, `record`, `fine` — maps to a material/presentation profile (§13.4) |
| `default_importance` | `PositiveSmallIntegerField(default=50)` | 0–100; copied into a node at creation, then editable per node |
| `allow_as_root` | `BooleanField(default=False)` | May appear without a hierarchy-role parent |
| `allow_children` | `BooleanField(default=True)` | May be the target of a hierarchy-role relation |
| `canonical_source` | `CharField(choices=CANONICAL_SOURCES, default="none")` | Which published model a node of this type must reference (`research_topic`, `project`, `publication`, `method`, `technology`, `profile`, `none`) |
| `filter_visible` | `BooleanField(default=True)` | Appears in the public filter control (§16.2) |
| `active` | `BooleanField(default=True)` | Inactive types are hidden from authoring pickers and blocked at publish |
| `sort_order` | `PositiveIntegerField(default=0)` | Deterministic ordering everywhere |

Constraints: deleting a type that is referenced by any node is **blocked**. Retirement is `active=False`.

#### `AtlasRelationType` — `atlas_relation_type` (admin-managed taxonomy)

| Field | Type | Rules |
|---|---|---|
| `key` | `SlugField(max_length=64, unique=True)` | Stable public relation key; immutable once used |
| `label_en`, `label_fa` | `CharField(max_length=120)` | Forward display copy ("uses") |
| `inverse_label_en`, `inverse_label_fa` | `CharField(max_length=120)` | Inverse reading ("used by") |
| `description_en`, `description_fa` | `TextField(blank=True)` | Authoring guidance: when to use this relation |
| `directed_default` | `BooleanField(default=True)` | Default for new relations; an edge may override only if the type allows it |
| `overridable_direction` | `BooleanField(default=False)` | Whether an individual relation may change `directed` |
| `semantic_role` | `CharField(choices=SEMANTIC_ROLES)` | Same vocabulary as node types: `area`, `record`, `utility` |
| `hierarchy_role` | `BooleanField(default=False)` | `True` = this relation participates in the hierarchy DAG (§5.6) |
| `default_weight` | `PositiveSmallIntegerField(default=1)` | 0–100; copied into a new relation |
| `visual_priority` | `PositiveSmallIntegerField(default=50)` | 0–100; selects the curve sample tier and emphasis order (§13.6) |
| `allowed_source_types` | `ManyToManyField(AtlasNodeType, related_name="+")` | Empty = any active type |
| `allowed_target_types` | `ManyToManyField(AtlasNodeType, related_name="+")` | Empty = any active type |
| `self_loop_policy` | `CharField(choices=SELF_LOOP_POLICY, default="forbid")` | `forbid` \| `allow` |
| `active` | `BooleanField(default=True)` | Inactive types cannot be used and block publish if referenced |
| `sort_order` | `PositiveIntegerField(default=0)` | Deterministic ordering |

Constraints: deleting an in-use relation type is **blocked**; retirement is `active=False`.

#### `AtlasVersion` — `atlas_version` (one topology, both locales)

| Field | Type | Rules |
|---|---|---|
| `status` | `CharField(choices=draft \| active \| archived)` | Exactly **one active version platform-wide** (no `locale` column) |
| `label` | `CharField(max_length=120, blank=True)` | Editor name ("2026 Q3") |
| `created_at` / `updated_at` | `DateTimeField` | `updated_at` drives the `If-Match` revision |
| `published_at` | `DateTimeField(null=True, blank=True)` | Set by activation |
| `created_from` | `FK(self, null=True, blank=True, SET_NULL)` | Clone provenance |
| `layout_revision` | `PositiveIntegerField(default=0)` | Increments on every layout recomputation |

Constraints: `UniqueConstraint(fields=["status"], condition=Q(status="active"), name="atlas_version_unique_active")`. Ordering `["-id"]`.

#### `AtlasNode` — `atlas_node` (locale-neutral)

| Field | Type | Rules |
|---|---|---|
| `version` | `FK(AtlasVersion, related_name="nodes")` | Same-version integrity enforced in `clean()` |
| `public_key` | `SlugField(max_length=80)` | Assigned at creation as `<node-type-key>-<8 lowercase hex>`; immutable thereafter; **unique per version** — *amended during Plan A execution (ruling R9, `plans/LEDGER-A-DOMAIN-API.md`): the earlier "unique globally (across versions)" wording is superseded, because the clone flow (§8.2 `Active vN ──clone──▶ Draft vN+1`) must carry a version's keys onto a coexisting draft or deep links would break on publish, and the execution rule "stable public keys must not silently mutate" requires exactly that. A key still never means two things inside the served topology, because exactly one version is active at a time.* |
| `node_type` | `FK(AtlasNodeType, PROTECT, related_name="nodes")` | Must be `active` to publish |
| `canonical_model` | `CharField(choices=CANONICAL_SOURCES)` | Copied from `node_type.canonical_source` at save; `none` allows an Atlas-only structural node |
| `canonical_translation_key` | `UUIDField(null=True, blank=True, db_index=True)` | Locale-neutral canonical reference (C6) |
| `importance` | `PositiveSmallIntegerField(default=50)` | 0–100 |
| `visible` | `BooleanField(default=True)` | Invisible nodes are not published **and** are not traversed by hierarchy validation |
| `mobile_overview_priority` | `CharField(choices=auto \| featured \| hidden, default="auto")` | The only compact/mobile-overview field. `auto` = the projection decides from importance and structure · `featured` = forced into the initial compact/mobile overview · `hidden` = excluded from the initial overview **only** — the node stays in the Atlas, in search, in the semantic index and in every focused neighbourhood |
| `pin_x`, `pin_y`, `pin_z` | `FloatField(null=True, blank=True)` | Optional layout pin override; `pin_x`/`pin_y` must both be present when either is set |
| `sort_order` | `PositiveIntegerField(default=0)` | Deterministic tie-breaking for layout and lists |

Constraints: `UniqueConstraint(fields=["version", "node_type", "canonical_translation_key"], condition=Q(canonical_translation_key__isnull=False))` (a canonical record appears at most once per version); unique `public_key` **per version** (`UniqueConstraint(["version", "public_key"])`) — *see the amendment on the `public_key` row above*; index `(version, visible)`, `(canonical_model, canonical_translation_key)`.

#### `AtlasNodeTranslation` — `atlas_node_translation` (per-locale overrides)

| Field | Type | Rules |
|---|---|---|
| `node` | `FK(AtlasNode, related_name="translations")` | |
| `locale` | `CharField(choices=Locale)` | fa \| en |
| `label_override` | `CharField(max_length=200, blank=True)` | Blank = use the canonical record's title for this locale |
| `summary_override` | `TextField(blank=True)` | Blank = use the canonical record's summary for this locale |
| `accessible_label_override` | `CharField(max_length=300, blank=True)` | Blank = the resolved label |
| `aliases` | `JSONField(default=list, blank=True)` | Optional search aliases/synonyms; list of non-empty strings, each ≤ 120 characters |

Constraint: unique `(node, locale)`.

#### `AtlasRelation` — `atlas_relation` (locale-neutral)

| Field | Type | Rules |
|---|---|---|
| `version` | `FK(AtlasVersion, related_name="relations")` | |
| `source` / `target` | `FK(AtlasNode, CASCADE, related_name="outgoing_relations" / "incoming_relations")` | Both must belong to `version` |
| `relation_type` | `FK(AtlasRelationType, PROTECT, related_name="relations")` | |
| `directed` | `BooleanField()` | Initialised from `relation_type.directed_default`; editable only when `overridable_direction` |
| `weight` | `PositiveSmallIntegerField(default=1)` | 0–100, initialised from `default_weight` |
| `visible` | `BooleanField(default=True)` | Invisible relations are not published |
| `sort_order` | `PositiveIntegerField(default=0)` | |

Constraints: unique `(version, source, target, relation_type)`; a self-loop is rejected unless `relation_type.self_loop_policy == "allow"`; an undirected relation must not duplicate an existing reversed pair (mirrors `GraphEdge.clean`).

The **public relation key is composed, never stored**: `key = f"{source.public_key}~{relation_type.key}~{target.public_key}"`, with source/target ordered by `public_key` (ascending) when `directed` is `False` so the identity does not depend on insertion order. Composed keys use `~` (an RFC 3986 unreserved character) so a key is URL-safe without percent-encoding; the legacy `->`/`:` composition of `GraphEdge` is not reused for that reason.

#### `AtlasRelationTranslation` — `atlas_relation_translation`

| Field | Type | Rules |
|---|---|---|
| `relation` | `FK(AtlasRelation, related_name="translations")` | |
| `locale` | `CharField(choices=Locale)` | |
| `explanation` | `TextField(blank=True)` | Optional localized explanation; blank = the relation type's `label_*` only |

Constraint: unique `(relation, locale)`.

#### `AtlasGroup`, `AtlasGroupTranslation`, `AtlasGroupMembership`

| Model / table | Fields |
|---|---|
| `AtlasGroup` / `atlas_group` | `version` FK; `public_key` (`group-<8 hex>`, immutable, **unique per version** per ruling R9); `sort_order`; `active` |
| `AtlasGroupTranslation` / `atlas_group_translation` | `group` FK; `locale`; `label` (required for both locales at publish); `description` (blank allowed); unique `(group, locale)` |
| `AtlasGroupMembership` / `atlas_group_membership` | `group` FK; `node` FK; `sort_order`; unique `(group, node)` |

Group membership is **not** a relation and never appears in the relation list, the relation inspector, the hierarchy DAG or the relationship counts. It influences layout, visual clustering and filtering only (§5.5).

### 5.4 Canonical-record reference pattern

A node never duplicates a CMS record. It references one logically, locale-neutrally:

```
AtlasNode { node_type → canonical_model, canonical_translation_key (UUID) }
```

Resolution for locale `L` (the single resolution rule used by validation, the public API and the admin preview):

1. Find the row of `canonical_model` whose `translation_key == canonical_translation_key` **and** `locale == L`, restricted to `objects.public()`.
2. If exactly one row resolves: its `title` is the node's label source, its summary-ish field (`summary`, `short_description`, `abstract` or `description`, in that precedence order, whichever the model defines) is the summary source, and its canonical route is derived from the existing route-family map.
3. If zero rows resolve and the corresponding `label_override` is non-blank: the override supplies the label, and the node publishes **without** a canonical link, with the inspector omitting the canonical-record line.
4. If zero rows resolve and no override exists: the locale projection is incomplete → publish-blocking issue `MISSING_LOCALE_PROJECTION` (§20).
5. If more than one row resolves, the payload is ambiguous → publish-blocking issue `AMBIGUOUS_CANONICAL_REF`.

`canonical_model = "none"` nodes (Atlas-only structural nodes) always require an override in both locales.

Validation requires `canonical_translation_key` to be set for every node whose type has a canonical source other than `none`, and requires the referenced record to be **publishable** (`objects.public()` resolves it) in both locales unless an override covers the missing locale.

### 5.5 Groups / clusters

- A node may belong to **multiple** groups; a group holds **many** nodes.
- Groups influence layout attraction (§12.4), visual clustering (only through layout and emphasis, never through invented edges) and the filter/context surface (§16.2).
- Group membership never creates, implies or renders a relationship. It is never counted in relation statistics and never appears in the relation inspector.
- Group copy is localized (`AtlasGroupTranslation.label`/`description`) and both locales are required at publish.
- Deleting an in-use group is an admin confirmation flow, not a silent cascade: removing a group never removes its nodes or relations.

### 5.6 Hierarchy representation

- Hierarchy exists **only** through relation types whose `hierarchy_role` is `True` (for example `specializes` / `parent-of`). There is no parent field on a node and no separate subnode entity.
- The subgraph of hierarchy-role relations restricted to `visible` nodes must be a **DAG** (no cycles). A cycle is a publish-blocking issue `HIERARCHY_CYCLE`.
- Multiple parents, orphan nodes, multiple relation types between the same pair and general graph cycles outside the hierarchy subgraph are all permitted.
- Layout derives a *placement* hint from the hierarchy (a depth for each node, §12.2). That hint is a presentation value; it must never be stored as, rendered as, or mistaken for a semantic parent. No relation row is created by layout.
- General (non-hierarchy) cycles are legal and are rendered as ordinary curved relations.

---

## 6. Node and relation taxonomy

### 6.1 Seeded node types (v1 defaults)

`key` is public and immutable after use. `canonical_source` binds each type to its CMS model.

| key | label_en | label_fa | semantic_role | visual_role | canonical_source | allow_as_root | allow_children | default_importance | filter_visible |
|---|---|---|---|---|---|---|---|---|---|
| `identity` | Identity | هویت | anchor | anchor | `profile` | yes | yes | 100 | no |
| `research-area` | Research area | دامنهٔ پژوهشی | area | domain | `research_topic` | yes | yes | 80 | yes |
| `project` | Project | پروژه | record | record | `project` | no | no | 60 | yes |
| `publication` | Publication | انتشار | record | record | `publication` | no | no | 60 | yes |
| `method` | Method | روش | utility | fine | `method` | no | no | 45 | yes |
| `technology` | Technology | فناوری | utility | fine | `technology` | no | no | 45 | yes |

`identity` exists because the published research identity is itself a node: it is the anchor the whole topology hangs from, it references the owner's canonical `Profile` record, and it keeps the About preview and the Atlas oriented around one centre. It is a system type: `filter_visible = False`, so it never appears as a filter chip, and its `semantic_role = anchor` excludes it from the "area/record/utility" inspector grouping.

`Experience` is **not** a primary Atlas type in v1 (§25).

### 6.2 Seeded relation types (v1 vocabulary)

| key | label_en / label_fa | inverse_en / inverse_fa | directed_default | hierarchy_role | visual_priority | self_loop | allowed source → target |
|---|---|---|---|---|---|---|---|
| `specializes` | specializes / تخصیص دارد به | generalizes / تعمیم می‌دهد | yes | **yes** | 90 | forbid | area → area |
| `related-to` | related to / مرتبط با | related to / مرتبط با | no | no | 40 | forbid | any → any |
| `uses` | uses / استفاده می‌کند از | used by / استفاده شده در | yes | no | 70 | forbid | project → method, project → technology, method → technology |
| `implements` | implements / پیاده‌سازی می‌کند | implemented by / پیاده‌سازی شده با | yes | no | 75 | forbid | project → method, project → technology, technology → method |
| `applies` | applies / به‌کار می‌گیرد | applied in / به‌کار رفته در | yes | no | 70 | forbid | project → research-area, publication → research-area |
| `produces` | produces / تولید می‌کند | produced by / تولید شده توسط | yes | no | 80 | forbid | project → publication, research-area → publication |
| `published-as` | published as / منتشر شده به‌صورت | publishes / منتشر می‌کند | yes | no | 80 | forbid | project → publication |
| `supports` | supports / پشتیبانی می‌کند | supported by / پشتیبانی شده توسط | yes | no | 60 | forbid | method → research-area, technology → research-area, method → project, technology → project |
| `informed-by` | informed by / برآمده از | informs / جهت می‌دهد به | yes | no | 50 | forbid | project → publication, research-area → publication, method → research-area |
| `evaluated-with` | evaluated with / ارزیابی شده با | evaluates / ارزیابی می‌کند | yes | no | 65 | forbid | project → method, publication → method, method → technology |
| `research-focus` | research focus / تمرکز پژوهشی | research focus of / تمرکز پژوهشی برای | yes | no | 95 | forbid | identity → research-area |

`research-focus` is seeded **only** to carry the three relations of the current published Research Universe into the Atlas with their existing meaning and their existing English display copy (`research focus`), so migration produces no semantic change (§23.3). It is a normal admin-manageable relation type; if the owner later retires it, the three relations are retargeted deliberately rather than silently mapped.

Rules:

- The vocabulary is **data**, not code. No frontend module may enumerate relation keys, and no frontend branch may key off a relation key. Display copy always comes from the payload's `relationTypes` catalog.
- `allowed_source_types` / `allowed_target_types` empty means "any active type"; a non-empty pair is enforced at validation (`RELATION_TYPE_NOT_ALLOWED`).
- An inactive relation type blocks publication of any version that references it (`RELATION_TYPE_INACTIVE`).
- `identity` is not listed as an allowed source anywhere except `research-focus`; authoring an identity→X relation of another type is rejected by the allowed-pair validation until the owner widens it in admin.
- `mutual`/undirected relations are expressed by `directed=false`; the inverse label is still used when the inspector renders the relation from the target side.

---

## 7. Multilingual topology

1. **One topology.** `AtlasVersion` has no locale. Node, relation and group identities and counts are identical in EN and FA.
2. **Stable identities.** `public_key`, relation keys and group keys are language-neutral, URL-safe (`[a-z0-9._~-]`), unique **within their version** (ruling R9 — a clone carries them unchanged so a publish never re-keys the site), and immutable after publish. Equal or similar copy never proves or creates identity; identity comes from `translation_key` and the stored keys.
3. **Localized surfaces.** Exactly these are localized: node label/summary/accessible label, node aliases, relation display copy (type label or inverse label) and per-relation explanation, group label/description, and every canonical `href` (`/en/…` vs `/fa/…`).
4. **Resolution.** The locale projection is built by the rule in §5.4, per node, per locale.
5. **Publish gate.** Publication is **blocked** unless every `visible` node and every `visible` relation resolves in **both** EN and FA: labels present (from override or canonical record), groups fully localized, and canonical links resolvable where a canonical record exists. The gate is enforced in the same transaction as activation (§8.3).
6. **No drift.** No code path may write a version-scoped row with a locale, and no API may serve a locale-specific topology. A projection is computed, never stored as a separate graph.
7. **Translation worklist.** The admin exposes a per-version translation coverage view: every node and relation with its EN and FA resolution status and the field that is missing. This is the authoring workflow for the gate in (5).
8. **Fallback is forbidden.** A missing FA projection never falls back to the EN copy, and vice versa. The honest outcomes are the override, the canonical row for that exact locale, or a blocking validation issue.

---

## 8. Versioning and publishing

### 8.1 Statuses and lifecycle

`draft` → `active` → `archived`, with exactly one `active` version platform-wide.

```
Active vN ──clone──▶ Draft vN+1 ──edit──▶ Validate ──▶ Preview EN/FA ──▶ Publish (atomic)
                                                                          │
                                          Active vN becomes Archived ◀────┘   Draft vN+1 becomes Active
```

- Cloning copies nodes, relations, translations, group memberships and layout pins into a new draft. `public_key`s are **copied**, because they identify the same entity across versions.
- Editing an `active` version is refused (`409 IMMUTABLE_ACTIVE`), mirroring `apps/api/admin_graph.py`.
- A draft may be incomplete; validation is a gate on activation, not on editing.
- Archiving keeps the row and its history. Archived versions are never served publicly.
- **No scheduled publishing in v1** (§25).

### 8.2 Admin lifecycle endpoints

| Method | Path | Behaviour |
|---|---|---|
| GET | `/api/v1/admin/atlas/versions` | List `{id, label, status, nodeCount, relationCount, publishedAt, updatedAt}` |
| POST | `/api/v1/admin/atlas/versions` | Create empty draft `{label}` |
| GET | `/api/v1/admin/atlas/versions/{id}` | Full draft/active detail with counts and revision |
| POST | `/api/v1/admin/atlas/versions/{id}/clone` | Clone into a new draft; returns the new id |
| GET | `/api/v1/admin/atlas/versions/{id}/validate` | Validation report `{blocking:[…], warnings:[…]}` (no mutation) |
| POST | `/api/v1/admin/atlas/versions/{id}/activate` | Publish (see §8.3) |
| POST | `/api/v1/admin/atlas/versions/{id}/layout` | Recompute layout (pins preserved); increments `layout_revision` |
| PUT | `/api/v1/admin/atlas/versions/{id}/graph` | Transactional bulk replace of nodes+relations+groups for the 2D editor |
| GET/POST/PATCH/DELETE | `/api/v1/admin/atlas/versions/{id}/nodes[/{key}]` | Node CRUD |
| GET/POST/PATCH/DELETE | `/api/v1/admin/atlas/versions/{id}/relations[/{key}]` | Relation CRUD by composed key |
| GET/POST/PATCH/DELETE | `/api/v1/admin/atlas/versions/{id}/groups[/{key}]`, `/groups/{key}/members` | Group CRUD + membership |
| GET/POST/PATCH/DELETE | `/api/v1/admin/atlas/node-types[/{key}]`, `/relation-types[/{key}]` | Taxonomy CRUD; delete blocked while referenced |
| GET/PATCH | `/api/v1/admin/atlas/versions/{id}/translations` | Coverage worklist + override writes |

Precondition and concurrency semantics follow the established graph admin API exactly: `If-Match: <updatedAt ISO>` is required on every mutation (`428 PRECONDITION_REQUIRED` when absent), a stale value returns `409 STALE_REVISION`, activation of an already-active version returns `409 ALREADY_ACTIVE`, and validation failure returns `409 VALIDATION_BLOCKED` with an issues array. Every mutation writes an audit entry (`atlas.*`) through the existing audit middleware.

### 8.3 Publish is transactional

Activation runs in one `transaction.atomic` block:

1. Re-run the full validator (`apps/atlas/validation.py`) against the draft. Any blocking issue aborts with `409 VALIDATION_BLOCKED` and a stable issue array; nothing is written.
2. Confirm that layout coordinates exist for every visible node (`MISSING_LAYOUT` otherwise).
3. Re-verify the locale gate for both EN and FA against `objects.public()` **inside the transaction**, so a record unpublished a second earlier cannot slip through.
4. Set the current active version to `archived`, set the draft to `active` and stamp `published_at`.
5. Enqueue one publication job through the existing I06 integration with the affected paths `/{locale}/atlas/` and `/{locale}/about/` for both locales, so the next build carries the new snapshot. The job is the rebuild signal, not the publish mechanism.

A failure at any step leaves the previously active version serving. There is no partially published state, and no scheduled activation.

### 8.4 Publishing does not require a frontend deploy

The runtime endpoint (§10) reads the active version through the database at request time. Activation therefore becomes visible to browsers within the freshness window (§11) without any build, deploy or cache purge. The build-time snapshot is refreshed by the ordinary rebuild path (step 5 above) and is a *freshness improvement*, never a correctness requirement.

---

## 9. Admin authoring UX

Admin is the primary authoring surface. The Atlas is authored in `Front-End/admin-panel` (React 19 SPA) against the endpoints in §8.2, using the established admin patterns (generic entity editing, `If-Match` saves, validation issue rendering, audit trail).

### 9.1 Surfaces

| Surface | Purpose |
|---|---|
| Atlas Versions | List, create, clone, open, validate, preview, publish, archive |
| Nodes | Table + detail form per node: type, canonical record picker, importance, visibility, mobile overview role, overrides, aliases, pins |
| Relations | Table + structured form (§9.3) |
| Node Types | CRUD over the taxonomy; key immutable once used; retire via `active` |
| Relation Types | CRUD over the taxonomy, including allowed source/target types, hierarchy role, self-loop policy, labels and inverse labels |
| Groups | CRUD + membership manager with localized labels/descriptions |
| Layout | Recompute, inspect coordinates, drag to pin, clear pins |
| Translations | Per-locale coverage worklist with the missing-field reason per row |
| Validate | The validation report for the open version: blocking issues with entity links, warnings with counts |
| Preview | 2D authoring preview and 3D final preview (§9.5) |
| Publish | Activation with the parity gate result shown before the action |

### 9.2 2D graph editor (v1)

- Renders the published layout coordinates on a canvas/SVG plane with labels; the same coordinates the public 3D view uses.
- **Select** a node → highlight its incident relations and dim the rest.
- **Inspect** a relation by selecting it in the graph or in the table; the inspector shows source, type, target, direction, weight, explanation, visibility.
- **Drag a node** → writes `pin_x`/`pin_y` only. Dragging never changes hierarchy, never creates a relation and never changes a relation's endpoints.
- The editor shows hierarchy-role relations with a distinct stroke style and flags any cycle attempt inline before the save reaches the validator.
- Free pan/zoom of the authoring plane is local view state and is not persisted.

### 9.3 Structured relation form

`Source` (node picker, filtered by `allowed_source_types`) · `Relation Type` (picker) · `Target` (picker, filtered by `allowed_target_types`) · `Directed` (only when `relation_type.overridable_direction`) · `Weight` (0–100) · `Explanation` (localized, optional) · `Visibility`. Saving performs the same validation as the bulk graph PUT and returns issues inline.

### 9.4 Relation table

Columns: source label, relation type, target label, directed, weight, visible, hierarchy, updated. Operations: filter (by type, source type, target type, visibility, hierarchy), edit, delete (with confirmation), inspect (opens the inspector). Bulk delete is transactional and re-runs validation on the resulting graph.

### 9.5 Preview modes

1. **2D authoring preview** — the editor itself (§9.2), optimized for editing.
2. **3D final preview** — the real 3D presentation on the real payload, opened in a scoped preview surface. It is the validation/review step before Publish, not the primary editing surface, and it must not become the editing canvas. It is driven by the short-lived, read-only, locale-scoped draft capability of §10.10 — the token never appears in a request URL, and this surface can neither activate nor mutate a version.

### 9.6 Authoring constraints stated in the UI

The admin must state, where the author is about to violate them: node type keys are immutable; a canonical record appears at most once per version; both locales must resolve before publish; hierarchy relations must stay acyclic; pins are presentation only and never semantics; groups are not relations. Drag-to-connect is not part of v1 (§25).

---

## 10. Public API contract

### 10.1 Endpoint

```
GET /api/atlas/{locale}            locale ∈ {fa, en}
```

- Public, unauthenticated, same-origin (C11), read-only.
- Serves the **active** version only. If no version is active, `404` with the normalized error envelope (`PRODUCT-INTERFACES-V2 §I08`). Drafts are never exposed, not even partially: a draft's nodes, relations, groups and coordinates are unreachable from this route.
- Never returns a payload from the other locale, and never falls back between locales.

### 10.2 Response shape

```json
{
  "contractVersion": "atlas01-1.0.0",
  "locale": "en",
  "version": {
    "id": 12,
    "revision": "12-2026-09-20T10:31:04.221000+00:00",
    "publishedAt": "2026-09-20T10:31:04.221000+00:00",
    "nodeCount": 62,
    "relationCount": 118,
    "layoutRevision": 7
  },
  "nodeTypes": [
    { "key": "research-area", "label": "Research area", "semanticRole": "area",
      "visualRole": "domain", "allowAsRoot": true, "allowChildren": true, "filterVisible": true }
  ],
  "relationTypes": [
    { "key": "uses", "label": "uses", "inverseLabel": "used by", "directed": true,
      "hierarchyRole": false, "visualPriority": 70 }
  ],
  "groups": [
    { "key": "group-4f1a2b3c", "label": "Vision & language", "description": "", "nodeKeys": ["research-area-1a2b3c4d"] }
  ],
  "nodes": [
    { "key": "research-area-1a2b3c4d", "type": "research-area", "label": "PARS-SQL / VTD-Edge",
      "summary": "…", "accessibleLabel": "…", "importance": 80, "mobileOverviewPriority": "featured",
      "aliases": ["Persian text-to-SQL"],
      "canonical": { "family": "researchtopic", "id": "1", "slug": "pars-sql-vtd-edge",
                     "title": "PARS-SQL / VTD-Edge", "routeFamily": "research",
                     "href": "/en/research/pars-sql-vtd-edge/" },
      "position": { "x": 41.882, "y": 12.021, "z": 6.5 } }
  ],
  "relations": [
    { "key": "identity-2b3c4d5e~research-focus~research-area-1a2b3c4d", "type": "research-focus",
      "source": "identity-2b3c4d5e", "target": "research-area-1a2b3c4d",
      "directed": true, "weight": 1, "hierarchy": false,
      "inverseLabel": "research focus of", "explanation": null }
  ]
}
```

### 10.3 Field rules

| Rule | Detail |
|---|---|
| Naming | camelCase at the API layer, snake_case in storage (existing convention) — the compact-overview field is `mobile_overview_priority` in the model and `mobileOverviewPriority` on the wire, and those are the only two spellings that exist anywhere |
| Omission | `null`/empty optional fields are omitted (`exclude_none=True`), never sent as empty strings |
| Ordering | `nodes` ordered by `(-importance, public_key)`; `relations` by `visual_priority DESC, key`; `groups` by `sort_order, key`; catalogs by `sort_order, key`. Deterministic and locale-independent |
| Identity | `key` values are the stable public keys of §5.3; relation `key` is composed exactly as specified there |
| Coordinates | `position.x/y/z` are the published layout values, rounded to 3 decimals, in scene units; every visible node has one |
| Canonical | `canonical` is present only when a canonical record resolved for this locale; `href` is the exact-locale site-relative path derived from the existing route-family map (`ROUTE_FAMILY_MAP` in `apps/api/record_resolver.py`) |
| Directions | `directed`, `hierarchy` and `inverseLabel` are per relation; `hierarchy` is derived from the relation type, never authored per relation |
| Mobile | `mobile` ∈ `auto` \| `featured` \| `hidden` |
| Weight | `weight` is an integer 0–100 |
| Visibility | Only `visible` nodes and relations are served |

### 10.4 Sizes and budgets

| Budget | Ceiling |
|---|---|
| Nodes served | 80 (`100` triggers the scale warning of §12.7) |
| Relations served | 150 (`250` triggers the scale warning) |
| Runtime payload | ≤ 60 KB gzip |
| Build-time embedded snapshot | ≤ 40 KB gzip, inline in the document (no extra request) |

The v1 target scale of 40–80 nodes and 60–150 relations is expected to produce roughly 20–40 KB gzip; the ceilings exist so a future graph growth is caught by measurement rather than by a user noticing.

### 10.5 Caching and conditional requests

- Every `200` carries `ETag: "<version.id>-<16 hex of a SHA-256 over the canonical JSON of this locale projection>"` and `Cache-Control: public, max-age=60`.
- `If-None-Match` with a matching ETag returns `304 Not Modified` with no body and the same `ETag`/`Cache-Control` headers. The `304` path must not query nodes, relations or canonical records: it is the cheap validity check behind §11.2.
- The ETag changes when the active version, the locale projection or the canonical resolution behind any node changes. Two consecutive requests over an unchanged active version must return the identical ETag — this is asserted by a backend test.
- Responses are never cached longer than 60 seconds, and the design tolerates a CDN layer behaving exactly as observed today on the sibling graph endpoint (`cf-cache-status: DYNAMIC`).

### 10.6 Error behaviour

| Condition | Response |
|---|---|
| Unknown locale | `404` envelope, `code: "atlas_not_found"` |
| No active version | `404` envelope, `code: "atlas_not_found"` |
| Active version exists but is internally invalid (a condition that validation should have prevented) | `500` envelope with a safe code, no partial payload; the runtime keeps its embedded snapshot (§11.3) |
| Unsupported method | `405` by the router |

No endpoint returns draft data, counts, or ids of unpublished entities under any error path.

### 10.7 No server-side search or neighbourhood endpoints in v1

The payload is small enough that search, filtering, neighbourhood computation and layout projection are client-side pure functions (§16). No Atlas search endpoint, no pagination and no per-node fetch exist in v1; this keeps the runtime path to exactly one request-with-conditional-revalidation.

### 10.8 Backward compatibility

`GET /api/graph/{locale}` and the whole existing graph admin surface stay exactly as they are for the duration of this program. The Atlas endpoint is additive, and the existing OpenAPI paths, schemas and pins keep their current meaning until a deliberate retirement card removes them.

### 10.9 Contract synchronization

The endpoint is added to `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` (a new `I09 — Atlas` section) by the backend implementation phase, the OpenAPI snapshot is exported, and the frontend regenerates `src/generated/public-api.ts` through the existing synchronization step (`npm run generate:api-types`) and re-pins `src/generated/openapi-hash.json` plus `contracts/openapi.public.sha256`. The TypeScript type of the payload comes from the generated snapshot; no hand-written duplicate of the wire shape is permitted in the frontend.

### 10.10 Draft preview transport

Publishing cannot be rehearsed on published data, so a draft version must be reviewable through the *same* presentation before activation — without ever exposing draft content on a durable, shareable, loggable URL.

**Capability mint (admin, authenticated).**

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/v1/admin/atlas/versions/{version_id}/preview-token` | Mint one short-lived read-only draft-preview capability for one version and one locale |

Request body: `{"locale": "en" | "fa"}`. Response: `{"preview_url": "/<locale>/atlas/preview/#token=<token>", "expires_at": "…", "version_id": "…"}`. The action follows the established admin conventions (staff session + CSRF + OTP, shared `If-Match` gate, audit entry) and mints only for a **non-active** version.

**The token is never carried in a request URL.** It travels in the URL **fragment** (`#token=…`), which browsers do not send to a server, do not include in `Referer`, and do not write to access logs. The preview page is therefore a static shell:

| Route | Presentation | Data |
|---|---|---|
| `/en/atlas/preview/`, `/fa/atlas/preview/` | The real Atlas presentation — 3D on desktop, 2D on compact or WebGL-less | The draft projection from §10.10.1 when a valid token is present; otherwise the ordinary active framing, honestly labelled |

Rules:

- The token is **read-only**, scoped to exactly one `AtlasVersion` **and** one locale, purpose-bound (`atlas-preview`), and short-lived (**TTL = 10 minutes**). It can never activate, publish, archive or otherwise mutate anything.
- Client behaviour, in order: read the token from `location.hash` → hold it **in memory only** → strip it with `history.replaceState()` **before** any fetch → call §10.10.1 with the token in an `Authorization` header → render. The token is never written to `localStorage`, `sessionStorage`, cookies, IndexedDB or any beacon/telemetry surface.
- An absent, malformed, expired, wrong-locale or wrong-version token produces the ordinary active view with no draft data and no draft-derived UI — never an error page that confirms a draft exists.
- The preview routes are `noindex, nofollow`, absent from the sitemap and from the route registry's indexable set, and never canonicalised (§4.4).

#### 10.10.1 Preview payload endpoint

```
GET /api/atlas/preview?locale=<en|fa>          Authorization: Bearer <preview-token>
```

- The **token** travels only in the `Authorization` header. The `locale` selector stays in the query string because it is not a secret and the response must be an exact-locale projection; it must equal the token's scope (a mismatch is `403`), and it is never inferred silently from the token.
- Documented ruling: the repository's existing share preview carries its token in a **path** (`/preview/share/<token>/`), which this design deliberately rejects for the Atlas — a credential in a path or query reaches access logs, analytics, `Referer` and browser history. There is no pre-existing `Authorization` convention for public API reads, so this endpoint establishes `Authorization: Bearer <token>`, and the contract and its test name that scheme explicitly. If the repository later adopts a different header convention, this is the one place that changes.
- Validation, in order: credential present → signature/opaque token valid and unforgeable → not expired → `purpose == "atlas-preview"` → `locale` matches the token's scope → the referenced version exists (a **draft** is the normal case) → read-only. Failures follow the existing API error conventions: `401` when the credential is absent or unparseable, `403` when it parses but is expired, wrong-purpose, wrong-locale or otherwise out of scope. A bad credential never produces `404`, because a probe must not learn whether a draft exists.
- The response is the §10.2 payload for the referenced version and locale, with `Cache-Control: no-store`, `Pragma: no-cache`, `X-Robots-Tag: noindex, nofollow` and `Referrer-Policy: no-referrer`.
- The signing/verification secret is **backend-only**, managed exactly like the existing backend secrets (`PREVIEW_SHARE_SECRET`, falling back to `SECRET_KEY`). No frontend bundle, build-time variable or client module ever receives a preview signing secret; no general-purpose share secret is exposed to frontend code.
- The endpoint never mutates, never activates, and is the only place draft data is ever served — `GET /api/atlas/{locale}` remains permanently draft-free.
- Ownership: **Plan A** owns the validation, the signing/verification primitive and this payload endpoint; **Plan B** owns the authenticated mint action; **Plan C** owns the static preview shell, the fragment consumption/removal and the `Authorization` fetch.

---

## 11. Hybrid freshness model

### 11.1 Build-time snapshot

At `astro build`, the Atlas route fetches `GET /api/atlas/{locale}` through the existing `PUBLIC_API_BASE_URL` seam and embeds the validated projection:

- The **semantic HTML index** is rendered from the snapshot (nodes, relations, groups, canonical links) so no-JS and crawler behaviour never depends on the runtime.
- The **payload** is embedded once as `<script type="application/json" data-atlas-payload>` with `<` escaped, exactly like the current `data-universe-payload` handoff.
- The **revision and ETag** are rendered onto the region element as `data-atlas-revision` and `data-atlas-etag` (both server-rendered facts, present with or without JavaScript) so the runtime revalidation in §11.2 needs no parse of the payload before deciding to call.
- If the fetch fails or returns `404`, the page renders its honest content states (§21) and still embeds nothing. A build never blocks on the Atlas.

### 11.2 Runtime revalidation

On page load, after the DOM is interactive and before any graphics work:

1. Read the embedded snapshot's `version.revision` and the region's `data-atlas-revision`.
2. Issue `GET /api/atlas/{locale}` with `If-None-Match: <embedded etag>` (the etag is embedded alongside the snapshot).
3. **`304`** → keep the embedded snapshot, do nothing. This is the expected steady-state path.
4. **`200`** with a newer `version.revision` → validate the new payload (§11.4); on success, adopt it as the active topology and re-render. Selection is preserved when the selected key still exists in the new payload; when it does not, the selection is cleared and a short non-blocking notice is shown in the inspector ("this entity is no longer published").
5. **`200`** with the same or an older `version.revision` than the embedded snapshot → keep the embedded snapshot. Version order is compared by `(publishedAt, id)`, never by a client clock.
6. **Any failure** (`404`, `5xx`, network error, abort) → keep the embedded snapshot silently. A failed refresh is never surfaced as an error state to the reader.

The revalidation request carries no credentials, no query parameters and no reader identifier. It is one request per page load, and it is aborted if the reader leaves.

### 11.3 Freshness contract

| Property | Value |
|---|---|
| First paint | Complete from the embedded snapshot; no network dependency, no layout shift when a refresh lands |
| Staleness window | ≤ 60 seconds of CDN/browser cache, plus one page load: a newly activated version is visible to a returning reader at the next page load, and to an open page at its next revalidation |
| Publishing without deploy | Required and satisfied by §8.4; the rebuild job only refreshes the embedded snapshot |
| Draft isolation | Drafts are unreachable from the public route (never enabled by the freshness path) |
| Failure bias | Always keep the snapshot; never clear the graph, never show an error for a refresh failure |

### 11.4 Payload validation and contract evolution

The runtime validator is pure, total and non-destructive, and its contract is:

- `contractVersion` must equal the client's supported version. A payload with an **unknown** `contractVersion` is **ignored**, and the embedded snapshot stays (forward compatibility: an older client must never crash on a newer payload).
- Required structure per node and relation is checked (keys non-empty and unique, types present in the catalogs, relation endpoints resolvable, coordinates finite, groups referencing existing nodes).
- The validator **validates, never reshapes**: it returns the payload unchanged on success. Any reshaping is a defect that hides a contract mismatch behind a silently reduced graph.
- On rejection, the embedded snapshot stays and the failure reason is written to the region as `data-atlas-refresh="rejected:<code>"` for diagnosis; no reader-visible error appears.

---

## 12. Layout model

### 12.1 Principles

- Layout is **deterministic**: identical input produces byte-identical coordinates, in every environment, on every run. No randomness, no clock, no viewport input, no physics that depends on frame timing.
- Layout is computed **once per version revision and stored**, then served. There is **one layout authority**; the 3D scene, the 2D projection, the About preview and the admin editor all consume the same stored coordinates. A presentation may transform (project, scale, crop) them; it must never re-simulate them.
- Layout may read hierarchy, groups, importance and pins. Layout must never write semantics: no relation is created, removed, redirected or retyped by layout, and a derived depth is never stored as a parent.
- No permanent browser physics, no idle simulation, no fully manual layout as the primary method.

### 12.2 Pipeline (executed in the backend at validation/activation time and on demand from the admin)

1. **Hierarchy depth.** Build the subgraph of `hierarchy_role` relations over `visible` nodes (already proven acyclic by validation). Assign each node `depth = longest path length from any root`, computed by a deterministic Kahn-style pass over nodes sorted by `public_key`; nodes unreachable from a root get `depth = 0` plus a placement ring slot (§12.7 warning `ISOLATED_NODE`).
2. **Importance radius.** `radius(node) = r_min + (r_max - r_min) * (importance / 100)`, with `r_min = 6` and `r_max = 18` scene units. The `identity` anchor's radius is `1.45×` the maximum domain radius, preserving the ratio the current scene already asserts.
3. **Seed placement.** Roots are seeded on a deterministic golden-angle spiral in the `y = 0` plane: `theta_k = k * 2.399963…`, `s_k = sqrt(k)` for `k = index + 1` in `public_key` order; non-root nodes are seeded at their parent's position offset by the same spiral at a smaller radius. This produces a stable, non-overlapping, non-radially-symmetric seed.
4. **Group attraction.** For each node, add a force toward the centroid of the groups it belongs to (a node in no group is unaffected). The attraction is a fixed fraction of the inter-node spacing, and the centroid is computed from the **seed** positions of that group's members in `public_key` order, so the force itself is a pure function.
5. **Importance-aware collision relaxation.** Run a fixed `N = 120` iterations of a positional relaxation over nodes taken in `public_key` order: for each pair closer than `radius(a) + radius(b) + gap`, push both apart along the connecting axis by half the overlap, damped by `0.5` per iteration. Bound every step so a single iteration cannot move a node more than `1` scene unit. Fixed iteration count, fixed order, fixed damping — no convergence test that depends on floating-point timing.
6. **Depth and depth-layering.** Spread depth layers along `z` by `dz = spread * (depth / max(1, max_depth))`, so hierarchy is legible in 3D without becoming a flat tree. `z` is otherwise authored by this rule only.
7. **Pins.** Overwrite `x`/`y` (and `z` when `pin_z` is set) for every node with pins, **after** relaxation, and never move a pinned node again. Pins are authoritative presentation decisions.
8. **Final collision pass.** One more relaxation pass restricted to unpinned nodes, so a pin cannot leave an unpinned neighbour overlapping it.
9. **Rounding and storage.** Round every coordinate to 3 decimals and store the resulting layout on the version (`layout_revision += 1`).

### 12.3 Determinism rules (binding)

- Iterate every collection in `public_key`/`sort_order` order; never rely on set or dict iteration order.
- No `random`, no `time`, no `hash()` of objects, no locale-dependent string collation.
- All arithmetic is IEEE-754 double; rounding happens once, at step 9.
- A unit test recomputes the layout for a fixed fixture twice and asserts identical coordinates, and asserts that recomputing a version's layout with unchanged input produces zero coordinate changes.

### 12.4 Group attraction limits

Group attraction must not be strong enough to move a node across the hierarchy structure: the maximum displacement attributable to group attraction is bounded at one half of the mean inter-root spacing, and a node in two groups is attracted to the midpoint of the two centroids rather than pulled to one group arbitrarily. Groups influence placement; they never become relations (§5.5).

### 12.5 Pinned coordinates are validated

`pin_x`/`pin_y` must both be present when either is set (`INVALID_PIN`), must be finite numbers within the scene bounds, and must not place two pinned nodes closer than the sum of their radii (`OVERLAPPING_PINS`, a warning in §20 unless the nodes are in the same group).

### 12.6 Relationship curves

Relations are drawn as bowed cubics between node surfaces, reusing the existing endpoint-driven curve construction (`buildEdgeCurve`, `EDGE_SAMPLES = 26`, bow `0.11` baseline). Atlas adds a per-relation sampling tier from `relation_type.visual_priority` (§13.6). Curve bows are a pure function of endpoint positions and the relation key, so they are reproducible and stable across reloads.

### 12.7 Scale warnings

| Condition | Severity |
|---|---|
| > 100 visible nodes | Warning `SCALE_NODES` |
| > 250 visible relations | Warning `SCALE_RELATIONS` |
| > 12 relations on one node | Warning `HIGH_DEGREE_HUB` |
| Node with no relations and no group | Warning `ISOLATED_NODE` |

Warnings never block publication. They are not hard product limits; a limit is introduced only if a benchmark proves the presentation cannot hold the scale (§19.6).

### 12.8 Projections, not re-layouts

| Presentation | Derivation |
|---|---|
| Desktop 3D | Stored coordinates, unscaled scene units |
| Mobile 2D SVG | Stored `x`/`y` (depth `z` folded into radius and draw order), mapped through one affine transform into the SVG `viewBox` |
| About preview | Stored coordinates of a deterministic subset (§15.2), mapped through one affine transform |
| Admin 2D editor | Stored coordinates, editor-owned viewport |

Every projection is a pure function of the stored layout plus the viewport box. No projection may run relaxation, sampling of random values, or gravity.

---

## 13. Desktop 3D presentation

### 13.1 Reuse, by name

The Atlas desktop presentation **reuses the current Research Universe renderer lineage**:

| Module | Reuse |
|---|---|
| `src/lib/visual/research-universe/scene-core.ts` | renderer, camera, lights, coalesced `requestRender`, `setVisible`, DPR clamp, ledger, context-loss reporting |
| `src/lib/visual/research-universe/dispose.ts` | disposal ledger |
| `src/lib/visual/research-universe/spheres.ts` | shared sphere geometries (extended to two tiers, §13.7) |
| `src/lib/visual/research-universe/materials.ts`, `presentation-profiles.ts`, `theme.ts` | token-resolved material registry, per-type profiles, per-theme render parameters |
| `src/lib/visual/research-universe/nodes.ts`, `edges.ts`, `core-object.ts` | instanced node batches, vertex-coloured edge lines, dedicated anchor mesh |
| `src/lib/visual/research-universe/labels.ts`, `leaders.ts` | projected chip/editorial labels with leader stems and collision handling |
| `src/lib/visual/research-universe/hit-testing.ts` | screen-space picking with slop radii |
| `src/lib/visual/research-universe/enhancement.ts` | the progressive-enhancement orchestration pattern (single-flight, one canvas, fallback on every failure) |

Atlas-specific modules are new files under `src/lib/visual/atlas/` and `src/lib/atlas/`; the reused modules are imported, not copied. Relocating the now-shared primitives into a neutral `src/lib/visual/core/` is a **separate, later** step performed only after the Retire phase (§23.6) and only under its own card.

The legacy engine (`graph-scene.ts`, `graph-controller.ts`, `graph-layout.ts`, `graph-motion.ts`, `hero-enhancement.ts`) is **never** imported, extended or revived by Atlas code.

### 13.2 Lifetime and budget invariants (inherited, non-negotiable)

- One canvas per route; the Atlas enhancement refuses to run when a second region exists or when the route is not the Atlas route.
- Lazy dynamic import of the scene modules; nothing three.js-related is in the document's critical path.
- Render-on-demand: a coalesced single frame per state change; **zero idle RAF**. Entering, hovering and leaving must not start a loop.
- `IntersectionObserver` pause when the stage is offscreen; `pagehide` disposal; ledger-complete disposal on teardown.
- Context loss → hide the canvas, keep every semantic control, write the reason into the DOM.
- DPR ceilings 1.5 (desktop) / 1.0 (mobile-critical widths) and the 1,500,000-pixel drawing-buffer ceiling remain in force.

### 13.3 States

| State | Entered by | Emphasis | Camera |
|---|---|---|---|
| `OVERVIEW` | initial load, `Escape` from `NODE FOCUS`/`RELATION FOCUS` with nothing selected, `Reset` | Structural nodes prominent, peripheral nodes quiet; all topology present | Published composition framing |
| `NODE FOCUS` | selecting a node (canvas, semantic control, search result, deep link) | Selected node emphasised; its one-hop neighbourhood (direct parents, children and relations) emphasised at full strength; everything else dimmed but present | Mild reframe (§13.5) |
| `RELATION FOCUS` | selecting a relation (canvas, relation control, search result, deep link) | Both endpoints and the relation emphasised; the rest dimmed | Mild reframe toward the relation midpoint |

Selection never removes data. No node or relation is added or deleted to express a state; `data-atlas-state` on the region publishes the current state for CSS and tests.

### 13.4 Visual mapping

- `node_type.visual_role` selects the presentation profile; `importance` selects radius, initial label tier and emphasis order.
- Materials, palette and lighting come from the existing token-driven registry; the Atlas introduces no new colours and no new material language. The restrained champagne role stays structural, and the teal/cyan brand and accent roles keep their existing meanings.
- No neon glow, no rim-glow rig, no orbital rings, no planetary language, no volumetric mist, no animated particle field.
- Edge colour/opacity/emphasis follow the existing edge implementation and the per-theme parameters in `theme.ts`.

### 13.5 Camera

- Overview framing fits the composition bounds with the existing `fitDistance` padding rule, computed against the **effective viewport** (§17.2) so the inspector never covers the graph.
- **Selection causes a mild reframe only**: a bounded yaw/pitch adjustment toward the node and a distance change no greater than 15 % of the current distance, animated within the existing 380–420 ms transition budget, instantly when motion is reduced.
- **Full focus** (bring the node to frame centre, tighten distance up to the existing `minDistanceScale`) is entered only by double-click on a node, the explicit `Focus` button, or a node deep link.
- Orbit (drag), zoom (wheel / buttons, hard-clamped by `ABOUT_ORBIT_LIMITS`-equivalent bounds), `Reset view`, `Clear selection` and `Escape` all remain available and keyboard-reachable through real buttons.
- Hover is enhancement only: no critical content depends on hover.

### 13.6 Labels and edges at scale

| Tier | Condition | Behaviour |
|---|---|---|
| Always-on | `importance ≥ 80` (structural), capped at 10 chips, or the selected/hovered node and its one-hop neighbours | Rendered with the existing chip/leader implementation, collision-aware |
| On demand | 40 ≤ `importance < 80` | Label appears while the node is hovered, selected, or inside a focused neighbourhood |
| Hidden until selected | `importance < 40` | Label appears only when the node is selected |

Edge sampling tiers from `relation_type.visual_priority`: `≥ 80` → 26 samples (current fidelity), `40–79` → 16, `< 40` → 10. Only relations in the focused neighbourhood may receive emphasis rendering. Edges are drawn in one vertex-coloured `LineSegments` per sampling tier, so the draw-call count stays a small constant rather than growing with the relation count.

### 13.7 Geometry tiers and the triangle budget (C9)

Two process-wide shared sphere geometries replace the single one:

| Tier | Segments | Triangles | Assigned to |
|---|---|---|---|
| `primary` | 32 × 20 | 1,216 | Nodes with `importance ≥ 80`, plus the anchor |
| `fine` | 16 × 12 | 352 | All other nodes |

Triangle counts follow three.js `SphereGeometry` exactly: `2 × widthSegments × (heightSegments − 1)`, so `32 × 20 → 1,216` and `16 × 12 → 352`. The existing repo comment calls the `primary` tier "≈ 1,200 triangles", which is this same figure.

Arithmetic at the v1 target scale (80 nodes: 20 structural, 1 anchor, 59 fine):

```
20 × 1216 + 1 × 1216 (anchor) + 59 × 352 = 24,320 + 1,216 + 20,768 = 46,304 triangles
```

which stays under the 50,000 ceiling. At the 100-node warning threshold with a 25 % structural mix:

```
25 × 1216 + 1 × 1216 (anchor) + 74 × 352 = 30,400 + 1,216 + 26,048 = 57,664 triangles
```

which is above the ceiling. That threshold is therefore exactly where the importance tier boundary, the tier segment counts, or the ceiling itself must be re-decided **with measured evidence** (§19.6) — a documented measurement point, not an assumption. At that scale the tier mix matters more than the node count: a 12 % structural mix (12 × 1216 + 1,216 + 87 × 352 = 14,592 + 1,216 + 30,624 = 46,432) stays inside the current ceiling without changing any constant. Relations contribute no triangles: they are `LineSegments`.

Node instancing remains one `InstancedMesh` per (geometry tier, presentation profile) that actually has members; the anchor is never instanced and is drawn exactly once by its dedicated object, as today.

### 13.8 Presentation/performance interaction

`data-atlas-presentation` (from §4.2) is authoritative for CSS and tests, and the enhancement module is the only writer of it.

---

## 14. Mobile 2D presentation

This section owns the **compact presentation** (`< 1024 px`, §4.2): every mobile viewport, plus tablets and small desktop windows without a suitable 3D viewport. It is also the no-WebGL fallback at any width, so nothing here may assume a small screen or a touch-only input device.

### 14.1 Technology

Deterministic SVG rendered inside the document plus the semantic HTML index. No Three.js, no canvas, no orbit, no physics, no pinch-to-explore requirement, no gesture-only affordance.

The SVG is a **presentation layer**: `aria-hidden="true"`, `focusable="false"`, no tab stops — exactly the rule the current canvas follows. Every interactive fact is a real HTML control (node buttons, relation buttons, inspector fields), so keyboard, switch, screen-reader and 44 px touch-target requirements are met by native elements rather than by SVG hit areas. Tap/click on an SVG element routes to the same selection transition as its HTML twin.

### 14.2 Initial overview selection

The initial mobile overview shows **8–15 nodes**, selected by this deterministic order:

1. Every node with `mobile_overview_priority = "featured"`.
2. Then nodes with `mobile_overview_priority = "auto"`, ordered by `(-importance, public_key)`.
3. Nodes with `mobile_overview_priority = "hidden"` are excluded from the initial overview. **Hidden means hidden from the initial mobile overview only** — the node remains in search, in the semantic index, in the inspector's neighbourhood views and in every relation. It is never removed from the Atlas.
4. The `identity` anchor is always included while it is visible.

If fewer than 8 nodes qualify, the smaller set is shown; no invented filler is added.

### 14.3 Layout of the 2D projection

- The projection maps stored `x`/`y` through one affine transform into a `viewBox` sized to the container's aspect ratio, with the padding needed for labels and the 44 px touch targets.
- Draw order is by `z` (far to near) so depth still reads; depth also modulates the drawn radius within a bounded factor.
- The transform is a pure function of the selected node set and the viewport box, so the same input always produces the same SVG.
- Labels avoid overlap by a deterministic offset rule (the existing leader-stem approach, no simulation).

### 14.4 Interaction

- **Tap a node** → selection, inspector updates below the SVG, URL updates, and the SVG re-frames to the node's neighbourhood view when the node is not in the current view.
- **Tap a relation** (through its HTML control, or the SVG edge when it is part of the current view) → relation selection with the same consequences.
- **View neighbourhood** → replaces the overview with the selected node and its direct neighbours (parents, children and related nodes), rendered with the same projection rules. A visible `Back to overview` control returns to the initial set. This is a *view* change, never a topology change.
- The inspector sits below the graph in natural document flow; there is no sticky overlay, no drawer and no focus trap.

### 14.5 Constraints

- No horizontal page overflow at 320 px, 390 px and 768 px (the existing responsive matrix gates this).
- Every interactive control is at least 44 × 44 CSS px.
- Reduced motion changes nothing structurally: the SVG has no motion to reduce. Transitions are removed by the existing `prefers-reduced-motion` rules.
- The full node set is reachable on mobile through search, the neighbourhood view and the semantic index even though the initial overview is a subset.

---

## 15. About preview

### 15.1 Presentation

- A lightweight **2D SVG projection** of the active Atlas version, rendered inside the existing About section position, with the existing About section heading and lead copy structure.
- **No Three.js on About after extraction.** The About route must end this program with zero canvas elements and zero WebGL code paths.
- A CTA links to `/…/atlas/`, and each preview node links to `/…/atlas/?focus=node:<key>` so a reader can enter the full Atlas already focused.

### 15.2 Node selection

The preview shows **6–10 nodes** chosen deterministically:

1. `mobile_overview_priority = "featured"` nodes first, ordered by `(-importance, public_key)`.
2. Then the remaining visible nodes by `(-importance, public_key)`.
3. The `identity` anchor is always included.
4. If fewer than 6 nodes are visible in the active version, the preview shows exactly those nodes (a 4-node version shows 4) with no filler.
5. Relations drawn are the relations among the selected nodes plus the relations from the anchor to the selected nodes.

### 15.3 Data rules

- The preview consumes the **same active Atlas version** and the same payload as the full Atlas. It never queries a separate source.
- **No separate About graph exists in CMS.** When no version is active, About shows an honest unavailable state (never a fabricated graph, never a cached copy of the retired Research Universe scene).
- The preview's semantic markup mirrors the same facts in HTML, so the About page stays readable with no JavaScript.

### 15.4 Budget

The preview adds no graphics dependency to the About document: it is inline SVG plus the payload script. It must not import any scene module, and the route must ship no additional JavaScript beyond the small selection/projection island described in §22.3.

---

## 16. Search, filter and deep-link behaviour

### 16.1 Search

- Search is client-side over the loaded payload (40–80 nodes); no endpoint.
- Match fields, in order of strength: localized node label → canonical record title → node aliases → node type label. Exact-prefix matches rank above substring matches; ranking is then `(-importance, public_key)` so it is stable.
- Persian normalization is applied to both the index and the query: Arabic-to-Persian character folding (`ي`→`ی`, `ك`→`ک`), removal of tatweel, non-breaking-space and zero-width characters, digit folding (Persian/Arabic-Indic → ASCII), and case folding for Latin text. Normalization is a pure function shared by search and the URL-state parser, and it is unit tested for fa and en.
- A result is a semantic selection: choosing it selects the node (or relation), updates the URL, updates the inspector and reframes the scene. Search never navigates away from the Atlas.
- Zero results renders an honest empty state with the query echoed and no invented suggestions.

### 16.2 Filters

**v1 filter set is fixed**: `All`, `Research Areas`, `Projects`, `Publications`, `Methods`, `Technologies`. Each filter maps to one `node_type.key` whose `filter_visible` is true; adding a filter is a data change (a new active node type with `filter_visible`), not a code change. The `identity` type is never a filter.

- Filters affect **presentation only**: they never change topology, never remove relations from the payload, never change counts in the inspector, and never write to the URL in v1.
- Default behaviour is **dim-first**: non-matching nodes and their relations are dimmed; matching nodes keep full emphasis. Hiding is used only where presentation requires it — specifically in the mobile overview and the About preview, where the selected subset governs what is drawn.
- The active filter is published as `data-atlas-filter` on the region.

### 16.3 Deep links

| URL | Meaning |
|---|---|
| `/en/atlas/?focus=node:<node-public-key>` | Node selected; inspector shows the node |
| `/fa/atlas/?focus=node:<node-public-key>` | Same entity, Persian projection |
| `/en/atlas/?focus=relation:<relation-public-key>` | Relation selected; inspector shows the relation |
| `/en/atlas/` | Overview, nothing selected |

Rules:

- Selection changes call `history.pushState()` with the new URL and never reload the document. `popstate` restores the selection encoded in the URL, including clearing the selection when the parameter is absent.
- Back/Forward must restore selection, inspector content and the corresponding camera/state.
- Keys are language-neutral: the same `focus` value is valid in both locales and resolves to the same entity with localized copy.
- The key grammar is `[a-z0-9._~-]+`; relation keys additionally contain `~` separators. The parser accepts percent-encoded and raw forms.
- **Unknown, retired, malformed or invisible keys never break the page**: the Atlas renders the overview with no selection and one non-blocking notice in the inspector region. It never 404s the route, never renders an empty graph, and never throws.
- URL state contains only the selected entity. It must **not** contain camera yaw, pitch, zoom, hover, filter state, or any other temporary visual state.
- The canonical link for the page is the route without query parameters.

### 16.4 Keyboard

`Escape` clears the selection and returns focus to the control that opened it (the semantic node/relation control, or the search field when the selection came from search). Tab order follows the document order of the semantic index; the SVG and the canvas add no tab stops.

---

## 17. Inspector behaviour

### 17.1 Structure

- **Non-modal.** No `role="dialog"`, no `aria-modal`, no focus trap, no scroll lock anywhere in the Atlas.
- Desktop (≥ 1024 px): a panel at the **logical end** of the workspace (`inline-end`), occupying **25–30 %** of the Atlas workspace width, beside the scene.
- Compact (< 1024 px): directly below the 2D graph in natural document flow.
- The panel is a region with a heading; its content is updated in place. One polite live region announces the newly selected entity's name and type — announcements are scoped to selection changes, never to camera or frame updates.

### 17.2 Scene framing accounts for the inspector

The 3D camera framing must be computed against the **effective viewport**: the stage width minus the inspector width when the inspector is present, including its gutter. The composition must not be centred in the full stage width, or every selection would shift the graph under the panel. This is a layout contract between the scene and the workspace, published as a CSS custom property (the effective width) that the scene reads on resize.

### 17.3 Node inspector content

Sections render **only when real data exists** for that section; empty sections are omitted rather than shown empty:

| Section | Source |
|---|---|
| Type | `node.type` → localized `nodeTypes` label |
| Title | `node.label` |
| Summary | `node.summary` (omitted when absent) |
| Parents | incoming hierarchy-role relations (`hierarchy: true`) with reverse display copy |
| Children / subnodes | outgoing hierarchy-role relations |
| Incoming relationships | non-hierarchy incoming relations, grouped by relation type with the inverse label |
| Outgoing relationships | non-hierarchy outgoing relations, grouped by relation type |
| Related projects | the neighbourhood's nodes whose type is `project` |
| Publications | the neighbourhood's nodes whose type is `publication` |
| Methods | the neighbourhood's nodes whose type is `method` |
| Technologies | the neighbourhood's nodes whose type is `technology` |
| Canonical record | `node.canonical` → labelled link plus the canonical title |

Neighbourhood-derived sections are grouped by the node type of the neighbour, so they are always consistent with the drawn relations and can never contradict the graph. Each listed entity is a selectable control (selecting it moves the selection and the URL) plus, when a canonical record exists, a link.

### 17.4 Relation inspector content

Relation type (forward or inverse display copy depending on the viewing direction) · source (selectable + link) · target (selectable + link) · localized explanation when present · inverse interpretation line when the type defines inverse copy · direction indicator · weight and hierarchy role shown as data, not as a claim about strength of evidence.

### 17.5 Behaviour

- Selection never scrolls the page on desktop; on mobile the inspector is below the graph and the page may scroll to it when the selection came from the semantic index (never on canvas tap, which would fight the reader's own scroll).
- The inspector is fully keyboard reachable in document order.
- No content depends on hover.

---

## 18. Accessibility

### 18.1 Non-negotiables

1. The canvas is **presentation-only** and `aria-hidden="true"`; it never takes a tab stop. The 2D SVG follows the same rule.
2. **Semantic HTML is authoritative** for assistive technology in every presentation: nodes, relations, groups, canonical links and the inspector exist as real elements.
3. Focus is always visible (`:focus-visible` twins for every Atlas control, using the existing token).
4. `Escape` clears selection and restores focus (§16.4).
5. Reduced motion is honoured, including a **live change**: the Atlas scene subscribes to `matchMedia('(prefers-reduced-motion: reduce)')` changes and applies the reduced pose/instant transitions without a reload. (This closes the gap where the current About scene samples the preference once.)
6. No-WebGL and context-loss paths keep the full semantic experience (§13.2, §21).
7. No-JS is a complete experience: the semantic index plus the honest content states.
8. **No modal dialog and no focus trap** are required or permitted by this design.
9. Every interactive target is at least **44 × 44** CSS px, including the in-stage controls. (The current in-stage control cluster is smaller; the Atlas must meet the target rather than inherit the exception.)
10. Status is never conveyed by colour alone: selection and emphasis states also publish text or shape (selected chip, type label, `aria-pressed`/`aria-expanded` state on controls).
11. RTL: all layout uses logical properties; the inspector sits at the logical end in both directions; SVG content is direction-neutral; the fa projection is verified at the same breakpoints as en.
12. Text zoom to 200 % and reflow at 400 % keep the semantic content usable; the graph itself is allowed to scroll or reduce its drawn subset, but never to hide content.
13. The Atlas region has a heading and a landmark, and the page keeps a valid document outline.

### 18.2 Screen-reader summary

The Atlas region begins with a concise programmatic summary: a heading, a one-sentence description, and the counts of areas, projects, publications, methods and technologies (counted from the payload, never authored). A `Skip to index` control jumps to the semantic index.

### 18.3 Acceptance

Accessibility evidence follows `Docs/06-quality` and the frontend's `docs/quality/ACCESSIBILITY.md`: keyboard-only pass, focus order, visible focus, axe scan on both locales and both presentations, reduced-motion assertions, 200 %/400 % zoom, and a screen-reader spot check of selection, relation reading and canonical navigation.

---

## 19. Performance

### 19.1 Inherited contracts (must not regress)

| Contract | Value |
|---|---|
| Active canvases per route | 1 |
| Idle rendering | 0 draw calls while nothing changes |
| Permanent RAF loops | none |
| DPR | ≤ 1.5 desktop, ≤ 1.0 at mobile widths |
| Drawing buffer | ≤ 1,500,000 px |
| Draw calls | ≤ 60 (aligned with `SCENE_PERFORMANCE_CEILINGS`) |
| Triangles | ≤ 50,000 (see §13.7 for the tier arithmetic at scale) |
| Scene JS | ≤ 300 KiB gzip, shared lazily with the existing chunks |
| Offscreen | rendering suspended while the stage is out of view |
| Teardown | complete disposal on `pagehide`; context loss → semantic fallback |
| Lazy import | the scene never loads before content renders and never on the critical path |

### 19.2 Atlas budgets (verify by measurement in Phase 3)

| Metric | Budget | Measurement |
|---|---|---|
| Time to first interactive Atlas frame after the document is interactive | ≤ 900 ms on a mid-range desktop profile | Playwright timing probe |
| Pick latency (pointer down → selection state written) at 80 nodes / 150 relations | ≤ 8 ms p95 | In-page probe over 200 picks |
| Frame duration during a drag at 80 / 150 | ≤ 16 ms p95 | rAF timing probe |
| Runtime payload | ≤ 60 KB gzip | Response size assertion |
| Embedded snapshot | ≤ 40 KB gzip | Build-output assertion |
| Label chips in the DOM at once | ≤ 40 | DOM count assertion |
| DOM nodes added by the Atlas presentation | ≤ 2,500 | DOM count assertion |
| Layout computation on activation (80 / 150) | ≤ 2 s | Backend test timing |

### 19.3 Picking at scale — the dependency-free plan

Picking stays O(n) screen-space projection with slop radii until a benchmark says otherwise. If the §19.2 pick budget is exceeded at the v1 target scale, the fallback technique is a **hand-rolled screen-space uniform grid**, specified here so no dependency is introduced:

1. On each pose change, project all nodes once (already required for labels) and bucket them into a uniform grid whose cell size is `2 × median projected radius`, rebuilt per pose in one pass.
2. A pick resolves only the cells intersecting the pick point plus a one-cell margin, then applies the existing per-candidate distance test.
3. Relations keep the polyline distance test with a coarse bounding-box rejection using the same grid.

**No spatial-index dependency may be added until a benchmark demonstrates the need** — and if it is added later, `kdbush`/`rbush`-class libraries remain subject to the design-authority dependency review.

### 19.4 Label and edge work bounds

Label projection is cached per pose and recomputed only when the pose or the viewport changes (not per frame while idle, and not twice for the same pose). Edge geometry is built once per version and re-sampled only by tier (§13.6); emphasis changes swap material/colour, never rebuild geometry.

### 19.5 Shared chunk reuse

`three` remains the single shared lazy chunk already present in the build. The Atlas adds scene code, not another copy of the engine. The Atlas route must not import `gsap` for the graph; scroll choreography is a Home concern.

### 19.6 Measured evidence rule

Any ceiling in §19.1 or §19.2 may be raised only with recorded measurements (device profile, node/relation counts, method, result) attached to the phase's evidence. A ceiling is never raised to make a test pass.

---

## 20. Validation rules

Validation lives in `Back-End/apps/atlas/validation.py` as a **pure** module (no HTTP, no imports at module top beyond the models it needs) returning a list of issues, exactly mirroring the established AB-06 pattern:

```json
{ "code": "HIERARCHY_CYCLE", "nodeKey": "research-area-1a2b3c4d", "messageToken": "atlas.hierarchyCycle" }
```

Codes are stable strings and are never renamed. `messageToken` is the localization key the admin renders. Validation runs in three places with identical results: the admin validate endpoint, the activation transaction, and a unit-test-accessible pure function.

### 20.1 Publish-blocking

| Code | Rule |
|---|---|
| `DANGLING_NODE_HIDDEN_RELATION` | A visible relation references an invisible node |
| `DANGLING_RELATION_ENDPOINT` | A relation's source or target no longer exists in the version |
| `CANONICAL_SOURCE_MISSING` | `canonical_translation_key` is required by the node type but absent |
| `CANONICAL_SOURCE_UNPUBLISHED` | The referenced canonical record does not resolve through `objects.public()` in a locale that lacks an override |
| `MISSING_LOCALE_PROJECTION` | A visible node has no resolvable label/summary for en or fa (no override **and** no canonical row in that locale) |
| `AMBIGUOUS_CANONICAL_REF` | More than one row matches `(canonical_model, translation_key, locale)` |
| `NODE_TYPE_INACTIVE` | A node uses an inactive node type |
| `RELATION_TYPE_INACTIVE` | A relation uses an inactive relation type |
| `RELATION_TYPE_NOT_ALLOWED` | A pair violates the relation type's allowed source/target types |
| `HIERARCHY_CYCLE` | The hierarchy-role subgraph contains a cycle |
| `SELF_LOOP_FORBIDDEN` | A self-loop where the relation type forbids it |
| `DUPLICATE_PUBLIC_KEY` | A node, group or composed relation key is not unique |
| `DUPLICATE_RELATION` | The same `(source, type, target)` exists twice, or an undirected relation duplicates its reversed pair |
| `INVALID_PIN` | Only one of `pin_x`/`pin_y` is set, or a pin is non-finite or out of bounds |
| `MISSING_LAYOUT` | A visible node has no stored coordinate at activation time |
| `GROUP_LOCALE_MISSING` | A group lacks a localized label for en or fa |
| `PAYLOAD_CONTRACT_INVALID` | The projected payload fails its own contract check (catalog references, key grammar, coordinate finiteness) |

**Locale parity is a publish blocker in both directions.** For every `visible` node, both the EN and the FA label/summary must resolve — from that locale's canonical record or from a per-locale override, never by falling back to the other locale (§5.3, "Fallback is forbidden") — before an `AtlasVersion` may become active. `MISSING_LOCALE_PROJECTION` covers the missing-EN and the missing-FA case identically; it is never a warning, and the activation transaction rejects the version (§8.3, §20.3). A node that is not `visible` follows the visibility rule exactly — it is neither published nor traversed — and is therefore not parity-gated: no stricter rule is invented for it. Warnings remain available for genuinely optional incompleteness (`SUMMARY_MISSING`, optional explanation absent, `ISOLATED_NODE`, unused taxonomy — §20.2).

### 20.2 Warnings (never blocking)

| Code | Rule |
|---|---|
| `ISOLATED_NODE` | No relations and no group membership |
| `NO_INBOUND_RELATIONS` | No incoming relation of any type |
| `NO_OUTBOUND_RELATIONS` | No outgoing relation of any type |
| `HIGH_DEGREE_HUB` | More than 12 relations on one node |
| `SUMMARY_MISSING` | No summary resolved for a visible node |
| `UNUSED_NODE_TYPE` | An active node type with no node in this version |
| `UNUSED_RELATION_TYPE` | An active relation type with no relation in this version |
| `OVERLAPPING_PINS` | Two pinned nodes closer than their combined radius (outside one group) |
| `SCALE_NODES` / `SCALE_RELATIONS` | The version exceeds 100 visible nodes / 250 visible relations |
| `SINGLE_LEVEL_HIERARCHY` | No hierarchy-role relation exists (the graph declares no structure) |

Warnings are shown in the admin with counts and entity links, and are never shown to readers as a defect.

### 20.3 Division of responsibility

The backend is the only authority on validity. The frontend may **defend** against a malformed payload (validate and fall back, §11.4) but must never re-derive validity, and must never "repair" a payload to make it render.

---

## 21. Failure and fallback states

| Condition | Reader-visible behaviour | Machine-visible state |
|---|---|---|
| No active version at build time | Atlas route renders an honest unavailable state with a route back to About; About renders its own unavailable state | `data-atlas-state="unavailable"` |
| API unreachable at build time | Same as above; the build does not fail | Build log records the skip |
| No active version at runtime (after a snapshot existed) | The embedded snapshot keeps rendering | `data-atlas-refresh="absent"` |
| Refresh returns a newer but invalid payload | Embedded snapshot keeps rendering | `data-atlas-refresh="rejected:<code>"` |
| Refresh network failure | Embedded snapshot keeps rendering, silently | `data-atlas-refresh="error"` |
| WebGL unavailable | 2D SVG presentation, full semantics | `data-atlas-presentation="2d"`, `data-atlas-enhancement="fallback"`, reason in `data-atlas-reason` |
| WebGL context lost | Canvas hidden, semantics and inspector keep working | `data-atlas-enhancement="fallback"`, `data-atlas-reason="context-lost"` |
| Scene module import rejected | Same as WebGL unavailable | `data-atlas-reason="import-rejected"` |
| Mobile viewport | 2D SVG presentation | `data-atlas-presentation="2d"` |
| JavaScript disabled | Semantic index with all nodes, relations, groups and canonical links | No `data-atlas-*` runtime state (attributes are server-rendered facts only) |
| Deep link to an unknown/retired key | Overview, no selection, one non-blocking notice | `data-atlas-focus="unknown"` |
| Deep link to an invisible node | Overview, no selection (invisible entities are not addressable) | `data-atlas-focus="unknown"` |
| Payload fails validation at build time | Build renders the semantic states without a graph payload | Build log records the rejection code |

Every failure path preserves: the page heading, the semantic index, the canonical links, and the route's availability. No failure path renders an empty stage without explanation, and no failure path shows an error to a reader for a *refresh* problem.

---

## 22. Testing strategy

The program's coverage must include the following. Framework choice follows each repository: `pytest` for the backend, `vitest` for frontend units, Playwright for browser behaviour. Test names and files below are the required minimum, not an exhaustive list.

### 22.1 Backend (pytest)

| Area | Required assertions |
|---|---|
| Model constraints | Unique active version; per-version unique public keys (ruling R9); `(version, node_type, translation_key)` uniqueness; a canonical record appears once per version; PROTECT on in-use taxonomy; composed relation key stability |
| Taxonomy validation | Inactive type blocked; allowed source/target pairs enforced; self-loop policy; key immutability once used |
| Multi-parent hierarchy | A node with two hierarchy parents is valid and its children/parents render in both directions |
| Hierarchy cycle rejection | A cycle in the hierarchy subgraph produces `HIERARCHY_CYCLE` and blocks activation |
| Locale parity | A node missing FA resolution produces `MISSING_LOCALE_PROJECTION` and a node missing EN resolution does the same; an override clears each; activation is rejected in both directions and passes only when both locales resolve; an invisible node is not parity-gated |
| Canonical resolution | `translation_key` resolution across locales; ambiguity rejected; unpublished record rejected; archived record rejected (snapshot rules respected) |
| Activation transaction | A failed validation leaves the previous active version serving; on success the previous version is archived in the same transaction; a concurrent activation attempt returns `409` |
| API conditional GET | Identical ETag for two requests over an unchanged version; ETag changes after activation; `If-None-Match` returns `304` with no body |
| Draft invisibility | Public route never serves draft nodes, relations, groups or coordinates; asserted after draft mutations |
| Locale isolation | The FA payload contains FA copy and FA hrefs and never EN copy as a fallback |
| Payload contract | Key grammar, catalog references, coordinate finiteness, ordering determinism (two builds byte-identical), and payload size budget |
| Layout determinism | Two computations produce identical coordinates; pins are honoured; recomputation with unchanged input changes nothing |

### 22.2 Frontend unit (vitest)

| Area | Required assertions |
|---|---|
| Payload validation | Unknown `contractVersion` ignored; missing fields rejected; validator returns the payload unchanged on success (no reshape); dangling relation rejected |
| Layout consumption | Coordinates come from the payload; no projection writes coordinates; two projections of the same input are identical |
| Stable IDs | Node/relation/group keys pass through unchanged; composed relation key matches the documented grammar |
| Search | Persian normalization (`ي/ك`, digits, ZWNJ, tatweel); prefix ranking; alias matching; zero-result state |
| Filters | Filter → type mapping; dim-first set computation; the filter never mutates the topology or the payload |
| URL state parser | `?focus=node:<key>` and `?focus=relation:<key>` round-trip; unknown key → no selection; malformed → no selection; camera state never parsed or written |
| Neighbourhood computation | Parents/children/related sets are correct, deterministic and cycle-safe |
| Mobile projection | Subset selection (`featured` first, then importance, `hidden` excluded), affine transform bounds, label offsets |
| About preview subset | 6–10 selection rule, fewer-when-available, anchor always included, relations among the subset |
| Importance ranking | Deterministic tiers and ordering for labels, radii and overview prominence |
| Reduced motion | Preference changes are applied live to the scene state machine |

### 22.3 Browser (Playwright)

Desktop 3D · mobile 2D · EN and FA for each · deep links for node and relation · Back/Forward restoration · search selection · every filter · node selection · relation selection · reduced motion (static pose, no transitions) · context loss fallback · no-WebGL fallback · no-JS semantics · accessibility scan · **idle draw calls equal zero** · performance at representative v1 scale (80 nodes / 150 relations, within §19.2 budgets).

The Atlas browser suite runs under the **research** Playwright configuration, which builds against a real published API through the existing `PUBLIC_API_BASE_URL` seam, because a hermetic build without a published Atlas exercises only the fallback path. Evidence capture must not be stored under Playwright's `test-results/`. The About preview is covered in the same suite, including the assertion that the About route ships zero canvases.

### 22.4 Gates and evidence

Every phase runs the owning repository's gates (`npm run lint`, `npm run format:check`, `npm test`, `npm run validate:design`, `npm run validate:seo`, `npm run build`, `uv run ruff check .`, `python -m pytest`) and records the exact commands and results. Per `Docs/00-governance/DEFINITION-OF-DONE.md`, a phase is complete only with tests, evidence, contract consistency and an explicit register entry for anything deferred. Browser-only behaviour is never claimed from a unit-only pipeline.

---

## 23. Migration strategy

The migration is additive and staged. The current `GraphVersion`, `GraphNode`, `GraphEdge`, `GraphNodeRelated` and `GraphGroup` rows are **not** modified, migrated in place or deleted by any step of this program; they are read once by an adapter and retired deliberately later.

### 23.1 Order

1. Additive Atlas models, taxonomy seeds, validation and layout (no reader-facing change).
2. Atlas admin API and authoring surfaces (drafts only; nothing public).
3. Public API `/api/atlas/{locale}` with conditional GET (still nothing mounted in the frontend).
4. Frontend `/atlas/` route (3D desktop, 2D mobile, semantic index) — additive route, no existing surface touched.
5. About switches to the 2D preview, reading the same active Atlas version.
6. Migration utility + parity proof (below), then retirement of the About Research Universe scene.
7. The legacy Home Research Universe path is handled by a separate card (§23.7).

### 23.2 Preflight (blocking the migration, not the earlier phases)

- Confirm that every canonical record the migration will reference has a **non-null `translation_key`** pairing its EN and FA rows. The field is nullable today; where a pair lacks it, the pairing is established through the existing admin sibling flow (or an audited data step) **before** Atlas nodes are created. The preflight runs in dry-run mode, reports the exact records needing a pairing, and is re-run until it reports zero.
- Confirm both rows of every pair are publishable, so the parity gate can pass.
- Confirm the existing graph's three relations and four nodes have exact per-locale labels to compare against.

### 23.3 Mapping

| Current | Atlas |
|---|---|
| `GraphNode(node_id="identity", type="identity")` → `relatedRecords: {family: "profile", id: 1 \| 2}` | `AtlasNode` of type `identity` referencing the `Profile` record's `translation_key` |
| `GraphNode(node_id="research-topic-N", type="research-topic", summary=…, position=…)` → `relatedRecords: {family: "researchtopic", id: N}` | `AtlasNode` of type `research-area` referencing the `ResearchTopic`'s `translation_key`, with `importance = 80` |
| `GraphEdge(relation_type="research-focus")` × 3 | `AtlasRelation` of type `research-focus`, `directed = true`, `weight = 1` |
| Published `position.x/y/z` | Not carried as coordinates: the Atlas layout is deterministic (§12). Positions may be carried as `pin_x = x`, `pin_y = y` when the owner wants the current composition preserved, decided per node during migration review |
| `GraphGroup` (authoring-only, unused) | Nothing to migrate |

### 23.4 Parity proof (required before retirement)

The migrated version must reproduce, per locale:

- Node count 4 and relation count 3, with the same per-locale labels as the live payload, character for character.
- The same canonical targets (the same `Profile` and the same three `ResearchTopic` records).
- The same English relation display copy (`research focus`).
- The identity node as the anchor with the same visual role, and no node or relation rendered that the old graph did not have.
- A side-by-side evidence record (old payload vs new payload, plus a rendered before/after capture set) stored outside the test runner's output directory.

Any discrepancy is fixed in the mapping, never by editing the evidence.

### 23.5 Deletions are separate and explicit

Retirement of the About Research Universe scene happens only after §23.4 passes, in its own commit, and removes: the About full-scene client path, the About canvas, the About-specific scene wiring, and the About tests that assert the retired behaviour. Tests are replaced with the Atlas/About-preview equivalents, not deleted without replacement. The `ru-about` suite's About-specific assertions about *selection semantics* move to the Atlas suite; the About suite is rewritten to assert the preview.

### 23.6 The old graph storage retires last

`GraphVersion`/`GraphNode`/`GraphEdge`/`GraphNodeRelated`/`GraphGroup` and `/api/graph/{locale}` stay in place until the owner confirms that no surface reads them. Their removal is a separate approved change with its own migration, and it must not be bundled into any Atlas phase.

### 23.7 The Home Research Universe path

`HeroGraph.astro`, `GraphNodeList.astro`, `home-scene.ts`, `home-motion.ts`, `home-preset.ts`, `hero-enhancement.ts` and the stale `tests/e2e/ru-home.e2e.ts` belong to the retired Home graph, not to the Atlas. They are **not** part of this program, are not reused as Atlas architecture, and are resolved by a separate card that either retires them or repoints them. Home's current presentation (Hero v2) is untouched.

---

## 24. Rollout phases

Each phase is a separate deliverable with its own commit(s), gates and evidence. No phase may begin before its predecessor's exit criteria are met.

| Phase | Scope | Repository | Exit criteria |
|---|---|---|---|
| **P0** | This specification + the `I09 — Atlas` contract section | coordination root, `Docs/03-contracts` | Specification approved; contract section written; no runtime change |
| **P1** | `Method`/`Technology` models + Atlas models + taxonomy seeds + migrations | `Back-End` | Migrations apply forward and back on a database copy; model-constraint tests pass; admin registers the new entities |
| **P2** | Validation module, layout module, tests | `Back-End` | Every §20 rule has a failing-then-passing test; layout determinism test passes |
| **P3** | Admin API + authoring surfaces (2D editor, relation form/table, translations, validate, preview) | `Back-End`, `Front-End/admin-panel` | Draft authoring round-trips through the admin UI; `If-Match` semantics tested; no public surface affected |
| **P4** | Public `/api/atlas/{locale}` with ETag/`304`, payload tests, OpenAPI export + pins | `Back-End`, `Front-End/public-site` (types) | Contract tests pass; ETag/`304` tests pass; draft invisibility asserted; frontend types regenerated and pinned |
| **P5** | `/atlas/` route: semantic index, 2D presentation, 3D desktop presentation, search, filters, deep links, inspector | `Front-End/public-site` | Browser suite green in both locales and both presentations; §19 budgets measured; accessibility evidence recorded; route registered in SEO/sitemap/nav registries |
| **P6** | Migration + parity proof | `Back-End` (data), coordination root (evidence) | §23.4 parity record complete; dry-run reports zero unpaired records |
| **P7** | About switch to the 2D preview + retirement of the About scene + test rewrite | `Front-End/public-site` | About ships zero canvases; About suite rewritten and green; no regression in the rest of the public site |
| **P8** | Old graph storage retirement (separate approval) | `Back-End`, `Front-End/public-site` | Owner confirms no consumer; removal is its own reviewed change |

Standing rules for every phase: land on `main` through the owning repository's own gates; production promotion is an owner-gated, host-side operation and is never part of a phase's definition of done; staging deploys follow the existing workflow, not a new pipeline.

---

## 25. Explicit deferred features

Recorded as deferred, not planned as part of v1. Each requires its own product decision before it becomes work.

| Deferred | Reason |
|---|---|
| `experience` as an Atlas node type | The owner's v1 scope sets the five primary types; employment history stays on the CV/About prose |
| Drag-to-connect in the admin graph editor | v1 uses the structured relation form; the connector flow is a candidate v1.1 improvement |
| Scheduled publishing | v1 publishes atomically and immediately |
| Filter state in the URL | v1 keeps URL state to the selected entity only |
| A spatial-index dependency (kdbush/rbush class) | Forbidden until a benchmark demonstrates need (§19.3) |
| Public detail routes for `method` and `technology` | They are published entities without public routes in v1 |
| Atlas in the primary navigation | About CTA and deep links are the v1 entry points |
| Atlas interaction analytics | The existing analytics event enum is closed and unchanged by this program |
| 3D as the primary admin editing surface | 3D preview is a review step, not an editor |
| Per-locale topology divergence | Explicitly forbidden by design, not deferred as an option |
| Inferred or suggested relations ("related by similarity") | Contradicts the authored-facts principle |
| Mobile 3D, WebXR, VR | 2D is the mobile presentation |
| Offline/PWA caching of the Atlas payload | No offline product requirement exists |
| Animated entry choreography for the Atlas | The character is restraint; motion stays bounded and preference-aware |
| Real-time collaborative authoring | Single-owner authoring with `If-Match` is sufficient |

---

## 26. Risks

| # | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | Triangle ceiling breached as the graph grows past the v1 target | Medium / Medium | Importance-tiered tessellation (§13.7) with arithmetic at 80 and 100 nodes; measurement gate before raising any ceiling |
| R2 | O(n) picking or label projection becomes measurable at 80 nodes | Medium / Medium | §19.2 pick and frame budgets with a benchmark gate, and the dependency-free broad-phase plan ready to implement |
| R3 | Locale parity becomes a daily authoring tax and blocks publishing | Medium / High | Translation coverage worklist in admin, override precedence, and **blocking** issues that name the exact missing field and locale — parity is a publish blocker in both directions, never a warning, so the repair path is explicit rather than a silent pass |
| R4 | The canonical-record reference depends on `translation_key`, which is nullable today | Medium / High | §23.2 preflight is blocking, dry-run first, with the existing admin sibling flow as the repair path |
| R5 | Two graph engines and a live legacy storage layer exist during the transition | High / Medium | Legacy modules are never imported by Atlas code; retirement is explicit, ordered and gated by parity evidence |
| R6 | Embedded snapshot size grows into layout-shift or HTML bloat | Low / Medium | §19.2 ceilings plus a build-time size assertion |
| R7 | CDN caching hides a new version from readers | Medium / Low | 60-second cache contract, conditional requests, and an accepted staleness window documented in §11.3 |
| R8 | Admin 2D editor and 3D preview drift apart from the public renderer | Medium / Medium | Both consume the stored layout and the same payload; the 3D preview renders the real presentation |
| R9 | Contracts drift (OpenAPI snapshot vs generated types vs pins) | Medium / Medium | §10.9 requires regeneration and re-pinning in the same change; contract tests assert the pin |
| R10 | Accessibility regressions in the new inspector/search surfaces | Medium / High | §18 non-negotiables + axe + keyboard-only evidence per phase; no modal patterns introduced |
| R11 | Scope creep from "3D is impressive" toward a visualisation showcase | Medium / High | §2.2 non-goals and §25 deferrals are the written boundary; the published graph must justify each entity |
| R12 | The stale Home Research Universe tests give a false sense of coverage | High / Low | Home's graph path is explicitly outside this program (§23.7) and is resolved by its own card |
| R13 | Publishing requires a frontend deploy after all | Low / High | §8.4 and §11.3 make deploy-free publication a tested property, not an intention |

---

## 27. Acceptance criteria

The program is accepted when all of the following are demonstrably true on the deployed staging (and, after owner promotion, production) artifacts.

**Data and authoring**

1. A published method and a published technology exist as first-class CMS records with both locales, and each can be used as an Atlas node.
2. Every node and relation in the active version was authored in the admin panel; no node or relation exists that an author did not create.
3. A canonical record appears at most once per version, and the system refuses a duplicate.
4. Deleting an in-use node type or relation type is blocked; retiring it is possible through `active`.
5. Hierarchy-role relations form a DAG; an attempted cycle blocks activation with `HIERARCHY_CYCLE`.
6. A node with two hierarchy parents publishes and renders both parents.
7. Activation is transactional: a failed validation leaves the previous version serving, and a successful activation archives the previous version in the same transaction.
8. Draft data appears on no public surface.
9. Publishing an Atlas version does not require a frontend deploy: the public endpoint serves the new version without any build step.

**Bilingual topologies**

10. EN and FA serve identical node, relation and group keys and counts.
11. No locale falls back to another locale's copy: a missing projection blocks publication instead.
12. A missing FA projection on a visible node blocks publication with a named issue.

**Presentations**

13. Desktop (≥ 1024 px, WebGL available): 3D Atlas with orbit, zoom, reset, clear, `Escape`, pick, hover, selection and relation selection.
14. Compact (< 1024 px, which includes every mobile viewport): deterministic 2D SVG Atlas with tap selection, inspector below the graph, and a working neighbourhood view; no orbit, no physics, no pinch requirement.
15. Desktop without WebGL: the 2D presentation with full semantics.
16. With JavaScript disabled: a semantic index of every node, relation, group and canonical link on both routes.
17. About shows a 2D preview of 6–10 nodes with a CTA and deep links, and the About route ships **zero** canvases.
18. One canvas element exists on the Atlas route, and none on About or Home.

**Interaction and URL**

19. `?focus=node:<key>` and `?focus=relation:<key>` select the right entity in both locales.
20. Back/Forward restores selection and inspector content.
21. An unknown or retired key renders the overview with a notice and never an error page or an empty graph.
22. The URL never encodes camera state, zoom, hover or filter state.
23. Filters dim rather than delete, and never change the inspector's relation counts.
24. Search matches localized labels, canonical titles, aliases and types, and applies Persian normalization.

**Accessibility**

25. The canvas and the SVG are `aria-hidden` and add no tab stops.
26. Full keyboard operation of selection, search, filters, inspector and relation reading, with visible focus everywhere.
27. `Escape` clears the selection and restores focus.
28. Reduced motion is honoured, including a live preference change, in both presentations.
29. Every interactive target is at least 44 × 44 CSS px.
30. Axe scans pass on `/en/atlas/`, `/fa/atlas/`, `/en/about/`, `/fa/about/` in both themes; no modal dialog or focus trap exists.

**Performance**

31. Idle draw calls are zero while the Atlas is untouched.
32. One canvas per route, no permanent RAF loop, offscreen pause active.
33. Pick latency ≤ 8 ms p95 and drag frame ≤ 16 ms p95 at 80 nodes / 150 relations.
34. Runtime payload ≤ 60 KB gzip and the embedded snapshot ≤ 40 KB gzip.
35. Context loss and a rejected scene import both degrade to the semantic experience without a reload.
36. Scene JS stays within the existing 300 KiB gzip ceiling, reusing the shared `three` chunk.

**Migration**

37. The migrated version reproduces the current published graph's four nodes, three relations, per-locale labels and canonical targets exactly.
38. The About Research Universe scene is retired only after (37) is evidenced, and its tests are replaced rather than dropped.
39. Hero v2 and Home are byte-for-byte unaffected by this program.

---

## 28. Open questions

Only questions that require measurement or code inspection remain. Every product decision above is final; none of the items below reopens one.

1. **Exact deterministic layout parameters.** The pipeline in §12.2 is fixed, but the numeric seeds (relaxation iterations, damping, spacing constants, group-attraction fraction) must be prototyped against a representative 60–80 node fixture and then frozen with the measured result. The prototype is a throwaway script; the frozen constants live in the layout module with the measurement recorded in the phase evidence.
2. **Exact broad-phase picking technique.** §19.3 defines the dependency-free screen-space grid. Whether it is needed at all, and its exact cell size and rebuild strategy, is decided by the §19.2 benchmark on real hardware.
3. **Exact wire serializer shape.** The payload fields are specified in §10.2, but the concrete Django Ninja `Schema` classes and camelCase aliases must be written to match the existing public API conventions (omission of empty optionals, ordering guarantees, `exclude_none`) as the implementation lands; contract tests assert the final shape, not a hand-written duplicate.
4. **Coordinate precision in the payload.** Three decimals are specified; whether the payload shrinks measurably at two decimals without visible displacement is a measurement question for the P5 payload budget, with the visible-displacement check as the acceptance condition.
5. **Whether the label count budget (§19.2, ≤ 40 chips) is the right ceiling at 80 nodes.** The first measurement at scale may show that fewer chips read better or that the ceiling can rise; the decision is measurement-led and recorded in the phase evidence.
6. **Whether the identity anchor needs its own public filter exclusion beyond `filter_visible = False`.** If the inspector's type grouping renders an anchor section that reads oddly, the presentation rule (not the data model) is adjusted after seeing the real 62-node fixture.
7. **Whether the shared `three` chunk should be split once the Atlas exists.** The Atlas reuses the existing shared chunk; if the P5 budget measurement shows the gateway paying for unused Atlas code, a split is evaluated as a build-level change under its own card.

---

*End of specification.*
