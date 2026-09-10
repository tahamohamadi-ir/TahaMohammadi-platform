# R7 Media Boundary Evidence (staging)

**Status: PARTIAL — public asset serving and the inactive boundary are verified;
the active/activate toggle leg is credential-gated** (owner decision 2026-09-10,
`COORD-080` F-05).

**Release:** `stage-601b2294-f1cfa37d-9c2c7045`, 2026-09-10.

| Probe                                                              | Result                          |
| ------------------------------------------------------------------ | ------------------------------- |
| Promoted static asset `/_astro/taha-mark-primary.YrmYLcZm_ZU1gyc.avif` | **200** `image/avif`         |
| `GET /media/does-not-exist-probe.png`                              | **404** (retry after one transient timeout; 2.8 s) |
| `GET /media/`                                                      | **404**                         |
| `GET /preview/` (no token)                                         | **404**                         |
| Audited pages (`/en/`, `/en/about/`, `/en/projects/`, `/en/gallery/`) | **0** raw `/media/` references |

Notes: approved/promoted media is compiled into `/_astro/` derivatives at build
time; the CMS `/media/` route stays reachable only for active files through the
same edge. Verifying an active CMS file (`200`) and the deactivate/activate
toggle requires admin credentials and is deferred with the owner decision.

**PASS assessment:** inactive boundary PASS; active-file leg deferred.
