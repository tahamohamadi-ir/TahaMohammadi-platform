# Knowledge Atlas v1 Plan C: Public Atlas Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `/en/atlas/` and `/fa/atlas/` — a hybrid-freshness, URL-addressable, accessible Atlas with desktop 3D, deterministic 2D SVG for compact viewports and WebGL-less desktops, a complete no-JS semantic index — built on the current Research Universe renderer lineage and the Plan A public API.

**Architecture:** Pure logic lives in `src/lib/atlas/*` (model, validator, snapshot, refresh, selection, URL codec, search, filters, neighbourhood, inspector projection, layout consumption, 2D projection) and is unit-tested without a DOM. The graphics layer lives in `src/lib/visual/atlas/*` and imports the existing Research Universe primitives (`scene-core`, `spheres`, `materials`, `theme`, `nodes`, `edges`, `labels`, `leaders`, `hit-testing`, `dispose`) without copying them. One Astro page per locale composes a server-rendered semantic index, an embedded validated snapshot, a 2D SVG presentation and the lazy 3D enhancement. The runtime revalidates the embedded snapshot with one conditional GET and adopts a newer active version when one exists.

**Tech Stack:** Astro 7.2.9 (static, no adapter, no framework integration — vanilla TS in `<script>` + dynamic `import()`), TypeScript 5.9, Three.js 0.173 (reused shared chunk), vitest 4, Playwright 1.62. No new dependency is added by this plan.

**Spec:** Docs/05-delivery/knowledge-atlas/KNOWLEDGE-ATLAS-V1-DESIGN-SPEC.md

**Depends on:** Plan A (public API + re-pinned types + exported fixtures). Does **not** depend on Plan B — `tests/fixtures/atlas/*.json` (Plan A Task 18 output) stand in for authored data.

## Global Constraints

