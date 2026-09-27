# DEAD-CODE-INVENTORY.md — Plan D Task 11 (Home/RU legacy) and Task 12 (retired GLB)

**Repository:** `Front-End/public-site` (own git repository, not a submodule)
**Branch / worktree:** `feat/knowledge-atlas-about-retirement` @ `0570358` (base `main` = `bddcebe`)
**Worktree:** `D:/Project/.atlas-worktrees/public-site-plan-d-retire`
**Produced:** 2026-09-27
**Status:** engineering evidence for the plan's Task 11/12. It is **not** owner acceptance and
**not** a production-readiness claim.

> **Repository boundary note.** This file lives in the *coordination* repository
> (`tahamohammadi-platform`), because `Docs/05-delivery/knowledge-atlas/plans/` is tracked there and
> **not** in `Front-End/public-site` (`git ls-files Docs` inside the public-site worktree returns 0
> files — its `Docs/` tree is only `architecture/`, `contracts/`, `design/`, `quality/`, which are
> untracked local directories). The retirements in §3/§4 are commits on the public-site branch.

---

## 1. Method — how each verdict was produced

A plain `grep` answers "is this name mentioned?". That is **not** sufficient, because a file can be
mentioned by a test, a doc, or a specimen and still be unreachable from a shipped page. Two of the
files below are named in this very plan, and a naive grep would have retired a **live** module.

Each candidate was therefore resolved with a **transitive import-graph reachability scan** over the
real entry points:

* **Entry set A (production):** every file under `src/pages/**` (74 entries) **plus** every Astro
  `<script src="…">` bundle entry. The second part is not optional: `src/pages/{en,fa}/atlas/index.astro`
  mounts the Atlas 3D runtime through `<script src="../../../scripts/atlas-runtime.ts">`, which lazily
  `import()`s `lib/visual/atlas/scene`. A scan walking only static `src/pages/**` imports reports that
  entire live subtree as dead.
* **Entry set B (`DESIGN_ATLAS` specimen build):** `src/atlas/AtlasRoute.astro`. The plan's
  three-part test (card item 15) requires "no dependency of the `DESIGN_ATLAS` specimen build", so
  this is a separate reachability root, not a subset of A.
* Edges: `from '…'`, `import(…)`, `require(…)`, bare `import '…'`, with extension/`index`
  resolution. Reachability is a BFS over those edges.

The scan is a **read-only analysis tool** and is **not committed**. Its summary on the current tree:

```
== ENTRIES ==
page entries: 74
atlas entry  : 1 (DESIGN_ATLAS specimen route)
reachable from pages only  : 252
reachable from atlas only  : 99
union reachable            : 279
```

Three independent lines back each verdict, all pasted verbatim: (1) repository-wide textual grep for
the module name and each exported symbol; (2) the reachability verdict (PROD / atlas / DEAD);
(3) the design spec's own pre-existing audit, which independently reached the same conclusion
(`KNOWLEDGE-ATLAS-V1-DESIGN-SPEC.md` §3, C13/C14/C17 — quoted in §2 and §5).

---

## 3. Task 11 — inventory, per file

**imports outside tests** lists every importing path, verbatim from the greps below.

### 3.1 `src/components/hero/HeroGraph.astro` — RETIRE

* **imports outside tests:** **none.** No file under `src/`, `tests/`, `scripts/`, `contracts/`,
  `.github/` imports it except tests. Repository-wide grep for `HeroGraph`:

```
src\components\hero\GraphNodeList.astro:8:  import type { HeroGraphNode } from '../../lib/hero-graph-content'
src\components\hero\hero-contract.test.ts:24: import HeroGraph from './HeroGraph.astro'
src\components\hero\HeroGraph.astro:16:     import type { HeroGraphModel } from '../../lib/hero-graph-content'
src\lib\hero-graph-resolve.test.ts:4:        import HeroGraph from '../components/hero/HeroGraph.astro'
```

  Remaining hits are the *symbol* `HeroGraphModel` / `adaptHeroGraph` from `lib/hero-graph-content`
  (a **different, live** module — §3.6) and prose in
  `src/components/home/HomeResearchGraph.astro:4` and `hero-contract.test.ts:326`
  (`expect(hero).not.toContain('HeroGraph')` — an assertion Home does **not** use it).
