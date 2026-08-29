# Font Acquisition Plan

Status: **final pair selected** (2026-08-29). Binaries are not yet pinned in the repository; token structure is defined for swap without layout refactor.

## Final selected families

| Locale | Display | Body/UI | License |
|---|---|---|---|
| English | **Newsreader Variable** | **Inter Variable** | SIL OFL 1.1 |
| Persian | **Estedad Variable** | **Vazirmatn Variable** | SIL OFL 1.1 |

Rationale: Newsreader gives English headings editorial character without harming long-form readability; Inter is a proven UI/body workhorse. Estedad provides distinctive Persian display; Vazirmatn is the most reliable open Persian text/UI face with official variable WOFF2 releases.

## Deliberately excluded

| Candidate | Decision |
|---|---|
| IRANSans | Proprietary — requires Fontiran license before any reconsideration |
| Kalameh / کلمه | Do not use from marketplace copies without verified deployment license |

## Swappable token architecture

Fonts are referenced only through semantic CSS variables — never hard-coded family names in components.

```css
:root {
  --font-display-en: "Newsreader Variable", "Georgia", serif;
  --font-body-en: "Inter Variable", system-ui, sans-serif;
  --font-display-fa: "Estedad Variable", "Vazirmatn Variable", sans-serif;
  --font-body-fa: "Vazirmatn Variable", "Tahoma", sans-serif;
}

html[lang="en"] {
  --font-display: var(--font-display-en);
  --font-body: var(--font-body-en);
}

html[lang="fa"] {
  --font-display: var(--font-display-fa);
  --font-body: var(--font-body-fa);
}
```

Runtime rules:

1. Components consume `--font-display` and `--font-body` only.
2. Swapping a family means updating the token map (or a single JSON theme file), not component CSS.
3. `font-display: swap` and metric-adjusted fallbacks are required on first pin.
4. Subset files are per-locale WOFF2 variables; do not claim coverage without a fixture.

## Future admin override (late phase — optional)

A site-settings field may later expose **approved** font token overrides (family slug + weight axis), stored in backend and emitted as CSS variables at build or request time. Constraints:

- Only families from an allowlist (the four above plus future licensed additions).
- Public site remains readable if admin override is absent or invalid.
- Not required for scaffold or MVP; document here so schema leaves room.

## Gate before adding binaries (PS-10)

1. Download release-pinned WOFF2 from official upstream; preserve `OFL.txt` beside binaries.
2. Record version, SHA-256, axes, and source URL in `Front-End/public-site` implementation docs.
3. Create Persian + Latin subsets with fixture-backed coverage claims.
4. Run computed-style QA: both locales, 200% zoom, mixed-direction strings, CLS budget.
5. Mark PS-10 PASS in `PRE-SCAFFOLD-READINESS.md`.

## Upstream sources

- Vazirmatn: https://github.com/rastikerdar/vazirmatn
- Estedad: https://github.com/aminabedi68/Estedad
- Inter: https://github.com/rsms/inter
- Newsreader: https://github.com/productiontype/Newsreader
