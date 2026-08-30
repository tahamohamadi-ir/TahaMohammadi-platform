# Home + Gateway Visual Recovery — Multi-Agent Execution Authority

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` or `superpowers:executing-plans`. Execute only the assigned Work Packet. Do not infer permission from reference documents.

**Goal:** Rebuild the public Home and Gateway on the tracked Design System and promoted assets, then hold `PUBLIC-190` open until independent visual QA and explicit owner acceptance.

**Architecture:** The work is divided into agent-neutral, resumable Work Packets. Five worker tools may be assigned, replaced, or paused without changing task authority. Every worker uses an isolated Git worktree and returns a commit-based Handoff Bundle; Master Chat alone changes assignments, integrates commits, and interprets acceptance.

**Tech stack:** Astro 7, TypeScript 5.9, Tailwind CSS 4, Vitest, `lucide-astro`, Astro Assets/Picture, Playwright Test, axe-core, self-hosted fonts, static-first HTML.

**Spec:** This file is the combined approved task specification, implementation plan, conflict map, dispatch guide, and recovery ledger for this visual-recovery slice.

**Baseline when this authority was written:**

- Coordination repository: `e748c3782fa7ffcef697810b2be051a28c4787d1`
- Public-site repository: `08583695cfc09828d0126b9c9d809aca966f0eb2`
- Both repositories were clean on `main`.
- Design-authority validator passed with 24 components, 6 templates, 10 asset references, 24 required files, 30 checksums, and 3 aliases.
- Public-site baseline passed 13 Vitest tests and produced a 15-page Astro build.

---

## 1. Authority, outcome, and non-negotiable boundaries

Read these sources completely before any worker changes a file:

1. Workspace `AGENTS.md`
2. `Docs/00-governance/AUTHORITY-ORDER.md`
3. `PROJECT-MANIFEST.md`
4. `Docs/references/frontend-design-authority/README.md`
5. `Front-End/public-site/AGENTS.md`
6. This execution authority
7. The exact Work Packet assigned by Master Chat

The following rules apply to every packet:

- Treat the coordination root and `Front-End/public-site` as separate repositories. Never combine their files in one commit.
- Do not copy code, CSS, components, routes, or runtime behavior from `D:\Project\Taha-personal-platform`.
- The old project and raster concepts are evidence only. Raster text is never content authority.
- Use only the tracked authority under `Docs/references/frontend-design-authority/` for visual implementation.
- Do not invent copy, translations, claims, routes, API fields, dates, links, records, publication state, alt text, or performance results.
- Public content must remain readable without JavaScript. Decorative atmosphere may progressively enhance and may be absent when JavaScript and images are disabled.
- Light/Dark and FA/EN use the same meaningful DOM anatomy. CSS uses logical properties.
- A build, HTTP 200, automated screenshot, or axe pass does not close visual acceptance.
- No worker pushes to `main`, force-pushes, rebases an integrated branch, or edits another packet's allowlist.
- Generated `dist/`, browser traces, screenshot output, caches, and dependency directories are not committed.
- Only Master Chat updates this document's assignment/status tables. Workers return Handoff Bundles instead of editing this file.

### Explicit owner decisions captured by this authority

- `PUBLIC-190` returns from Done to **structure complete; visual acceptance open**.
- New page-family development is frozen until Home visual acceptance.
- Existing logo and favicon are approved as-is; derivatives are allowed, redesign is not.
- `project-dashboard-systems` maps to the Organizational Dashboard project.
- `project-data-architecture` maps to PARS-SQL.
- `blog-coral-stairs`, `learning-sage-library`, and `gallery-ivory-forms` are decorative previews for Writing, Teaching, and Creative respectively.
- `project-visual-communication-network` remains deferred and must not enter runtime.
- `project-placeholder-ivory-stairs` is not used on Home.
- The Home graph uses one text-free Light backplate and one text-free Dark backplate, with semantic DOM content overlaid.
- Independent Visual QA returns `PASS` or `REVISE`; the owner gives the final acceptance.

### Corrected content and dependency gates

The initial recovery outline is supplemented by existing higher-authority contracts:

- `PUBLIC-070` and `PUBLIC-080` must close before `PUBLIC-130 → 140 → 150 → 160 → 170` can close.
- `PUBLIC-180` state primitives must exist before Home can pass `PUBLIC-190`.
- The FA Home must not synthesize translations of EN-only research-focus cards. The exact FA research-statement record may supply its own `data.focus_areas` to the semantic graph/list, but the EN card records are omitted in FA until approved FA records exist.
- `writing.visual-discourse.en` and `writing.vtd-edge.en` remain Writing manuscripts, not Publications. They are omitted from FA Home and FA detail generation because the route-composition contract requires exact-locale records.
- Do not create About, Research, Contact, CV, Teaching, or Creative page families in this recovery. When a target route does not exist, render the approved unavailable state or omit the action; never publish a broken anchor.
- Existing Project and Writing stubs may remain only where their current seed and route contracts permit them. This recovery does not broaden their content authority.

---

## 2. Definition of done

The recovery is complete only when all of the following agree:

- `PUBLIC-070`, `080`, `130`, `140`, `150`, `160`, `170`, `180`, and `260` have test evidence.
- Home and Gateway consume real Design System components rather than page-specific copies of button/card/shell behavior.
- Home uses `portal-orbit-*`; Gateway uses `portal-centered-*`.
- Approved media is processed from `src/assets` into AVIF/WebP responsive output; no original multi-megabyte art PNG is served directly.
- The browser does not download both theme variants on initial load.
- The graph backplate is decorative and all graph labels/links remain semantic DOM content.
- The six shared templates and the 24-component inventory appear in a local-only Visual Atlas.
- A normal build contains no `/_design/` route or artifact.
- Automated QA passes, manual QA is recorded, independent QA returns `PASS`, and the owner explicitly accepts.
- Only after the preceding gates may `PUBLIC-190` become Done and `PUBLIC-200+` resume.

Until then, the status is **implementation/review in progress; visual acceptance open**.

---

## 3. Execution topology and editable assignment board

Worker names are assignments, not authorities. Master Chat may change the `Assigned tool` cell without changing packet scope.

| Wave | Work Packet | Initial assigned tool | Start condition | Parallelism | State |
|---|---|---|---|---|---|
| 0 | `WP-00` Preflight and branch topology | Master Chat | immediately | alone | ready |
| 1 | `WP-10` Governance, contracts, QA harness, theme/focus foundation | Codex | `WP-00` accepted | alone on shared files | ready |
| 2A | `WP-20` Components, shell, templates, Visual Atlas | Cursor | `WP-10` integrated | parallel with `WP-30` | queued |
| 2B | `WP-25` Art direction and graph image generation | image-capable Codex or ChatGPT Sol | `WP-10` integrated | parallel with `WP-20` and asset inventory | queued |
| 2C | `WP-30` Asset pipeline and promotion | Antigravity | `WP-10` integrated; `WP-25` accepted before final asset commit | parallel with `WP-20` | queued |
| 3 | `WP-40` Gateway and Home reconstruction | OpenCode | `WP-20` and `WP-30` integrated | alone on Home/Gateway | queued |
| 4 | `WP-50` Independent visual/accessibility QA | Hermes | `WP-40` integrated and full suite green | read-only except one QA report | queued |
| 5 | `WP-60` Acceptance and status closure | Master Chat + owner | `WP-50=PASS` | alone | queued |

State vocabulary is exactly: `queued`, `active`, `review`, `revise`, `accepted`, `blocked`.

Additional Codex/ChatGPT Sol sessions may be opened as **read-only design advisers** for a bounded question such as hierarchy, responsive composition, RTL typography, crop, or a difficult interaction. An adviser does not receive a file allowlist, does not modify a repository, and does not become a merge owner. It returns a recommendation with authority citations and explicit trade-offs; the active packet owner implements only after Master Chat accepts the recommendation.

### Worktree and branch policy

Use a separate worktree per worker. The worker must show the resolved repository root and current branch before editing.

Recommended public-site branches:

```text
cx/public-recovery-integration
cx/public-recovery-foundation
cx/public-recovery-design-system
cx/public-recovery-assets
cx/public-recovery-home
cx/public-recovery-qa
```

Recommended coordination branches:

```text
cx/home-recovery-governance
cx/home-recovery-qa-report
```

Recommended worktree parent:

```text
D:\Project\worktrees\tahamohammadi-platform\
```

No worker assumes a branch exists. Master Chat provides the exact base commit and worktree path in the dispatch prompt. Workers do not create a second worktree if the supplied path already exists; they stop and report the collision.

### Integration rule

1. Worker commits only the exact packet scope.
2. Worker returns a Handoff Bundle and commit hash.
3. Master Chat inspects `git show --stat`, `git diff <base>..<commit> --name-only`, tests, and prohibited paths.
4. Master Chat returns `ACCEPT`, `REVISE`, or `BLOCK`.
5. Only accepted commits are cherry-picked onto `cx/public-recovery-integration` or the coordination integration branch.
6. The next wave starts from the new integration commit, never from another worker's dirty checkout.

---

## 4. File ownership and conflict matrix

| File or area | Exclusive owner by phase | Forbidden concurrent edits | Resolution |
|---|---|---|---|
| Root Decision Log, task board, asset ledger | `WP-10`, then `WP-30` only for asset evidence | all other workers | separate root commits; `WP-30` starts from integrated `WP-10` root commit |
| `package.json`, lockfile, Playwright config | `WP-10` | `WP-20/30/40/50` | install all approved dependencies once in Wave 1 |
| `astro.config.mjs` | `WP-10` for base hook, then `WP-20` for Atlas hook | `WP-30/40/50` | sequential ownership transfer after integration |
| `src/styles/global.css` | `WP-10` extraction only | all later packets | reduce to imports/base compatibility; later code uses scoped styles or owned style modules |
| token/base/theme/focus styles | `WP-10` | all others | consumers may use variables but not redefine them |
| UI components, shell, templates, Atlas | `WP-20` | all others | Home consumes public interfaces only |
| promoted-media manifest/component/assets | `WP-30` | all others | Home requests asset IDs; never imports authority paths directly |
| Gateway page/component styles | `WP-40` | all others | must consume `WP-20/30` interfaces |
| Home components, Home content adapter, Home styles | `WP-40` | all others | no edits to token/global/shell/media internals |
| unit/contract tests beside owned code | owning packet | other packets | each packet owns its focused tests |
| acceptance E2E specs | `WP-10` creates failing contract; Master Chat may approve surgical fixes | implementation workers may not weaken assertions | failing assertions are fixed in production code or escalated |
| screenshot artifacts | `WP-50`, ignored output only | everyone | never commit |
| final QA report | `WP-50` only | implementation workers | report may be revised, production code may not be edited by QA |
| this execution authority | Master Chat only | every worker | handoff via chat, not direct edits |

### Amendment B — controlled legacy-shell extraction (2026-08-30)

**Decision:** The `WP-10` foundation extraction left the legacy shell selectors in
`src/styles/global.css`, while `WP-20` is the owner of the new `shell.css` module.
To resolve that sequencing gap without reopening token, base, theme, Home, or
Gateway ownership, Master Chat transfers one narrow mechanical operation to
`WP-20 / PUBLIC-150`.

**Supersession:** This amendment supersedes the `global.css` prohibition in the
`WP-20` allowlist and the ownership-matrix row above **only for the exact source
segments listed below**. Every other `global.css` edit remains exclusively owned
by `WP-10` and forbidden to `WP-20`.

**Exact permitted operation:** In one replacement `PUBLIC-150` commit, Cursor may
move, without semantic redesign, the legacy selectors for:

- `.site-body`;
- `.skip-link` and `.skip-link:focus`; and
- the source segment headed `/* Site shell — header, main, footer */`, including
  its header, navigation, language-toggle, footer, and shell theme-control
  selectors;

from `src/styles/global.css` to `src/styles/shell.css`. Equivalent selectors must
exist exactly once after the move. `SiteLayout.astro` is the only layout permitted
to import `shell.css`; `BaseLayout.astro` must remain at its accepted WP-10/PUBLIC-140
content and no `shell-focus.css` (or duplicate focus stylesheet) may be created.

**Focused proof allowed for this amendment:** Cursor may add a new
`tests/e2e/public-150-shell.e2e.ts` owned by WP-20. It must assert that keyboard
activation of the SkipLink moves focus to `#main-content` and that the destination
has a visible tokenized focus outline. Cursor must not edit
`tests/e2e/wp10-foundation.accessibility.e2e.ts`, other WP-10 acceptance tests,
Playwright configuration, package files, or global token/base/theme rules.

