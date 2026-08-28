# Platform Workspace Design

## Goal

Create a clean three-repository workspace for a new public frontend, a new admin frontend, and a migrated backend.

## Approved approach

Use three independent Git repositories under one local coordination root.
Keep cross-repository documents in `Docs/` and local implementation documents in each repository.

## Migration rule

Copy the tracked backend source exactly from legacy commit `cdaa283fac9da57c6d88e22aa0751be6214b6cf6`.
Exclude ignored databases, media, caches, virtual environments, secrets, and build output.
Preserve legacy infrastructure as non-active reference until paths and deployment assumptions are rewritten.

Do not copy legacy frontend implementation code.
Preserve approved visual assets and design references as non-executable evidence.

## Architecture

- Public site: Astro, TypeScript, Tailwind, bounded React islands.
- Admin panel: React, TypeScript, Vite.
- Backend: Python 3.12, Django 5.2.9, Django Ninja 1.6.2, PostgreSQL 17.

## Documentation architecture

One document owns each cross-repository rule.
Repository documents link to cross-repository contracts and add only local implementation detail.
Agent adapters point to `AGENTS.md` instead of copying policy.

## Verification

- Three local repositories track their matching GitHub remotes.
- Backend copy hashes match the exact legacy tracked files.
- All managed design-reference hashes match their manifest.
- No legacy frontend source exists in the new frontend repositories.
- Documents contain no unresolved placeholders.
- Every roadmap deliverable maps to a task and release gate.
