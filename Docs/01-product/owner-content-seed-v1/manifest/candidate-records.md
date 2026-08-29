# Owner Content Manifest

This registry is populated with **candidate records only**. It does not approve publication. Every public-facing record remains `needs-owner-input` or `private` until Taha explicitly approves the wording, source, and publication state.

## Record fields

| Field | Meaning |
|---|---|
| `content_id` | Stable internal manifest identifier |
| `surface` | Public route or admin setting that may consume the value |
| `locale` | `fa`, `en`, or locale-independent |
| `source_path` | Owner-provided file or approved backend record path |
| `source_hash` | SHA-256 when the source is a file |
| `approval_state` | `approved`, `needs-owner-input`, `private`, `unavailable`, or `superseded` |
| `publication_state` | `not-public`, `draft`, `published`, or `retired` |
| `translation_state` | `not-needed`, `approved`, `untranslated`, or `not-authorized` |
| `notes` | Scope and restrictions, not a substitute for the value itself |

## Candidate records

| content_id | surface | locale | source_path | source_hash | approval_state | publication_state | translation_state | notes |
|---|---|---|---|---|---|---|---|---|
| identity.name.en | /en/about | en | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Confirm preferred English spelling. |
| identity.name.fa | /fa/about | fa | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Confirm preferred Persian spelling. |
| identity.title.en | /en | en | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Primary professional title. |
| identity.title.fa | /fa | fa | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | عنوان حرفه‌ای اصلی. |
| profile.headline.en | /en | en | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Hero headline. |
| profile.headline.fa | /fa | fa | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | تیتر اصلی صفحه خانه. |
| profile.short-bio.en | /en/about | en | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Short public biography. |
| profile.short-bio.fa | /fa/about | fa | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | زندگی‌نامه کوتاه عمومی. |
| research.statement.en | /en/research | en | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Research statement; digital health/wearable phrased as developing direction. |
| research.statement.fa | /fa/research | fa | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | بیانیه پژوهشی؛ سلامت دیجیتال/پوشیدنی به‌عنوان مسیر در حال توسعه. |
| research.focus | /research | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Six focus areas; public labels need owner approval. |
| engineering.statement.en | /en/about | en | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Technical engineering summary. |
| engineering.statement.fa | /fa/about | fa | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | خلاصه فنی/مهندسی. |
| project.pars-sql | /projects/pars-sql | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Repository URL included; confirm project naming and public scope. |
| project.behavior-platform | /projects/behavioral-evidence | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | private | not-public | not-needed | Employer/IP-sensitive. Do not publish until explicit clearance. |
| project.dashboard-research | /projects/organizational-dashboards | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Confirm organization naming, screenshots, metrics, and media rights. |
| writing.visual-discourse | /writing/visual-discourse | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Manuscript in final revision; do not present as peer-reviewed publication. |
| writing.vtd-edge | /writing/vtd-edge | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Manuscript in preparation; exact title requires approval. |
| writing.dashboard-book | /writing/dashboard-book | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Book manuscript under revision; not published. |
| education.ma.visual-communication | /about/education | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Confirm dates/GPA/thesis wording against official records before publication. |
| education.ba.interior-architecture | /about/education | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Confirm dates/GPA against official records before publication. |
| experience.mci | /about/experience | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Keep employer-sensitive details out of public copy. |
| experience.naeo | /about/experience | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Organization naming and project disclosure require owner clearance. |
| experience.shaparak | /about/experience | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Confirm preferred organization naming. |
| experience.sajaya | /about/experience | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Confirm preferred organization naming. |
| learning.stanford-health-ai | /learning | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Publish only after certificate/credential source is added. |
| learning.partial-ml-dl-genai | /learning | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Must remain explicitly partial; not a completed certification. |
| availability.phd-2027 | /contact | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Time-sensitive availability statement; review regularly. |
| contact.email | /contact | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Preferred contact channel. |
| contact.linkedin | /contact | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Canonical LinkedIn URL. |
| contact.github | /contact | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Public GitHub profile. |
| contact.orcid | /contact | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Public ORCID identifier. |
| contact.location | /contact | locale-independent |  |  | needs-owner-input | not-public | not-needed | No public location selected yet. |
| contact.phone | /contact | locale-independent |  |  | private | not-public | not-needed | Private by default. |
| document.academic-cv | /cv | locale-independent |  |  | needs-owner-input | not-public | not-needed | Add owner-approved current academic CV file; record hash. |
| document.professional-resume | /cv | locale-independent |  |  | needs-owner-input | not-public | not-needed | Add owner-approved current professional resume file; record hash. |
| legal.copyright | sitewide | locale-independent | Docs/01-product/owner-content-seed-v1/source/owner-public-content.md | 0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770 | needs-owner-input | draft | not-needed | Owner/legal decision required before publication. |
| legal.privacy-contact | /contact | locale-independent |  |  | needs-owner-input | not-public | not-needed | Must match actual contact-form/data-processing implementation. |

## Source file integrity

`Docs/01-product/owner-content-seed-v1/source/owner-public-content.md` SHA-256: `0c8851020f78ef4424b67e8cd5c92772f813bf21a5d18bd13f4942781c6a1770`
