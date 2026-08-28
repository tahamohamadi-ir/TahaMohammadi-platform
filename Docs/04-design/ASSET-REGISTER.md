# Asset Register

## Preserved source

The managed design pack is stored at `Docs/references/site-redesign/`.
Its `SHA256SUMS.txt` contains 33 managed binary records.
All 33 records matched after transfer on 2026-08-28.

## Runtime candidates

| Role | Candidate master |
|---|---|
| Gateway dark/light | `portal-centered-dark.png`, `portal-centered-light.png` |
| Home dark/light | `portal-orbit-dark.png`, `portal-orbit-light.png` |
| Project and research previews | four `project-*.png` masters |
| Writing | `blog-coral-stairs.png` |
| Teaching | `learning-sage-library.png` |
| Creative | `gallery-ivory-forms.png` |

## Delivery rule

Preserve master files unchanged.
Generate responsive AVIF and WebP derivatives during the public-site implementation.
Preload only the actual LCP image.
Lazy-load non-critical media.
Record owner publication approval before a candidate becomes public.
