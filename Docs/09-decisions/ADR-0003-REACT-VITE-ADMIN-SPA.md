# ADR-0003 — React and Vite Admin SPA

Status: Accepted

Date: 2026-08-28

## Decision

Use React and TypeScript with Vite for the independently deployed administration frontend.

## Consequences

The backend remains authoritative for sessions, permissions, validation, publication, and audit state. Authentication, state, editor, and deployment details require focused ADRs before implementation.
