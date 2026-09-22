# Plan D migration evidence (Tasks 1–6, backend)

Branch: `feat/knowledge-atlas-migration` (worktree
`D:/Project/.atlas-worktrees/backend-plan-d`).
Base: backend@`bdb546f`. Database: development copy (production untouched).
Machine: DESKTOP-K05IG1H (Windows).
Date (UTC): 2026-09-22.

## Task 1 — legacy graph inventory

Command: `manage.py atlas_graph_inventory`
(`Back-End/apps/atlas/management/commands/atlas_graph_inventory.py`,
read-only; test `test_graph_inventory.py` asserts it writes nothing).

Result on development: **no `GraphVersion` rows** — the dev database was
empty, so the legacy graph was rebuilt there from the paired canonical rows
(profile pair + three research-topic pairs, `translation_key`-paired EN/FA)
before the migration ran. Production data was never touched.

## Task 2 — frozen legacy payloads

Live source (capture time 2026-09-22):
`https://tahamohamadi.ir/api/graph/en|fa` — 4 nodes / 3 edges per locale.

| File | sha256 (first 16 hex) | Shape |
|---|---|---|
| `apps/atlas/tests/fixtures/legacy-graph/en.json` | `d07ffc8fb52d0c32` | 4 nodes / 3 edges |
| `apps/atlas/tests/fixtures/legacy-graph/fa.json` | `8961752dfac8682d` | 4 nodes / 3 edges |

Test `test_legacy_parity_fixture.py` pins: 4 nodes + 3 edges per locale,
verbatim labels, `research-focus` on every edge, identity `relatedRecords`
family `profile`, topic nodes family `researchtopic`. A later live-graph
change fails loudly instead of re-baselining.

## Task 3 — taxonomy seed

Command: `manage.py atlas_seed_taxonomy [--dry-run]`
(`Back-End/apps/atlas/management/commands/atlas_seed_taxonomy.py` —
the vocabulary is a literal table in the command; `update_or_create`
keyed by `key`).

Development run: first run `created=17 updated=0`, second run
`created=0 updated=0` (idempotent). 6 node types + 11 relation types
per spec §6.1/§6.2, including `research-focus` (`directed_default=True`,
`hierarchy_role=False`, allowed pair `identity → research-area`).

## Task 4 — dry-run migration

Command: `manage.py atlas_migrate_graph --dry-run`
(`Back-End/apps/atlas/management/commands/atlas_migrate_graph.py` +
`Back-End/apps/atlas/migration_parity.py`; tests
`test_migrate_graph.py` — 4 passed — and the parity unit tests inside
`test_migration_parity_live.py`).

Development output (verbatim, 2026-09-22 re-run after the lint pass —
byte-identical mapping, same canonical prefixes):

```text
identity -> identity-00000001 (identity, canonical profile:e1f5f055)
research-topic-1 -> research-area-00000001 (research-area, canonical research_topic:01fdbb41)
research-topic-3 -> research-area-00000003 (research-area, canonical research_topic:938fb27b)
research-topic-5 -> research-area-00000005 (research-area, canonical research_topic:5b0da7b1)
identity-00000001 -> research-area-00000001 (research-focus)
identity-00000001 -> research-area-00000003 (research-focus)
identity-00000001 -> research-area-00000005 (research-focus)
atlas_migrate_graph: dry-run nodes=4 relations=3 unresolved=0
```

Design facts the tests pin: the Atlas topology is locale-neutral (EN and
FA graphs describe the SAME entities — dedupe by canonical identity, EN
key wins deterministically); edge endpoints resolve to the KEPT node's
public key; an unpaired record is reported (`SystemExit: unresolved`),
never guessed; a second run updates the migrated draft, never duplicates
it.

## Task 5 — executed migration (development)

```bash
manage.py atlas_migrate_graph --label "Research Universe v1"
# atlas_migrate_graph: migrated draft id=1 nodes=4 relations=3
manage.py shell -c "...recompute_layout..."
# layout_revision: 1
manage.py shell -c "...validate_version....to_dict()..."
# blocking: []
```

Warnings (all honest for a 4-node graph, all acceptable per the plan):
`NO_INBOUND_RELATIONS` (identity), `NO_OUTBOUND_RELATIONS` (3 areas),
`SINGLE_LEVEL_HIERARCHY`, `SUMMARY_MISSING` (nodes carry no summary
overrides yet). The draft lives in the development database only —
it is not in git by design.

## Task 6 — parity proof

Test: `Back-End/apps/atlas/tests/test_migration_parity_live.py`
(seeds the frozen payloads' verbatim titles, runs the REAL
`atlas_migrate_graph` command, compares the REAL `build_locale_projection`
output via `compare_parity` — 2 passed, plus a tamper-negative test
proving the comparator is a real gate).

Parity table (§23.4), per locale:

| Check | en | fa |
|---|---|---|
| nodes (4 == 4) | PASS | PASS |
| relations (3 == 3) | PASS | PASS |
| labels (verbatim, incl. FA `روایت‌محور` ZWNJ) | PASS | PASS |
| canonicalTargets (family per position; pk values are per-database) | PASS | PASS |
| relationTypes (`research-focus` in catalog) | PASS | PASS |
| relationEndpoints (identity → each area label pair) | PASS | PASS |
| localeParity | PASS | PASS |

Note on `canonicalTargets`: the frozen legacy ids are production row pks
(1/2/3); any seeded database mints its own pks, so ids compare by POSITION
(Nth legacy node ↔ Nth Atlas node, family must match), never by value.
Proving two databases share primary keys would be the wrong assertion.

## Gates for this branch

```bash
env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test ./.venv/Scripts/python.exe -m pytest apps/atlas/tests/test_migrate_graph.py apps/atlas/tests/test_migration_parity_live.py apps/atlas/tests/test_legacy_parity_fixture.py apps/atlas/tests/test_seed_taxonomy.py apps/atlas/tests/test_graph_inventory.py -q
# 12 passed
uv run ruff check apps/atlas/migration_parity.py apps/atlas/management/commands/atlas_migrate_graph.py apps/atlas/tests/test_migrate_graph.py apps/atlas/tests/test_migration_parity_live.py
# All checks passed!
```

(`ruff` on the four NEW files only. The repo's older committed files,
e.g. `atlas_seed_taxonomy.py`, carry pre-existing UP031 findings and are
out of scope — no drive-by reformat.)
