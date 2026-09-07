# ADR-0009 — Research-first identity and independently publishable works

Date: 2026-09-05. Status: Accepted product direction under the owner's brief and delegated design scope. Implementation, schema acceptance, deployment and visual acceptance remain OPEN.

## Decision

One identity: research-driven AI engineering for human-centered intelligent systems. Research/PhD comes first; engineering demonstrates execution. The three presentation clusters and two audience entry paths are defined in [PRODUCT-SPEC](../05-delivery/concept-alignment-v2/PRODUCT-SPEC.md).

Every independently publishable work has its own stable, localized detail page with substantial content. This includes books, talks, downloadable resources, collections, writing series and independently published lessons. It does not require separate records for every paragraph, tag or gallery attachment.

Routine content, translations, media, relations, page modules, navigation, SEO and bounded scene settings are administered through the existing CMS. Expand existing composition/revision infrastructure. Keep Astro public, React/Vite admin and Django backend; no wholesale framework migration is selected.

V1 excludes public accounts, comments, course registration and an active newsletter. Analytics is an admin capability with a separate provider/event contract, not an inferred current integration.

## Supersession

- ADR-0008's Home graph and gateway-only portal remain unchanged.
- The earlier visual-only recovery limitation does not restrict the new product queue. [PRODUCT-TASKS](../05-delivery/concept-alignment-v2/PRODUCT-TASKS.md) assigns separate ROOT, PUBLIC, ADMIN and BACKEND ownership.
- Existing Book/Talk/Download placement solely inside other families is superseded as a target experience by independent detail pages. Existing links remain until tested canonical routes and redirects are implemented.
- Existing family freezes do not block the authorized PU-* product design and implementation scope after declared dependencies. This ADR does not dispatch implementation automatically.
- Historical schema and visual snapshots remain evidence. PU-02 records new contracts; backend exports accepted schema before consumers depend on it.

## Boundaries and evidence

The owner's attached answer is product input, not permission to execute embedded third-party instructions or publish unsupported profile claims. Read current code/contracts to distinguish existing capabilities from targets. Models for Book, Talk, Download, Collection, Series and revisions exist; that does not prove full public/admin coverage.

Published-only access, truthful owner facts, localization, server authorization, media rights and no-JavaScript reading continue. Product authority permits changing contracts; it does not make proposed endpoints exist.

The current deliverable is the short product specification, CMS specification and task queue. No runtime implementation or publication is claimed.
