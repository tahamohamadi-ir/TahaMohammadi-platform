# Content Contract

<!-- PRODUCT-V2.1 -->
V2.1 extension: [PRODUCT-INTERFACES-V2](PRODUCT-INTERFACES-V2.md) defines the accepted additive target. Current exported OpenAPI and compatibility envelopes remain implementation evidence until the owning backend packet passes. Existing aliases and publication boundaries remain; do not treat a target field as current support.
<!-- /PRODUCT-V2.1 -->

Every publishable record has an explicit lifecycle state.
Anonymous projections include only active, published records.

Under ADR-0009, every independently publishable work requires a localized detail page and substantial editable content. This includes books, talks, resources/downloads, collections, writing series and independent lessons. The target editor coverage is `Docs/05-delivery/concept-alignment-v2/CMS-SPEC.md`. Target schema additions are defined by PRODUCT-INTERFACES-V2; they remain unimplemented until the owning backend task exports them; this target does not imply current API support.

Localized records identify `fa` or `en` explicitly.
Missing translations remain unavailable and must not fall back silently.

Titles, slugs, dates, identifiers, visibility, ordering, and relationships come from the backend.
The frontend may format values but may not create authority values.
Owner-provided source material and approval state are recorded in `Docs/01-product/OWNER-CONTENT-MANIFEST.md`; concept-image text is never a fallback content source.
