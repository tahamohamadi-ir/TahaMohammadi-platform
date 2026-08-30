# Asset Promotion Ledger

The owner approved the contents of `Front-End/Assets` on 2026-08-29 as source material for this project. The files below are therefore source-approved. Runtime promotion evidence for Group A/B assets is recorded by `PUBLIC-260` / `WP-30`.

| ID | Canonical source | Role | Runtime status | Remaining promotion evidence |
|---|---|---|---|---|
| portal-centered-dark | `art/portal-centered-dark.png` | Dark gateway atmosphere | **Runtime promoted** — decorative `alt=""`; ThemePicture single-theme loading | Measured byte ceilings after WP-40 build review |
| portal-centered-light | `art/portal-centered-light.png` | Light gateway atmosphere | **Runtime promoted** — decorative `alt=""` | Measured byte ceilings after WP-40 build review |
| portal-orbit-dark | `art/portal-orbit-dark.png` | Dark Home hero atmosphere | **Runtime promoted** — decorative `alt=""` | Consumer wiring in WP-40; byte ceilings pending |
| portal-orbit-light | `art/portal-orbit-light.png` | Light Home hero atmosphere | **Runtime promoted** — decorative `alt=""` | Consumer wiring in WP-40; byte ceilings pending |
| brand-primary | `brand/taha-mark-primary.png` | Primary identity mark | **Runtime promoted** — localized content alt | Do not upscale past 256×233 |
| brand-favicon | `brand/taha-mark-favicon.png` | Browser icon | **Runtime promoted** — 16/32/48/64 PNG + ICO in `public/icons/` | Link tags in layout owned by later shell work |
| project-dashboard-systems | `art/project-dashboard-systems.png` | Organizational Dashboard preview | **Runtime promoted** — maps to `organizational-dashboard-research` | Focal/crop review in WP-40 |
| project-data-architecture | `art/project-data-architecture.png` | PARS-SQL preview | **Runtime promoted** — maps to `pars-sql-vtd-edge` | Focal/crop review in WP-40 |
| blog-coral-stairs | `art/blog-coral-stairs.png` | Writing decorative preview | **Runtime promoted** — decorative `alt=""`; rail `writing` | Consumer wiring in WP-40 |
| learning-sage-library | `art/learning-sage-library.png` | Teaching decorative preview | **Runtime promoted** — decorative `alt=""`; rail `teaching` | Consumer wiring in WP-40 |
| gallery-ivory-forms | `art/gallery-ivory-forms.png` | Creative decorative preview | **Runtime promoted** — decorative `alt=""`; rail `creative` | Consumer wiring in WP-40 |
| project-visual-communication-network | `art/project-visual-communication-network.png` | Project preview | **Deferred** | Must not enter runtime |
| project-placeholder-ivory-stairs | `art/project-placeholder-ivory-stairs.png` | Honest future-work placeholder | **Excluded from Home/runtime** | Never attach to a real project slug |
| home-graph-backplate-light | `art/home-graph-backplate-light.png` | Light graph decorative backplate | **Blocked — awaiting WP-25 ACCEPT** | Do not add to authority manifest/checksums until Master Chat accepts generated sources |
| home-graph-backplate-dark | `art/home-graph-backplate-dark.png` | Dark graph decorative backplate | **Blocked — awaiting WP-25 ACCEPT** | Do not add to authority manifest/checksums until Master Chat accepts generated sources |

## Owner decisions recorded for Home + Gateway recovery

These decisions resolve role and mapping only. Derivative generation, consumer wiring, crop review, and visual acceptance remain downstream.

| Decision | Scope | Promotion boundary retained |
|---|---|---|
| Existing logo and favicon approved as-is; derivatives allowed, redesign not approved. | `brand-primary`, `brand-favicon` | Runtime scaffold promoted; layout link tags pending |
| Organizational Dashboard mapping confirmed. | `project-dashboard-systems` | Runtime promoted to `home.project.preview` |
| PARS-SQL mapping confirmed. | `project-data-architecture` | Runtime promoted to `home.project.preview` |
| Writing, Teaching, and Creative are decorative preview roles. | `blog-coral-stairs`, `learning-sage-library`, `gallery-ivory-forms` | Decorative `alt=""`; rail mapping only |
| Visual communication network remains deferred. | `project-visual-communication-network` | Must not enter runtime |
| Placeholder ivory stairs is excluded from Home. | `project-placeholder-ivory-stairs` | It is not a Home asset or a substitute for a project record. |
| Home graph uses text-free Light/Dark backplates with semantic overlays. | Home graph backplates | **Blocked until WP-25 Master Chat ACCEPT** |

## Alt policy (WP-30)

| Category | Asset IDs | Alt policy |
|---|---|---|
| Decorative atmosphere | `portal-centered-*`, `portal-orbit-*` | `alt=""` |
| Decorative rails | `blog-coral-stairs`, `learning-sage-library`, `gallery-ivory-forms` | `alt=""` |
| Decorative favicon source | `brand-favicon` | `alt=""` (icon link context supplies meaning) |
| Content brand mark | `brand-primary` | `Taha Mohammadi` / `طه محمدی` by locale |
| Content project previews | `project-dashboard-systems`, `project-data-architecture` | Localized generic preview alt until record-specific alt is approved |

## Transform recipes (WP-30)

| Group | Asset IDs | Widths | Formats |
|---|---|---|---|
| Atmosphere | portal-centered-*, portal-orbit-* | 320, 390, 768, 1024, 1280, 1440, 1672 | AVIF, WebP, source fallback |
| Project / rail previews | project-*, blog-coral-stairs, learning-sage-library, gallery-ivory-forms | 320, 480, 640, 800, 1024 | AVIF, WebP, source fallback |
| Graph backplates (deferred) | home-graph-backplate-* | 320, 480, 640, 768, 1024 | AVIF, WebP, source fallback |

Focal/crop values are measured during WP-40 EN/FA review; CSS guesses are not copied into this ledger.

## Promotion checklist

See `ASSET-PROMOTION-OWNER-GUIDE.md` for what the owner must decide vs what agents handle.

1. Confirm source SHA-256 against the authority manifest. **Done for Group A/B runtime assets in WP-30.**
2. Confirm owner publication approval and rights/credit statement.
3. Define meaningful `alt` text or explicitly mark the image decorative. **Done for Group A/B in WP-30.**
4. Define responsive width set, AVIF/WebP derivatives, focal/crop rule, and maximum bytes. **Width sets and formats scaffolded; byte ceilings pending build measurement.**
5. Assign a published record or honest unavailable state; do not assign invented content. **Project and rail mappings recorded.**
6. Run Light/Dark, RTL/LTR, narrow/desktop, missing-media, and performance QA. **Pending WP-40/WP-50.**
7. Record resulting runtime path and approval evidence in this ledger. **Partial — graph backplates blocked on WP-25.**
