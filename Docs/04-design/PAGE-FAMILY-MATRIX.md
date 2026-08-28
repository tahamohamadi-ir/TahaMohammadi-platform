# Page Family Matrix

| Family | Template | Required states | Primary evidence |
|---|---|---|---|
| Language gateway | Gateway shell | ready, image unavailable | centered gateway references |
| Home | Home template | loaded, partial, honest empty | light and dark Home references |
| Research and publications | Collection index, evidence detail | loaded, empty, filtered, error | research/publications reference |
| Projects | Collection index, evidence detail | loaded, empty, filtered, error | projects reference |
| Writing | Editorial index, long-form detail | loaded, empty, error | writing and blog references |
| Teaching | Collection index, detail | loaded, empty, error | teaching reference |
| Creative | Collection index, visual detail | loaded, empty, error | creative references |
| About and CV | Utility and evidence sections | loaded, untranslated, file unavailable | about/CV reference |
| Contact | Utility form | idle, submitting, sent, validation error, service error | contact reference |
| Search | Utility search | loading, ready, no results, index unavailable | native design system |

Each route must use one shared family template.
Route-specific code supplies content and approved variations only.
