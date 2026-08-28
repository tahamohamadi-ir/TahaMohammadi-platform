# Platform Workspace Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Establish the three-repository workspace, migrate the backend baseline, preserve design references, and create complete governance documents.

**Architecture:** Three independent Git repositories sit under one local coordination root. The root owns cross-repository contracts; each repository owns implementation documents.

**Tech Stack:** Git and Markdown for the workspace baseline; Python 3.12, Django 5.2.9, and Django Ninja 1.6.2 for the migrated backend. Public/admin runtime choices remain ADR-controlled.

**Spec:** `Docs/superpowers/specs/2026-08-28-platform-workspace-design.md`

## Global Constraints

- Do not copy legacy frontend source.
- Copy backend tracked files from commit `cdaa283fac9da57c6d88e22aa0751be6214b6cf6`.
- Exclude secrets, databases, media, caches, environments, and build output.
- Treat reference documents as non-executable evidence.
- Keep the three repositories independent.

### Task 1: Connect repositories

**Files:** Git metadata in the three target repository roots.

**Produces:** Three `main` branches tracking their matching `origin/main`.

- [x] Initialize the three local repository directories.
- [x] Add the exact GitHub remotes.
- [x] Fetch and check out `main`.
- [x] Verify upstream tracking.

### Task 2: Copy backend baseline

**Files:** Legacy tracked `apps/cms/**` to `Back-End/**`.

**Produces:** An exact backend source baseline.

- [x] Enumerate tracked backend files at the source commit.
- [x] Copy each tracked file while removing the legacy path prefix.
- [x] Compare SHA-256 hashes for all 198 copied files.
- [x] Confirm zero mismatches.

### Task 3: Preserve reference package

**Files:** `Docs/references/site-redesign/**`.

**Produces:** A central immutable evidence package.

- [x] Copy the design handoff package.
- [x] Validate all 33 managed binary hashes.
- [x] Keep concept assets outside runtime repositories.

### Task 4: Create canonical documents

**Files:** Root documents and `Docs/**`.

**Produces:** Governance, architecture, contracts, roadmap, tasks, quality, migration, operations, and agent guidance.

- [x] Create the document ownership structure.
- [x] Record verified migration facts.
- [x] Create release gates and task mapping.
- [x] Validate relative links and prohibited-marker-free authoritative content.

### Task 5: Create repository adapters

**Files:** Repository README, AGENTS, manifests, roadmaps, task lists, docs, and agent adapters.

**Produces:** Self-contained clones that retain workspace boundaries.

- [x] Create public-site documents.
- [x] Create admin-panel documents.
- [x] Create backend documents.
- [x] Validate each repository independently.

### Task 6: Commit and publish bootstrap state

**Files:** All authorized bootstrap files.

**Produces:** Clean local repositories and matching remote `main` branches.

- [x] Run repository status and exclusion checks.
- [x] Commit exact manifests in each product repository.
- [x] Push each product repository to GitHub.
- [x] Commit the root coordination repository locally.
- [x] Record final product-repository commit identifiers.

### Verification evidence before publication

- [x] Authoritative Markdown relative links resolve.
- [x] Authoritative documents contain no unresolved task markers.
- [x] Public/admin repositories contain no legacy runtime frontend source.
- [x] Backend dependency sync passes from the new path.
- [x] Backend Ruff passes.
- [x] All 636 backend tests pass.
- [x] Django settings check and migration-plan generation pass.
