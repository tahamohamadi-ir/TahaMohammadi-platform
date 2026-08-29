# Content Contract

Every publishable record has an explicit lifecycle state.
Anonymous projections include only active, published records.

Localized records identify `fa` or `en` explicitly.
Missing translations remain unavailable and must not fall back silently.

Titles, slugs, dates, identifiers, visibility, ordering, and relationships come from the backend.
The frontend may format values but may not create authority values.
Owner-provided source material and approval state are recorded in `Docs/01-product/OWNER-CONTENT-MANIFEST.md`; concept-image text is never a fallback content source.