**Required replacement-commit evidence:** The commit parent is accepted
`PUBLIC-140` (`edef566043233263ba59f2229ed40f3653f749f0`); it contains no unrelated
file changes; `global.css` has no remaining copied selector from the listed
legacy-shell segments; full Vitest, design validation, normal build, WP-10
foundation/a11y checks, the new focused shell E2E, and `git diff --check` pass.

---

### Known high-risk conflicts

- `src/styles/global.css` is approximately 2,272 lines and currently mixes tokens, theme, Gateway, shell, stubs, and Home. Freeze it after `WP-10` extracts foundations.
- `Header.astro`, `ThemeToggle.astro`, `BaseLayout.astro`, `SiteLayout.astro`, `navigation.ts`, `astro.config.mjs`, `package.json`, and the lockfile must never be edited concurrently.
- `components.json` contains 24 names but ownership spans tasks: `ThemeToggle` belongs to `PUBLIC-070`; `Header` and `LanguageToggle` belong to `PUBLIC-150`; the remaining 21 components belong to `PUBLIC-140`. The 24-component gate closes only after all three owners' outputs are integrated.
- Current Header links the alternate locale to Home rather than the equivalent route. The LanguageToggle interface must receive `alternateHref` and availability from the route contract.
- Current `ThemeToggle` uses a fixed element ID and is not safe when Atlas renders multiple instances. `WP-10` makes it instance-safe before Atlas work.
- Current media declarations use incorrect `1920×1080` dimensions; the four portal masters are `1672×941`.
- Current Home loads both theme images into the DOM and prioritizes Dark even in Light mode.
- Current Home contains broken links to unimplemented page families and unauthorized FA fallback content. `WP-40` must correct both without adding those families.

