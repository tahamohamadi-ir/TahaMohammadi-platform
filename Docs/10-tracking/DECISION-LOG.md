# Decision Log

<!-- PRODUCT-V2.1 -->
2026-09-05 reconciliation: ADR-0010 records target interfaces, actual coverage, canonical execution graph, retired CA aliases and synchronized three-repository entry points. See `Docs/05-delivery/concept-alignment-v2/RECONCILIATION.md` for verification. Runtime, migration, deployment and owner visual acceptance remain open.
<!-- /PRODUCT-V2.1 -->

## 2026-09-05 — Research-first product extension

ADR-0009 records the owner's completed brief: unified research-driven identity, three presentation clusters, independent detail pages and broad admin editing. PRODUCT-SPEC, CMS-SPEC and PRODUCT-TASKS extend V2 with 15 families and 25 parent tasks. New routes and API capabilities are targets pending implementation; existing runtime and publication status are not advanced. User tooling was verified separately in V2 TOOLING.md.

| Date | Decision | Evidence |
|---|---|---|
| 2026-09-05 | Owner-directed concept alignment V2: rebuild hero/graph with GSAP + Three.js, put graph inside Home hero, reserve procedural portal for gateway under delegated design judgment; permit bounded existing-page visual remediation; preserve content and release gates | ADR-0008; `Docs/05-delivery/concept-alignment-v2/`; planning complete, runtime/visual acceptance open |
| 2026-08-28 | Use three independent GitHub repositories under one local workspace | Owner instruction and repository verification |
| 2026-08-28 | Rebuild both frontends from scratch | Owner instruction |
| 2026-08-28 | Copy the usable tracked backend baseline | Owner instruction and zero-mismatch copy check |
| 2026-08-28 | Keep design references central and non-executable | Reference manifest and authority boundary |
| 2026-08-29 | Treat `Front-End/Assets/concepts` as UI/UX source and `concepts/page-families` as page-detail source | Owner instruction |
| 2026-08-29 | Use a hybrid design-reference model: ignored local incoming source plus one curated tracked authority | Owner instruction and consolidation design |
| 2026-08-29 | Use same-origin reverse-proxy delivery as the pre-scaffold auth/CSRF baseline | Migrated backend production settings and deployment topology |
| 2026-08-29 | Treat global agent skills and plugins as workstation tooling, not product dependencies; use of a skill does not authorize repository, design-authority, contract, or runtime changes | Agent-tooling review; `02-architecture/DEPENDENCY-POLICY.md`; `04-design/DESIGN-AUTHORITY.md` |
| 2026-08-29 | Seed v1.1 + tracked design authority take priority over live legacy CMS content; replace `tahamohamadi.ir` with greenfield stack rather than migrate old DB unless a later task proves faster | Owner instruction; no legacy content migration in Wave 0 |
| 2026-08-29 | Home + Gateway recovery: retain `PUBLIC-190` as structure complete with visual acceptance open; freeze `PUBLIC-200+`; record approved logo/favicon, dashboard/PARS-SQL mappings, decorative rails, deferred visual-network asset, Home exclusion for ivory stairs, and semantic text-overlaid Light/Dark graph backplates | Approved Home + Gateway execution authority, Section 1 |
| 2026-09-02 | Accept ADR-0006 (error envelope normalization plan) by owner-delegated agent review; plan remains evidence-gated, no wire change by itself | Owner session instruction ("خودت بررسی کن، بهترین انتخاب رو انجام بده"); review verified inventory against source/fixtures; `Docs/09-decisions/ADR-0006-ERROR-ENVELOPE-NORMALIZATION.md` |
| 2026-09-02 | Approve the legacy route deprecation plan (`/admin/`, `/staff/`, `/api/admin/profiles/...`): phases evidence-gated, removals only via separate accepted ADR | Owner session approval; `Back-End/docs/contracts/LEGACY-ROUTE-DEPRECATION.md` |
| 2026-09-02 | G-E decision: add `DELETE /api/v1/admin/media/{id}` with a usage guard (admin media delete UX unblocked) | Owner session choice; `Back-End/docs/contracts/ADMIN-ROUTE-RECONCILIATION.md` gap G-E |
| 2026-09-02 | G-G decision: migrate profile sibling-locale creation from the legacy surface into the accepted admin API (`/api/v1/admin/`) | Owner session choice; `Back-End/docs/contracts/ADMIN-ROUTE-RECONCILIATION.md` gap G-G |
| 2026-09-26 | Plan D Task 8: retire the About Three.js mount — `ResearchUniverse.astro` deleted with its About-scoped CSS (`.ru-about*`, `.ru-controls*`); shared `.ru-*` base kept for HeroGraph; section position/heading/lead unchanged; About ships 0 canvases (EN+FA build proof) | Gates: EVIDENCE-C Tasks 1–24, Task 7 unit 4/4 on base `bddcebe`, EVIDENCE-D Task 6 parity; public-site `4959604` |
| 2026-09-26 | Plan D Task 9 ruling: about-preview SVG carries no per-node anchors by design (spec §14.1, aria-hidden presentation) — node `focus` deep-link coverage stays on the Atlas index (`product-atlas.e2e.ts`); `product-about.e2e.ts` asserts node count/CTA/prose/no-canvas/reduced-motion/axe instead, and subsumes `about-atlas.e2e.ts` (deleted); engineering heading not asserted — loader hardcodes `engineering_body: null` | public-site `5dd9ae3`; new spec 4/4 hermetic green |
| 2026-09-26 | Plan D Task 10: retire stale Home RU spec — live `https://tahamohamadi.ir/en/` 200 serves Hero v2 (`data-hero-*` ×9) with zero `data-universe-region`; `ru-home.e2e.ts` deleted; `playwright.research.config.ts` deleted with it (existed solely for `ru-*` CMS-gated suites; default/atlas/knowledge-atlas configs cover survivors); surviving coverage: Atlas → `product-atlas.e2e.ts`, Home presentation → Hero v2 specs | public-site `0570358`; Home pages render HomeHero, no production HeroGraph consumer |
