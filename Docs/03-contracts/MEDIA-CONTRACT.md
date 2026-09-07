# Media Contract

<!-- PRODUCT-V2.1 -->
V2.1 extension: [PRODUCT-INTERFACES-V2](PRODUCT-INTERFACES-V2.md) defines the accepted additive target. Current exported OpenAPI and compatibility envelopes remain implementation evidence until the owning backend packet passes. Existing aliases and publication boundaries remain; do not treat a target field as current support.
<!-- /PRODUCT-V2.1 -->

- The backend owns upload validation, storage names, metadata, and public URLs.
- Public and admin clients use media identifiers returned by the API.
- Image media requires MIME sniffing, dimension checks, size limits, and alt-text fields.
- Public derivatives use responsive AVIF and WebP when supported.
- Original files remain unchanged when derivatives are generated.
- Private or draft media must not be exposed through predictable URLs.
- Runtime media promotion additionally requires the tracked authority hash and an approved `ASSET-PROMOTION-LEDGER.md` record.
