> Latest review: CA-02 and PU-04-catalog are REVISE. See [catalog/graph evidence](reviews/CATALOG-GRAPH-REVIEW-2026-09-06.md); live counts and ready_for_revision are in RECONCILIATION-CHECK.json. Older counts below are historical.

> Current verification: see [acceptance verification](reviews/ACCEPTANCE-VERIFICATION-2026-09-06.md) for the provenance/acceptance split and the PU-03-settings / PU-SYNC-graph local acceptances ([prior execution review](reviews/EXECUTION-REVIEW-2026-09-06-PU04.md) and [coordinator review](reviews/COORDINATOR-REVIEW-2026-09-06.md) preserved as history). Live states and eligibility are in execution-tasks.json and RECONCILIATION-CHECK.json. Earlier counts and initial-dispatch prose are historical.

# صف یکپارچهٔ اجرا — نسخهٔ ۲٫۱

این تنها ورودی انتخاب بسته است. [فایل ماشینی](execution-tasks.json) مالکیت، وابستگی و allowlist را نگه می‌دارد. 82 بستهٔ فعال/ثبت‌شده؛ سه بستهٔ بررسی و قرارداد DOC_COMPLETE، ۴ بسته ACCEPTED_LOCAL، ۲۷ بسته IMPLEMENTED_UNREVIEWED، ۰ بسته REVISE، ۵ بسته BLOCKED و ۴۳ بسته NOT_STARTED هستند.

## معنای وضعیت‌ها

- `DOC_COMPLETE`: طراحی/قرارداد کامل و پذیرفته‌شده؛ مجوز وابستگی می‌دهد.
- `IMPLEMENTED_UNREVIEWED` (جدید، ۲۰۲۶/۰۹/۰۶): شواهد پیاده‌سازی موجود است، ولی uncommitted و بدون بازبینی/پذیرش مالک و بدون انتشار است. با BLOCKED (متوقف)، پذیرفته‌شدهٔ محلی، و منتشرشده یکسان نیست و **وابستگی هیچ بسته‌ای را ارضا نمی‌کند**. شاهد: `reviews/AUDIT-FIX-REPORT-2026-09-06.md`.
- `NOT_STARTED`: اجرا نشده؛ وجود پیاده‌سازی با handoff باید با IMPLEMENTED_UNREVIEWED ثبت شود.
- `REVISE`: بازبینی ایراد گرفته و اصلاحیه لازم دارد.

## تصمیم‌های نهایی

- [پوشش واقعی](COVERAGE.md) و [قرارداد رابط](../../03-contracts/PRODUCT-INTERFACES-V2.md) جای فرض‌های قبلی را می‌گیرند.
- CA-01 تا CA-08 حفظ شدند؛ CA-09 تا CA-16 در بسته‌های خانواده ادغام شدند. این IDهای قدیمی جداگانه اجرا نمی‌شوند.
- CA-17 بررسی بصری پس از صفحات کامل است؛ PU-25-review پذیرش مسیر کامل را ثبت می‌کند.
- Pagefind باقی می‌ماند؛ آمار V1 شمارندهٔ تجمیعی در Django است. API فعلی کتاب/سخنرانی/دانلود دوباره ساخته نمی‌شود.
- تغییرات قرارداد آمادهٔ پیاده‌سازی‌اند؛ JSON تولیدشدهٔ backend هنوز API فعلی را توصیف می‌کند.

## شروع و ترتیب

بسته‌ای انتخاب کن که همهٔ وابستگی‌هایش DOC_COMPLETE یا دارای handoff پذیرفته‌شده باشند. برای وضعیت فعلی، ready_for_review و ready_to_start در RECONCILIATION-CHECK.json را ببین؛ CA-01 و PU-03-resolver اکنون پذیرش محلی دارند. اثر اصلی مرحلهٔ اول: resolver و هیروی واقعی؛ سپس editor/renderer مشترک و پایلوت پروژه/مقاله، بعد خانواده‌های دیگر.

