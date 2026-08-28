# ADR-0002 — Static-first Astro Public Site

Status: Accepted

Date: 2026-08-28

## Decision

Use Astro and TypeScript for the bilingual public shell, Tailwind CSS over semantic design tokens, and React only for bounded interactive islands. Primary public content remains readable without client JavaScript.

## Consequences

Rendering and caching must preserve content freshness and SEO. Islands cannot own the document shell or basic navigation. Detailed package, deployment, and route versions remain separately controlled.
