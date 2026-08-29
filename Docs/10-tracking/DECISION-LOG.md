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
