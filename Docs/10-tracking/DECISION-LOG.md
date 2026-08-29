# Decision Log

| Date | Decision | Evidence |
|---|---|---|
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
