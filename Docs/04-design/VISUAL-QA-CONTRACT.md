# Visual QA Contract

## Required comparison

Capture the matching PF-01 through PF-08 reference and implementation at the same viewport, locale, theme, and state.
Compare hierarchy, spacing, typography, asset role, crop, density, and interaction affordance.

Concept references are not pixel-perfect implementation specifications.
Visible deviations require a documented reason and owner acceptance.

## Automated checks

- No unresolved design variables
- No unprocessed CSS directives
- No horizontal page overflow
- Exactly one page heading
- Correct language and direction
- Bounded icon and control dimensions
- Expected fonts in computed styles
- No missing critical media or search assets

## Manual checks

- Keyboard-only navigation
- Real 200 percent browser zoom
- Screen-reader landmarks and form feedback
- Light and Dark visual review
- Persian and English review
- Reduced-motion review
- Asset promotion-ledger role, crop, text alternative, and derivative review
- Gateway, Home, PF-01 through PF-08, search, and all honest content-state review

Build success does not close manual visual acceptance.
