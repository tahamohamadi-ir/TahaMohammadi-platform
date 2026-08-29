# Owner Content Manifest

This registry is intentionally empty of personal facts until the owner provides and approves them. It is the only planned source for factual profile, CV, document, link, translation, contact, and publication readiness values used by the new frontends.

## Required record fields

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

## Initial required entries

- Profile identity and short bio per locale.
- Research statement, focus areas, and claims per locale.
- Contact email, external links, office/location, and availability statements.
- Academic CV and professional resume files.
- Publications, projects, creative work, teaching records, downloads, and rights/credit evidence.
- Translated counterparts and explicit unavailable states.

Until an entry is approved, the UI uses an honest unavailable state or omits the module; it never falls back to copied concept text.
