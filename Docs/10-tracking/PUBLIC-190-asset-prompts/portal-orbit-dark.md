# portal-orbit-dark

| Field | Value |
|---|---|
| **Asset ID** | `portal-orbit-dark` |
| **Priority** | P0 |
| **Used on** | Home — `HomeHero` atmosphere (`home.hero.atmosphere`, dark theme) |
| **Concept reference** | `Docs/references/frontend-design-authority/concepts/home-dark-concept-v3-final.png` |
| **Current gap** | Dark hero lacks cinematic depth and controlled glow vs concept; orbital field too faint |

## Drop-in path

| Step | Path |
|---|---|
| Authority master | `Docs/references/frontend-design-authority/art/portal-orbit-dark.png` |
| Runtime source | `Front-End/public-site/src/assets/media/art/portal-orbit-dark.png` |

## Output spec

| Property | Value |
|---|---|
| Intrinsic size | 1672 × 941 px |
| Master format | PNG |
| Color tokens (dark) | canvas `#071225`, surface `#0b1630`, brand `#16b8a6`, signature `#c89b3c`, research `#8b75dc` |

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: wide 16:9 decorative hero atmosphere for an academic personal website (dark theme)
Primary request: preserve the exact geometry, framing, and negative-space balance of the approved light hero companion — monumental arch and staircase in the right third, subtle orbital rings and sparse nodes — but render in deep navy scientific atlas lighting.
Style/medium: deep near-navy canvas (#071225), layered blue surfaces (#0B1630), restrained turquoise identity light (#16B8A6), scarce gold (#C89B3C), trace royal violet (#8B75DC). Cinematic but quiet — not cosmic nebula spectacle.
Composition/framing: landscape 16:9, left two-thirds empty for HTML, arch right third, readable at 320px.
Constraints: theme-only conversion of light companion geometry; no text, logos, UI, watermark, people, or border. HTML supplies all copy.
```

## Negative prompt

```text
text, logo, UI, watermark, oversaturated nebula, star-field noise, planet spectacle, neon, clutter, asymmetric crop vs light companion, border
```

## Handback checklist

- [ ] PNG 1672×941, geometry matches light companion
- [ ] SHA-256 for ledger