---

## 5. Stable interfaces between packets

### 5.1 Design contract snapshot

`WP-10` creates a portable snapshot under `Front-End/public-site/contracts/design-authority/`:

```text
tokens.json
components.json
templates.json
manifest.json
```

`manifest.json` records the central source path, source SHA-256 for each JSON file, inventory counts, and snapshot date. A validator must:

- fail on local snapshot hash drift;
- assert exactly 24 component names and 6 template IDs;
- compare with the central authority when the workspace path exists;
- still validate the pinned local snapshot in a standalone public-site clone.

### 5.2 Token interface

`src/styles/tokens.css` exposes three layers:

```text
--primitive-*
--color-* / --space-* / --radius-* / --font-* / --motion-* / --layout-*
--button-* / --card-* / --control-* / --shell-*
```

Every value comes from the pinned `tokens.json`. `WP-20`, `WP-30`, and `WP-40` may consume these variables but may not introduce replacement theme palettes.

### 5.3 Component interface

The component export index must include exactly the authority inventory:

```text
Button, IconButton, Link, Chip, Badge, ThemeToggle, LanguageToggle,
Header, Breadcrumbs, LocalTabs, FilterBar, Pagination, SectionLead,
Card, FeaturedRecord, ContentRow, PublicationRow, MetadataGroup,
TimelineNode, MediaTile, TOCItem, ContactCTA, Input, Textarea
```

Shared component props follow these rules:

- `locale: 'fa' | 'en'` where visible copy or direction is involved;
- `disabled`, `loading`, `error`, and unavailable states are explicit props, not inferred from empty labels;
- all icon-only controls require `label`;
- `Link` receives a real `href`; unavailable actions use a non-anchor state component;
- directional icons mirror in RTL, semantic/data icons do not;
- interactive target size is at least 44×44 CSS pixels.

### 5.4 Template interface

Create these six slot/anatomy templates without adding public routes:

```text
HomeTemplate
CollectionIndexTemplate
EditorialIndexTemplate
LongFormDetailTemplate
EvidenceVisualDetailTemplate
AboutContactUtilityTemplate
```

Templates own hierarchy and slots. Route pages own data and content. Optional slots collapse without fake placeholders.

### 5.5 Promoted media interface

`src/lib/media/promoted-media.ts` defines:

```ts
import type { ImageMetadata } from 'astro';

export type Locale = 'fa' | 'en';
export type Theme = 'light' | 'dark';
export type MediaSlot =
  | 'gateway.atmosphere'
  | 'home.hero.atmosphere'
  | 'home.graph.backplate'
  | 'home.project.preview'
  | 'home.rail.preview'
  | 'brand.mark';

export interface PromotedMedia {
  id: string;
  source: ImageMetadata;
  authorityPath: string;
  sourceSha256: string;
  intrinsic: { width: number; height: number };
  approval: { ledgerId: string; decision: string; decisionDate: '2026-08-29' };
  semantics:
    | { kind: 'decorative'; alt: '' }
    | { kind: 'content'; altByLocale: Readonly<Record<Locale, string>> };
  placement: {
    slot: MediaSlot;
    theme: Theme | 'both';
    locales: readonly Locale[];
  };
  transform: {
    formats: readonly ['avif', 'webp'];
    widths: readonly number[];
    sizes: string;
    fit: 'cover' | 'contain';
    focalByLocale: Readonly<Partial<Record<Locale, string>>>;
    loading: 'lazy' | 'eager';
    fetchPriority: 'auto' | 'high';
    measuredByteCeiling: Readonly<Partial<Record<string, number>>>;
  };
}

export function getPromotedMedia(id: string, expectedSlot: MediaSlot): PromotedMedia;
```

`getPromotedMedia` throws during build/test on an unknown ID, deferred ID, slot mismatch, missing alt policy, invalid hash, or absent transform recipe.

`PromotedPicture.astro` renders normal responsive media through Astro `Picture`. `ThemePicture.astro` keeps Light/Dark `<picture>` markup inert inside templates and mounts only the resolved theme, preventing both variants from downloading. A no-JS fallback may use the system preference; content meaning must not depend on it.

### 5.6 Theme and Atlas interface