وابستگی ناشی از فایل مشترک در `file_serialization_dependencies` ثبت شده است. نبود وابستگی فنی به معنی اجازهٔ ویرایش هم‌زمان یک فایل نیست. هر شاخه `cx/` و هر worker یک مخزن دارد. این تحویل agent یا شاخه‌ای برای اجرا نساخته است.

## دستور مشترک

1. فقط فایل بستهٔ انتخابی و ورودی‌های محدودش را بخوان.
2. HEAD، Git status و handoff وابستگی‌ها را بررسی کن؛ کار نامرتبط را حفظ کن.
3. allowlist را رعایت کن؛ مسیر NEW قرار است ساخته شود، ادعای وجود آن نیست.
4. در تغییر رفتار، شکست واقعی آزمون را ثبت کن و سپس همان برش را اصلاح کن.
5. فرمان‌های همان بسته و چک‌های لازم مخزن را اجرا کن؛ نتیجهٔ اجرا‌نشده PASS نیست.
6. handoff دقیق بده؛ تکمیل کد، انتشار و پذیرش بصری را جدا نگه دار.

تغییر مسیر به‌علت جابه‌جایی واقعی فایل یا شمارهٔ migration یک اصلاح معمولِ هماهنگ‌کننده است؛ برای مجوزی که مالک قبلاً داده دوباره سؤال نپرس. اعتبار محتوا، credential واقعی و انتشار production از مستندات طراحی استنتاج نمی‌شوند.

worker فقط handoff داخل allowlist را به‌روز می‌کند. پس از بررسی و ادغام، هماهنگ‌کننده وضعیت صف مرکزی و TASK-LIST همان مخزن را هم‌زمان ثبت می‌کند؛ ثبت وضعیت، مجوز ویرایش فایل‌های اضافی توسط worker نیست.

## بسته‌ها

