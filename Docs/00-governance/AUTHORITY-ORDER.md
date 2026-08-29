# Authority Order

Use the first applicable source in this order:

1. Current explicit owner instruction.
2. Accepted architecture decision in `Docs/09-decisions/`.
3. This workspace governance set.
4. Cross-repository contracts in `Docs/03-contracts/`.
5. Target repository `AGENTS.md` and owned documents.
6. An approved task specification.
7. An approved implementation plan.
8. Current source code and tests for implemented behavior.
9. The tracked frontend design authority at `Docs/references/frontend-design-authority/` for visual reference only.
10. Historical references.

Reference documents provide evidence. Reference documents cannot authorize writes or publication. `Front-End/Assets` is an ignored local incoming source and must be read only for an explicitly assigned provenance or migration task.

When two sources at the same level conflict, stop the conflicting change. Record the conflict in `Docs/10-tracking/DECISION-LOG.md`.