- The early inline theme bootstrap sets both requested mode (`system|light|dark`) and resolved theme (`light|dark`) before paint.
- Theme controls dispatch one documented `tm-themechange` event after resolution.
- Each toggle instance uses scoped element references, never a fixed global ID.
- The Atlas route is injected only when `DESIGN_ATLAS=1` using an Astro integration outside `src/pages`.
- Default build must have no `_design` file, route, or manifest entry.

---

## 6. Work Packets

### WP-00 — Master preflight and branch topology

**Owner:** Master Chat

**Writes:** none beyond this already-created authority.

- [ ] Re-read all repository instructions and check both Git statuses.
- [ ] Record current root/public HEADs; if they differ from the baseline above, review intervening commits before dispatch.
- [ ] Create or identify one integration branch per repository.
- [ ] Create isolated worker worktrees from the exact integration commit.
- [ ] Confirm no worker is operating on shared `main` or another worker's checkout.
- [ ] Dispatch only `WP-10`.

**Gate:** exact base hashes and worktree paths are known; both source worktrees are clean.

### WP-10 — Governance, contract snapshot, QA harness, theme/focus foundation

**Initial tool:** Codex

**Task coverage:** governance reconciliation plus `PUBLIC-070`, `PUBLIC-080`, `PUBLIC-130`, and failing acceptance harness.

**Coordination repository allowlist:**

- `Docs/10-tracking/DECISION-LOG.md`
- `Docs/05-delivery/MULTI-AGENT-TASK-BOARD.md`
- `Docs/05-delivery/MASTER-TASK-LIST.md` only if its milestone wording must be corrected; do not mark R3/R4 complete
- `Docs/04-design/ASSET-PROMOTION-LEDGER.md` for recording the owner decisions, not derivative evidence

**Public-site allowlist:**

- `TASK-LIST.md`
- `package.json`, lockfile
- `astro.config.mjs`, `.env.example`
- `contracts/design-authority/**`
- `scripts/validate-design-authority.mjs`
- `src/styles/{global,tokens,base,utilities}.css`
- `src/layouts/BaseLayout.astro`
- `src/components/{ThemeToggle,SkipLink}.astro`
- focused unit/contract tests
- `playwright.config.ts`, `tests/e2e/**`

**Required implementation:**

- [ ] First add failing tests for snapshot hash/count validation, exact semantic token values, three-state and multi-instance theme behavior, visible focus/reduced motion, Atlas exclusion, locale/direction/one-H1/no-overflow, and the target screenshot matrix.
- [ ] Run focused tests and record the expected failures.
- [ ] Install `lucide-astro`, `@playwright/test`, and `@axe-core/playwright` once; commit the resulting lockfile.
- [ ] Add scripts named `validate:design`, `test:visual`, `test:a11y`, `build:atlas`, and retain existing `test`/`build` behavior.
- [ ] Create the pinned contract snapshot and standalone validator.
- [ ] Extract authority-equal tokens from `global.css` into three-layer `tokens.css`; import `fonts.css`, tokens, base, and utilities in deterministic order.
- [ ] Make theme bootstrap and ThemeToggle support `system`, `light`, and `dark`, avoid first-paint mismatch, support multiple Atlas instances, and publish `tm-themechange`.
- [ ] Add reduced-motion and general focus-visible behavior without hiding focus.
- [ ] Change `PUBLIC-190` to `[~] structure complete; visual acceptance open`, record the freeze on `PUBLIC-200+`, and make the true prerequisite chain explicit.
- [ ] Record all owner asset decisions listed in Section 1; do not claim derivative completion.
- [ ] Run focused tests, full Vitest, default build, design validator, and `git diff --check`.
- [ ] Commit root and public changes separately and return two Handoff Bundles.

**Acceptance:** tests that belong to later packets may remain failing only when they are clearly named acceptance tests and Master Chat records that expected state. Existing tests and the default build must remain green.

### WP-20 — Components, shell, templates, and Visual Atlas

**Initial tool:** Cursor

**Task coverage:** `PUBLIC-140 → PUBLIC-150 → PUBLIC-160 → PUBLIC-170` in that order.

**Allowlist:**

- `src/components/ui/**`
- `src/components/{Header,Footer,LanguageToggle}.astro`
- `src/layouts/SiteLayout.astro`
- `src/lib/navigation.ts`
- `src/styles/shell.css`
- `src/components/templates/**`
- `src/atlas/**`
- `src/integrations/design-atlas.mjs`
- `docs/design/DESIGN-ATLAS.md`
- `astro.config.mjs` only for the conditional Atlas integration after `WP-10`
- focused tests for these files

**Forbidden:** Home components/content, assets/media manifests, `global.css`, package files, public page-family routes, central Docs.

**Required implementation:**

- [ ] Add failing inventory tests for the 21 components owned here; the integrated 24-name test includes ThemeToggle, Header, and LanguageToggle.
- [ ] Implement each component's authority anatomy, variants, disabled/loading/error/unavailable behavior, 44px target, keyboard behavior, focus parity, and RTL direction.
- [ ] Replace shell emoji/CSS marks with Lucide icons; use accessible names and localized visible/assistive labels.
- [ ] Refactor existing Header/Footer/SkipLink rather than replacing them wholesale.
- [ ] Implement LanguageToggle with `currentLocale`, `alternateHref`, and `available`; never send an unavailable locale to Home as a fallback.
- [ ] Build the six slot-based templates with exactly one H1 responsibility and no fake content.
- [ ] Build the Atlas outside `src/pages`, containing foundations, all 24 components and relevant states, all six templates, Home/Gateway specimens, EN/FA, Light/Dark, reduced motion, and a state sheet.
- [ ] Add stable `data-visual-id` values to Atlas specimens and shared component roots.
- [ ] Use conditional `injectRoute({ pattern: '/_design', entrypoint: ... })` only when `DESIGN_ATLAS=1`.
- [ ] Verify positive Atlas build and negative production build.
- [ ] Run all focused tests, full Vitest, build, design validator, and `git diff --check`.
- [ ] Commit one reviewable commit after each task boundary: components, shell, templates, Atlas.

**Gate:** 24 integrated component names, six templates, Atlas positive build, production negative build, keyboard/RTL tests, and no page-family implementation.