* **production consumer:** **none.** Reachability `DEAD` — absent from both the 252-file production
  closure and the 99-file Atlas closure. The page chain is
  `src/pages/{en,fa}/index.astro` → `HomeContent.astro` → `HomeHero.astro` → `HeroSequence.astro`;
  `HomeHero.astro` renders `HeroSequence` and contains no `HeroGraph` import.
* **replacement coverage:** Home's presentation is Hero v2 (`HeroSequence.astro` →
  `src/lib/visual/hero-sequence.ts`, both hard-protected and untouched). The interactive research
  surface moved to the Atlas 2D preview: `AboutAtlasPreview.astro` → `AtlasProjection2d.astro`,
  covered by `tests/e2e/product-about.e2e.ts` and `src/components/about/AboutAtlasPreview.test.ts`.
* **verdict: retire.** The design spec recorded this as C14: *"The Home Research Universe path is
  unwired: `HeroGraph.astro` is rendered by no page."* A prior audit
  (`docs/quality/hero-v2-stage4_2/FINAL-CLOSEOUT.md:53`) deliberately left it in place only because
  `src/lib/hero-graph-resolve.test.ts:305` still rendered it. Tasks 9/10 removed the stale RU specs;
  this task removes the last render-level references.

### 3.2 `src/components/hero/GraphNodeList.astro` — RETIRE

* **imports outside tests:** `src\components\hero\HeroGraph.astro:30: import GraphNodeList from './GraphNodeList.astro'`
  — that importer is itself retired here, so the set becomes empty.
* **production consumer:** none. Reachability `DEAD`.
* **replacement coverage:** the native `<details>`/`<summary>` node disclosure was Home-graph-only;
  the Atlas 2D preview renders its own SVG projection (`src/lib/atlas/projection-svg.ts` via
  `AtlasProjection2d.astro`).
* **verdict: retire** (sole importer retired in the same commit).


| File | Reachability | Verdict | Why |
| --- | --- | --- | --- |
| `scene-core.ts` | PROD + atlas | **KEEP** | imported by `atlas/scene.ts:37,70` |
| `spheres.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:38` |
| `nodes.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:43` |
| `edges.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:47` |
| `core-object.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:48` |
| `layout.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:58` |
| `presentation-profiles.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:59` |
| `theme.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:63` |
| `hit-testing.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:67`, `atlas/picking.ts:23` |
| `labels.ts` | PROD + atlas | **KEEP** | `atlas/scene.ts:68` |
| `materials.ts` | PROD + atlas | **KEEP** | via `nodes.ts:33` (reached by `atlas/scene.ts`) |
| `dispose.ts` | PROD + atlas | **KEEP** | `UniverseLedger`, imported by `nodes/edges/materials/scene-core` |
| `leaders.ts` | PROD + atlas | **KEEP** | via `labels.ts:28` (`atlas/scene.ts:68`) |
| `home-scene.ts` | DEAD | **RETIRE** | no importer anywhere |
| `home-motion.ts` | DEAD | **RETIRE** | only importer is `universe.test.ts:67` |
| `about-scene.ts` | DEAD | **RETIRE** | no importer; About RU mount removed by Task 8 |
| `about-controls.ts` | DEAD | **RETIRE** | only importer is `universe.test.ts:75` |
| `enhancement.ts` | DEAD | **RETIRE** | only importers are `HeroGraph.astro:362` (retired here) and `universe.test.ts:77` |

Verbatim grep for the RU-retired files across `src`, `tests`, `scripts`:

