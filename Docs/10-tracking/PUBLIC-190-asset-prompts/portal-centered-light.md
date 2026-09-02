# portal-centered-light

| Field | Value |
|---|---|
| **Asset ID** | `portal-centered-light` |
| **Priority** | P0 |
| **Used on** | Language gateway (`gateway.atmosphere` light); PF-08 contact hero reuses same slot today |
| **Concept reference** | `Docs/references/frontend-design-authority/concepts/language-gateway-dark-concept-v1.png` (layout only — convert to light) |
| **Current gap** | Centered portal glow weaker than concept; floor illumination and node orbit too subtle for gateway + contact atmosphere |

## Drop-in path

| Authority | `Docs/references/frontend-design-authority/art/portal-centered-light.png` |
| Runtime | `Front-End/public-site/src/assets/media/art/portal-centered-light.png` |

## Output spec

1672 × 941 PNG; tokens: canvas `#f7f8f5`, brand `#087c73`, signature `#a77b28`.

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: centered 16:9 gateway atmosphere (light theme)
Primary request: symmetrical monumental arch and short stairs centered in frame, subtle orbital geometry and floor illumination radiating outward, calm museum daylight, generous vertical breathing room for centered language-choice UI (UI is HTML — do not draw buttons).
Style/medium: warm ivory (#F7F8F5), ink-navy lines (#182328), turquoise nodes (#087C73), scarce gold accents (#A77B28), faint lavender points.
Composition/framing: centered arch, balanced radial symmetry, soft floor glow, 16:9.
Constraints: no text, language labels, logo, theme icons, buttons, watermark, or border. Remove all interface chrome — pure atmosphere only.
```

## Negative prompt

```text
English text, Persian text, buttons, UI, logo, watermark, asymmetric crop, people, flags, neon, border frame
```