### WP-25 — Art direction and graph image generation

**Initial tool:** image-capable Codex or ChatGPT Sol

**Mode:** no repository writes. Generated candidates stay in the tool's generated-image location until Master Chat accepts one Light and one Dark result.

**Inputs:**

- the two exact prompts in `WP-30`;
- the tracked Home Light/Dark concepts as style/composition references;
- Light/Dark semantic palettes from the pinned design tokens;
- the requirement that semantic nodes, text, links, and logo remain DOM overlays.

**Required process:**

- [ ] Inspect the relevant tracked concept images before generation.
- [ ] Generate Light and Dark as separate image calls; do not ask one call to produce a combined sheet.
- [ ] Validate each output at full resolution and at a 320px preview.
- [ ] Reject any output containing text-like marks, letters, digits, logos, UI controls, watermarks, embedded labels, more or fewer than five usable landing zones, an obstructed center, or a palette that does not blend with its theme canvas.
- [ ] If a variant fails, perform one targeted iteration describing only the defect to correct.
- [ ] Return the final generated paths, dimensions, final prompts, generation mode, and a short acceptance rationale to Master Chat.
- [ ] Do not copy files into either repository and do not edit manifests or ledgers.

**Gate:** Master Chat visually inspects both files and returns `ACCEPT` with exact selected paths, or `REVISE` with one bounded visual correction.

### WP-30 — Asset pipeline, graph sources, crop/alt mapping

**Initial tool:** Antigravity

**Task coverage:** `PUBLIC-260` including approved Group A/B assets and graph backplates.

**Coordination allowlist:**

- `Docs/references/frontend-design-authority/art/home-graph-backplate-{light,dark}.png`
- `Docs/references/frontend-design-authority/AUTHORITY-MANIFEST.json`
- `Docs/references/frontend-design-authority/SHA256SUMS.txt`
- `Docs/references/frontend-design-authority/agent-kit/assets.json`
- `Docs/04-design/ASSET-PROMOTION-LEDGER.md`

**Public-site allowlist:**

- `src/assets/media/**`
- `src/lib/media/**`
- `src/components/media/**`
- `public/icons/**`
- media-focused tests
- removal of replaced raw files under `public/media/**`
- `astro.config.mjs` only to remove obsolete local-media proxy bypass after consumers no longer use it; otherwise escalate to Master Chat

**Forbidden:** Home/Gateway consumers, Home content, global/tokens/shell styles, package files, task status, public routes.

**Source inventory and runtime decisions:**

| Authority ID | Intrinsic | Runtime decision |
|---|---:|---|
| `portal-centered-light/dark` | 1672×941 | Gateway decorative, `alt=""` |
| `portal-orbit-light/dark` | 1672×941 | Home hero decorative, `alt=""` |
| `brand-primary` | 256×233 | approved mark; do not upscale past source |
| `brand-favicon` | 64×64 | derive only 16/32/48/64 PNG and ICO sizes |
| `project-dashboard-systems` | 1536×1024 | Organizational Dashboard preview |
| `project-data-architecture` | 1536×1024 | PARS-SQL preview |
| `blog-coral-stairs` | 1536×1024 | Writing decorative preview, `alt=""` |
| `learning-sage-library` | 1536×1024 | Teaching decorative preview, `alt=""` |
| `gallery-ivory-forms` | 1536×1024 | Creative decorative preview, `alt=""` |
| `project-visual-communication-network` | 1536×1024 | deferred; absent from runtime |
| `project-placeholder-ivory-stairs` | 1536×1024 | absent from Home/runtime in this slice |
| graph backplates | generated 1024×1024 | decorative, theme-specific, `alt=""` |

**Transform sets:**

- atmosphere: `320, 390, 768, 1024, 1280, 1440, 1672`
- project and rail previews: `320, 480, 640, 800, 1024`
- graph backplates: `320, 480, 640, 768, 1024`
- formats: AVIF first, WebP second, source-format fallback
- focal/crop values are measured and recorded after the six-width EN/FA review; do not copy the current CSS guesses
- `measuredByteCeiling` is set from accepted generated output and used as a no-regression ceiling; do not invent a pre-measurement byte claim

**ImageGen input produced by `WP-25`:**

An image-capable Codex or ChatGPT Sol session generates exactly two sources with the built-in ImageGen tool and returns them to Master Chat. Master Chat performs the acceptance review and gives only the selected local paths plus an `ACCEPT` decision to this packet. Antigravity is the only worker allowed to copy selected files into tracked authority and update checksums. A text-only model may refine prompts or critique outputs but must not claim that it generated or visually inspected an image it could not access.

Light prompt:

```text
Use case: stylized-concept
Asset type: square decorative backplate for a semantic research graph on a personal academic website
Primary request: create a text-free orbital constellation backplate with five clear node landing zones and a calm empty center for a DOM overlay
Style/medium: precise editorial scientific atlas, thin orbital geometry, restrained depth, warm ivory and mineral-white canvas, subtle turquoise with very limited gold, violet, emerald, and coral accents
Composition/framing: 1:1 square, centered radial system, five balanced peripheral anchor regions, generous negative space, readable at 320px
Constraints: no text, no letters, no numbers, no logo, no icons, no interface controls, no watermark, no embedded labels; background must blend with the Light canvas; semantic nodes and labels will be HTML overlays
```

Dark prompt:

```text
Use case: stylized-concept
Asset type: square decorative backplate for a semantic research graph on a personal academic website
Primary request: create a text-free orbital constellation backplate with five clear node landing zones and a calm empty center for a DOM overlay
Style/medium: precise scientific atlas with restrained luminous depth, deep navy canvas, layered blue surfaces, turquoise identity light, very limited gold, violet, emerald, and coral accents
Composition/framing: 1:1 square, centered radial system, five balanced peripheral anchor regions, generous negative space, readable at 320px
Constraints: no text, no letters, no numbers, no logo, no icons, no interface controls, no watermark, no embedded labels; background must blend with the Dark canvas; semantic nodes and labels will be HTML overlays
```

**Required implementation:**

