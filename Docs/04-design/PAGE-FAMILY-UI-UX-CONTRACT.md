# Page-Family UI/UX Contract

Each page family uses semantic templates and native controls. Raster concepts define hierarchy, media role, theme language, and responsive intent; they do not supply publishable copy, hard-coded records, or sliced controls.

| ID | Visual authority | Family | Required states | Required QA |
|---|---|---|---|---|
| PF-01 | `concepts/page-families/creative-index-light.png` | Creative collection | ready, empty, unavailable, error | Light EN, Dark EN, Light FA narrow, keyboard media navigation |
| PF-02 | `concepts/page-families/creative-detail-dark.png` | Visual/evidence detail | ready, media unavailable, private, error | Dark EN, Dark FA, captions, focus order, reduced motion |
| PF-03 | `concepts/page-families/writing-index-light.png` | Writing index | ready, empty, filtered, no-results, error | Light EN, Light FA, long label, no-JS listing |
| PF-04 | `concepts/page-families/projects-index-dark.png` | Sanitized projects collection | ready, empty, filtered, error | Dark EN, Dark FA, disclosure guard, image crop |
| PF-05 | `concepts/page-families/research-publications-index-light.png` | Research and publications | ready, empty, filtered, unavailable, error | Light EN, Light FA, graph/list parity, publication facts |
| PF-06 | `concepts/page-families/teaching-index-dark.png` | Teaching and learning | ready, empty, unavailable, error | Dark EN, Dark FA, course-card reading order |
| PF-07 | `concepts/page-families/about-cv-light.png` | About, profile, CV | ready, untranslated, document unavailable, error | Light EN, Light FA, 200% zoom, truthful file state |
| PF-08 | `concepts/page-families/contact-dark.png` | Contact and collaboration | idle, client validation, submitting, sent, server error, rate-limited | Dark EN, Dark FA, labels/errors, keyboard, no data persistence claim |

## Shared rules

- All families must support `fa` RTL and `en` LTR with one meaningful DOM order.
- Use logical CSS properties and isolate emails, URLs, identifiers, dates, and code.
- Headings, landmarks, labels, errors, empty messages, and recovery actions are semantic content, not image overlays.
- A visible raster placeholder is permitted only in local visual review; it must not become a published record or false claim.
- Responsive recomposition may change columns and media placement but not information hierarchy or keyboard order.
