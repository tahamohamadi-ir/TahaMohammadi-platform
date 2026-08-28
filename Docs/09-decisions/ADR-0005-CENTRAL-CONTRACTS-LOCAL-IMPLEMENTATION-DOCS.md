# ADR-0005 — Central Contracts and Local Implementation Documents

Status: Accepted

Date: 2026-08-28

## Decision

Keep cross-repository authority, product, interface, design, release, migration, quality, and agent rules in the coordination root. Keep implementation detail beside the repository that owns it.

## Consequences

Each rule has one owner. Repository documents link to shared contracts and may narrow them but cannot silently redefine them. Standalone clones retain local instructions and name their external contract dependency.