- [ ] Add failing tests for exact authority hashes, allowed runtime IDs, slot enforcement, alt policy, transform recipes, deferred-asset rejection, and correct intrinsic dimensions.
- [ ] Copy exact-hash approved masters to `src/assets/media` and implement `PromotedMedia`, `getPromotedMedia`, `PromotedPicture`, and `ThemePicture`.
- [ ] Add the two inspected graph sources, update authority manifest/checksums/assets inventory, and record their generation prompt and approval evidence in the ledger.
- [ ] Remove raw public media after all consumers have an asset ID; no unapproved/deferred art remains publicly addressable.
- [ ] Build and inspect AVIF/WebP/srcset/sizes output and record measured byte ceilings.
- [ ] Verify only the selected theme source is requested during initial page load.
- [ ] Run authority validation, exact SHA checks, focused tests, full Vitest, build, and `git diff --check`.
- [ ] Commit central authority/ledger and public asset pipeline separately.

**Gate:** ledger, authority hashes, runtime manifest, built derivatives, network evidence, crop review, and public file removal agree.

### WP-40 — Gateway and Home reconstruction

**Initial tool:** OpenCode

**Task coverage:** Gateway refinement and `PUBLIC-190` structural/visual reconstruction; no status closure.

**Allowlist:**

- `src/pages/index.astro`
- `src/pages/{en,fa}/index.astro`
- `src/components/home/**`
- `src/lib/home-content.ts`
- `src/styles/{gateway,home}.css`
- Home/Gateway focused unit tests
- exact-locale stub generation only where tests prove current FA fallback violates the seed; do not add route families

**Forbidden:** tokens/global/base/shell styles, shared UI internals, promoted-media internals/assets, package/config files, central Docs, task status, new page-family routes.

**Required behavior:**

- [ ] Add failing tests for correct portal slot IDs, exact-locale filtering, absence of broken anchors, graph semantics, independent card actions, five EN interest cards, omitted FA EN-only cards/manuscripts, and unavailable action states.
- [ ] Rebuild Gateway with the centered ThemePicture, accurate source ratio, concept-aligned scale/crop, and preserved semantic language selection.
- [ ] Rebuild Home hero with the orbit ThemePicture, tokenized scrim, one H1, localized role content from the approved seed, and no English shared role line on FA.
- [ ] Use real Button/Link/Chip/SectionLead/Container or equivalent accepted primitives; do not recreate them in Home CSS.
- [ ] Render the research graph as a semantic list of links/labels over an `aria-hidden` ThemePicture backplate. Do not put `role="img"` around focusable descendants.
- [ ] EN renders five authorized interest cards. FA omits EN-only card records and presents only exact-locale authorized research-statement data in the graph/list.
- [ ] Render Journey as an ordered list using TimelineNode and Lucide icons, with descriptions only from approved content.
- [ ] Render exactly two approved project records in an intentional two-column feature grid; no placeholder card.
- [ ] Project media uses approved asset IDs and localized content alt supplied through the media contract.
- [ ] Keep manuscript links in `/writing`; omit EN-only manuscript cards and generated detail routes from FA.
- [ ] Rail previews use the three approved decorative assets. When Creative/Teaching routes are unavailable, render the seed-backed unavailable state without an anchor. Do not add those routes.
- [ ] Hero/CTA/Header actions to unavailable Research/About/CV/Contact routes are omitted or rendered through the shared unavailable state; no `href` may resolve to a missing built page.
- [ ] Replace giant card anchors with a semantic title link and independent action; non-interactive previews must not appear clickable.
- [ ] Isolate mixed-direction technical text with `bdi`/`dir="ltr"` only where the content requires it.
- [ ] Verify identical meaningful DOM order across locale/theme, no-JS readability, reduced motion, 320px reflow, and 200% zoom.
- [ ] Run focused tests, full Vitest, full Playwright acceptance harness, default build, design validator, and `git diff --check`.
- [ ] Commit Gateway and Home as separate reviewable commits.

**Gate:** no out-of-scope route, no content fallback, no broken anchor, no duplicated primitive, no raw public art, and all implementation tests pass. `PUBLIC-190` remains open.

### WP-50 — Independent visual and accessibility QA

**Initial tool:** Hermes

**Mode:** read-only for all implementation and authority files. The only allowed tracked write is the QA report `Docs/10-tracking/PUBLIC-190-VISUAL-QA.md` on its own coordination branch.

**Required matrix:**

| Target | Locale | Theme | Viewport |
|---|---|---|---:|
| Gateway | neutral language chooser | Light/Dark | 1440 |
| Gateway | neutral language chooser | Light/Dark | 390 |
| Home | EN | Light/Dark | 1440 |
| Home | FA | Light/Dark | 390 |
| Home | EN and FA | Light/Dark | 768 |
| Home and Gateway | applicable | Light/Dark | real browser 200% zoom |

Also spot-check 320, 1024, and 1280 CSS pixels because they are authority breakpoints.

**Automated checks:**

- correct `lang`, `dir`, canonical/alternate rules, and exactly one H1;
- no horizontal page overflow;
- keyboard order, skip link, navigation, theme, locale, CTA, graph nodes, cards;
- no axe serious/critical findings;
- content remains readable with JavaScript disabled and images blocked;
- reduced-motion removes non-essential continuous/transform motion;
- default build has no `/_design`; Atlas build has the 24/6 inventory;
- selected `currentSrc` is generated AVIF/WebP at a suitable width;
- initial request log contains only one theme variant per media slot;
- no deferred asset or raw multi-megabyte authority PNG is publicly addressable;
- all visible anchors return a built route or an expected external destination.

**Manual checks:**

- compare implementation and concept at the same viewport; assess hierarchy, typography, spacing, density, media language, crop, depth, and affordance;
- Light/Dark and RTL/LTR parity;
- real browser 200% zoom and 320px reflow;
- keyboard-only operation and visible focus;
- screen-reader landmarks, graph/list meaning, unavailable states, and mixed-direction reading;
- crop/focal integrity and absence of raster text;
- truthful partial/empty/unavailable content states.

Capture output goes under ignored `test-results/visual/`. Record each screenshot's SHA-256 in the report; do not commit binary baselines.

**Report result:** exactly one of:

- `PASS` — all automated gates pass, manual checks pass, and every visible deviation is documented as acceptable.
- `REVISE` — list each finding with severity, route, viewport, theme, locale, evidence path/hash, expected contract, and owning packet.

