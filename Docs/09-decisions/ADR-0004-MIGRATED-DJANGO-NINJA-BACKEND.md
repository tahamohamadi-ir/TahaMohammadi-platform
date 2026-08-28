# ADR-0004 — Migrated Django and Django Ninja Backend

Status: Accepted

Date: 2026-08-28

## Decision

Preserve and move the usable Python 3.12, Django 5.2.9, and Django Ninja 1.6.2 backend into its independent repository, with PostgreSQL as production data authority.

## Consequences

The migration baseline remains behavior-compatible and hash-verifiable. Legacy infrastructure is reference-only until standalone paths and operations are rewritten and tested.