- **Hero v2 and Home are untouched.** No file under `src/components/home/**`, `src/components/hero/**`, `src/lib/visual/hero-sequence.ts` or `src/styles/hero-*.css` is modified. The Atlas adds a route; it changes nothing on `/`.
- **One canvas per route.** The Atlas route owns the only canvas; About must own none once Plan D lands; Home has none.
- **Render-on-demand only.** No permanent `requestAnimationFrame` loop, no idle rendering, no physics, no animation-on-hover loops. Idle draw calls must be 0.
- **The 3D presentation requires WebGL *and* ≥ 1024 px.** Below that, 2D. This is a presentation rule, not a suggestion.
- **Never revive the legacy engine.** `graph-scene.ts`, `graph-controller.ts`, `graph-layout.ts`, `graph-motion.ts`, `hero-enhancement.ts` are not imported anywhere in this plan.
- **Layout authority is the backend** (spec §12.1). Plan C consumes stored coordinates. The deterministic pieces this plan owns are coordinate validation, pin precedence, radius/label-tier derivation, 2D transforms and selection subsets — **never a re-simulation** (group attraction, hierarchy seeding and collision relaxation are Plan A's `apps/atlas/layout.py`).
- **A validator validates, never reshapes.** The runtime validator returns the payload unchanged on success.
- **Presentation layers are `aria-hidden` with no tab stops.** Canvas and SVG alike; every interactive fact is a native HTML control.
- **No new dependency**, including no spatial index (spec §19.3) — the broad-phase fallback, if a benchmark demands it, is hand-rolled.
- **Deterministic fixtures.** Browser specs must not depend on the production API; the hermetic fixture server carries the Atlas from `tests/fixtures/atlas/`.
- **The draft preview capability never appears in a URL.** It is read from the URL **fragment**, stripped with `history.replaceState()` before the first fetch, sent only in an `Authorization: Bearer` header to `GET /api/atlas/preview?locale=…`, and never written to `localStorage`, `sessionStorage`, cookies, IndexedDB or a beacon. No Atlas module receives the signing secret, which stays backend-only.
- **Exactly one compact-overview field.** The payload's `mobileOverviewPriority` (model `mobile_overview_priority`) is the only compact-overview input; no module reads a `mobile` or `mobileOverview` alias.

**Commands (from `Front-End/public-site`):**

```bash
npm test -- src/lib/atlas/model.test.ts          # focused unit
npm run lint && npm run format:check             # gates
npm test                                         # full unit suite
npm run build                                    # astro build (42 pages locally)
npx playwright test tests/e2e/product-atlas.e2e.ts            # hermetic (fixture-backed)
npx playwright test --config playwright.knowledge-atlas.config.ts tests/knowledge-atlas/  # live-API
npm run validate:seo && npm run validate:design
```

## File Map

**Created — pure logic**

| Path | Responsibility |
|---|---|
| `src/lib/atlas/model.ts` | `ATLAS_CONTRACT_VERSION = 'atlas01-1.0.0'`, payload types (mirrored from the generated OpenAPI types), key-grammar helpers |
| `src/lib/atlas/validate.ts` | Runtime payload validator: contract version, key uniqueness, catalog references, relation endpoints, finite coordinates, group integrity |
| `src/lib/atlas/snapshot.ts` | Build-time loader (`fetchAtlasSnapshot(locale)`) + serialisation for the embedded payload; returns the honest availability states |
| `src/lib/atlas/refresh.ts` | Conditional revalidation: `If-None-Match`, adopt-newer, keep-snapshot-on-failure, `data-atlas-refresh` reasons |
| `src/lib/atlas/selection.ts` | The single selection state machine (`overview` / `node` / `relation`) shared by every presentation |
| `src/lib/atlas/url-state.ts` | `?focus=node:<key>` / `?focus=relation:<key>` codec: parse, serialise, normalise (fa-aware), unknown-key handling; no camera state |
| `src/lib/atlas/search.ts` | Search index + Persian normalisation + deterministic ranking |
| `src/lib/atlas/filters.ts` | Filter → node-type mapping, dim-first set computation |
| `src/lib/atlas/neighborhood.ts` | One-hop sets (parents, children, incoming, outgoing, by target type) |
| `src/lib/atlas/inspector.ts` | Inspector projection: ordered sections with only the data that exists |
| `src/lib/atlas/layout.ts` | Coordinate consumption: pin precedence, radius from importance, bounds, draw order, label tiers |
| `src/lib/atlas/projection-2d.ts` | Pure 2D projection model: affine transform, node set selection, edge paths, label offsets |
| `src/lib/atlas/preview.ts` | Draft-preview bootstrap: read the capability from the URL **fragment**, strip it with `history.replaceState()` before any fetch, fetch the draft projection with an `Authorization` header, mark `noindex`; never persists the capability |

**Created — presentation**

| Path | Responsibility |
|---|---|
| `src/lib/visual/atlas/enhancement.ts` | Orchestrator: eligibility, lazy imports, selection wiring, refresh, fallback on every failure |
| `src/lib/visual/atlas/scene.ts` | 3D scene (reuses RU primitives), states, emphasis, camera, tiers |
| `src/lib/visual/atlas/controls.ts` | Orbit/zoom/reset/clear/Escape + pointer-capture guard for in-stage controls |
| `src/lib/visual/atlas/picking.ts` | Screen-space pick with slop; the only place a broad phase may be added |
| `src/components/atlas/AtlasPageContent.astro` | Page composition: heading, lead, semantic index, stage, inspector, payload script, enhancement entry |
| `src/components/atlas/AtlasIndex.astro` | No-JS semantic index (nodes, relations, groups, canonical links) |
| `src/components/atlas/AtlasProjection2d.astro` | SVG presentation for `mobile-overview` / `webgl-fallback` / about-preview |
| `src/components/atlas/AtlasInspector.astro` | Node + relation inspector markup with every detail block rendered server-side |
| `src/components/atlas/AtlasControls.astro` | Search, filter chips, view controls (all native form controls) |
| `src/pages/en/atlas/index.astro`, `src/pages/fa/atlas/index.astro` | Routes |
| `src/pages/en/atlas/preview/index.astro`, `src/pages/fa/atlas/preview/index.astro` | Draft-preview shells: `noindex, nofollow`, out of the sitemap and the indexable registry, same presentation code path as the Atlas route (Task 8) |
| `src/styles/atlas.css` | Atlas presentation (logical properties only) |

**Created — tests, fixtures, tooling**

| Path | Responsibility |
|---|---|
| `tests/fixtures/atlas/{en,fa}.json`, `tests/fixtures/atlas/benchmark.json` | Copied unchanged from Plan A's `--dump-atlas-fixture` output |
| `src/lib/atlas/*.test.ts`, `src/lib/visual/atlas/*.test.ts` | Unit coverage |
| `tests/e2e/product-atlas.e2e.ts` | Hermetic browser coverage (deep links, presentation switch, filters, search, a11y, idle draws, fallback) |
| `tests/knowledge-atlas/ka-live.e2e.ts` | Live-API confirmation against `TM_E2E_API_BASE_URL` (topology parity, real data, contract version) |
| `playwright.knowledge-atlas.config.ts` | Config for the live-API suite (mirrors `playwright.research.config.ts`, `testDir: './tests/knowledge-atlas'`) |
| `scripts/atlas-pick-benchmark.mjs` | Node script measuring pick latency at benchmark scale (Task 18) |

**Modified**

| Path | Change |
|---|---|
| `scripts/e2e-site-settings-fixture.mjs` | Serve `/api/atlas/{locale}` from the Atlas fixtures (the Home-content precedent) |
| `src/lib/seo-route-registry.ts`, `scripts/seo-route-registry.mjs` | Add `atlas` to `LOCALE_INDEX_ROUTES` |
| `astro.config.mjs` | Sitemap filter already excludes preview/atlas-design paths; confirm `/atlas/preview/` is excluded in both locales — verify against the built sitemap, do not assume |
| `docs/design/ROUTES-AND-PAGE-FAMILIES.md` | Record the new canonical route |

**Cross-plan interfaces**

| Interface | Direction | Note |
|---|---|---|
| `GET /api/atlas/{locale}` payload | consumes | Plan A; shape frozen by `atlas01-1.0.0` |
| Draft-preview capability consumption (`/{locale}/atlas/preview/#token=…`) + the shell routes | **produces** | Consumed by Plan B task 17 (its declared dependency). The minting primitive and `GET /api/atlas/preview` are Plan A task 15's; the capability is sent only in an `Authorization` header, never in a URL |
| `AtlasProjection2d` about-preview mode | **produces** | Consumed by Plan D task 7 |
| `ATLAS_CONTRACT_VERSION` | produces | Must equal the backend constant; a test asserts the literal |

---

### Task 1: Contract types and key grammar

**Files:**
- Create: `src/lib/atlas/model.ts`
- Test: `src/lib/atlas/model.test.ts`

**Interfaces:**
- Produces: `ATLAS_CONTRACT_VERSION`, `AtlasPayload`, `AtlasNodeOut`, `AtlasRelationOut`, `AtlasGroupOut`, `AtlasNodeTypeOut`, `AtlasRelationTypeOut`, `AtlasVersionMeta`, `isRelationKey(key)`, `isNodeKey(key)`, `relationKeyParts(key)`
- Consumes: `components['schemas'][...]` from `@/generated/public-api` where the generated schema exists; otherwise a local interface **plus** a test asserting the field-set literal copied from the API document

- [ ] **Step 1: Write the failing tests**

```ts
import { ATLAS_CONTRACT_VERSION, isNodeKey, isRelationKey, relationKeyParts } from './model'

it('mirrors the backend contract version literally', () => {
  expect(ATLAS_CONTRACT_VERSION).toBe('atlas01-1.0.0')
})


it('distinguishes node keys from composed relation keys', () => {
  expect(isNodeKey('research-area-1a2b3c4d')).toBe(true)
  expect(isRelationKey('research-area-1a2b3c4d')).toBe(false)
  expect(isRelationKey('identity-2b3c4d5e~research-focus~research-area-1a2b3c4d')).toBe(true)
  expect(relationKeyParts('a-11111111~uses~b-22222222')).toEqual({
    source: 'a-11111111', relationType: 'uses', target: 'b-22222222',
  })
  expect(relationKeyParts('not-a-relation')).toBeNull()
  expect(isNodeKey('Bad Key')).toBe(false)
})
```

- [ ] **Step 2: Run — expect FAIL** (`Cannot find module './model'`).
- [ ] **Step 3: Implement** the module: the version constant, the payload interfaces matching the documented wire shape, and the key helpers (`^[a-z0-9][a-z0-9._~-]{1,79}$` for nodes/groups; exactly two `~` separators for relations).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the public Atlas model and key grammar"`

---

### Task 2: Runtime payload validator

**Files:**
- Create: `src/lib/atlas/validate.ts`
- Test: `src/lib/atlas/validate.test.ts`

**Interfaces:**
- Produces: `validateAtlasPayload(raw: unknown): { ok: true; payload: AtlasPayload } | { ok: false; reason: AtlasRejection }` where `AtlasRejection = 'not-object' | 'unknown-contract' | 'nodes-not-array' | 'relations-not-array' | 'duplicate-key' | 'unknown-type' | 'dangling-relation' | 'missing-coordinate' | 'non-finite-coordinate' | 'unknown-group-member'`
- Scope note: this is the **client-side payload contract validator** for the runtime refresh path. The publish-gate validator (issue codes, DAG, locale parity) is Plan A's `apps/atlas/validation.py` and must not be duplicated here; the frontend only ever defends, never re-derives publish validity (spec §20.3).

- [ ] **Step 1: Write the failing tests**

```ts
it('ignores an unknown contract version instead of guessing', () => {
  expect(validateAtlasPayload({ ...payloadFixture, contractVersion: 'atlas02-2.0.0' }))
    .toEqual({ ok: false, reason: 'unknown-contract' })
})


it('returns the payload unchanged on success', () => {
  const result = validateAtlasPayload(payloadFixture)
  expect(result.ok).toBe(true)
  if (result.ok) expect(result.payload).toBe(payloadFixture)  // identity, never a copy
})


it('rejects duplicate keys and dangling relations', () => {
  expect(reason({ ...payloadFixture, nodes: [...payloadFixture.nodes, payloadFixture.nodes[0]] }))
    .toBe('duplicate-key')
  expect(reason(withRelation(payloadFixture, { target: 'does-not-exist' }))).toBe('dangling-relation')
})


it('rejects a node whose type is missing from the catalog', () => {
  expect(reason({ ...payloadFixture, nodeTypes: [] })).toBe('unknown-type')
})


it('rejects non-finite coordinates and unknown group members', () => {
  expect(reason(withNode(payloadFixture, { position: { x: Number.NaN, y: 0, z: 0 } }))).toBe('non-finite-coordinate')
  expect(reason(withGroup(payloadFixture, { nodeKeys: ['missing'] }))).toBe('unknown-group-member')
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** as a total, side-effect-free function with the identity-return contract and no reshaping.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the runtime payload validator"`

---

### Task 3: Build-time snapshot loader

**Files:**
- Create: `src/lib/atlas/snapshot.ts`
- Test: `src/lib/atlas/snapshot.test.ts`

**Interfaces:**
- Produces: `type AtlasSnapshot = { status: 'ready'; payload: AtlasPayload; etag: string | null; html: AtlasIndexModel } | { status: 'unavailable' } | { status: 'invalid'; reason: AtlasRejection }`; `fetchAtlasSnapshot(locale, fetchFn?)`; `serializeAtlasPayload(payload)` (JSON with `<` escaped)
- Consumes: `buildPublicApiUrl`, `canFetchPublicApi` from `src/lib/api/resolve-url.ts`

- [ ] **Step 1: Write the failing tests** — no API configured ⇒ `unavailable` and **no fetch attempted**; 404 ⇒ `unavailable`; malformed ⇒ `invalid` with the reason and **no partial model**; valid ⇒ `ready` with the ETag captured from the response headers and an index model carrying every visible node and relation.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** (build-time only; no client code paths in this module).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the build-time snapshot loader"`

---

### Task 4: Fixtures and hermetic fixture server

**Files:**
- Create: `tests/fixtures/atlas/en.json`, `tests/fixtures/atlas/fa.json`, `tests/fixtures/atlas/benchmark.json` (copied from Plan A's dump)
- Modify: `scripts/e2e-site-settings-fixture.mjs`
- Test: `tests/e2e/product-atlas.e2e.ts` (Task 29 owns the browser assertions; this task only wires the data)

**Interfaces:**
- Produces: fixture routes `GET /api/atlas/en` and `GET /api/atlas/fa` serving the fixture bytes with `ETag` and `Cache-Control: public, max-age=60`; `GET /api/atlas/en` with a matching `If-None-Match` returning `304`

- [ ] **Step 1: Write the failing test** — a small node assertion run through the existing harness:

```bash
node -e "const f=require('./tests/fixtures/atlas/en.json'); if(f.contractVersion!=='atlas01-1.0.0') process.exit(1); if(f.nodes.length<6) process.exit(1); console.log('fixture ok', f.nodes.length, f.relations.length)"
```
Expected: prints `fixture ok <nodes> <relations>` (the Plan A scale fixture is the 72-node benchmark; the copied `en.json` is the smaller editorial fixture — assert whichever count the Plan A dump produced, never a hoped-for number).
- [ ] **Step 2: Wire the fixture server** — add the two routes beside the existing settings/home routes, reading the files at startup, computing the ETag once (`createHash('sha256')` of the file bytes), honouring `If-None-Match`, and touching nothing else in that script.
- [ ] **Step 3: Prove the server answers**

```bash
TM_E2E_SETTINGS_PORT=4399 node scripts/e2e-site-settings-fixture.mjs & sleep 1
curl -s -D - http://127.0.0.1:4399/api/atlas/en | head -6
kill %1
```
Expected: `200`, `ETag`, `Cache-Control: public, max-age=60`, JSON body; a second call with `If-None-Match` returns `304`.
- [ ] **Step 4: Commit** — `git commit -m "test(atlas): serve Atlas fixtures hermetically"`

---

### Task 5: Routes and route registrations

**Files:**
- Create: `src/pages/en/atlas/index.astro`, `src/pages/fa/atlas/index.astro`
- Modify: `src/lib/seo-route-registry.ts`, `scripts/seo-route-registry.mjs`, `docs/design/ROUTES-AND-PAGE-FAMILIES.md`
- Test: `src/lib/routes.test.ts` (extend)

**Interfaces:**
- Produces: the two routes with `SiteLayout`, exact-locale `title`/`canonical`/`alternate`, and `data-atlas-region`; `atlas` present in both registry modules
- Scope note: these are the **only** Atlas routes registered as indexable. The draft-preview shells (`/{locale}/atlas/preview/`) are created in Task 8 and are deliberately excluded from `LOCALE_INDEX_ROUTES` and the sitemap, so nothing here may add them.

- [ ] **Step 1: Write the failing tests** — `LOCALE_INDEX_ROUTES` (both the TS and the `.mjs` copy) contains `atlas`, and the route helper produces `/en/atlas/` + `/fa/atlas/` with mutual alternates.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the page shell (frontmatter loads the snapshot, renders `AtlasPageContent`) and the registry entries. Do **not** add a navigation entry (spec §4.3 defers that).
- [ ] **Step 4: Run — expect green**, then build and confirm the route exists:

```bash
npm run build && ls dist/en/atlas/index.html dist/fa/atlas/index.html && npm run validate:seo
```
Expected: both files exist; `validate:seo` passes (canonical, alternates, sitemap entry present).
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the bilingual Atlas routes"`

---

### Task 6: Region, semantic index and content states

**Files:**
- Create: `src/components/atlas/AtlasPageContent.astro`, `src/components/atlas/AtlasIndex.astro`
- Modify: `src/pages/{en,fa}/atlas/index.astro`
- Test: `src/components/atlas/atlas-index.test.ts` (Astro container render, mirroring `src/components/about/product-about.test.ts` style)

**Interfaces:**
- Produces: server markup with `data-atlas-region`, `data-atlas-status="ready|empty|unavailable|invalid"`, `data-atlas-revision`, `data-atlas-etag`, `data-atlas-presentation="list"` (the server-rendered default before capability detection), the payload script, the semantic index (`<ul>` of nodes with canonical links, `<ol>` of relations with labelled endpoints, group sections) and honest content states for the other three statuses
- Consumes: `AtlasSnapshot`

- [ ] **Step 1: Write the failing tests** — the ready render contains one list item per visible node with its canonical `href`, one relation item per visible relation whose endpoints resolve to labels, a group section per group, and the payload script with escaped `<`; the unavailable render contains no payload script, no list, and the honest message; the invalid render states that published data failed validation and shows nothing invented.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run — expect green**, then build and inspect the hermetic page:

```bash
npm run build:atlas 2>/dev/null || npm run build
grep -o 'data-atlas-status="[a-z]*"' dist/en/atlas/index.html | head -1
```
Expected: with no API configured the local build prints `data-atlas-status="unavailable"` (the honest state), and the E2E build (fixture-backed) prints `ready`. Record both.
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): render the semantic index and honest content states"`

---

### Task 7: Runtime refresh

**Files:**
- Create: `src/lib/atlas/refresh.ts`
- Test: `src/lib/atlas/refresh.test.ts`

**Interfaces:**
- Produces: `refreshAtlas(options: {locale, embedded: {revision, etag}, fetchFn, onAdopt, onKeep}): Promise<AtlasRefreshOutcome>` with outcomes `'not-modified' | 'adopted' | 'kept-older' | 'kept-invalid' | 'kept-error' | 'absent'`, and `data-atlas-refresh` written by the caller
- Consumes: `validateAtlasPayload`

- [ ] **Step 1: Write the failing tests**

```ts
it('sends If-None-Match and keeps the snapshot on 304', async () => {
  const fetchFn = vi.fn().mockResolvedValue(new Response(null, { status: 304 }))
  const outcome = await refreshAtlas({ locale: 'en', embedded: { revision: '1-2026', etag: '"1-abc"' }, fetchFn, onAdopt: vi.fn(), onKeep: vi.fn() })
  expect(fetchFn).toHaveBeenCalledWith('/api/atlas/en', expect.objectContaining({ headers: expect.objectContaining({ 'If-None-Match': '"1-abc"' }) }))
  expect(outcome).toBe('not-modified')
})


it('adopts a newer revision and preserves the selection when the key survives', async () => { /* … */ })
it('clears the selection when the selected key disappeared', async () => { /* … */ })


it('keeps the snapshot when the payload is invalid or the request fails', async () => {
  for (const bad of [invalidPayload, new Error('offline')]) { /* … */ expect(outcome).toMatch(/^kept-/) }
})


it('never adopts an unknown contract version', async () => { /* outcome === 'kept-invalid' */ })
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with `(publishedAt, id)` ordering (never a client clock) and no reader identifier in the request.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add conditional runtime refresh"`

---

### Task 8: Draft-preview shell (declared dependency of Plan B)

**Files:**
- Create: `src/lib/atlas/preview.ts`, `src/pages/en/atlas/preview/index.astro`, `src/pages/fa/atlas/preview/index.astro`
- Modify: `src/components/atlas/AtlasPageContent.astro` (accept a preview payload + preview label), `astro.config.mjs` (sitemap exclusion for `/atlas/preview/`), `src/lib/seo-route-registry.ts` + `scripts/seo-route-registry.mjs` (assert **exclusion**, not inclusion)
- Test: `src/lib/atlas/preview.test.ts`

**Interfaces:**
- Produces: `consumePreviewFragment(history, location): string | null` — reads the capability from `location.hash` (`#token=…`), keeps it in memory only, and calls `history.replaceState(null, '', location.pathname + location.search)` **before** anything else, returning the capability or `null` when the fragment is absent or malformed.
- Produces: `fetchPreviewSnapshot(locale, capability)` calling `GET /api/atlas/preview?locale=<locale>` with `Authorization: Bearer <capability>` — **Plan A task 15's** endpoint, whose capabilities are minted by **Plan B task 6**. `?locale` is the only query parameter; the capability never appears in a URL, a log, a `Referer`, history entry or any storage.
- Produces: the preview route renders the same region markup as `/…/atlas/` with `data-atlas-preview="true"` and the real presentation when the capability is valid, `<meta name="robots" content="noindex, nofollow">` always, and the honest **active** framing (`data-atlas-preview="false"`) when there is no valid capability — never an error page and never a hint that a draft exists.
- Critical rule: no code path in this module may touch `localStorage`, `sessionStorage`, `document.cookie`, `indexedDB` or `sendBeacon`; a test asserts the module source contains none of those identifiers.
- Consumes: `validateAtlasPayload` (Task 2) and the presentation entry (Task 12) — the preview renders through the same code path as the public Atlas, so what the owner reviews is what will ship.
- Consumed by: **Plan B task 17** (the admin's read-only 3D preview frames this route with the minted `preview_url`, fragment included).

- [ ] **Step 1: Write the failing tests**

```ts
it('reads the capability from the fragment and strips it before any fetch', () => {
  const replaceState = vi.fn()
  const capability = consumePreviewFragment({ replaceState } as any,
                                            { hash: '#token=cap.abc', pathname: '/en/atlas/preview/', search: '' } as any)
  expect(capability).toBe('cap.abc')
  expect(replaceState).toHaveBeenCalledWith(null, '', '/en/atlas/preview/')
})


it('sends the capability only in the Authorization header', async () => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => payloadFixture })
  await fetchPreviewSnapshot('fa', 'cap.abc', { fetch: fetchMock, apiBase: 'https://example.test' })
  const [url, init] = fetchMock.mock.calls[0]
  expect(url).toBe('https://example.test/api/atlas/preview?locale=fa')
  expect(url).not.toContain('cap.abc')
  expect(init.headers.Authorization).toBe('Bearer cap.abc')
})


it('falls back to the honest active framing when the capability is rejected', async () => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: false, status: 403, json: async () => ({ code: 'preview_forbidden' }) })
  expect(await fetchPreviewSnapshot('en', 'cap.expired', { fetch: fetchMock, apiBase: 'https://example.test' }))
    .toEqual({ state: 'unavailable', preview: false })
})


it('never persists the capability anywhere', () => {
  const source = readFileSync('src/lib/atlas/preview.ts', 'utf8')
  for (const forbidden of ['localStorage', 'sessionStorage', 'document.cookie', 'indexedDB', 'sendBeacon']) {
    expect(source).not.toContain(forbidden)
  }
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the two shell routes (each renders `AtlasPageContent` with the preview flag), the fragment helper, the authorized fetch, and the `noindex, nofollow` metadata. Register the routes in Astro only — **never** in `LOCALE_INDEX_ROUTES`.
- [ ] **Step 4: Run — expect green**, then prove the shells are non-indexable and the fragment leaves no trace:

```bash
npm test -- src/lib/atlas/preview.test.ts
npm run build && ls dist/en/atlas/preview/index.html dist/fa/atlas/preview/index.html
grep -c "noindex, nofollow" dist/en/atlas/preview/index.html
grep -c "atlas/preview" dist/sitemap-0.xml || echo "absent from the sitemap (correct)"
npm run validate:seo
```
Expected: both shells built; `noindex, nofollow` present; the preview routes absent from the sitemap; `validate:seo` green.
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the fragment-scoped draft preview shell"`

---

### Task 9: Selection state and URL codec

**Files:**
- Create: `src/lib/atlas/selection.ts`, `src/lib/atlas/url-state.ts`
- Test: `src/lib/atlas/selection.test.ts`, `src/lib/atlas/url-state.test.ts`

**Interfaces:**
- Produces: `createSelectionModel(payload)` → `{ state, selectNode(key), selectRelation(key), clear(), subscribe(fn), exists(key) }` publishing `data-atlas-state="overview|node|relation"`; `parseFocus(search): {kind:'node'|'relation', key:string} | null`; `serializeFocus(focus)` → `node:<key>` / `relation:<key>`; `buildFocusUrl(href, focus | null)`; `applyFocus(history, focus)` (pushState, never a reload); `readFocusFromLocation()`
- Produces: unknown/deleted keys resolve to `null` selection plus the reason `'unknown'`
- The URL grammar is exactly the spec's: `/en/atlas/?focus=node:<public-key>` and `/fa/atlas/?focus=relation:<public-key>` (spec §16.3). The `node:`/`relation:` discriminator is parsed from the value, and the composed relation key's `~` characters are percent-encoded by `serializeFocus` and accepted in both raw and encoded form by `parseFocus`.

- [ ] **Step 1: Write the failing tests**

```ts
it('round-trips node and relation focus with the node:/relation: discriminator', () => {
  const node = { kind: 'node' as const, key: 'research-area-1a2b3c4d' }
  expect(buildFocusUrl('/en/atlas/', node)).toBe('/en/atlas/?focus=node:research-area-1a2b3c4d')
  expect(parseFocus('?focus=node:research-area-1a2b3c4d')).toEqual(node)

  const relation = { kind: 'relation' as const, key: 'a-11111111~uses~b-22222222' }
  expect(buildFocusUrl('/en/atlas/', relation)).toBe('/en/atlas/?focus=relation:' + encodeURIComponent(relation.key))
  expect(parseFocus('?focus=relation:' + encodeURIComponent(relation.key))).toEqual(relation)
  expect(parseFocus('?focus=relation:' + relation.key)).toEqual(relation)   // raw form accepted too
})


it('treats unknown, malformed and invisible keys as no selection', () => {
  expect(parseFocus('?focus=node:nope')).toEqual({ kind: 'node', key: 'nope' })  // parse is grammar-only
  expect(parseFocus('?focus=nope')).toBeNull()                                  // missing discriminator
  expect(parseFocus('?focus=relation:not-a-relation-key')).toBeNull()           // wrong key arity
  expect(createSelectionModel(payload).resolve('node:nope')).toEqual({ selected: null, reason: 'unknown' })
})


it('never encodes camera state', () => {
  const url = buildFocusUrl('/en/atlas/', { kind: 'node', key: 'research-area-1a2b3c4d' })
  expect(url).not.toMatch(/yaw|pitch|zoom|hover/)
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the model plus a thin history adapter; `popstate` re-reads the URL and re-applies (Task 10 wires it to the DOM).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add shared selection state and URL codec"`

---

### Task 10: Search, filters and neighbourhood

**Files:**
- Create: `src/lib/atlas/search.ts`, `src/lib/atlas/filters.ts`, `src/lib/atlas/neighborhood.ts`
- Test: `src/lib/atlas/search.test.ts`, `src/lib/atlas/filters.test.ts`, `src/lib/atlas/neighborhood.test.ts`

**Interfaces:**
- Produces: `buildSearchIndex(payload)` → `search(query, {limit})` returning ranked `{kind, key, label, type}`; `normalizeFa(text)`; `filterOptions(payload)` (the six fixed filters mapped to `filterVisible` types), `filterSet(payload, filterKey)` (dim-first membership); `neighborhoodOf(payload, nodeKey)` → `{parents, children, incoming, outgoing, byType}`

- [ ] **Step 1: Write the failing tests** — Persian normalisation folds `ي/ك`, Persian and Arabic-Indic digits, ZWNJ, tatweel; prefix beats substring; aliases and canonical titles match; ranking is `(-importance, key)`; `filterSet` never returns a topology change (the payload is untouched — assert identity); `neighborhoodOf` is cycle-safe on a fixture containing a general cycle and returns both parents for a multi-parent node.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** (all three modules pure).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add search, filters and neighbourhood computation"`

---

### Task 11: Inspector projection

**Files:**
- Create: `src/lib/atlas/inspector.ts`
- Test: `src/lib/atlas/inspector.test.ts`

**Interfaces:**
- Produces: `nodeInspectorModel(payload, key)` and `relationInspectorModel(payload, key)` returning ordered sections `[{id, heading, items[]}]` where each item is `{key, label, type, href?, relationLabel?}`; **only sections with at least one real member are returned**; canonical record included when present; empty selection returns `{sections: [], prompt}`

- [ ] **Step 1: Write the failing tests** — a node with no publications has no `publications` section; a node with two parents lists both under `parents`; the relation model carries source, target, forward/inverse label, explanation (when present) and direction; a node whose canonical record is missing omits the canonical section and still renders.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** on top of `neighborhood.ts`; every neighbour item groups by the neighbour's node type so the lists can never contradict the drawn relations.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add inspector data projection"`

---

### Task 12: Layout consumption

**Files:**
- Create: `src/lib/atlas/layout.ts`
- Test: `src/lib/atlas/layout.test.ts`

**Interfaces:**
- Produces: `resolveLayout(payload)` → `{ nodes: Array<{key, x, y, z, radius, tier, drawOrder}>, bounds, center }`; `radiusFor(node)`; `tierFor(node)` (`primary` when `importance ≥ 80`, else `fine`); `labelTierFor(node)` (`always` ≥ 80 capped at 10 by importance, `on-demand` 40–79, `selected` < 40); `assertComplete(layout)` (every visible node has finite coordinates)

- [ ] **Step 1: Write the failing tests**

```ts
it('consumes stored coordinates and never re-computes them', () => {
  const layout = resolveLayout(payloadFixture)
  expect(layout.nodes.map(n => [n.key, n.x, n.y, n.z])).toEqual(
    payloadFixture.nodes.filter(n => n.visible).map(n => [n.key, n.position.x, n.position.y, n.position.z]))
})


it('derives radius and tiers from importance deterministically', () => {
  expect(tierFor({ importance: 80 })).toBe('primary')
  expect(tierFor({ importance: 79 })).toBe('fine')
  expect(radiusFor({ importance: 100 })).toBeGreaterThan(radiusFor({ importance: 40 }))
})


it('flags a missing coordinate instead of inventing one', () => {
  expect(() => assertComplete(resolveLayout(withoutCoordinate(payloadFixture)))).toThrow(/missing coordinate/i)
})


it('is stable across calls and independent of node order', () => {
  expect(resolveLayout(payloadFixture)).toEqual(resolveLayout({ ...payloadFixture, nodes: [...payloadFixture.nodes].reverse() }))
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** (pure; no attraction, no relaxation — those are Plan A's).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add deterministic layout consumption"`

---

### Task 13: 2D SVG projection engine

**Files:**
- Create: `src/lib/atlas/projection-2d.ts`, `src/components/atlas/AtlasProjection2d.astro`
- Modify: `src/pages/{en,fa}/atlas/index.astro`
- Test: `src/lib/atlas/projection-2d.test.ts`

**Interfaces:**
- Produces: `project2d(payload, { mode: 'mobile-overview' | 'webgl-fallback' | 'about-preview', viewport: {width, height}, focusKey })` → `{ viewBox, nodes: Array<{key, cx, cy, r, tier, labelOffset}>, edges: Array<{key, path}>, transform }`
- Produces: `selectOverviewNodes(payload, {mode})` — mobile 8–15 (`featured` first, then `(-importance, key)`, `hidden` excluded, anchor always included), about-preview 6–10 with the same rule and a smaller cap
- Consumes: `layout.resolveLayout`

- [ ] **Step 1: Write the failing tests**

```ts
it('is deterministic for the same input and viewport', () => {
  expect(project2d(payloadFixture, { mode: 'mobile-overview', viewport: { width: 390, height: 520 }, focusKey: null }))
    .toEqual(project2d(payloadFixture, { mode: 'mobile-overview', viewport: { width: 390, height: 520 }, focusKey: null }))
})


it('selects 8–15 nodes for the mobile overview and honours hidden', () => {
  const keys = selectOverviewNodes(payloadFixture, { mode: 'mobile-overview' }).map(n => n.key)
  expect(keys.length).toBeGreaterThanOrEqual(8)
  expect(keys.length).toBeLessThanOrEqual(15)
  expect(keys).toContain(payloadFixture.anchorKey)
  expect(keys).not.toContain(payloadFixture.hiddenKey)
})


it('keeps every projected node inside the viewBox', () => {
  const projected = project2d(payloadFixture, { mode: 'mobile-overview', viewport: { width: 390, height: 520 }, focusKey: null })
  for (const node of projected.nodes) {
    expect(node.cx - node.r).toBeGreaterThanOrEqual(0)
    expect(node.cy - node.r).toBeGreaterThanOrEqual(0)
    expect(node.cx + node.r).toBeLessThanOrEqual(390)
    expect(node.cy + node.r).toBeLessThanOrEqual(520)
  }
})


it('reduces the about-preview selection to at most 10 and never fabricates filler', () => {
  expect(selectOverviewNodes(payloadFixture, { mode: 'about-preview' }).length).toBeLessThanOrEqual(10)
  expect(selectOverviewNodes(smallPayload, { mode: 'about-preview' }).map(n => n.key)).toEqual(smallPayload.visibleKeys)
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the pure projection plus the Astro presentation (paths as `<path>`, nodes as `<g>`; the component renders **no** interactive attributes — the HTML controls own interaction, per spec §14.1).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the 2D SVG projection engine"`

---

### Task 14: Inspector and controls components

**Files:**
- Create: `src/components/atlas/AtlasInspector.astro`, `src/components/atlas/AtlasControls.astro`
- Modify: `src/components/atlas/AtlasPageContent.astro`
- Test: `src/components/atlas/AtlasInspector.test.ts`

**Interfaces:**
- Produces: the **node inspector** and the **relation inspector** — server-rendered blocks for every node and relation (only the selected one visible once JS runs; the first one hidden when nothing is selected), a `role="status"` announcement target, the search input, six filter chips (native buttons/radios), and view controls (`Zoom in`, `Zoom out`, `Focus`, `Reset`, `Clear`, `Back to overview`) as native `<button>`s
- Consumes: `inspector.ts` models, `filterOptions`

- [ ] **Step 1: Write the failing tests** — every node and relation in the fixture has an inspector block; with no selection the prompt shows and no block is visible; the six filters match `filterOptions` exactly and never include the anchor type; every control is a `<button>` or `<input>` with an accessible name; each control is ≥ 44 px by CSS contract (assert via the stylesheet rule, since the container test has no layout).
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): render the inspector and control surfaces"`

---

### Task 15: Enhancement orchestrator and capability detection

**Files:**
- Create: `src/lib/visual/atlas/enhancement.ts`
- Modify: `src/components/atlas/AtlasPageContent.astro` (the inline module script)
- Test: `src/lib/visual/atlas/enhancement.test.ts`

**Interfaces:**
- Produces: `enhanceAtlasRegion(region, options)` returning `{state: 'enhanced'|'fallback'|'list', reason, dispose}`; writes `data-atlas-presentation`, `data-atlas-enhancement`, `data-atlas-reason`, `data-atlas-state`; decides 3D vs 2D from `WebGLRenderingContext` availability + `matchMedia('(min-width: 1024px)')`
- Consumes: `refresh.ts`, `selection.ts`, `url-state.ts`, and (lazily) `./scene`, `./controls`, `./picking`, the RU `labels` module

- [ ] **Step 1: Write the failing tests** — eligible region + capable environment ⇒ `enhanced`; no WebGL ⇒ `list`/`2d` with reason `webgl-unavailable`; `matchMedia` false ⇒ `2d`; a rejected dynamic import ⇒ `fallback` with reason `import-rejected` (inject `loadScene`); a second region never enhances (`already-enhanced`); the refresh runs before the scene is constructed and never blocks the first paint.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** mirroring the proven RU orchestration pattern (single-flight, dispose-all on `pagehide`, per-failure reasons).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the enhancement orchestrator"`

---

### Task 16: Desktop 3D scene

**Files:**
- Create: `src/lib/visual/atlas/scene.ts`
- Modify: `src/lib/visual/atlas/enhancement.ts` (lazy import)
- Test: `src/lib/visual/atlas/scene.test.ts`

**Interfaces:**
- Produces: `createAtlasScene({canvas, payload, theme, motion, onFrame, onError})` → `{ setSelection, setSelectedRelation, setHovered, setState, orbit, zoomBy, focusNode, resetView, setTheme, setMotion, setVisible, resize, render, stats, dispose }`
- Consumes (imports, never copies): `../research-universe/{scene-core, spheres, materials, presentation-profiles, theme, nodes, edges, core-object, dispose}` and `../research-universe/{labels, leaders, hit-testing}`

- [ ] **Step 1: Write the failing tests** (unit, with a stubbed core) — exactly one `THREE.WebGLRenderer` per scene; no `requestAnimationFrame` while idle (assert the scheduler is not called after construction settles); `setState('node')` emphasises the one-hop neighbourhood and dims the rest without removing anything; **full disposal** — `dispose()` releases every ledger-tracked resource and leaves no listener behind; `setMotion('reduced')` makes focus/reset instant.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the scene with two geometry tiers from the shared sphere module (add a second shared geometry `16 × 12` beside the existing `32 × 20`, both still process-wide singletons), instancing per (tier, profile), and emphasis through material/colour swaps only.
- [ ] **Step 4: Run — expect green**, then prove it renders in a browser:

```bash
npx playwright test tests/e2e/product-atlas.e2e.ts -g "desktop 3D"
```
Expected: `data-atlas-presentation="3d"`, one visible canvas, zero console errors.
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the desktop 3D scene"`

---

### Task 17: Interaction, framing and visual tiers

**Files:**
- Create: `src/lib/visual/atlas/controls.ts`, `src/lib/visual/atlas/picking.ts`
- Modify: `src/lib/visual/atlas/scene.ts`, `src/components/atlas/AtlasPageContent.astro`
- Test: `src/lib/visual/atlas/controls.test.ts`, `src/lib/visual/atlas/picking.test.ts`

**Interfaces:**
- Produces: pointer orbit, clamped wheel/button zoom, click-vs-drag classification (reuse `CLICK_SLOP_PX`/`CLICK_MAX_MS` reasoning from the RU controls), double-click and `Focus` → full focus, `Reset`, `Clear`, `Escape` clears and restores focus, mild reframe on selection (≤ 15 % distance change), inspector-aware framing via the effective-viewport CSS variable, label tiers and edge sampling tiers from `visualPriority`
- Consumes: `hit-testing.projectNodes/projectEdges/pickAt`

- [ ] **Step 1: Write the failing tests** — drag never selects; a click below the slop selects; zoom is clamped at both ends; `Escape` restores focus to the control that opened the selection; the framing call receives the effective width (stage minus inspector), not the full stage width; only `always`-tier labels exist at rest, capped at 10.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** with the pointer-capture guard so in-stage buttons keep working (the RU regression that must not return).
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add interaction, framing and visual tiers"`

---

### Task 18: Benchmark the current O(n) picking (**measurement, no implementation**)

**Files:**
- Create: `scripts/atlas-pick-benchmark.mjs`, `docs/quality/KNOWLEDGE-ATLAS-PICK-BENCHMARK.md`
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: a recorded p95 pick latency at the benchmark scale (72 nodes / 136 relations) and an explicit pass/fail against the spec's 8 ms budget

- [ ] **Step 1: Write the benchmark** — a Node script that loads `tests/fixtures/atlas/benchmark.json`, builds the projection inputs with the real modules (bundled through `esbuild` exactly as existing one-off probes do), runs 200 picks at 10 pseudo-random-but-fixed screen points, and prints `p50/p95` and the triangle/draw-call figures.
- [ ] **Step 2: Run it and record the result**

```bash
node scripts/atlas-pick-benchmark.mjs --fixture tests/fixtures/atlas/benchmark.json --iterations 200
```
Expected: prints p50/p95 and the counts. Write the numbers into `docs/quality/KNOWLEDGE-ATLAS-PICK-BENCHMARK.md` with the machine, date and command.
- [ ] **Step 3: Decide with evidence** — if p95 ≤ 8 ms, record `broad-phase: not required` and **skip Task 19 entirely** (mark it in the task log as not executed, with this evidence). If p95 > 8 ms, record `broad-phase: required` and proceed to Task 19.
- [ ] **Step 4: Commit** — `git commit -m "perf(atlas): benchmark screen-space picking at v1 scale"`

---

### Task 19: Broad-phase picking (**conditional — execute only if Task 18 says required**)

**Files:**
- Create: `src/lib/visual/atlas/picking-grid.ts`
- Modify: `src/lib/visual/atlas/picking.ts`
- Test: `src/lib/visual/atlas/picking-grid.test.ts`

**Interfaces:**
- Produces: `buildPickGrid(projectedNodes, {cellSize})` (uniform screen-space grid, rebuilt per pose), `queryGrid(grid, point, {margin})` returning candidate indices; the existing per-candidate distance test is unchanged

- [ ] **Step 1: Write the failing tests** — the grid returns a superset of the brute-force candidates (never a false negative) for 200 fixed points; the grid result equals brute force under the same slop; cell size derives from the median projected radius.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the dependency-free grid and switch `picking.ts` to it **only** when the payload exceeds `PICK_GRID_THRESHOLD = 40` nodes (small graphs keep the simpler path).
- [ ] **Step 4: Run — expect green**, then re-run the benchmark and record the improvement in the same evidence document.
- [ ] **Step 5: Commit** — `git commit -m "perf(atlas): add dependency-free broad-phase picking"`

---

### Task 20: Mobile 2D behaviour and neighbourhood view

**Files:**
- Modify: `src/components/atlas/AtlasProjection2d.astro`, `src/components/atlas/AtlasPageContent.astro`, `src/lib/visual/atlas/enhancement.ts`
- Test: `src/lib/atlas/projection-2d.test.ts` (extend), `tests/e2e/product-atlas.e2e.ts` (Task 29)

**Interfaces:**
- Produces: compact-presentation tap selection (SVG element → same selection transition as the HTML control), inspector below the graph, `View neighborhood` / `Back to overview` controls that switch the projected node set without changing topology, and 44 px minimum targets on every control

- [ ] **Step 1: Write the failing tests** — the neighbourhood view contains exactly the selected node, its parents, children and direct relations; `Back to overview` restores the previous set byte-identically; nothing in the mobile path imports the 3D scene module.
- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): add the mobile 2D experience and neighbourhood view"`

