# Design System Specification

## Token layers

1. Primitive values
2. Semantic Light roles
3. Semantic Dark roles
4. Component aliases

CSS variables must exist in browser-computed styles.
The production CSS must not contain unprocessed framework directives.

## Typography

| Locale | Display | Body and UI |
|---|---|---|
| English | Newsreader Variable | Inter Variable |
| Persian | Estedad Variable | Vazirmatn Variable |

Fonts must be self-hosted after license and subset review.
Each locale uses only its two assigned families.

## Component baseline

The canonical component inventory is `references/site-redesign/implementation-reference/agent-kit/components.json`.
Do not create a second general component library.

Every interactive component must define:

- default, hover, focus, active, disabled, loading, error, and success behavior;
- keyboard behavior;
- RTL and LTR behavior;
- minimum 44 by 44 CSS-pixel target where applicable;
- reduced-motion behavior.

## Theme rule

Themes may change color, illumination, and depth.
Themes must not change content order, route meaning, or DOM anatomy.
