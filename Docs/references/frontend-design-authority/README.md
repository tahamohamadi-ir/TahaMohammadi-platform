# Frontend Design Authority

This is the sole tracked visual and machine-readable reference for the greenfield public site and admin panel. It was curated from the owner-provided local incoming package at `Front-End/Assets` on 2026-08-29.

## Read order

1. Workspace `AGENTS.md` and `Docs/00-governance/AUTHORITY-ORDER.md`.
2. `AUTHORITY-MANIFEST.json` and `SHA256SUMS.txt`.
3. `design-dna.json`, then `Docs/04-design/DESIGN-DNA.md`.
4. `concepts/` and `concepts/page-families/` for UI/UX hierarchy and page detail.
5. `agent-kit/` for component/template/token contracts.
6. `Docs/04-design/ASSET-PROMOTION-LEDGER.md` before using any file in runtime.

## Boundaries

- `concepts/` and `concepts/page-families/` are UI/UX references. They do not supply factual public copy or native controls.
- `art/` and `brand/` are candidate source media. Runtime use requires a promotion-ledger approval, responsive derivative plan, and accessible text alternative.
- `provenance/` explains source history and is not a runtime dependency.
- `archive/` is intentionally empty in this tracked authority. Unique unmanaged local evidence remains only under the ignored local incoming tree.
- `ALIASES.json` records semantically named copies without storing duplicate bytes.
- No component, route, API field, owner fact, translation, right, or publication state may be inferred from a raster reference.

## Integrity

Run the validator from either the workspace root or this directory:

```powershell
node Docs/references/frontend-design-authority/agent-kit/validate.mjs
```

The validator checks asset existence, hashes, alias equivalence, duplicate hashes, JSON shape, the 24-component and six-template inventories, and the offline Figma policy. `SHA256SUMS.txt` is the binary integrity ledger.
