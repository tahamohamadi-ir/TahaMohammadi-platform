# Content completion implementation — 2026-09-07

User authority: implement the approved content-completion plan, controlled templates, all owner/public copy editable, seed initialization only, preserve existing implementations, and align all 15 families with V2 references.

Status: IN_PROGRESS. No release or visual acceptance is asserted.

Ruling: work in the existing four repositories on dedicated `cx/content-completion-2026-09-07` branches, retaining the user's uncommitted implementation. Fresh checkouts would omit that implementation and cause duplicate work. No commits, pushes, deployments or real database mutations are part of this execution.

## Work ownership

| Work | Owner | Interface/dependency | Decision |
|---|---|---|---|
| Queue reconciliation and contract coordination | ROOT | all packets | Preserve prior acceptance evidence; reopen affected packets and dependent review gates |
| Lesson and Story repair | PUBLIC | current generated schema | No backend schema edits; regression tests first |
| Seed safety | BACKEND | current seed importer | Independent of public repair; no real database writes |
| Managed localized copy and module data | BACKEND then ADMIN/PUBLIC | additive settings/schema | Backend produces contract before consumer generation |
| Remaining families and visual alignment | PUBLIC | shared renderers + managed copy | Reuse existing pages; verify against tracked concepts |
| Integration journeys and final review | each owner then ROOT | completed data flow | Real assertions, no placeholder E2E acceptance |

Each implementation task must record its source edits and verification below. Historical review files remain intact.
