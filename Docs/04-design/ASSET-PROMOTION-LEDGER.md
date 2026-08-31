# Asset Promotion Ledger

The owner approved the contents of `Front-End/Assets` on 2026-08-29 as source material for this project. The files below are therefore **source-approved**. Runtime contract staging for Group A/B assets is recorded by `PUBLIC-260` / `WP-30`; final runtime promotion remains open until consumer wiring, derivative inspection, crop review, byte ceilings, and network evidence close in WP-40/WP-50.

| ID | Canonical source | Role | Runtime status | Remaining promotion evidence |
|---|---|---|---|---|
| portal-centered-dark | `art/portal-centered-dark.png` | Dark gateway atmosphere | **Runtime contract staged** — ThemePicture responsive pipeline; decorative `alt=""` | Consumer wiring in WP-40; measured byte ceilings; network evidence |
| portal-centered-light | `art/portal-centered-light.png` | Light gateway atmosphere | **Runtime contract staged** — ThemePicture responsive pipeline; decorative `alt=""` | Consumer wiring in WP-40; measured byte ceilings; network evidence |
| portal-orbit-dark | `art/portal-orbit-dark.png` | Dark Home hero atmosphere | **Runtime contract staged** — ThemePicture responsive pipeline; decorative `alt=""` | Consumer wiring in WP-40; byte ceilings; network evidence |
| portal-orbit-light | `art/portal-orbit-light.png` | Light Home hero atmosphere | **Runtime contract staged** — ThemePicture responsive pipeline; decorative `alt=""` | Consumer wiring in WP-40; byte ceilings; network evidence |
| brand-primary | `brand/taha-mark-primary.png` | Primary identity mark | **Runtime contract staged** — localized content alt in registry | Consumer wiring in WP-40; do not upscale past 256×233 |
| brand-favicon | `brand/taha-mark-favicon.png` | Browser icon | **Runtime contract staged** — 16/32/48/64 PNG + ICO in `public/icons/` | Layout link tags owned by later shell work |
| project-dashboard-systems | `art/project-dashboard-systems.png` | Organizational Dashboard preview | **Runtime contract staged** — maps to `organizational-dashboard-research` | Consumer-supplied localized alt in WP-40; focal/crop review |
| project-data-architecture | `art/project-data-architecture.png` | PARS-SQL preview | **Runtime contract staged** — maps to `pars-sql-vtd-edge` | Consumer-supplied localized alt in WP-40; focal/crop review |
| blog-coral-stairs | `art/blog-coral-stairs.png` | Writing decorative preview | **Runtime contract staged** — decorative `alt=""`; rail `writing` | Consumer wiring in WP-40 |
| learning-sage-library | `art/learning-sage-library.png` | Teaching decorative preview | **Runtime contract staged** — decorative `alt=""`; rail `teaching` | Consumer wiring in WP-40 |
| gallery-ivory-forms | `art/gallery-ivory-forms.png` | Creative decorative preview | **Runtime contract staged** — decorative `alt=""`; rail `creative` | Consumer wiring in WP-40 |
| project-visual-communication-network | `art/project-visual-communication-network.png` | Project preview | **Deferred** | Must not enter runtime |
| project-placeholder-ivory-stairs | `art/project-placeholder-ivory-stairs.png` | Honest future-work placeholder | **Excluded from Home/runtime** | Never attach to a real project slug |
| home-graph-backplate-light | `art/home-graph-backplate-light.png` | Light graph decorative backplate | **Blocked — awaiting WP-25 ACCEPT** | Do not add to authority manifest/checksums until Master Chat accepts generated sources |
| home-graph-backplate-dark | `art/home-graph-backplate-dark.png` | Dark graph decorative backplate | **Blocked — awaiting WP-25 ACCEPT** | Do not add to authority manifest/checksums until Master Chat accepts generated sources |

## Owner decisions recorded for Home + Gateway recovery

These decisions resolve role and mapping only. Derivative generation, consumer wiring, crop review, and visual acceptance remain downstream.

| Decision | Scope | Promotion boundary retained |
|---|---|---|
| Existing logo and favicon approved as-is; derivatives allowed, redesign not approved. | `brand-primary`, `brand-favicon` | Runtime contract staged; layout link tags pending |
| Organizational Dashboard mapping confirmed. | `project-dashboard-systems` | Runtime contract staged to `home.project.preview` |
| PARS-SQL mapping confirmed. | `project-data-architecture` | Runtime contract staged to `home.project.preview` |
| Writing, Teaching, and Creative are decorative preview roles. | `blog-coral-stairs`, `learning-sage-library`, `gallery-ivory-forms` | Decorative `alt=""`; rail mapping only |
| Visual communication network remains deferred. | `project-visual-communication-network` | Must not enter runtime |
| Placeholder ivory stairs is excluded from Home. | `project-placeholder-ivory-stairs` | It is not a Home asset or a substitute for a project record. |
| Home graph uses text-free Light/Dark backplates with semantic overlays. | Home graph backplates | **Blocked until WP-25 Master Chat ACCEPT** |

## Alt policy (WP-30 / WP-30A)

| Category | Asset IDs | Alt policy |
|---|---|---|
| Decorative atmosphere | `portal-centered-*`, `portal-orbit-*` | `alt=""` |
| Decorative rails | `blog-coral-stairs`, `learning-sage-library`, `gallery-ivory-forms` | `alt=""` |
| Decorative favicon source | `brand-favicon` | `alt=""` (icon link context supplies meaning) |
| Content brand mark | `brand-primary` | `Taha Mohammadi` / `طه محمدی` by locale (registry-owned) |
| Content project previews | `project-dashboard-systems`, `project-data-architecture` | **Consumer-supplied localized alt required** — registry must not invent preview copy |

## Transform recipes (WP-30)

| Group | Asset IDs | Widths | Formats |
|---|---|---|---|
| Atmosphere | portal-centered-*, portal-orbit-* | 320, 390, 768, 1024, 1280, 1440, 1672 | AVIF, WebP, source fallback |
| Project / rail previews | project-*, blog-coral-stairs, learning-sage-library, gallery-ivory-forms | 320, 480, 640, 800, 1024 | AVIF, WebP, source fallback |
| Graph backplates (deferred) | home-graph-backplate-* | 320, 480, 640, 768, 1024 | AVIF, WebP, source fallback |

Focal/crop values are measured during WP-40 EN/FA review; CSS guesses are not copied into this ledger.

## Promotion checklist

See `ASSET-PROMOTION-OWNER-GUIDE.md` for what the owner must decide vs what agents handle.

1. Confirm source SHA-256 against the authority manifest. **Done for Group A/B source-approved assets in WP-30.**
2. Confirm owner publication approval and rights/credit statement.
3. Define meaningful `alt` text or explicitly mark the image decorative. **Done for decorative and brand assets; project previews require consumer alt in WP-40.**
4. Define responsive width set, AVIF/WebP derivatives, focal/crop rule, and maximum bytes. **Width sets and formats scaffolded; byte ceilings and network evidence pending WP-40/WP-50.**
5. Assign a published record or honest unavailable state; do not assign invented content. **Project and rail mappings recorded.**
6. Run Light/Dark, RTL/LTR, narrow/desktop, missing-media, and performance QA. **Pending WP-40/WP-50.**
7. Record resulting runtime path and approval evidence in this ledger. **Partial — runtime contract staged; graph backplates blocked on WP-25; final runtime promotion open.**
