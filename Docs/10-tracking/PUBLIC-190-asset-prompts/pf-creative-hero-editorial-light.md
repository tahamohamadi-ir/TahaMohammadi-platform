# pf-creative-hero-editorial-light

| Field | Value |
|---|---|
| **Asset ID** | `pf-creative-hero-editorial-light` (proposed — **not yet in registry**) |
| **Priority** | P1 |
| **Used on** | PF-01 Creative index — tall hero media column beside copy (concept shows portrait editorial panel, not 3:2 rail crop) |
| **Concept reference** | `concepts/page-families/creative-index-light.png` (hero right panel) |
| **Current gap** | `gallery-ivory-forms` landscape crop in 42% hero column does not match concept portrait editorial proportion |

## Drop-in path (proposed)

| Authority (proposed) | `Docs/references/frontend-design-authority/art/pf-creative-hero-editorial-light.png` |
| Runtime (after promotion) | `Front-End/public-site/src/assets/media/art/pf-creative-hero-editorial-light.png` |

## Output spec

1200 × 1600 PNG (3:4 portrait); proposed slot `home.rail.preview` or new `page-family.hero.panel` after ledger ADR.

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: tall 3:4 editorial hero panel for Creative/Gallery index (light theme)
Primary request: single dominant sculptural artwork composition — ivory arches, matte sphere, translucent plane, soft violet accent form — composed for vertical hero column beside collection statement. Calm museum lighting, generous upper negative space.
Style/medium: warm ivory (#F7F8F5), soft violet (#6047B8 family), turquoise reflection (#087C73), precise shadows — matches gallery-ivory family but portrait framing.
Composition/framing: 3:4 portrait, center-weighted forms, crop-safe top/bottom for responsive hero.
Constraints: no text, framed pictures with titles, logos, UI, watermark, people, or border.
```

## Negative prompt

```text
landscape 16:9, text, gallery labels, logos, UI, watermark, people, border
```

## Engineering note

Requires new `MediaSlot` or hero-specific mapping in `page-family-empty-chrome.ts` after owner approves promotion.
