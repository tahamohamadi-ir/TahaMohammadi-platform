# pf-contact-atmosphere-dark

| Field | Value |
|---|---|
| **Asset ID** | `pf-contact-atmosphere-dark` (proposed — **not yet in registry**) |
| **Priority** | P1 |
| **Used on** | PF-08 Contact hero — dedicated atmosphere (today reuses `portal-centered-dark` via `gateway.atmosphere`) |
| **Concept reference** | `concepts/page-families/contact-dark.png` |
| **Current gap** | Contact concept shows stronger radial glow and collaboration mood than gateway-centered portal reuse |

## Drop-in path (proposed)

| Authority | `Docs/references/frontend-design-authority/art/pf-contact-atmosphere-dark.png` |
| Runtime | `Front-End/public-site/src/assets/media/art/pf-contact-atmosphere-dark.png` |

## Output spec

1672 × 941 PNG; proposed slot `page-family.contact.atmosphere` or extend `gateway.atmosphere` with contact-specific dark asset.

## Generation prompt (English)

```text
Use case: stylized-concept
Asset type: wide 16:9 contact/collaboration atmosphere (dark theme)
Primary request: centered soft radial glow from floor-level portal light, subtle orbital lines and nodes, deep navy canvas — evokes research collaboration and message intent without form UI.
Style/medium: canvas #071225, turquoise glow #16B8A6, scarce gold #C89B3C, quiet violet dust #8B75DC. More intimate and centered than gateway language-choice layout.
Composition/framing: 16:9, glow pool lower-center, upper area calm for headline and topic chips (HTML).
Constraints: no text, form fields, buttons, email addresses, logos, UI, watermark, or border.
```

## Negative prompt

```text
form UI, email text, buttons, logos, watermark, people, border, neon overload
```
