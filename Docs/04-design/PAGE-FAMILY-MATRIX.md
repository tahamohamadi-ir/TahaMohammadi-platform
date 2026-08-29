# Page Family Matrix

| Family | Template | Required states | Primary evidence |
|---|---|---|---|
| Language gateway | Gateway shell | ready, image unavailable | centered gateway references |
| Home | Home template | loaded, partial, honest empty | light and dark Home references |
| Research and publications | Collection index, evidence detail | loaded, empty, filtered, error | PF-05 research/publications Light |
| Projects | Collection index, evidence detail | loaded, empty, filtered, error | PF-04 projects Dark |
| Writing | Editorial index, long-form detail | loaded, empty, error | PF-03 writing Light |
| Teaching | Collection index, detail | loaded, empty, error | PF-06 teaching Dark |
| Creative | Collection index, visual detail | loaded, empty, error | PF-01/PF-02 creative Light/Dark |
| About and CV | Utility and evidence sections | loaded, untranslated, file unavailable | PF-07 About/CV Light |
| Contact | Utility form | idle, submitting, sent, validation error, service error | PF-08 contact Dark |
| Search | Utility search | loading, ready, no results, index unavailable | native design system |

Each route must use one shared family template.
Route-specific code supplies content and approved variations only.
The full per-family contract and visual QA matrix are in `PAGE-FAMILY-UI-UX-CONTRACT.md`.