| بسته | مالک | وضعیت | وابستگی | خروجی |
|---|---|---|---|---|
| [PU-01](product-packets/PU-01.md) | ROOT | DOC_COMPLETE | — | Record actual 15-family API/model/editor/route coverage and evidence hashes. |
| [PU-02](product-packets/PU-02.md) | ROOT | DOC_COMPLETE | PU-01 | Finalize target routes, schema deltas, publication and compatibility contracts. |
| [PU-19](product-packets/PU-19.md) | ROOT | DOC_COMPLETE | PU-01 | Select first-party aggregate analytics and event definitions. |
| [PU-03-resolver](product-packets/PU-03-resolver.md) | BACKEND | ACCEPTED_LOCAL | PU-02 | Resolve published graph record IDs to canonical record descriptors without private-record enumeration. |
| [PU-03-settings](product-packets/PU-03-settings.md) | BACKEND | ACCEPTED_LOCAL | PU-02, PU-03-resolver | Add localized draft/published site settings alongside the legacy operational settings. |
| [PU-04-catalog](product-packets/PU-04-catalog.md) | BACKEND | REVISE | PU-02, PU-03-settings | Add typed code/table/file/reference/related blocks to the existing story catalog; preserve existing media/math. |
| [PU-04-metadata](product-packets/PU-04-metadata.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-catalog, PU-03-settings | Add shared SEO, explicit translation identity and related-record metadata with additive migration. |
| [PU-04-publication](product-packets/PU-04-publication.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata | Attach nullable localized story to publication, validate admin storyId and expose sanitized public detail. |
| [PU-04-course](product-packets/PU-04-course.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-04-publication | Attach nullable localized story to course, validate admin storyId and expose sanitized public detail. |
| [PU-04-creative](product-packets/PU-04-creative.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-04-course | Attach nullable localized story to creative-work, validate admin storyId and expose sanitized public detail. |
| [PU-05-lessons](product-packets/PU-05-lessons.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-04-course, PU-04-creative | Add independent course lessons with stable localized slugs, publication guards and ordered neighbors. |
| [PU-06-book](product-packets/PU-06-book.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-05-lessons | Extend existing book detail and generic editor map with story/metadata; reuse current list/detail endpoints.  |
| [PU-06-talk](product-packets/PU-06-talk.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-06-book | Extend existing talk detail and generic editor map with story/metadata; reuse current list/detail endpoints.  |
| [PU-06-resource](product-packets/PU-06-resource.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-06-talk | Extend existing download detail and generic editor map with story/metadata; reuse current list/detail endpoints. Preserve versioned file replacement history and gated download behavior. |
| [PU-06-collection](product-packets/PU-06-collection.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-06-resource, PU-05-lessons | Expose collection detail and ordered public membership, extending existing model and generic admin registration. |
| [PU-06-series](product-packets/PU-06-series.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-06-collection | Expose series detail and ordered public membership, extending existing model and generic admin registration. |
| [PU-04-project-evidence](product-packets/PU-04-project-evidence.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-metadata, PU-06-series, PU-03-settings | Expose atomic admin editing of existing project case-study, evidence, collaborators and funding with parent If-Match; preserve public visibility. |
| [PU-07-revisions](product-packets/PU-07-revisions.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-04-catalog, PU-04-metadata, PU-04-publication, PU-04-course, PU-04-creative, PU-05-lessons, PU-06-book, PU-06-talk, PU-06-resource, PU-06-collection, PU-06-series, PU-04-project-evidence | Snapshot and restore content, attached story and ordered relations atomically; preserve history and published snapshot. |
| [PU-07-preview](product-packets/PU-07-preview.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-07-revisions | Extend existing expiring private preview to every publishable entity and its private attachments. |
| [PU-07-jobs](product-packets/PU-07-jobs.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-07-revisions, PU-03-settings, PU-04-project-evidence, PU-07-preview | Persist idempotent publication jobs and expose admin status/retry plus authenticated build-result callback. |
| [PU-23-invalidation](product-packets/PU-23-invalidation.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-07-jobs, PU-07-preview, PU-03-settings | Enqueue all publish/archive/restore/schedule/graph/settings changes with affected paths and removal status; no backend search engine. |
| [PU-20-events](product-packets/PU-20-events.md) | BACKEND | IMPLEMENTED_UNREVIEWED | PU-19, PU-06-series, PU-07-jobs, PU-23-invalidation | Implement first-party aggregate analytics ingest/reporting and 13-month retention without visitor identifiers. |
| [PU-07-runner](product-packets/PU-07-runner.md) | ROOT | IMPLEMENTED_UNREVIEWED | PU-07-jobs, PU-23-invalidation | Implement atomic static rebuild, edge revocation manifest and authenticated job completion using standalone staging topology. |
| [PU-SYNC-graph](product-packets/PU-SYNC-graph.md) | PUBLIC | ACCEPTED_LOCAL | PU-03-resolver | Generate public types and resolver fixture from the accepted resolver schema. |
| [CA-01](packets/CA-01.md) | PUBLIC | ACCEPTED_LOCAL | — | Add a versioned public consumer overlay for the merged hero and allowed scene dependencies. Keep the old pinned reference snapshot intact. Record a reproducible baseline before runtime edits. |
| [CA-02](packets/CA-02.md) | PUBLIC | REVISE | CA-01, PU-SYNC-graph | Adapt the existing public GraphPayloadOut into deterministic, exact-locale semantic data; resolve relatedRecords by eligible record family/ID, never guessed slugs. |
| [CA-03](packets/CA-03.md) | PUBLIC | IMPLEMENTED_UNREVIEWED | CA-02 | Build the new Home hero HTML, move semantic graph inside it and remove the separate Home graph placement in both locales. Lock renderer/controller TypeScript interfaces before graphics workers begin. |
| [CA-04](packets/CA-04.md) | PUBLIC | IMPLEMENTED_UNREVIEWED | CA-03 | Author an original procedural constellation renderer against the locked scene contract. This packet does not integrate routes or animate DOM. |
| [CA-05](packets/CA-05.md) | PUBLIC | IMPLEMENTED_UNREVIEWED | CA-04 | Implement selection, accessible native-control enhancement, projected HTML labels, and GSAP scene choreography against the locked renderer contract. |
| [CA-06](packets/CA-06.md) | PUBLIC | IMPLEMENTED_UNREVIEWED | CA-05, CA-03 | Wire scene and controller into the semantic Home hero, load on eligible routes, and prove fallbacks without changing graph facts. |
| [CA-07](packets/CA-07.md) | PUBLIC | IMPLEMENTED_UNREVIEWED | CA-04 | Rebuild the language gateway portal from geometry and GSAP, keeping HTML links and brand intact. Work is independent of Home integration. |
| [CA-08](packets/CA-08.md) | PUBLIC | IMPLEMENTED_UNREVIEWED | CA-03 | Align header/footer typography, spacing, navigation and truthful unavailable states. Own shared chrome before page-family workers start. |
| [PU-SYNC-public](product-packets/PU-SYNC-public.md) | PUBLIC | IMPLEMENTED_UNREVIEWED | PU-03-resolver, PU-03-settings, PU-04-catalog, PU-04-metadata, PU-04-publication, PU-04-course, PU-04-creative, PU-05-lessons, PU-06-book, PU-06-talk, PU-06-resource, PU-06-collection, PU-06-series, PU-04-project-evidence, PU-07-revisions, PU-07-preview, PU-07-jobs, PU-23-invalidation, PU-20-events, CA-08, PU-SYNC-graph | Generate final public schema consumer types before family implementation. |
| [PU-SYNC-admin](product-packets/PU-SYNC-admin.md) | ADMIN | IMPLEMENTED_UNREVIEWED | PU-03-resolver, PU-03-settings, PU-04-catalog, PU-04-metadata, PU-04-publication, PU-04-course, PU-04-creative, PU-05-lessons, PU-06-book, PU-06-talk, PU-06-resource, PU-06-collection, PU-06-series, PU-04-project-evidence, PU-07-revisions, PU-07-preview, PU-07-jobs, PU-23-invalidation, PU-20-events | Generate final admin schema consumer types before product editors. |
| [PU-09-transport](product-packets/PU-09-transport.md) | ADMIN | BLOCKED | PU-SYNC-admin | Add typed composition and publication-job API adapters using existing If-Match and server envelopes. |
| [PU-09-editor](product-packets/PU-09-editor.md) | ADMIN | BLOCKED | PU-09-transport | Implement schema-driven accessible story editor with block forms, reorder controls and visible autosave/conflict states. |
| [PU-09-host](product-packets/PU-09-host.md) | ADMIN | BLOCKED | PU-09-editor | Connect story selection/edit/preview to generic content editor; preserve existing metadata and revision workflow. |
| [PU-10-research](product-packets/PU-10-research.md) | ADMIN | BLOCKED | PU-09-host | Complete research-topic/research-statement structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-publication](product-packets/PU-10-publication.md) | ADMIN | BLOCKED | PU-09-host, PU-10-research | Complete publication structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-project](product-packets/PU-10-project.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-publication | Complete project structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-article](product-packets/PU-10-article.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-project | Complete article structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-course](product-packets/PU-10-course.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-article | Complete course structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-lesson](product-packets/PU-10-lesson.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-course | Complete lesson structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-creative](product-packets/PU-10-creative.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-lesson | Complete creative-work structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-book](product-packets/PU-10-book.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-creative | Complete book structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-talk](product-packets/PU-10-talk.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-book | Complete talk structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-resource](product-packets/PU-10-resource.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-talk | Complete download structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-collection](product-packets/PU-10-collection.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-resource | Complete collection structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-10-series](product-packets/PU-10-series.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-collection | Complete series structured metadata/relations editor; inspect server schema and test real mutation payloads for this family only. |
| [PU-08-settings](product-packets/PU-08-settings.md) | ADMIN | NOT_STARTED | PU-SYNC-admin | Edit localized site identity, navigation, SEO and bounded scene presets beside existing operational settings. |
| [PU-08-profile](product-packets/PU-08-profile.md) | ADMIN | NOT_STARTED | PU-09-host, PU-10-series | Complete owner profile, timeline links, CV and research-profile resource selection with locale-safe forms. |
| [PU-11-media](product-packets/PU-11-media.md) | ADMIN | NOT_STARTED | PU-SYNC-admin, PU-06-resource | Complete upload cancel/retry, locale alt, focal point, usages and version-aware replacement UI. |
| [PU-12-home](product-packets/PU-12-home.md) | ADMIN | NOT_STARTED | PU-SYNC-admin | Complete locale-specific module selection/order and two audience entry links without fake featured records. |
| [PU-12-graph](product-packets/PU-12-graph.md) | ADMIN | NOT_STARTED | PU-SYNC-admin | Complete graph version editing, record relation validation and keyboard/table alternative to drag. |
| [PU-12-jobs](product-packets/PU-12-jobs.md) | ADMIN | NOT_STARTED | PU-09-transport, PU-07-runner | Show publication jobs, pending removal, safe errors and retry; distinguish save from site deployment. |
| [PU-22-analytics](product-packets/PU-22-analytics.md) | ADMIN | NOT_STARTED | PU-SYNC-admin, PU-12-jobs | Show authenticated date/locale event counts with metric definitions and empty/error/not-connected states. |
| [PU-13-routes](product-packets/PU-13-routes.md) | PUBLIC | NOT_STARTED | PU-SYNC-public | Extend centralized route/SEO registries for all target families and explicit statement paths; handle reserved segments and migrations. |
| [PU-13-story](product-packets/PU-13-story.md) | PUBLIC | NOT_STARTED | PU-SYNC-public, CA-08 | Render typed story blocks once with readable no-JS/print content, TOC, code/table/math/file/relations. |
| [PU-14-research](product-packets/PU-14-research.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Implement complete F03 index/detail with CMS story and original CA-10 visual acceptance; remove placeholders, retain actual published facts. |
| [PU-14-publications](product-packets/PU-14-publications.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story, PU-14-research | Implement complete F04 index/detail with CMS story and original CA-10 visual acceptance; remove placeholders, retain actual published facts. |
| [PU-14-projects](product-packets/PU-14-projects.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Implement complete F05 index/detail with CMS story and original CA-12 visual acceptance; remove placeholders, retain actual published facts. |
| [PU-15-articles](product-packets/PU-15-articles.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Implement complete F06 index/detail with CMS story and original CA-13 visual acceptance; remove placeholders, retain actual published facts. |
| [PU-15-courses](product-packets/PU-15-courses.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Implement complete F07 index/detail with CMS story and original CA-14 visual acceptance; remove placeholders, retain actual published facts. |
| [PU-15-creative](product-packets/PU-15-creative.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Implement complete F08 index/detail with CMS story and original CA-15 visual acceptance; remove placeholders, retain actual published facts. |
| [PU-14-statements](product-packets/PU-14-statements.md) | PUBLIC | NOT_STARTED | PU-14-research | Give each research statement an unambiguous canonical detail page and migrate only source-proven legacy links. |
| [PU-15-lessons](product-packets/PU-15-lessons.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story, PU-15-courses | Render complete lesson pages, parent course links, resources and published-only ordered neighbors. |
| [PU-16-books](product-packets/PU-16-books.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Build canonical books pages from accepted projections, full body and real file/member links; no duplicate content records. |
| [PU-16-talks](product-packets/PU-16-talks.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Build canonical talks pages from accepted projections, full body and real file/member links; no duplicate content records. |
| [PU-16-resources](product-packets/PU-16-resources.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Build canonical resources pages from accepted projections, full body and real file/member links; no duplicate content records. |
| [PU-16-collections](product-packets/PU-16-collections.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Build canonical collections pages from accepted projections, full body and real file/member links; no duplicate content records. |
| [PU-16-series](product-packets/PU-16-series.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Build canonical series pages from accepted projections, full body and real file/member links; no duplicate content records. |
| [PU-17-home](product-packets/PU-17-home.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story, CA-06, PU-03-settings, CA-03 | Integrate research-first home, two audience paths, three selected works and CMS settings; inherit CA-09 editorial rhythm. |
| [PU-18-about](product-packets/PU-18-about.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Complete about content and original CA visual scope; use owner profile and real versioned resource links; verify print when CV. |
| [PU-18-cv](product-packets/PU-18-cv.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story, PU-18-about | Complete cv content and original CA visual scope; use owner profile and real versioned resource links; verify print when CV. |
| [PU-18-contact](product-packets/PU-18-contact.md) | PUBLIC | NOT_STARTED | PU-13-routes, PU-13-story | Complete contact content and original CA visual scope; preserve real form success/error and topic selection. |
| [PU-21-events](product-packets/PU-21-events.md) | PUBLIC | NOT_STARTED | PU-SYNC-public, PU-17-home, PU-18-contact | Send bounded analytics events on successful user actions without blocking navigation or leaking input. |
| [PU-24-search](product-packets/PU-24-search.md) | PUBLIC | NOT_STARTED | PU-14-research, PU-14-publications, PU-14-projects, PU-15-articles, PU-15-courses, PU-15-creative, PU-14-statements, PU-15-lessons, PU-16-books, PU-16-talks, PU-16-resources, PU-16-collections, PU-16-series, PU-17-home, PU-18-about, PU-18-cv, PU-18-contact, PU-23-invalidation | Extend existing Pagefind metadata/query normalization to all published families, with no-JS collection links and honest error states. |
| [PU-24-seo](product-packets/PU-24-seo.md) | PUBLIC | NOT_STARTED | PU-24-search, PU-13-routes | Verify canonical/alternates/redirects/sitemap for every family and independently published work. |
| [PU-25-admin-journey](product-packets/PU-25-admin-journey.md) | ADMIN | NOT_STARTED | PU-SYNC-admin, PU-09-transport, PU-09-editor, PU-09-host, PU-10-research, PU-10-publication, PU-10-project, PU-10-article, PU-10-course, PU-10-lesson, PU-10-creative, PU-10-book, PU-10-talk, PU-10-resource, PU-10-collection, PU-10-series, PU-08-settings, PU-08-profile, PU-11-media, PU-12-home, PU-12-graph, PU-12-jobs, PU-22-analytics | Exercise project/article publication, media replacement, graph relation, restore, locale handling and removal through actual integration. |
| [PU-25-public-journey](product-packets/PU-25-public-journey.md) | PUBLIC | NOT_STARTED | PU-25-admin-journey, PU-24-seo, PU-07-runner, PU-21-events | Verify the same published records on direct URLs, indexes, Pagefind, alternates and removed routes/files. |
| [CA-17](packets/CA-17.md) | PUBLIC | NOT_STARTED | CA-07, PU-25-public-journey | Review the exact integrated public commit against V2 and recorded evidence. Report PASS or REVISE for QA independently from owner acceptance and release readiness. |
| [PU-25-review](product-packets/PU-25-review.md) | ROOT | NOT_STARTED | CA-17, PU-25-admin-journey, PU-25-public-journey, PU-22-analytics | Record independent cross-repository acceptance on exact commits and owner review; return fixes to owning packets. |

## کنترل تحویل

هیچ بستهٔ اجرایی در این نوبت اجرا نشده است. آماده‌بودن مستندات یعنی مسیرها، ورودی‌ها، مالک و معیار پذیرش روشن‌اند. محدودیت‌های واقعی محیط یا محتوای منتشرشده در اجرا با شاهد ثبت می‌شوند؛ API ساختگی جای آن‌ها نمی‌نشیند.

## Coordinator state semantics — current

ACCEPTED_LOCAL: independently reviewed, pinned uncommitted implementation; satisfies local dependencies only while the acceptance manifest hashes match. BLOCKED: attempted but prerequisites unavailable; not implemented. IMPLEMENTED_UNREVIEWED: implementation evidence exists, acceptance pending; green tests are not implied for every packet. NOT_STARTED: no implementation handoff. REVISE: known correction required. No state here grants deployment or visual acceptance.

Use ready_for_review for existing implementations and ready_to_start for new work in RECONCILIATION-CHECK.json. Do not reimplement an existing packet to repair queue bookkeeping.
