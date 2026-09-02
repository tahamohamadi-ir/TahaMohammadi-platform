# project-placeholder-ivory-stairs

| Field | Value |
|---|---|
| **Asset ID** | `project-placeholder-ivory-stairs` |
| **Priority** | P2 |
| **Status** | **Excluded from Home/runtime** — honest future-work placeholder only |
| **Used on** | Empty project slots when no approved preview exists (never attach to real slug) |
| **Concept reference** | `concepts/page-families/projects-index-dark.png` (sanitized placeholder states) |
| **Current gap** | No runtime honest placeholder art wired; risks reusing real project previews |

## Drop-in path

| Authority | `Docs/references/frontend-design-authority/art/project-placeholder-ivory-stairs.png` |
| Runtime | Only after explicit ledger row for placeholder slot — not `home.project.preview` for real slugs |

## Output spec

1536 × 1024 PNG; decorative `alt=""`.

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: wide 3:2 honest future-work placeholder
Primary request: warm-ivory arch and ascending staircase, restrained geometric blocks, soft light, faint turquoise shadow (#087C73), one small antique-gold point (#A77B28). Clearly generic — not evidence of a specific project.
Style/medium: calm editorial placeholder, no claims of results or metrics.
Composition/framing: 3:2 landscape.
Constraints: no people, evidence claims, text, logo, UI, watermark, or border. Must not resemble a finished case study cover.
```

## Negative prompt

```text
dashboard metrics, text, logos, UI, watermark, people, border, realistic product screenshots
```

## Owner boundary

Never map to `HOME_PROJECT_ASSET_BY_SLUG` or any published slug.
