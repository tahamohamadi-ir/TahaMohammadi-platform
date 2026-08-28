# Content Migration Manifest

Content is not migrated from screenshots or frontend fallback files.

Authorized content sources are:

1. Published backend database records.
2. Explicit owner-approved seed files.
3. Owner-provided downloads with preserved filenames.

Before production migration:

- export record counts by model and lifecycle state;
- export media references and hashes;
- restore into isolated staging;
- compare counts, identifiers, locales, relationships, and public projections;
- record owner acceptance.
