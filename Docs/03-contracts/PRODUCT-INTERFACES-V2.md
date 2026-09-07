# Product interfaces V2 — implementation contract

Status: accepted target for scoped implementation under ADR-0010. **Not a deployed API or a replacement for source-generated OpenAPI.** Existing consumers continue using the current snapshots until the owning backend packet exports and verifies its additive change.

## I01 — Existing interfaces to reuse

Snapshot evidence: `Back-End/docs/contracts/openapi/current/public-openapi.json` version 0.4.0 and `admin-openapi.json` version 0.1.0. Exact hashes and source coverage: `Docs/05-delivery/concept-alignment-v2/SOURCE-INVENTORY.json` and `COVERAGE.md`.

| Work | Existing public list / detail prefix | Existing admin entity | Delta |
|---|---|---|---|
| Article | `/api/articles/{locale}` / `/{slug}` | `article` | Render existing story; richer editor |
| Research topic | `/api/research/topics/{locale}` / `/{slug}` | `research-topic` | Render existing story and separate statement routes |
| Research statement | `/api/research/statements/{locale}` / `/{slug}` | `research-statement` | Dedicated canonical page |
| Publication | `/api/publications/{locale}` / `/{slug}` | `publication` | Optional story + metadata/relations editing |
| Project | `/api/projects/{locale}` / `/{slug}` | `project` | Render existing story/case study; expand admin evidence coverage |
| Book | `/api/books/{locale}` / `/{slug}` | `book` | Public page absent; add optional story |
| Talk | `/api/talks/{locale}` / `/{slug}` | `talk` | Public page absent; add optional story |
| Resource | `/api/downloads/{locale}` / `/{slug}` | `download` | Reuse gated file endpoint `/{slug}/file`; add story/version history |
| Course | `/api/teaching/{locale}` / `/{slug}` | `course` | Optional story + independently published lessons |
| Creative work | `/api/creative/{locale}` / `/{slug}` | `creative-work` | Optional story; retain gallery/rights |
| Series | `/api/series/{locale}` list only | `series` | Add detail with ordered members |
| Collection | No endpoint in reviewed public snapshot | Not in generic entity registry | Add entity, ordered members and projection |

Existing admin CRUD: `/api/v1/admin/content/{entity}` and `/{id}`; schema, transition, revisions and restore already exist. Updates use the existing If-Match timestamp behavior. Composition CRUD/schema and optimistic locking already exist at `/api/v1/admin/composition`. Existing composition statuses exclude scheduled; content lifecycle includes scheduled. Do not offer scheduling for a composition merely because a content entity supports it.

Media upload/edit/replace/presentation, graph payload/version activation, home modules and global site settings already exist. Extend these surfaces instead of duplicating them. Public aliases `/courses`, `/creative-works`, `/research/projects` and `/research/publications` remain compatibility-only.

## I02 — Canonical frontend routes

All entries below have the `/{locale}/` prefix; locale is exactly fa/en. Existing families keep their current canonical paths. API path names do not dictate browser path names.

| Browser path | Source | State |
|---|---|---|
| `books/`, `books/{slug}/` | Existing books endpoints | New PUBLIC routes |
| `talks/`, `talks/{slug}/` | Existing talks endpoints | New PUBLIC routes |
| `resources/`, `resources/{slug}/` | Existing downloads endpoints | New PUBLIC routes |
| `collections/`, `collections/{slug}/` | I05 collections endpoints | New BACKEND + PUBLIC |
| `blog/series/{slug}/` | I05 series detail | New detail; series list remains on blog |
| `education/{courseSlug}/lessons/{lessonSlug}/` | I05 lessons | New BACKEND + PUBLIC |
| `research/statements/{slug}/` | Existing statement detail | New canonical path; topic retains `research/{slug}/` |

Reserve `series` within article slug namespace and `statements` within research topic namespace for new records. Existing collisions require an explicit migration map preserving the published URL through tested redirects; never rename silently. A topic and statement with the same slug must not compete in one route. Existing statement links move only after the migration manifest identifies their present meaning.

