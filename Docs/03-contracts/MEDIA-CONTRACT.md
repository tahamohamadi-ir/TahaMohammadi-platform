# Media Contract

- The backend owns upload validation, storage names, metadata, and public URLs.
- Public and admin clients use media identifiers returned by the API.
- Image media requires MIME sniffing, dimension checks, size limits, and alt-text fields.
- Public derivatives use responsive AVIF and WebP when supported.
- Original files remain unchanged when derivatives are generated.
- Private or draft media must not be exposed through predictable URLs.