Hermes must not fix production code. A `REVISE` report returns the affected packet to its current or replacement worker.

### WP-60 — Master integration and owner acceptance

**Owner:** Master Chat and project owner.

- [ ] Review every worker diff and Handoff Bundle against its allowlist.
- [ ] Re-run design validator, Vitest, default build, Atlas build, Playwright, axe, and Git checks from the integrated branch.
- [ ] Confirm both repositories are clean except intended integrated commits.
- [ ] Review `PUBLIC-190-VISUAL-QA.md` and all screenshot hashes.
- [ ] Present a concise acceptance dossier to the owner without declaring acceptance.
- [ ] If the owner requests changes, assign a new revision packet and preserve the QA result as `REVISE`.
- [ ] Only after independent `PASS` and explicit owner approval, update `PUBLIC-190` to Done and unfreeze `PUBLIC-200+` in separate coordination/public status commits.

---

## 7. Test commands and expected gates

Use `npm.cmd` on Windows. Commands run from `Front-End/public-site` unless noted.

```powershell
npm.cmd install
npm.cmd run validate:design
npm.cmd test
npm.cmd run build
npm.cmd run build:atlas
npm.cmd run test:visual
npm.cmd run test:a11y
git diff --check
git status --short --branch
```

Authority validation runs from the coordination root:

```powershell
node Docs/references/frontend-design-authority/agent-kit/validate.mjs
```

Production Atlas leak check:

```powershell
Remove-Item Env:DESIGN_ATLAS -ErrorAction SilentlyContinue
npm.cmd run build
if (Test-Path -LiteralPath 'dist\_design') { throw 'Visual Atlas leaked into production build.' }
if (Select-String -Path 'dist\**\*' -Pattern '/_design' -SimpleMatch -ErrorAction SilentlyContinue) { throw 'Visual Atlas route leaked into production output.' }
```

Atlas positive check:

```powershell
$env:DESIGN_ATLAS='1'
npm.cmd run build
if (-not (Test-Path -LiteralPath 'dist\_design\index.html')) { throw 'Visual Atlas was not generated.' }
Remove-Item Env:DESIGN_ATLAS
```

Workers must report the command, exit code, and meaningful summary. “Passed locally” without output evidence is not a gate.

---

## 8. Checkpoint, token exhaustion, and reassignment protocol

No work depends on a particular model finishing a long conversation. A worker must checkpoint at each independently green step and before its context/token budget becomes unsafe.

### Checkpoint rules

- Commit only green, coherent work. Do not commit broken build output merely to save state.
- If the implementation is not green, leave the worktree intact and return the exact dirty manifest plus failing output; do not create a misleading completion commit.
- Never hand off “continue from my memory.” Hand off from a commit hash plus explicit uncommitted diff state.
- A replacement worker starts from the last accepted or checkpoint commit in a fresh worktree.
- Master Chat may reassign any packet or split its remaining unchecked steps without changing completed acceptance evidence.

### Required Handoff Bundle

Every worker response must end with this exact structure:

```markdown
## HANDOFF BUNDLE
Packet: WP-XX
Tool: <tool name>
Repository: <coordination|public-site>
Base commit: <full SHA>
Result commit(s): <full SHA list or NONE>
State: <review|blocked|token-exhausted>

Completed steps:
- <exact checklist items>

Remaining steps:
- <exact first unfinished action, then the rest>

Changed files:
- <path and purpose>

Tests:
- <command> — <exit code> — <result>

Dirty worktree:
- <clean, or exact git status lines>

Known risks or decisions:
- <evidence-backed item; NONE if empty>

Resume instruction:
Start from <commit SHA>. Read this execution authority and WP-XX. First run <exact command>. Then perform <exact next action>. Do not edit <conflict files>.
```

### Replacement-agent prompt

Master Chat fills and sends this when a tool runs out of tokens or becomes unavailable:

```text
You are replacing a previous worker on WP-XX. This is a continuation, not a restart.

Repository/worktree: <exact path>
Required base/checkpoint commit: <full SHA>
Execution authority: D:\Project\tahamohammadi-platform\Docs\superpowers\plans\2026-08-29-home-gateway-multi-agent-execution-authority.md
Previous Handoff Bundle: <paste verbatim>

Read all startup authorities, verify HEAD and git status, then run the first command in Resume instruction. Work only inside WP-XX's allowlist. Preserve accepted commits and tests. If the checkpoint cannot be reproduced, stop and return BLOCKED evidence; do not rebuild from memory or broaden scope.

Return the standard HANDOFF BUNDLE.
```

---

## 9. Copy/paste dispatch prompts

Master Chat supplies exact paths and SHAs before sending. Do not dispatch a queued packet early.

### Prompt for Codex — WP-10

```text
Execute WP-10 only from the approved Home + Gateway execution authority:
D:\Project\tahamohammadi-platform\Docs\superpowers\plans\2026-08-29-home-gateway-multi-agent-execution-authority.md

Coordination worktree: <exact path and branch>
Public-site worktree: <exact path and branch>
Coordination base SHA: <full SHA>
Public-site base SHA: <full SHA>

Read every required startup file. Verify both HEADs and clean status. Implement governance reconciliation, pinned design snapshots, dependency/tooling setup, failing acceptance harness, PUBLIC-070/080, and PUBLIC-130 exactly as WP-10 specifies. Use TDD. Do not implement shared UI components, assets, Home, Gateway, templates, or Atlas specimens. Keep root and public changes in separate commits.

Return two standard HANDOFF BUNDLE sections and do not claim visual acceptance.
```

### Prompt for Cursor — WP-20

```text
Execute WP-20 only from the approved Home + Gateway execution authority:
D:\Project\tahamohammadi-platform\Docs\superpowers\plans\2026-08-29-home-gateway-multi-agent-execution-authority.md

Public-site worktree: <exact path and branch>
Base SHA containing accepted WP-10: <full SHA>

Read every required startup file. Verify HEAD and clean status. Implement PUBLIC-140, then 150, then 160, then 170. Respect the exact allowlist and component ownership split. Use scoped styles, consume tokens, do not edit Home/assets/global CSS/package files, and do not add page routes. Make separate reviewable commits for components, shell, templates, and Atlas. Run the gates after each boundary.

Return one standard HANDOFF BUNDLE listing every commit in order.
```