---

### Task 21: EN/FA parity, RTL and accessibility

**Files:**
- Modify: `src/styles/atlas.css`, `src/components/atlas/*.astro`, `src/lib/visual/atlas/*.ts`
- Test: `tests/e2e/product-atlas.e2e.ts` a11y section (Task 29 owns the assertions), `src/lib/atlas/parity.test.ts`

**Interfaces:**
- Produces: one stylesheet using logical properties only; a parity test proving EN and FA fixtures project to identical geometry (same keys, same coordinates, same transform) while text differs; `aria-hidden` on canvas and SVG with no tab stops; `:focus-visible` on every control; reduced-motion live subscription; `zoom 200 %`/`reflow 400 %` usability documented in the evidence
- Produces the spec §18 contract explicitly: (1) the **keyboard path** — every node and relation reachable as a native control in document order, arrow-key traversal inside the projected node set, and no canvas- or SVG-only operation; (2) **focus restoration** — `Escape` returns focus to the control that opened the selection, including after a refresh that cleared it; (3) the **screen-reader inspector** — the selected entity's name, type and its sections are reachable as text, with one polite announcement per selection change and none per frame; (4) the **no-JS index** — the semantic node/relation/group lists complete without scripting; (5) **SVG presentation semantics** — the 2D projection is `aria-hidden`, `focusable="false"`, and its interactive twins are the HTML controls
- Produces: the "60–80 node" representative-scale demonstration — the 72-node benchmark fixture drives the browser-scale assertions (spec §19.2) so the plan's scale claim is exercised at the documented size

