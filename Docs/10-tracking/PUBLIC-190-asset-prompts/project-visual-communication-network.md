# project-visual-communication-network

| Field | Value |
|---|---|
| **Asset ID** | `project-visual-communication-network` |
| **Priority** | P1 |
| **Status** | **Deferred** — authority master exists; must not enter runtime until ledger promotion |
| **Used on** | Future project preview when owner maps slug (e.g. visual-communication research) |
| **Concept reference** | `concepts/page-families/projects-index-dark.png` |
| **Current gap** | Not promoted; projects index reuses `project-data-architecture` thumb for multiple rows |

## Drop-in path

| Authority | `Docs/references/frontend-design-authority/art/project-visual-communication-network.png` |
| Runtime | `Front-End/public-site/src/assets/media/art/project-visual-communication-network.png` (after promotion) |

## Output spec

1536 × 1024 PNG; slot `home.project.preview` when approved.

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: wide 3:2 project cover — visual communication network
Primary request: connected translucent turquoise, teal, mint, ivory, and silver architectural blocks with fine relationship lines, sparse nodes, soft daylight, one antique-gold accent (#C89B3C).
Style/medium: premium academic-editorial 3D still life, calm engineering-network metaphor.
Composition/framing: 3:2 landscape, crop-safe.
Constraints: no text, charts with labels, flags, faces, screens with UI, logo, watermark, or border.
```

## Negative prompt

```text
text, chart labels, UI screens, logos, watermark, faces, border
```

## Owner note

Promotion requires explicit ledger row + slug mapping before runtime wiring.