All lists are linked pages, not just modal launchers. Old writing/teaching/creative redirects stay. Slug changes use a durable per-family/locale redirect registry: unique old path, cycle rejection, published target validation; unknown/deleted targets produce unavailable/404, not redirects to unrelated content. No redirect is inferred from a title.

## I03 — Shared content and story extensions

Reuse current public `story` structure: `{locale, title, sections:[{layout,ratio,blocks:[{blockType,settings}]}]}`. Public projection removes disabled sections/blocks, sanitizes content and resolves only public media. Add a nullable `story` to missing detail schemas; existing body/description fields remain compatible. A published story must match parent locale. A draft edit must not change the currently published document until explicit publication.

Add admin `fields.storyId` for missing entity maps; retain existing field names. Add typed publication metadata: `seoTitle`, `seoDescription`, `socialImageId`, `translationKey`, and ordered `relatedRecords` where missing. Public additions: `seo:{title,description,image}`, `alternates:[{locale,slug,routeFamily,courseSlug?}]`, `relatedRecords:[WorkRef]`. Empty optional metadata falls back to that record's actual title/summary, not another locale or raster text. Translation identity is stable and explicit; equal slugs do not prove a translation relationship.

`WorkRef` target: `{family,id,locale,slug,title,summary,routeFamily,courseSlug?}`. IDs refer to existing records; `courseSlug` only for lessons. The backend validates allowed family and exact-locale publication. Public references to unpublished/missing items are omitted. Admin sees a safe validation issue without treating that record as public.

`family` uses the existing graph wire convention: lowercase Django model name (`researchtopic`, `researchstatement`, `creativework`), not the hyphenated admin entity name. `id` is the existing positive record ID serialized as a decimal string. Use the registry in `apps/api/admin_common.py` and an explicit mapping to browser route families. Extend the registry for collection/lesson only when their projections exist. Never silently rewrite existing graph payload keys.

Block catalog additions: `code {code,language,caption?}`, `table {caption,columns:[{key,label}],rows:[object]}`, `file {downloadId,label?}`, `references {items:[{label,url?}]}`, `related {records:[{family,id}]}`. All settings reject unknown keys; no executable JS/MDX. Existing figure can carry a sanitized SVG diagram. Limits: code 100k characters, table 20 columns/500 rows, references 100 entries, related 24 records; larger data is a downloadable resource. Use existing math/media blocks; do not add a second format for them.

`heading` levels must produce a valid document outline; IDs derive deterministically from block identity/order with collision handling. Legacy accordion/tabs must expose their text in no-JS/print output. Unknown block versions block new publication; historical content remains readable through its supported renderer.

Revision target: snapshot parent fields, relations and full attached composition together. Restore is atomic and creates a new revision; never mutates history. Preview covers every publishable entity, is expiring/noindex/private, and cannot expose a public media URL for private files. Extend the existing preview service; do not manufacture public preview routes. Enforcement (A04, 2026-09-06): public reads serve the latest publication snapshot while the live row is a draft workspace (restore-as-draft enqueues no removal); only explicit archive invalidates snapshots and removes the document from public reads.

Project editing gap: add `GET|PUT /api/v1/admin/content/project/{id}/case-study` with parent If-Match and atomic `{details,evidence,collaborators,funding}` update. `details` uses existing model fields `depth,problem,constraints,technical_decisions,trade_offs,outcomes_summary,lessons_learned,testing_summary`; nested row fields come from the existing models and must be enumerated by the source-generated admin schema. Existing diagram/screenshot endpoints are reused. Publish checks respect evidence visibility and existing featured-case requirements; a nested draft/private row never leaks through the public projection.

