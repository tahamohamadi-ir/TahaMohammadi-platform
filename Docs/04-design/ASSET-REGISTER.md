# Asset Register

## Canonical source

The managed design pack is stored at `Docs/references/frontend-design-authority/`.
`SHA256SUMS.txt`, `AUTHORITY-MANIFEST.json`, and `ALIASES.json` are the integrity and deduplication records. `Front-End/Assets` remains an ignored local comparison source; it is not an active runtime or agent authority.

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
Record owner publication approval, rights/credit, alt or decorative decision, crop/focal rule, and derivative output in `ASSET-PROMOTION-LEDGER.md` before a candidate becomes public.
