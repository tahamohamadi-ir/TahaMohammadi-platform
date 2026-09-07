# Test Strategy

<!-- PRODUCT-V2.1 -->
V2.1 acceptance adds every independent detail family and the admin→preview→publish→deployed URL→revise→remove journey. Use PU-25-admin-journey, PU-25-public-journey, CA-17 and PU-25-review from EXECUTION.md. Keep FA/EN, light/dark, six widths, keyboard, 200% zoom and no-JS content evidence. Pagefind full-text interaction may require JS; linked collection browsing must remain available. No prior PASS is advanced by this documentation change.
<!-- /PRODUCT-V2.1 -->

## Backend

- Unit tests for validators and services
- Model and migration tests
- API and permission integration tests
- PostgreSQL integration tests
- OpenAPI compatibility tests

## Public site

- Unit tests for adapters and formatters
- Static build and route tests
- Component state tests
- Playwright browser and visual tests
- No-JavaScript and search-index tests

## Admin panel

- Unit tests for state and validation
- Component interaction tests
- Mock-contract integration tests
- Playwright authentication and workflow tests

Every defect fix starts with a failing regression test.
