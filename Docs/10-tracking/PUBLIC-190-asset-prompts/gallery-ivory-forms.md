# gallery-ivory-forms

| Field | Value |
|---|---|
| **Asset ID** | `gallery-ivory-forms` |
| **Priority** | P0 |
| **Used on** | Home creative rail; PF-01 hero side media and grid/masonry placeholders (`home.rail.preview`) |
| **Concept reference** | `concepts/page-families/creative-index-light.png` (featured work + grid mood) |
| **Current gap** | Rail crop too small for PF-01 hero column; sculptural ivory/violet balance weaker than concept gallery atmosphere |

## Drop-in path

| Authority | `Docs/references/frontend-design-authority/art/gallery-ivory-forms.png` |
| Runtime | `Front-End/public-site/src/assets/media/art/gallery-ivory-forms.png` |

## Output spec

1536 × 1024 PNG (3:2); slot `home.rail.preview`; tokens: canvas `#f7f8f5`, research soft `#eeeaf9`, brand `#087c73`.

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: wide 3:2 art-gallery decorative preview
Primary request: curated sculptural composition — ivory arches, matte spheres, translucent planes, one soft royal-violet form, restrained turquoise reflection. Elegant spatial balance, tactile materials, calm negative space suitable for hero crop and masonry thumbnails.
Style/medium: premium editorial gallery still life, warm ivory (#F7F8F5), soft violet accent (#6047B8 family), turquoise reflection (#087C73), precise lighting.
Composition/framing: 3:2 landscape, crop-safe center-weighted forms, no framed pictures with content.
Constraints: no text, letters, numbers, logos, UI, watermark, people, or recognizable artworks with titles.
```

## Negative prompt

```text
text on frames, gallery labels, logos, UI, watermark, people, stock photos, busy clutter, border
```
