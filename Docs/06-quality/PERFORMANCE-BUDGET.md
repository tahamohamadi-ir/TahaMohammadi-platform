# Performance Budget

<!-- PRODUCT-V2.1 -->
V2.1 acceptance adds every independent detail family and the admin→preview→publish→deployed URL→revise→remove journey. Use PU-25-admin-journey, PU-25-public-journey, CA-17 and PU-25-review from EXECUTION.md. Keep FA/EN, light/dark, six widths, keyboard, 200% zoom and no-JS content evidence. Pagefind full-text interaction may require JS; linked collection browsing must remain available. No prior PASS is advanced by this documentation change.
<!-- /PRODUCT-V2.1 -->

## Public site targets

- Initial public content works without client JavaScript.
- Route-specific JavaScript is loaded only for owned interactions.
- LCP media uses responsive formats and one intentional preload.
- CLS target is at most 0.1.
- INP target is at most 200 milliseconds on representative hardware.
- LCP target is at most 2.5 seconds at the 75th percentile.

Each new dependency must include measured bundle and runtime impact.
