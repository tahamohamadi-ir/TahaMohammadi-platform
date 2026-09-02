# pf-about-identity-abstract-light

| Field | Value |
|---|---|
| **Asset ID** | `pf-about-identity-abstract-light` (proposed) |
| **Priority** | P1 |
| **Used on** | PF-07 About — abstract portrait / identity placeholder (no owner portrait approved) |
| **Concept reference** | `concepts/page-families/about-cv-light.png` |
| **Current gap** | Implementation lacks concept's explicit abstract identity plate beside profile hero |

## Drop-in path (proposed)

| Authority | `Docs/references/frontend-design-authority/art/pf-about-identity-abstract-light.png` |
| Runtime | `Front-End/public-site/src/assets/media/art/pf-about-identity-abstract-light.png` |

## Output spec

1024 × 1024 PNG square; decorative `alt=""`; proposed slot `page-family.profile.placeholder`.

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: square abstract identity placeholder for About/CV (light theme)
Primary request: non-photographic identity plate — layered geometric portrait silhouette built from ivory planes, thin navy lines, turquoise and gold accent nodes suggesting researcher-engineer-designer intersection. No human face or photograph.
Style/medium: editorial scientific atlas, warm ivory (#F7F8F5), ink navy (#182328), brand turquoise (#087C73), signature gold (#A77B28).
Composition/framing: 1:1 square, centered abstract form, calm negative space.
Constraints: no face, no real person, no text, logo, UI, watermark, or border.
```

## Negative prompt

```text
real face, photograph, text, logo, UI, watermark, stock headshot, border
```
