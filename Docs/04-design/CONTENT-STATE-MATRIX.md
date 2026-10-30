# Content State Matrix

| State | Meaning | Required presentation |
|---|---|---|
| `loading` | A bounded request is active | Named region and non-blocking status |
| `ready` | Valid content is available | Normal template |
| `empty` | Query succeeded with no records | Honest message and valid next action |
| `untranslated` | Alternate locale is unpublished | Link to available locale when authorized |
| `unavailable` | A known dependency is absent | Safe explanation without fabricated data |
| `error` | Request or validation failed | Recovery action and stable error message |
| `no-results` | Search or filter has no matches | Clear query reset action |
| `unauthorized` | Authentication is required | Sign-in path without leaking data |
| `forbidden` | User lacks permission | Safe denial and navigation recovery |
| `rate-limited` | Server accepted identity but rejected frequency | Safe wait/retry explanation without exposing limits or internal data |
| `conflict` | A revision changed after the editor opened it | Preserve unsaved work, show conflict state, and offer explicit refresh/compare recovery |

Decorative empty-state art must not replace the state message.
Icons must have bounded computed dimensions.
Form submissions distinguish transport failure, server validation, authorization, rate limit, and success; no generic success state is shown before backend confirmation.

## Granularity: page vs. section

The table above governs both levels, but the required presentation differs by scope:

- **Page level** (an index or detail route has no content at all): render exactly one state per the table above — most commonly a single `ContentState` (`unavailable` or `empty`) with a real heading, message, and a working action back to a live page. The rest of the page's normal layout (hero, filters, record list, pagination, related bands, …) is not rendered alongside it.
- **Section level** (the page has real content, but one sub-section of it does not): the section is **hidden**, not replaced with placeholder chrome. A section with no content contributes nothing to the page — no "Awaiting approved CMS copy" text, no skeleton rows, no disabled controls standing in for a feature that is not wired up. If every section on an otherwise-composed page is empty, the page-level state above applies instead.

This was a deliberate correction (2026-10): the page-family system previously substituted a full fabricated replica of the populated page — disabled filters, skeleton rows, a decorative "featured" band, fake pagination, placeholder bibliography rows — for the `unavailable`/`empty` states on every index and several detail pages. That is exactly the "fabricated data" the `unavailable` row's required presentation already prohibited; it was removed project-wide in favor of the single-`ContentState` pattern described above. See `src/components/{about,contact,creative,cv,projects,publications,research,teaching,writing}/*PageContent.astro` for the current pattern, and the equivalent tests in those directories (e.g. `public-210.behavior.test.ts`) for what is and is not expected to render.