Nested update rows: evidence `{id?,label,value,source,last_verified,visibility}`; collaborators `{id?,name,role,publication_approved}`; funding `{id?,funder,grant_id,publication_approved}`. For this full-aggregate PUT, omitted rows are removed only after a usage summary/confirmation in admin; IDs belonging to another project are rejected. Values/enums follow existing model validation, not frontend guesses. New row IDs are allocated by the backend; audit and revision snapshot cover the whole transaction.

## I04 — Localized settings and reference resolution (new endpoints)

`GET /api/v1/site/{locale}` → `{locale,revision,brandName,tagline,footerText,seo:{title,description},navLinks:[{label,href}],audienceLinks:[{kind,label,href}],scene:{graphPreset,portalPreset,motion,density},updatedAt}`. `kind`: research/employment; presets are named renderer-supported enums, motion off/reduced/full, density low/standard. No arbitrary shader/code/CSS. Missing localized settings return 404; no other-language fallback. Home module contents still come from existing home-composition and home-modules surfaces.

V1 preset values are `graphPreset: "atlas-v2"` and `portalPreset: "arch-v2"`; introducing another value requires matching renderer and schema changes. `revision` is an opaque server-issued string. nav/audience arrays contain at most 20/2 entries respectively. href permits registered site-relative paths or validated https professional links; reject javascript/data URLs and unknown local routes. Theme contrast is validated for both presets, not left to arbitrary owner CSS.

`GET|PUT /api/v1/admin/site/{locale}` uses the same editable fields plus draft/published state and If-Match. PUT validates both link destinations and preset choices; returns persisted state. Add `POST /api/v1/admin/site/{locale}/publish` to publish the draft snapshot and enqueue I06. Existing `/api/site` and `/api/v1/admin/site` retain operational/contact/download compatibility; localized strings migrate explicitly with no automatic translation. Frontend falls back only to already approved exact-locale content while this endpoint is absent.

`GET /api/v1/records/{locale}/resolve?refs=family:id,family:id` → `{items:[WorkRef],unresolved:[{family,id}]}`. Maximum 50 unique references; preserve request order among results, malformed input 400. Unresolved response does not distinguish private, missing or unpublished records. No broad identifier enumeration endpoint. Use this to bridge graph `relatedRecords {family,id}` to real slugs: existing list projections generally lack IDs. Old `/api/graph/{locale}` remains compatible.

Resolver R1 clarification: IDs use canonical ASCII `[1-9][0-9]*` within the actual record-key storage range. Reject leading zeros, non-ASCII digits and overlong/out-of-range integers before conversion/query; malformed values return the I08 envelope, never an unhandled conversion error.

## I05 — Collection, series and lesson endpoints (new)

`GET /api/v1/collections/{locale}` → `{count,items:[CollectionCard]}` with page/pageSize (1-based, default 20, max 50). Detail: `GET /api/v1/collections/{locale}/{slug}` → `{locale,slug,title,description,curatorName,criteria,curatedDate,story,items:[WorkRef],seo,alternates}`. Card omits story/items. Reuse Collection model; migrate existing M2M members to ordered membership records deterministically. Support all publishable families, reject cycles and duplicates, preserve existing members.

`GET /api/v1/series/{locale}/{slug}` → `{locale,slug,title,description,story,items:[WorkRef],seo,alternates}`; members are ordered articles only. Keep existing series list and article `series` filter. Explicit member positions replace incidental ordering; removed drafts are not public neighbors.

`GET /api/v1/lessons/{locale}?course={courseSlug}` → `{count,items:[LessonCard]}`. Detail: `GET /api/v1/lessons/{locale}/{courseSlug}/{lessonSlug}` → `{locale,slug,title,summary,courseSlug,position,story,resources:[WorkRef],previous:WorkRef|null,next:WorkRef|null,seo,alternates}`. Both parent and lesson must be published in the requested locale. Add Lesson model with lifecycle/localization, required Course FK and uniqueness `(course,locale,slug)`. Parent and lesson locales must match.

