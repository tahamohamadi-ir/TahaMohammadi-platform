# R7 Draft-Leak Evidence (staging)

**Status: PARTIAL — public-surface draft absence verified; the preview-token leg
is credential-gated** (owner decision 2026-09-10, `COORD-080` F-05).

**Release:** `stage-601b2294-f1cfa37d-9c2c7045`, 2026-09-10.

| Probe                                                              | Result                                                       |
| ------------------------------------------------------------------ | ------------------------------------------------------------ |
| `GET /api/landings/en`, `/api/landings/fa`, `/api/home-composition/en` | **0** `draft` / `unpublished` / `archived` markers in payloads |
| `GET /api/v1/internal/health`                                      | **404** (internal boundary closed)                            |
| Every staging response                                             | `x-robots-tag: noindex, nofollow, noarchive`                  |
| Public pages `/en/`, `/fa/`, `/en/about/`, `/en/projects/`, `/en/gallery/` | **200**, published content only                        |
| `GET /preview/` without a token                                    | **404**                                                       |

**Not verified live:** valid preview-share token opens a draft outside any
session; expired token returns 410. Both legs require creating a preview link
from an authenticated admin session (owner credentials). Server-side coverage:
`Back-End/tests/test_preview_share.py`, publication/state tests in the
952-test backend suite.

**PASS assessment:** public-surface leg PASS; preview-token leg deferred.
