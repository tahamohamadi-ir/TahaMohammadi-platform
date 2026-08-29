# OpenAPI Review Report — source snapshot

Status: **technical mapping reviewed; selected public-client baseline recorded; owner acceptance pending**.

Evidence source: `Back-End/docs/contracts/openapi/current/PROVENANCE.json`, generated against the recorded backend commit using development settings. The snapshot contains 40 public paths, 47 admin paths, and 103 operations. Endpoint-access fixtures pass in backend tests; this report does not turn the snapshot into an accepted public contract.

## Public route-family mapping

| Public family | Candidate observed endpoint(s) | Review result | Required acceptance decision |
|---|---|---|---|
| Gateway | None | No API required | Keep as static locale selection. |
| Home | `GET /api/home-composition/{locale}`, `GET /api/site` | Candidate available | Confirm whether a profile projection is also required and define cache/rebuild behavior. |
| About | `GET /api/profiles/{locale}/about` | Canonical baseline recorded from the existing profile seed and route registry | Render an honest unavailable state if no published `about` record exists. |
| Research | `GET /api/research/topics`, `/statements`, `/projects`, `/publications` per locale | Candidate available | Confirm the aggregate layout and which detail kinds receive public routes. |
| Publications | `GET /api/publications/{locale}[/{slug}]` | Canonical baseline recorded | Research-prefixed endpoint remains backend compatibility only. |
| Projects | `GET /api/projects/{locale}[/{slug}]` | Canonical baseline recorded | Research-prefixed endpoint remains backend compatibility only. |
| Writing | `GET /api/articles/{locale}[/{slug}]` | Candidate available | Freeze pagination/filter query names and legacy blog redirect mapping. |
| Teaching | `GET /api/teaching/{locale}[/{slug}]` and `/courses` aliases | Canonical baseline recorded | `/courses` remains backend compatibility only. |
| Creative | `GET /api/creative/{locale}[/{slug}]` and `/creative-works` aliases | Canonical baseline recorded | `/creative-works` remains backend compatibility only; rights-cleared visibility still applies. |
| CV / downloads | `GET /api/site`, `GET /api/downloads/{locale}[/{slug}]`, file stream | Canonical baseline recorded | `/api/site` is limited to locale-neutral operational fields; owner-approved file availability still applies. |
| Contact | `POST /api/contact`, `GET /api/site` | Candidate available | Accept field, abuse-control, success, and unavailable-email behavior. |
| Search | None | Baseline recorded: intentionally no API | Pagefind/local-index contract and honest unavailable-index response are required. |

## Admin workflow mapping

| Workflow | Observed endpoint group | Review result | Required acceptance decision |
|---|---|---|---|
| Session and MFA | `/auth/csrf`, `/auth/login`, `/auth/logout`, `/auth/me`, `/auth/mfa/*` | Candidate available | Freeze cookie/session expiry and re-auth UX. |
| Content and revisions | `/content/schema`, `/content/{entity}`, revisions, transitions, preview links | Candidate available | Freeze entity identifiers, revision conflict shape, and lifecycle vocabulary. |
| Media | `/media`, licenses, orphans, presentation, replace | Candidate available | Confirm no-delete policy or add an explicit governed deletion endpoint. |
| Home composition | `/home-modules/{locale}` and validation | Candidate available | Freeze `If-Match` conflict response and preview contract. |
| Timeline | `/timeline/{locale}` plus reorder | Candidate available | Freeze event/link validation and conflict response. |
| Research graph | `/graph/versions`, payload, validation, activation | Candidate available | Freeze graph publish policy and client validation display shape. |
| Profile/site settings | `/site`, `/tags`, `/featured`, content entities | Candidate available | Freeze owner-content boundary and permissions. |
| Rebuild / health | `/health/`, `/rebuild-trigger/` outside admin OpenAPI | Excluded from admin v1 | Keep both as infrastructure operations; no admin route/button/client call. |

## Acceptance blockers discovered by review

No unresolved API route, locale, or admin-workflow decision remains for scaffold foundation. Owner approval remains required for factual content, fonts, and runtime asset promotion under their separate gates.

No frontend may treat a candidate mapping above as accepted until each applicable decision is recorded in the API, locale, content, and error contracts.