Admin uses existing generic content endpoints with registered entities `collection` and `lesson`. Fields add `courseId`, `position` for lessons; `members:[{family,id,position}]` for collections/series, existing metadata and `storyId`. Schema must expose structured field types/options so the generic editor can render controls. Admin-only IDs never become guessed public URLs.

## I06 — Publishing, rebuilding and removal

Current rebuild helpers can start a legacy script; no reviewed admin job-status API proves a completed deployment. Replace that integration through scoped tasks, preserving existing signed trigger compatibility until its replacement is verified.

Create persisted publication jobs with idempotency key, requested content revision, locale, affected paths, state `queued|running|succeeded|failed`, timestamps, safe error code and deployed revision. Enqueue after transaction commit for publish, scheduled publish, archive, restore-to-published, graph activation and localized settings publication. Multiple changes may coalesce; record which revisions each successful job includes.

Job wire shape: `{id,state,locale,requestedRevision,deployedRevision,affectedPaths,revokedPaths,removalState,createdAt,startedAt,finishedAt,errorCode,updatedAt}`. `id` is a UUID string, revisions are opaque strings, deployedRevision/errorCode and start/finish timestamps may be null. locale is fa/en or null for a multi-locale job. affectedPaths is an array of canonical path strings. `affectedPaths` is the rebuild set: the record's own URLs plus shared pages (locale home, list indexes, parent aggregates) so a fresh build drops references from indexes/search. `revokedPaths` (A01, 2026-09-06) is the deny set: the record's own detail/file URLs only, never shared pages; archiving one record must not deny home or list pages. The runner denies only `revokedPaths` (pre-A01 payloads without the key fall back to `affectedPaths`). removalState is `not_requested|pending|effective|failed`. All timestamps are ISO 8601 UTC. List response is `{count,items}` with page/pageSize default 1/20, max pageSize 50. Retry accepts `{}` plus `Idempotency-Key` and current If-Match; repeated same key returns the same job, not another deployment.

New admin endpoints: `GET /api/v1/admin/publication-jobs` (paged/filterable), `GET /api/v1/admin/publication-jobs/{id}`, `POST /api/v1/admin/publication-jobs/{id}/retry` (If-Match/idempotent). Success means deployed artifact plus Pagefind/sitemap match the requested content snapshot; process creation is not success.

ROOT build runner uses current `Infra/staging/` topology, explicit configured checkout roots and authenticated machine callbacks `POST /api/v1/internal/publication-jobs/{id}/result`. Callback authenticates method+path+timestamp+body digest, rejects replay and stale timestamps. Never expose secrets in job output. This internal route is not a public anonymous operation.

A configured runner receives only the job UUID as its process argument. It reads its payload through authenticated `GET /api/v1/internal/publication-jobs/{id}`. Machine authentication headers: `X-Publication-Timestamp` (Unix seconds), `X-Publication-Nonce` (unique UUID), and `X-Publication-Signature` (hex HMAC-SHA256). Signed text joins uppercase method, path, timestamp, nonce and hex SHA256 of exact body bytes with newline separators. Reject timestamps outside 300 seconds, reused nonces and empty/missing configured secrets. Use no query-string secrets. Internal endpoints stay off the anonymous edge routing surface.

Result body: `{state,artifactRevision?,errorCode?}` where state is running/succeeded/failed. A transactional compare-and-set admits queued→running→succeeded/failed; repeated identical final results are idempotent, conflicting terminal transitions return 409. The running claim is exclusive (A03, 2026-09-06): only queued→running succeeds — a second claim gets 409 and the losing runner stops without building; terminal results require the claim, so queued→succeeded/failed is 409. succeeded requires artifactRevision matching the requested publication snapshot; failed requires a safe registered errorCode. Every job carries a non-empty server-issued opaque revision when the caller passes none. The runner verifies the full artifact set (site entry, sitemap, Pagefind) before the atomic swap and never serves a partial release; a job left running whose artifact is already active is resumed, otherwise recovery is a fresh admin retry job. The runner confirms edge-deny effectiveness independently before sending effective removal status through its authenticated result extension `{removalState?:"effective"|"failed"}`. Effectiveness is staged and fail-closed (A02, 2026-09-06): manifest write, file-content check, configured edge validate+reload, and an HTTP 404 probe of every revoked path at the ingress. Manifest text alone never counts as proof; any configured stage failure reports removal failed, never effective. Deployed revision and removal state never come from a browser claim.

