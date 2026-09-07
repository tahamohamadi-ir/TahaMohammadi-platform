# Actual coverage — 2026-09-05

Source-based inventory, not runtime acceptance. Hashes and repository HEADs are in SOURCE-INVENTORY.json. Public schema 0.4.0/admin schema 0.1.0 were parsed locally; code and routes were inspected. No staging mutation or database query was performed.

| Family | Current source/API evidence | Gap and owner packet |
|---|---|---|
| F01 Gateway | PUBLIC `src/pages/index.astro`; current raster assets | Procedural portal CA-07; localized settings PU-03-settings/PU-08-settings |
| F02 Home | PUBLIC `src/components/home/`; API `/api/graph/{locale}` + home-composition; ADMIN HomePage/GraphEditPage | Merged graph hero CA-01–06; ID/slug bridge PU-03-resolver; editorial/CMS PU-17-home |
| F03 Research | Topics/statements both have detail API and optional story; PUBLIC research-content and research/[slug] route | Explicit statement canonical route; shared story rendering PU-14-research/PU-14-statements |
| F04 Publications | DetailOut has bibliography/abstract/links; admin generic entity exists | Nullable story PU-04-publication; complete detail/editor PU-14-publications/PU-10-publication |
| F05 Projects | ProjectDetailOut includes story/case_study/evidence; admin generic + case-media subset | Full nested editor API PU-04-project-evidence; frontend PU-14-projects/PU-10-project |
| F06 Blog | ArticleDetailOut.story + body; generic ContentEditPage treats fields individually | Typed story renderer/editor PU-13-story/PU-09-*; family PU-15-articles/PU-10-article |
| F07 Education | Teaching/Course detail has body/outcomes/prerequisites; no Lesson model or endpoint | PU-04-course, PU-05-lessons, PU-15-courses/lessons, PU-10-course/lesson |
| F08 Gallery | Creative detail includes body/cover/gallery/rights; MediaPage exists | Structured story and polished detail/editor PU-04-creative/PU-15-creative/PU-10-creative/PU-11-media |
| F09 Books | `/api/books/{locale}/{slug}` + book generic entity; no books PUBLIC route | Extend story only; reuse endpoints PU-06-book/PU-16-books/PU-10-book |
| F10 Talks | `/api/talks/{locale}/{slug}` + talk entity; no talks PUBLIC route | PU-06-talk/PU-16-talks/PU-10-talk |
| F11 Resources | Download list/detail/gated file endpoints + download entity; only CV consumer placement | PU-06-resource/PU-16-resources/PU-10-resource and media replacement |
| F12 Collections/series | Collection model M2M exists but no exported public endpoint/admin entity; Series list exists, no detail | Ordered member/detail contracts PU-06-collection/series and matching PUBLIC/ADMIN packets |
| F13 About/CV | Profile APIs and profile-about adapter; current CV files/site settings; timeline editor | Typed owner editing and resource links PU-08-profile/PU-18-about/cv |
| F14 Contact | `/api/contact`; PUBLIC adapter and form | Refine existing form/CTAs in PU-18-contact; no email-service replacement |
| F15 Search/system | PUBLIC search-content.ts and src/integrations/pagefind.mjs | Extend existing static index and canonical metadata PU-24-search/seo; no backend search service |

## Cross-cutting findings

- Story exists on Article, ResearchTopic, ResearchStatement and Project. Do not recreate these columns. Extend missing families additively.
- Composition schema/CRUD and If-Match exist. A full visual block editor is absent from current ADMIN router/components; PU-09 creates it.
- Content revisions/restore exist. Atomic parent+story snapshots, all-family previews and published-snapshot isolation need explicit tests/extensions. Current preview-share entity map contains landing/profile/article only.
- Generic admin content entity list has 13 entries; collection/lesson are absent. Generic fields do not establish full nested evidence editing.
- Graph relatedRecords exposes family+id. Most public list/detail projections have no record ID. The original CA-02 instruction to resolve via list adapters is insufficient; I04 defines a limited resolver.
- `/api/site` has unlocalized identity strings; the existing contract prohibits public locale-sensitive use. I04 adds a compatible localized settings surface.
- Rebuild service defaults to a legacy host script and its trigger response is not deployment completion. No publication-job or analytics route appears in the reviewed OpenAPI.
- Current public package has Astro, GSAP and lucide; Three.js and React are absent. Three.js installation belongs only to CA-04. A React migration is not part of this plan.

## Status meaning

Existing source/API = observed implementation shape, not tested correctness or production availability. NEW/PROPOSED file labels in packets are intentional additions. Missing content and environment credentials are execution inputs; they do not prevent completing this design/contract handoff.
