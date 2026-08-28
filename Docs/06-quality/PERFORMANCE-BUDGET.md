# Performance Budget

## Public site targets

- Initial public content works without client JavaScript.
- Route-specific JavaScript is loaded only for owned interactions.
- LCP media uses responsive formats and one intentional preload.
- CLS target is at most 0.1.
- INP target is at most 200 milliseconds on representative hardware.
- LCP target is at most 2.5 seconds at the 75th percentile.

Each new dependency must include measured bundle and runtime impact.
