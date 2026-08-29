# Route Registry

## Rule

Locale is part of every public route. The root `/` is a language gateway. Each published page must set `lang`, `dir`, canonical URL, and alternates from this one registry. Detail slugs come only from accepted backend projections; no frontend fallback slug is permitted.

## Canonical route families

| Family | English and Persian path shape | Detail policy | Status |
|---|---|---|---|
| Gateway | `/` | None | Design accepted; runtime not scaffolded |
| Home | `/{locale}/` | None | Design accepted; runtime not scaffolded |
| About | `/{locale}/about/` | Fetch only `/api/profiles/{locale}/about`; profile sections are anchors, not fabricated detail records | Design accepted; unavailable state when the published `about` profile is absent |
| Research | `/{locale}/research/` | `/{locale}/research/{slug}/` only for published, localized eligible records | API/route gate open |
| Publications | `/{locale}/publications/` | `/{locale}/publications/{slug}/` only for published, localized eligible records | API/route gate open |
| Projects | `/{locale}/projects/` | `/{locale}/projects/{slug}/` only for sanitized, published, localized eligible records | API/route gate open |
| Writing | `/{locale}/writing/` | `/{locale}/writing/{slug}/` for published localized articles | API/route gate open |
| Teaching | `/{locale}/teaching/` | `/{locale}/teaching/{slug}/` for published localized courses/resources | API/route gate open |
| Creative | `/{locale}/creative/` | `/{locale}/creative/{slug}/` for public rights-cleared work | API/route gate open |
| CV | `/{locale}/cv/` | Downloads only when owner-approved file is available | Content gate open |
| Contact | `/{locale}/contact/` | None | Contact contract gate open |
| Search | `/{locale}/search/` | Query state is URL-addressable; unavailable index remains honest | Search implementation gate open |

`{locale}` is exactly `fa` or `en`. The legacy `/blog/**` family is redirect-only to the equivalent `/writing/**` path once an accepted redirect mapping exists. No other redirect is assumed.

## Alternate and fallback rules

- Render an alternate link only when the equivalent record is published in the alternate locale.
- If a record exists but is not published in the requested locale, show the distinct `untranslated` state; do not silently substitute the other locale.
- If a locale-equivalent detail record does not exist, preserve the current route with an honest unavailable response.
- Preserve query/filter state only when its fields are accepted in the public contract.
