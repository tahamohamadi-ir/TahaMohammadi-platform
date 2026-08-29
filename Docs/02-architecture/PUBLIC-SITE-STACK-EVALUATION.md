# Public site stack evaluation

Date: 2026-08-29  
Status: **Accepted** — reaffirms ADR-0002 (Astro static-first public site).

## Question

Is **Astro 7 + TypeScript 5.9 + Tailwind CSS 4 + React 19 (islands only)** the best architecture for this bilingual public site, or should we switch?

## Product constraints (non-negotiable)

| Constraint | Implication |
|---|---|
| Public content readable without JavaScript | Favors static HTML shell; JS only for bounded enhancement |
| Bilingual `fa` / `en` with honest untranslated states | Needs explicit locale routing, hreflang, no silent fallback |
| Content from Django published API | Front end is a consumer; not the CMS |
| Strong SEO, accessibility, RTL/LTR | Clean HTML, semantic tokens, computed-style QA |
| Bounded interactivity (theme, contact, search UI, graph phase 1) | Islands or small client bundles — not a full SPA shell |
| Independent deploy from admin and backend | Static or edge-friendly public artifact preferred |

## Options considered

| Option | Fit | Main trade-off |
|---|---|---|
| **Astro + islands (chosen)** | Excellent | Less ecosystem than Next for app-like features |
| Next.js App Router (static export or SSR) | Good for hybrid apps | Ships React runtime broadly; heavier default JS; more config for true no-JS content |
| Nuxt 3/4 (Vue) | Good static + i18n | New UI framework vs existing React admin panel skill reuse |
| SvelteKit | Excellent performance | Smaller ecosystem; team would maintain Astro + React admin + Svelte public |
| Remix / React Router SSR | Good for forms + mutations | Overkill for static-first public site; session not needed on public shell |
| Plain HTML + minimal JS | Maximum simplicity | Poor DX at PF-01–PF-08 scale, design system, and typed API adapters |

## Why Astro wins for *this* project

1. **No-JS readability is default**, not an export mode. Astro compiles pages to HTML; React hydrates only where `client:*` is declared.
2. **Bilingual static site** maps naturally to file-based routes (`/fa/...`, `/en/...`) plus `astro:i18n` and sitemap hreflang — aligned with `ROUTE-REGISTRY.md`.
3. **Performance and SEO** benefit from zero default client bundle; important for research/portfolio credibility and Core Web Vitals.
4. **React islands** reuse the same React 19 skills as the admin panel without turning the public site into a second SPA.
5. **Tailwind CSS 4** over semantic CSS variables matches the design authority token model.
6. **Backend separation** stays clean: build-time or request-time fetch from `/api/`; no need for Next server actions or a Node SSR tier for the public site.

## When we would reconsider

Switch away from Astro only if a future requirement demands most pages to be highly dynamic, personalized, or authenticated in the public shell — e.g. a logged-in reader area with real-time collaboration. That is explicitly out of scope (`NON-GOALS.md`).

## Accepted stack (unchanged)

| Layer | Choice |
|---|---|
| Framework | Astro 7 |
| Language | TypeScript 5.9 |
| Styling | Tailwind CSS 4 on semantic CSS variables |
| Interactivity | React 19 islands only (`client:visible`, `client:idle`, etc.) |
| Search | Pagefind (local index; no backend search dependency) |
| API | Typed client from accepted OpenAPI; fetch at build or SSR as needed per route |
| Deploy | Static output behind same-origin reverse proxy (`DEPLOYMENT-TOPOLOGY.md`) |

## Implementation guardrails

- React must not own `<html>`, global nav, or primary content columns.
- Every route family in `ROUTE-REGISTRY.md` must render meaningful HTML with JS disabled.
- Islands are allowed for: theme toggle, contact progressive enhancement, search UI, research graph phase 1, and similar bounded widgets.
- Do not import legacy `apps/web` code.

## Related decisions

- ADR-0002 — Static-first Astro public site
- ADR-0003 — React/Vite admin SPA (complementary, not competing)
