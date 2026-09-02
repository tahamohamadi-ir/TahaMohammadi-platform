# portal-orbit-light

| Field | Value |
|---|---|
| **Asset ID** | `portal-orbit-light` |
| **Priority** | P0 |
| **Used on** | Home — `HomeHero` atmosphere (`home.hero.atmosphere`, light theme) |
| **Concept reference** | `Docs/references/frontend-design-authority/concepts/home-light-concept-v3-final.png` (hero arch + orbital field, right third) |
| **Current gap** | Implementation arch reads flat vs concept; left negative space too weak; orbital depth and turquoise/gold restraint below concept |

## Drop-in path

| Step | Path |
|---|---|
| Authority master | `Docs/references/frontend-design-authority/art/portal-orbit-light.png` |
| Runtime source | `Front-End/public-site/src/assets/media/art/portal-orbit-light.png` |

## Output spec

| Property | Value |
|---|---|
| Intrinsic size | 1672 × 941 px (16:9) |
| Master format | PNG (lossless master); runtime derives AVIF + WebP |
| Color tokens (light) | canvas `#f7f8f5`, ink navy `#182328`, brand `#087c73`, signature `#a77b28`, research `#6047b8`, coral accent sparing `#d45f45` |

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: wide 16:9 decorative hero atmosphere for an academic personal website (light theme)
Primary request: monumental limestone arch and short staircase in the right third, opening into a subtle scientific orbital field — concentric rings, thin constellation paths, sparse luminous nodes, fine spatial dust. Generous calm negative space on the left two-thirds for HTML headline and CTAs.
Style/medium: warm ivory limestone (#F7F8F5), ink-navy line work (#182328), restrained turquoise identity light (#087C73), scarce antique-gold accents (#A77B28), barely visible lavender research points (#6047B8). Editorial research atmosphere — refined architectural 3D still life, not neon sci-fi.
Composition/framing: landscape 16:9, arch anchored right third, orbital geometry readable at 320px width, soft museum daylight, no hard vignette border.
Constraints: no text, letters, numbers, logos, UI chrome, browser frame, watermark, people, flags, or political symbols. Background must blend with light canvas; all copy is HTML overlay.
```

## Negative prompt

```text
text, typography, watermark, logo, UI buttons, neon overload, cyberpunk, stock photo people, busy clutter left side, oversaturated glow, lens flare spectacle, cartoon, low resolution, jpeg artifacts, border frame
```

## Handback checklist

- [ ] PNG exactly 1672×941
- [ ] SHA-256 recorded for ledger update
- [ ] Visually pairs with `portal-orbit-dark` geometry (theme-only companion)