- [ ] **Step 1: Write the failing tests**

```ts
it('projects identical geometry for both locales', () => {
  const en = project2d(enFixture, { mode: 'mobile-overview', viewport: { width: 390, height: 520 }, focusKey: null })
  const fa = project2d(faFixture, { mode: 'mobile-overview', viewport: { width: 390, height: 520 }, focusKey: null })
  expect(fa.nodes.map(n => [n.key, n.cx, n.cy, n.r])).toEqual(en.nodes.map(n => [n.key, n.cx, n.cy, n.r]))
  expect(fa.nodes.map(n => n.label)).not.toEqual(en.nodes.map(n => n.label))
})


it('keeps the canvas and the SVG out of the accessibility tree and the tab order', () => {
  const html = renderAtlasRegion(readySnapshot)
  expect(html).toContain('data-atlas-canvas aria-hidden="true"')
  expect(html).not.toMatch(/<canvas[^>]*tabindex/)
  expect(html).not.toMatch(/<svg[^>]*tabindex/)
})
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Implement** the stylesheet rules and the a11y attributes; add a `matchMedia` change listener that calls `scene.setMotion(...)` live.
- [ ] **Step 4: Run — expect green.**
- [ ] **Step 5: Commit** — `git commit -m "feat(atlas): meet locale parity, RTL and accessibility contracts"`

---

### Task 22: Performance budget verification

**Files:**
- Create: `docs/quality/KNOWLEDGE-ATLAS-PERFORMANCE.md`
- Test: `tests/knowledge-atlas/ka-performance.spec.ts`

**Interfaces:**
- Produces: recorded measurements for every budget in spec §19.2 — first interactive frame, pick p95, drag frame p95, runtime payload gzip, embedded snapshot gzip, label chip count, DOM count — plus the idle-draw assertion

- [ ] **Step 1: Write the specs** — instrument the draw entry points (all **four**: `drawArrays`, `drawElements`, `drawArraysInstanced`, `drawElementsInstanced`), count idle draws over 1500 ms of no interaction, measure payload sizes from the network layer, and count DOM nodes added by the presentation.
- [ ] **Step 2: Run against the fixture-backed build and the benchmark fixture**

```bash
npx playwright test tests/e2e/product-atlas.e2e.ts -g "idle|budget"
```
Expected: `idle draw calls == 0`; payload/snapshot sizes inside their ceilings; label chips ≤ 40.
- [ ] **Step 3: Record** every number in `docs/quality/KNOWLEDGE-ATLAS-PERFORMANCE.md` with the command and the machine. Any ceiling that cannot be met is reported, **never** fixed by raising the ceiling (spec §19.6).
- [ ] **Step 4: Commit** — `git commit -m "perf(atlas): verify the v1 performance budgets"`

---

### Task 23: Browser suite

**Files:**
- Create: `playwright.knowledge-atlas.config.ts`
- Test: `tests/e2e/product-atlas.e2e.ts`, `tests/knowledge-atlas/ka-live.e2e.ts`

**Interfaces:**
- Produces: hermetic coverage on the fixture-backed build for — desktop 3D, compact 2D, deep link (node + relation) in both locales, Back/Forward, node focus, relation focus, search selection, every filter, reduced motion, WebGL unavailable, context loss, no-JS semantics, axe scan, idle draws, representative-scale performance — and a live-API confirmation spec (topology parity + contract version against `TM_E2E_API_BASE_URL`)

- [ ] **Step 1: Write the specs** — one `test.describe` per area; assertions read only documented product facts (`data-atlas-*`, the semantic index, the inspector) and never a screenshot.
- [ ] **Step 2: Run the hermetic suite**

```bash
npx playwright test tests/e2e/product-atlas.e2e.ts
```
Expected: green, with the presentation, revision and refresh attributes asserted at every step.
- [ ] **Step 3: Run the live suite**

```bash
TM_E2E_API_BASE_URL=https://tahamohamadi.ir npx playwright test --config playwright.knowledge-atlas.config.ts
```
Expected: green (or honestly skipped with the reason recorded if the production API has no active Atlas version yet — the fixture build remains the acceptance surface until Plan D activates the migrated version).
- [ ] **Step 4: Prove the axe scan** covers `/en/atlas/`, `/fa/atlas/` in both themes.
- [ ] **Step 5: Commit** — `git commit -m "test(atlas): add hermetic and live browser suites"`

---

### Task 24: Plan C acceptance run

**Files:**
- Modify: `Docs/05-delivery/knowledge-atlas/plans/EVIDENCE-C-TASKS.md` (create)
- Test: none (verification is the evidence/command steps below; no new test file)

**Interfaces:**
- Produces: the evidence Plan D cites before switching About and retiring the About scene

- [ ] **Step 1: Full frontend gates**

```bash
npm run lint && npm run format:check && npm test && npm run validate:design && npm run build && npm run validate:seo
```
Expected: all green; build succeeds with the Atlas routes present; page count recorded.
- [ ] **Step 2: Browser gates** — the hermetic Atlas suite plus the existing suites that must not regress:

```bash
npx playwright test tests/e2e/product-atlas.e2e.ts tests/e2e/public-080-a11y-crawl.e2e.ts tests/e2e/public-300-nojs-crawl.e2e.ts
```
Expected: green, with per-spec baselines recorded separately (never one combined figure).
- [ ] **Step 3: Confirm the frozen surfaces are untouched**

```bash
git diff --stat origin/main...HEAD -- src/components/home src/components/hero src/styles/hero-sequence.css src/styles/hero-graph.css
```
Expected: **empty**. Hero v2 and Home are byte-identical to the branch base.
- [ ] **Step 4: Write the evidence file** with commands, outputs, budgets and the untouched-surface proof.
- [ ] **Step 5: Commit** — `git commit -m "docs(atlas): record Plan C acceptance evidence"`

---

**Plan C completion criterion:** `/en/atlas/` and `/fa/atlas/` work fully against Atlas API data — desktop 3D, compact/fallback 2D, deep linking, search, filters, an accessible inspector, no-JS semantics, honest fallbacks and measured budgets — with Hero v2 and Home untouched and no new dependency added.