### Prompt for image-capable Codex or ChatGPT Sol — WP-25

```text
Execute WP-25 only from the approved Home + Gateway execution authority:
D:\Project\tahamohammadi-platform\Docs\superpowers\plans\2026-08-29-home-gateway-multi-agent-execution-authority.md

This is an art-direction and image-generation packet with no repository writes. Read WP-25 and the two exact prompts in WP-30. Inspect the tracked Home Light/Dark concept references and pinned semantic palettes. Generate Light and Dark in separate built-in ImageGen calls. Validate full-resolution and 320px previews against every rejection rule. Iterate only when a specific defect exists.

Return: final image paths, dimensions, exact final prompts, generation mode, discarded-variant reasons, and a concise visual acceptance rationale. Do not modify code, Docs, authority manifests, checksums, or ledgers. Do not claim final project acceptance; Master Chat decides ACCEPT or REVISE.
```

### Prompt for Antigravity — WP-30

```text
Execute WP-30 only from the approved Home + Gateway execution authority:
D:\Project\tahamohammadi-platform\Docs\superpowers\plans\2026-08-29-home-gateway-multi-agent-execution-authority.md

Coordination worktree: <exact path and branch>
Public-site worktree: <exact path and branch>
Coordination base SHA containing accepted WP-10: <full SHA>
Public-site base SHA containing accepted WP-10: <full SHA>
Master Chat graph source paths and inspection decision: <paste exact paths and approval>

Read every required startup file. Verify both HEADs and clean status. Implement PUBLIC-260 exactly as WP-30 specifies: authority hashes, approved mappings, typed runtime manifest, Astro responsive media, single-theme loading, alt/crop ledger, graph source promotion, and removal of raw/deferred public assets. Do not edit Home/Gateway consumers, shared styles, package files, or routes. Keep root and public changes in separate commits.

Return two standard HANDOFF BUNDLE sections and measured build/media evidence.
```

### Prompt for OpenCode — WP-40

```text
Execute WP-40 only from the approved Home + Gateway execution authority:
D:\Project\tahamohammadi-platform\Docs\superpowers\plans\2026-08-29-home-gateway-multi-agent-execution-authority.md

Public-site worktree: <exact path and branch>
Base SHA containing accepted WP-10, WP-20, and WP-30: <full SHA>

Read every required startup file. Verify HEAD and clean status. Reconstruct Gateway and Home using only integrated Design System and promoted-media interfaces. Correct exact-locale content filtering and broken-link behavior without creating new page families. Do not edit shared component internals, tokens/global/shell styles, assets, package/config, central Docs, or task status. Use TDD and commit Gateway and Home separately.

Return one standard HANDOFF BUNDLE and do not claim PUBLIC-190 Done.
```

### Prompt for Hermes — WP-50

```text
Execute WP-50 independent QA only from the approved Home + Gateway execution authority:
D:\Project\tahamohammadi-platform\Docs\superpowers\plans\2026-08-29-home-gateway-multi-agent-execution-authority.md

Integrated public-site worktree: <exact read-only path or QA branch>
Integrated public-site SHA: <full SHA>
Coordination QA-report worktree: <exact path and branch>

Read every required startup file. Verify the integrated SHA and clean status. Run the entire automated and manual matrix in WP-50. Do not change implementation, tests, authority, assets, dependencies, or config. Screenshot artifacts remain ignored. Your only tracked write is Docs/10-tracking/PUBLIC-190-VISUAL-QA.md. The report result must be exactly PASS or REVISE and every finding must identify its owning packet.

Return the standard HANDOFF BUNDLE plus the QA result. Do not mark PUBLIC-190 Done.
```

---

## 10. Master Chat review contract

When the owner pastes a worker output into Master Chat, review in this order:

1. **Identity:** packet, repository, base SHA, result SHA, and worktree are explicit.
2. **Scope:** every changed file is inside the packet allowlist; no unrelated cleanup.
3. **Authority:** no reference instruction was executed as authority; no content/route/status was invented.
4. **Dependencies:** base includes all required accepted packets.
5. **Tests:** failing-first evidence exists; focused and full commands have real results.
6. **Conflict:** changed shared files have the correct phase owner and no integrated concurrent edit.
7. **Behavior:** inspect the actual diff, not the worker's summary.
8. **Visual claim:** screenshots/builds do not imply acceptance; only `WP-50 PASS` plus owner approval closes.

Master Chat responds with one of:

```text
ACCEPT — commit(s) may be integrated; next packet/base is ...
REVISE — keep packet open; exact required corrections are ...
BLOCK — do not integrate; authority/dependency/conflict is ...
```

For `REVISE`, Master Chat supplies a bounded revision prompt referencing the same packet and accepted base. For token exhaustion, Master Chat uses the replacement-agent prompt in Section 8.

---

## 11. Final acceptance dossier

Before asking the owner for visual acceptance, Master Chat provides:

- integrated root/public commit hashes;
- exact changed-file manifests per repository;
- Design System 24-component and six-template evidence;
- asset source hashes, runtime mappings, derivative formats/widths, byte ceilings, and network selection evidence;
- automated command results;
- matrix screenshot paths and SHA-256 values;
- independent QA result and unresolved deviations;
- confirmation that `PUBLIC-190` is still open;
- a single explicit owner decision request: accept or return named findings for revision.

No other page-family work resumes until that decision is recorded.

---

## 12. Technical references

- Astro integration `injectRoute`: <https://docs.astro.build/en/reference/integrations-reference/>
- Astro Assets and `Picture`: <https://docs.astro.build/en/reference/modules/astro-assets/>
- Tracked design authority: `Docs/references/frontend-design-authority/`
- Design System contract: `Docs/04-design/DESIGN-SYSTEM-SPEC.md`
- Responsive/RTL contract: `Docs/04-design/RESPONSIVE-RTL-SPEC.md`
- Visual QA contract: `Docs/04-design/VISUAL-QA-CONTRACT.md`
- Route/content composition: `Docs/01-product/owner-content-seed-v1/cms-package/route-composition.v1.1-seed.json`
