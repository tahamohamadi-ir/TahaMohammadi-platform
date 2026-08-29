# Asset Migration Manifest

The deduplicated tracked handoff package is preserved under `Docs/references/frontend-design-authority/`. Its local owner-provided comparison input remains at `Front-End/Assets` and is ignored by Git.

## Migration rule

- One canonical file is retained per promoted SHA-256 under the tracked authority.
- Requested byte-identical names are represented in `ALIASES.json`, not as second files.
- The local nested `assets/` mirror and byte-identical `others/` files are removed only after `provenance/DELETION-MAP.json` records their retained same-hash path.
- Unique unmanaged local evidence is retained under `Front-End/Assets/archive/unmanaged-unique/` and never becomes authority by proximity.
- The former `Docs/references/site-redesign/` tree was retired after link, hash, manifest, and agent-kit validation. Git history preserves the prior tree; agents must not revive it.

The bootstrap-era `site-redesign` pack tracked 33 managed binary hashes. After deduplication into `frontend-design-authority`, 30 unique binaries remain under checksum validation; the three retired hashes were byte-identical duplicates consolidated per `provenance/DELETION-MAP.json`.

The original `SHA256SUMS.txt` remains the integrity authority for managed binaries.

Runtime promotion requires:

1. Owner publication approval.
2. A named route and role.
3. Verified crop and alt behavior.
4. Responsive derivative generation.
5. Public-site asset tests.

Concept files remain reference-only.