Failed ordinary publish leaves last successful site visible with a clear admin pending/error state. **Unpublish/revoke must not wait for a rebuild to hide content**: push affected paths to an edge deny manifest before reporting removal complete; invalidate related pages/index/artifacts and gated files. If this step fails, report removal pending/failed, never removed. A direct static media URL cannot provide revocation; use existing gated download delivery or scoped edge invalidation for revoked public files. Runner publishes an atomic directory/revision swap and retains rollback artifacts; no live deploy is authorized by this planning delivery.

## I07 — Search and analytics

Keep Pagefind in `public-site/src/integrations/pagefind.mjs`. Index rendered, exact-locale published pages; mark record type/axis for filters, exclude preview/404/private/redirect pages. Normalize Persian query variants. Full-text search needs JS; no-JS users get linked collection navigation. Reading content never needs JS. No new backend full-text search service.

Analytics provider decision: first-party aggregate counters in the existing Django/PostgreSQL service, with no external paid service or visitor accounts for V1. New `POST /api/v1/analytics/events` accepts `{event,pagePath,locale,target?}`; event enum `page_view|cv_download|research_profile_download|demo_click|contact_click|contact_submit_success`. pagePath must be a valid canonical path without query/fragment. target is a registered action ID, never arbitrary text/URL. Server timestamps the event, rejects oversized/unknown fields and enforces same-origin/rate limits. Do not collect email, message, full referrer URL, cookie ID or persistent visitor identifier. Operational abuse logs follow their existing policy separately. Enforcement (A09, 2026-09-06): pagePath must match a registered canonical route whose locale equals the event locale (the locale-neutral gateway `/` excepted); the V1 target registry is exactly `cv_download → {academic_cv, industry_resume}` with an empty target required for every other event until its sender registers real action IDs; bodies over 4096 bytes are rejected with 413; every ingest rejection uses the I08 error envelope (schema-shape failures keep 422 with the envelope).

Store daily aggregates only: date, locale, path, event, target, count; 13-month rolling retention. Label metrics **received events**, not unique people, professors, applications or verified human visits. Bots/retries may inflate counts; document this next to reports. New `GET /api/v1/admin/analytics?from=YYYY-MM-DD&to=YYYY-MM-DD&locale=...` returns `{from,to,timezone:"UTC",updatedAt,metric:"received_events",rows:[{date,pagePath,locale,event,target,count}]}`; maximum 366 days. Authentication/OTP required; no public read endpoint. Failed analytics must not block navigation or forms.

## I08 — Compatibility and validation

New endpoint errors follow ERROR-CONTRACT target envelope. Existing endpoint errors retain ERROR-COMPATIBILITY-MATRIX until explicitly migrated. Admin session, OTP, CSRF, authorization and If-Match checks remain server-enforced. A frontend flag never grants a permission.

Each BACKEND packet owns schema export and targeted contract tests. Generated current snapshots are never edited manually. Separate PUBLIC/ADMIN synchronization packets generate types and test fixtures from the accepted backend snapshot; handoff pins its hash. After later backend changes, repeat those same synchronization packets before consumer integration. No unbounded lockfile/dependency edits are implied.

Data migrations are additive first: nullable story/SEO/translation additions; deterministic ordered-member backfill; no fabricated text, translation or publication state. Migrations need forward/backout evidence on a database copy. Preserve old endpoint/field behavior until all consumers pass their tests. User content still controls whether a particular record can be published.
