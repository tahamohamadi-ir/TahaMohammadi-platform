# Visual packet queue — reconciled

Use [EXECUTION.md](EXECUTION.md) and [execution-tasks.json](execution-tasks.json) for dispatch. This replaces the former independent CA schedule. `tasks.json` is now the synchronized CA-only view.

CA-01–08 preserve the original hero/gateway/shell work. CA-02 additionally requires the accepted ID resolver and generated public types. CA-09–16 are SUPERSEDED aliases: their visual checks transfer to the PU family packets listed in the canonical queue. CA-17 reviews all public families after the completed publication journey.

## Dispatch prompt

Implement only the assigned active packet from execution-tasks.json. Read workspace/owner AGENTS.md, ADR-0008/0009/0010 and the packet's bounded context. Verify dependency handoffs and base HEAD, then use only that repository's exact allowlist. Preserve locale/theme/no-JS and published-content guarantees. Return the packet handoff with real checks, UI evidence and its stop marker. Do not dispatch retired CA packets or begin another task.

## Handoff contract

Report task ID, repository, branch, base HEAD, resulting commit or uncommitted state, changed paths, focused failing-before/passing-after evidence, required checks, source schema hash, screenshots with route/locale/theme/width/state, dirty status and unresolved issues. Tests/builds do not imply visual or release acceptance. Runtime screenshots remain ignored artifacts; handoff documents may reference exact paths.

## Figma

No Figma file is claimed or required. The review board remains a schematic reference. If Figma is later requested, bind frames and annotations to the active execution packet IDs, not the retired CA schedule.