```
=== RU enhancement.ts importers ===
src\components\hero\HeroGraph.astro:361: // fallback untouched (see research-universe/enhancement).
src\components\hero\HeroGraph.astro:362: import { enhanceUniverseRegion } from '../../lib/visual/research-universe/enhancement'
src\lib\research-universe\universe.test.ts:77: import { validateUniversePayload } from '../visual/research-universe/enhancement'

=== validateUniversePayload / enhanceUniverseRegion users ===
src\components\hero\HeroGraph.astro:362,372
src\lib\research-universe\universe.test.ts:77,1159,1160,1173,1176,1178,1183,1187,1191

### 3.4 `src/lib/research-universe/*` — the model / preset layer

* **`adapter.ts` — RETIRE.** imports outside tests: `src\components\hero\HeroGraph.astro:19`
  (retired here) and `src\lib\research-universe\universe.test.ts:20`. No production consumer.
  *Replacement:* `hero-graph-content.ts` (`adaptHeroGraph`) is the live equivalent, already covered by
  `src/lib/hero-graph-content.test.ts`.
* **`home-preset.ts` — RETIRE.** imports outside tests: `src\components\hero\HeroGraph.astro:20`
  and `universe.test.ts:22`. No production consumer.
* **`about-preset.ts` — RETIRE.** imports outside tests: **none** — only
  `src\lib\research-universe\universe.test.ts:21`. Orphaned when Task 8 removed the About RU mount.
* **`hierarchy.ts` — RETIRE.** imports outside tests: `src\components\hero\GraphNodeList.astro:10`
  and `universe.test.ts:25`. No production consumer.
* **`model.ts` — KEEP (with reason).** Not part of the dead Home path: a live **type** dependency of
  the Atlas scene.

```
src\lib\visual\atlas\scene.ts:69:      import type { UniverseNodeKind } from '../../research-universe/model'
src\lib\visual\research-universe\about-scene.ts:32 / enhancement.ts:39 / home-scene.ts:30
src\lib\visual\research-universe\layout.ts:28 / materials.ts:28 / nodes.ts:50 / presentation-profiles.ts:25
```

  Reachability `PROD + atlas`. `UNIVERSE_MODEL_VERSION` / `toUniverseRendererPayload` are also used
  by `universe.test.ts`'s payload guards. **Keep** — removing them would touch the live Atlas scene.
* **`universe.test.ts` — RETIRE (with its subjects).** Reachability `DEAD`; a test whose entire
  subject set is retired. It is **not** a loss of live coverage: each production module it covers is
  separately covered by `src/lib/hero-graph-content.test.ts`, `src/lib/visual/atlas/scene.test.ts`,
  and `src/lib/visual/research-universe/presentation.test.ts`.

### 3.5 `src/lib/visual/hero-enhancement.ts` — RETIRE

* **imports outside tests:** **none.** Only `src\components\hero\hero-enhancement.test.ts:12`.
  Reachability `DEAD`.
* **production consumer:** none. This is the CA-06 progressive-enhancement loader for the retired hero
  graph. The design spec lists it as part of the legacy engine, C13: *"a legacy CA-03/04/05 engine
  (`graph-scene.ts`, `graph-controller.ts`, `graph-layout.ts`, `graph-motion.ts`,

### 3.6 Modules explicitly KEPT because live code still needs them

| File | Reachability | Live consumer (verbatim) |
| --- | --- | --- |
| `src/lib/visual/scene-contract.ts` | PROD + atlas | `src\components\gateway\GatewayPortal.astro:48`, `atlas/scene.ts:32`, `HeroGraph.astro:28` |
| `src/lib/visual/graph-scene.ts` | atlas | `src\components\hero\GraphInteractionDemo.astro:455`, `GraphSceneDemo.astro:366` |
| `src/lib/visual/graph-controller.ts` | atlas | `src\components\hero\GraphInteractionDemo.astro:456` |
| `src/lib/visual/graph-motion.ts` | atlas | `src\components\hero\GraphInteractionDemo.astro:457` |
| `src/lib/visual/graph-layout.ts` | atlas | reached via `graph-scene.ts` |
| `src/components/hero/GraphInteractionDemo.astro` | atlas | `src\atlas\sections\GraphInteractionSection.astro:13` |
| `src/components/hero/GraphSceneDemo.astro` | atlas | `src\atlas\sections\GraphSceneSection.astro:16` |
| `src/components/hero/HeroSequence.astro` | PROD | `src\components\home\HomeHero.astro:11` |
| `src/lib/visual/hero-sequence.ts` | PROD | `src\components\hero\HeroSequence.astro:188` — **hard-protected, untouched** |
| `src/lib/visual/atlas/scene.ts` | PROD | `src\scripts\atlas-runtime.ts:263` (dynamic), mounted by `src\pages\{en,fa}\atlas\index.astro:19` |
| `src/lib/hero-graph-content.ts` | PROD + atlas | `src\lib\home-content.ts:12`, `lessons-content.ts:10`, `story-content.ts:8`, `teaching\LessonDetailContent.astro:13` |
| `src/lib/visual/portal-scene.ts`, `gateway-motion.ts` | PROD | gateway route |
| `src/components/home/**` | PROD | **hard-protected, untouched** |

### 3.7 The shared `.ru-*` CSS base — KEEP (constraint-checked, not assumed)

The brief warned: *"the shared `.ru-*` base must be KEPT if `HeroGraph.astro` still uses it."*
Verified rather than assumed, with a repository-wide grep for `ru-` outside the stylesheet itself:

```
src\components\hero\HeroGraph.astro:153,155,160,167,198,200,203,213,229,257,272,276,277,284,287,290,302,303,304,309,313,318,325
    (.ru-track/.ru-stage/.ru-canvas/.ru-labels/.ru-edges/.ru-edge/.ru-panel*)
src\lib\visual\research-universe\labels.ts:61,70,75,88,93,203,205,208,224
    ('ru-label', 'ru-labels--editorial', '--ru-label-gap', 'ru-label__title', 'ru-label__meta')
src\lib\visual\research-universe\leaders.ts:68                            ('ru-leaders')
src\lib\visual\research-universe\spheres.ts:55                            ('ru-shared-sphere')
src\lib\visual\research-universe\layout.ts:420, presentation-profiles.ts:258, labels.ts:224   (CSS custom-property names only)
src\lib\visual\research-universe\presentation.test.ts:118                 ('ru-shared-sphere')
src\lib\research-universe\universe.test.ts:984                            (a CSS-variable name, in a comment)
```

**Verdict: KEEP — the `.ru-*` base is required by live production code, not by `HeroGraph.astro`.**

---

## 4. Task 11 — commits created

Two commits, each independently revertible, neither touching `src/components/home/**`,
`hero-sequence.ts`, or `src/styles/hero-*.css`.

**Commit 1 — `chore(atlas): retire the unwired Home research-universe hero path`**
Deletes `src/components/hero/HeroGraph.astro`, `src/components/hero/GraphNodeList.astro`,
`src/lib/research-universe/{adapter,home-preset,about-preset,hierarchy,universe.test}.ts`,
`src/lib/visual/hero-enhancement.ts`,
`src/lib/visual/research-universe/{home-scene,home-motion,about-scene,about-controls,enhancement}.ts`,
and `src/components/hero/hero-enhancement.test.ts`.
Trims the now-dangling assertions from `src/components/hero/hero-contract.test.ts` and
`src/lib/hero-graph-resolve.test.ts`.

**Commit 2 — `test(atlas): retarget the runtime-purity scan onto the Atlas scene`**
Updates `src/lib/visual/research-universe/runtime-purity.test.ts` only. That test is a **source scan
over its own directory** (`readdirSync(HERE)`), and its final assertion pins an explicit module list
including `home-scene.ts` and `about-scene.ts`. After commit 1 those files no longer exist, so the
"still contains the modules the direction is made of" guard would fail. The fix retargets the
required-list onto the modules the **Atlas** scene actually consumes. The two *substantive* bans (no
glTF loader import; no `signature-v*.glb` / `research-universe/models` reference) are **kept verbatim
and unweakened** — the plan forbids weakening this test to make a move pass, so they are byte-identical.

This is a separate commit precisely so reverting the retirement cannot leave a weakened purity guard
behind, and vice versa.

---

## 5. Task 12 — retired GLB handling

### 5.1 No runtime consumer (plan Step 1)

```
$ grep -rn "research-universe/models|signature-v1|signature-v3" src tests scripts docs
(no output)
```

The plan expects "no runtime reference; the purity test is the only mention (it asserts the
absence)". The stricter grep above **excludes `runtime-purity.test.ts` entirely** and still returns
nothing. Confirmed independently — the GLB names appear nowhere in `src/`, `tests/`, `scripts/`,
`docs/`, or in the built output:


### 5.3 Provenance — checked before touching owner artwork

Per the brief, the Asset Promotion Ledger and Design-Assets provenance were checked **before** any
move:

* **Asset Promotion Ledger** (`Docs/04-design/ASSET-PROMOTION-LEDGER.md`): grep for
  `research.universe|glb|GLB|signature` → **no rows**. These assets were never promoted for runtime
  use, so nothing authorises shipping them.
* **Design-Assets** (`D:/Project/tahamohammadi-platform/Design-Assets/research-universe/`) exists and
  is the documented non-shipping home. `Design-Assets/research-universe/export/` already holds
  `taha-research-universe-signature-v3.glb` and `-v2.glb`.
* **Byte-identical provenance confirmed by SHA-256** for v3:

```
public/research-universe/models/taha-research-universe-signature-v3.glb
  D633AADE47311B69C18D4B13F8755B6F8B8AA8677488FCAD709E5552126D70BD
Design-Assets/research-universe/export/taha-research-universe-signature-v3.glb
  D633AADE47311B69C18D4B13F8755B6F8B8AA8677488FCAD709E5552126D70BD
public/research-universe/models/taha-research-universe-signature-v1.glb
  CDD963E1BD0B35C0DEFBAB8F91A59965DE06A57BB34555C13EE864C755DC4F20
```

* **`Design-Assets/research-universe/README.md:17`** documents v1's canonical location as
  `Front-End/public-site/public/research-universe/models/taha-research-universe-signature-v1.glb`, and
  its source of truth is the tracked `.blend` at
  `Design-Assets/research-universe/source/taha-research-universe-signature-v1.blend`. **v1's
  provenance is therefore the `.blend`, not the shipped GLB** — the GLB is a regenerable export
  (`build_ru_signature_v1.py --glb …`).

### 5.4 Verdict and what was done

The plan's Step 3 asks for the artefacts to be moved into a non-shipping location that preserves
history, with the purity test's path expectation updated so the ban stays enforced from the new
location.

**Deliberate deviation, stated plainly:** the two binaries were **not** copied into

---

## 6. Deliberate non-removals (each with the reason and the live consumer)

| Item | Why not removed |
| --- | --- |
| `src/lib/research-universe/model.ts` | live type dependency of the Atlas 3D scene (`atlas/scene.ts:69`) |
| `src/lib/visual/research-universe/{scene-core,spheres,nodes,edges,core-object,layout,presentation-profiles,theme,hit-testing,labels,materials,dispose,leaders}.ts` | live — imported by `atlas/scene.ts` and/or `atlas/picking.ts` (§3.3) |
| `src/lib/visual/{graph-scene,graph-controller,graph-layout,graph-motion}.ts` | dependency of the `DESIGN_ATLAS=1` specimen build (fails part 2 of the three-part test) |
| `src/components/hero/{GraphInteractionDemo,GraphSceneDemo}.astro` | Atlas specimens, mounted by `src/atlas/sections/*` |
| `src/styles/research-universe.css` (whole file) | the shared `.ru-*` base is emitted by the live Atlas scene via `labels.ts` / `leaders.ts` / `spheres.ts` |
| `.ru-track` / `.ru-stage` / `.ru-scene` selectors inside it | lose their only emitter with `HeroGraph.astro`, but sit in the same file as the live base — splitting a stylesheet that live code imports is out of scope for a retirement commit; logged as debt |
| `src/lib/visual/hero-sequence.ts`, `src/styles/hero-*.css`, `src/components/home/**` | **hard constraints — untouched** |
| `src/lib/visual/scene-contract.ts`, `src/lib/hero-graph-content.ts` | live (`GatewayPortal.astro:48`, `home-content.ts:12`) |
| `src/lib/visual/{portal-scene,gateway-motion}.ts` | live gateway route |
| `public/research-universe/models/*.glb` | §5.4 — provenance/ownership decision, logged as debt |
| `src/lib/visual/gateway-scene.ts` | `DEAD` per the scan but **outside Task 11's stated scope** (Home/RU legacy) and referenced by `tests/e2e/ca07-gateway-scene.e2e.ts:76`; not touched |

---

## 7. Verification actually executed

Run in `D:/Project/.atlas-worktrees/public-site-plan-d-retire`. Full command output is reported to
the coordinator in the task response; summarised here for the record.

* `npm run lint` — pass (exit 0).
* `npm test` — pass.
* `npm run build` — pass; `dist/research-universe/models/` still present (GLBs deliberately retained).

**A pre-existing baseline failure was found and is not attributable to this task:**
`src/foundation.contract.test.ts › keeps the default production build free of Atlas output…` failed
when the suite ran concurrently, with
`EPERM: operation not permitted, rename '…\node_modules\.vite\deps_temp_e5c99132' -> '…\deps'`.
Re-run in isolation it passes **16/16**. It is a Windows `node_modules/.vite` cache-rename race
between concurrent Vitest processes, not a code defect.

---

## 8. Claims deliberately **not** made

* No owner acceptance, no visual acceptance, no production-readiness claim.
* No staging or production deployment was performed, and none is implied.
* The `DESIGN_ATLAS=1` specimen build was re-run (plan Task 11 Step 4) to confirm no specimen was
  lost; the four legacy `graph-*` modules were kept precisely so that build keeps its pages.
* Playwright end-to-end specs were **not** executed in this environment; `tests/e2e/*` was not run.
  This file therefore makes no claim about runtime browser behaviour.

`Design-Assets/research-universe/models/`, and were **not** deleted from
`public/research-universe/models/`. Reasons:

1. `Design-Assets/` is **untracked in the coordination repository** — `git ls-files
   Design-Assets/research-universe/` returns nothing and `git check-ignore` reports no rule. A copy
   placed there would be an *untracked local file*, which does not "preserve history" in the sense
   the plan means; it would look preserved while being one `git clean` away from gone. Adding 1.3 MB
   of binaries to a repository that currently tracks none of that folder is a repository-level
   decision belonging to its owner, not to this task.
2. v3 is **already** preserved byte-identically at
   `Design-Assets/research-universe/export/` (hash above), so removing it from the shipping path
   loses nothing.
3. v1's source of truth is the **tracked `.blend`**, from which the GLB is a one-command
   regeneration. Deleting the shipping copy loses a derived artefact, not owner artwork.
4. The brief's standing instruction is explicit: *"prefer leaving an untracked-but-referenced asset
   alone over deleting it."*

So `public/research-universe/models/*.glb` is **left in place and recorded as debt** (§6), and the
purity test is left **unweakened**. The 1.32 MiB is therefore **still shipped** — stated here as an
open item rather than presented as a completed retirement.

```
=== Step 1 of Task 12: no runtime consumer of the GLBs ===
(empty)
=== gltf refs anywhere in built html/js ===
(no output)
```

### 5.2 The production build ships them today (plan Step 2)

```
$ Get-ChildItem -Recurse dist/research-universe -File
Name                                    Length
----                                    ------
taha-research-universe-signature-v1.glb 847500
taha-research-universe-signature-v3.glb 535604
```

**1,383,104 bytes (1.32 MiB) of never-requested binaries in the shipped image.** Both are
git-tracked in `public/research-universe/models/`.

`src/styles/research-universe.css` defines `.ru-label*` (lines 50–125), `.ru-leaders` (371–496) and
friends, and the **live Atlas 3D scene** instantiates exactly those class names at runtime via
`labels.ts:61` / `leaders.ts:68` / `spheres.ts:55` (`atlas/scene.ts:68` → `createLabelLayer`).
Deleting the base would strip the Atlas scene's labels.

The narrow `.ru-about*` / `.ru-controls*` blocks were already removed with the Task 8 mount. What
remains is the shared base plus the Home-scoped `.ru-track` / `.ru-stage` / `.ru-scene`, which lose
their only emitter with `HeroGraph.astro`. Those sit in the same file as the live base, and splitting
a stylesheet that live code imports is not a retirement — logged as debt in §6.

  `hero-enhancement.ts`) reachable only from the `DESIGN_ATLAS=1` specimen build and unit tests."*
* **replacement coverage:** Home v2 is `hero-sequence.ts` (hard-protected); the Atlas 3D runtime has
  its own `lib/visual/atlas/enhancement.ts`, which imports nothing from `hero-enhancement.ts`
  (verified: it imports only `atlas/refresh`, `atlas/url-state`, `atlas/selection`, `atlas/model`).
* **verdict: retire** — and note the one place the scan **disagrees with the spec**: C13 says this
  file is `DESIGN_ATLAS`-reachable, but `GraphInteractionDemo.astro` / `GraphSceneDemo.astro` import
  `graph-scene/graph-controller/graph-motion`, **not** `hero-enhancement`. The spec grouped five
  files; only four are Atlas-reachable. Recorded rather than silently followed.

src\lib\visual\research-universe\enhancement.ts:193,258,344
```

```
=== home-motion ===      src\lib\research-universe\universe.test.ts:67
=== about-controls ===    src\lib\research-universe\universe.test.ts:75
```

`about-preset.ts` (RU) is in §3.4. `runtime-purity.test.ts` is **kept and updated**, not retired — §4.

### 3.3 `src/lib/visual/research-universe/*` — split verdict, decided per file

This is the directory the brief flagged as needing per-file judgement. The decisive fact is that
**`src/lib/visual/atlas/scene.ts` — the live Atlas 3D scene — statically imports modules from it.**
Verified import lines:

```
src\lib\visual\atlas\scene.ts:37: } from '../research-universe/scene-core'
src\lib\visual\atlas\scene.ts:38: import { sharedSphereTriangles } from '../research-universe/spheres'
src\lib\visual\atlas\scene.ts:43: } from '../research-universe/nodes'
src\lib\visual\atlas\scene.ts:47: } from '../research-universe/edges'
src\lib\visual\atlas\scene.ts:48: import { createUniverseCore } from '../research-universe/core-object'
src\lib\visual\atlas\scene.ts:58: } from '../research-universe/layout'
src\lib\visual\atlas\scene.ts:59: import { resolvePresentationProfile } from '../research-universe/presentation-profiles'
src\lib\visual\atlas\scene.ts:63: } from '../research-universe/theme'
src\lib\visual\atlas\scene.ts:67: } from '../research-universe/hit-testing'
src\lib\visual\atlas\scene.ts:68: import { createLabelLayer, type LabelLayer } from '../research-universe/labels'
src\lib\visual\atlas\picking.ts:23: …'../research-universe/hit-testing'
```


---

## 2. Correction to the task's "known remaining dead code" list

The brief supplied a candidate list and asked that it not be trusted blindly. Verification changed
**three** entries. This matters: two corrections are the difference between a correct retirement and
deleting live code.

| Brief's claim | Verified reality | Evidence |
| --- | --- | --- |
| `src/components/about/ResearchUniverse.astro` "still present on your branch's base" | **Already deleted** in `4959604` (Task 8) | `Test-Path` → `False`; `git show --stat 4959604` lists `src/components/about/ResearchUniverse.astro \| 419 ---` |
| `tests/e2e/ru-about.e2e.ts` "check ru-about" | **Already deleted** in `5dd9ae3` (Task 9) | `Test-Path` → `False`; `git show --stat 5dd9ae3` lists `tests/e2e/ru-about.e2e.ts \| 685 ---` |
| `src/lib/research-universe/*` — "`adapter.ts` and `universe.test.ts` are still imported by `HeroGraph.astro`. **HeroGraph is a real consumer**, so decide carefully per file" | `HeroGraph.astro` is **not a production consumer of anything** — it is itself unreachable from every page and from the Atlas specimen. It is the correct *first* retirement, not a reason to keep its dependencies | Reachability `DEAD`; no `src/pages/**` or `src/atlas/**` file imports it (§3.1) |
| `HeroGraph.astro` is a "known consumer candidate" for the shared `.ru-*` CSS | Correct, and it is the **only** DOM consumer — which is why retiring it is safe, but it means the `.ru-*` base's fate must be handled, not left silently | §3.7 |

**Consequence:** the brief's inference ("HeroGraph is a real consumer, therefore keep the RU
library") is inverted. `HeroGraph.astro` is a dead leaf; the live consumer of most of the RU library
is a *different* file — `src/lib/visual/atlas/scene.ts` (§3.3).
