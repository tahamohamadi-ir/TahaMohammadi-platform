# project-data-architecture

| Field | Value |
|---|---|
| **Asset ID** | `project-data-architecture` |
| **Priority** | P1 |
| **Used on** | Home project `pars-sql-vtd-edge`; PF-04 projects hero and row previews (`home.project.preview`) |
| **Concept reference** | `concepts/page-families/projects-index-dark.png` |
| **Current gap** | Modular data-architecture read weaker vs concept evidence rows; hero lacks technical depth |

## Drop-in path

| Authority | `Docs/references/frontend-design-authority/art/project-data-architecture.png` |
| Runtime | `Front-End/public-site/src/assets/media/art/project-data-architecture.png` |

## Output spec

1536 × 1024 PNG; slot `home.project.preview` (consumer-supplied alt at runtime).

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: wide 3:2 project-cover artwork — data architecture theme
Primary request: abstract modular data architecture — translucent stacked cubes, refined cylindrical database form, thin branching data paths, luminous nodes suggesting natural-language-to-data pipeline.
Style/medium: deep slate navy, cool lavender, restrained turquoise (#16B8A6 / #087C73), soft silver, tiny antique-gold highlights (#C89B3C). Serious academic engineering mood.
Composition/framing: 3:2 landscape, crop-safe, no literal dashboard UI.
Constraints: no words, letters, numbers, code snippets, logos, charts with labels, browser chrome, watermark, or border.
```

## Negative prompt

```text
readable code, chart labels, dashboard UI, logos, watermark, text, numbers, border
```
