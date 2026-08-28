# ADR-0001 — Three Independent Product Repositories

Status: Accepted

Date: 2026-08-28

## Decision

Use independent repositories for the public site, admin panel, and backend beneath one local coordination root.

## Consequences

Each product has its own history, dependencies, CI, releases, and rollback. Cross-product interface changes require coordinated contract evidence. The root repository must ignore nested product repositories.
