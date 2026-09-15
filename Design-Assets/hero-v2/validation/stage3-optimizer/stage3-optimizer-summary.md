# Hero v2 — Stage 3 pivot-offset sweep

Constrained closure pass: the authored angles are unchanged and the FRAME_04
crowding is solved by moving the rotation pivot along the direction derived
from the core -> HEALTH vector. Every row is a real scene build with the
sequence fit, cameras and relation curves recomputed.

| candidate | offset | min gap px | clearance d/m % | 01->04 movement % | continuity | core drift % | hard | score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| k0.00-splus | 0.00 | 1.00 | 8.62 / 4.39 | 8.38 | 0.590 | 1.33 | FAIL | — |
| k0.04-splus | 0.04 | 2.10 | 8.62 / 4.39 | 8.21 | 0.596 | 1.33 | FAIL | — |
| k0.06-splus | 0.06 | 2.60 | 8.62 / 4.39 | 8.12 | 0.602 | 1.32 | FAIL | — |
| k0.08-splus | 0.08 | 3.10 | 8.62 / 4.39 | 8.04 | 0.608 | 1.32 | FAIL | — |
| k0.10-splus | 0.10 | 3.70 | 8.61 / 4.39 | 7.95 | 0.615 | 1.32 | FAIL | — |
| k0.12-splus | 0.12 | 4.20 | 8.61 / 4.39 | 7.87 | 0.622 | 1.32 | FAIL | — |
| k0.14-splus | 0.14 | 4.80 | 8.61 / 4.39 | 7.78 | 0.629 | 1.32 | FAIL | — |
| k0.16-splus | 0.16 | 5.30 | 8.61 / 4.39 | 7.70 | 0.637 | 1.32 | PASS | 0.65 |
| k0.20-splus | 0.20 | 6.10 | 8.61 / 4.39 | 7.53 | 0.652 | 1.32 | PASS | 0.56816 |
| k0.22-splus | 0.22 | 6.40 | 8.60 / 4.39 | 7.44 | 0.660 | 1.32 | PASS | 0.51794 |
| k0.24-splus | 0.24 | 6.70 | 8.60 / 4.39 | 7.36 | 0.668 | 1.32 | PASS | 0.48719 |
| k0.26-splus | 0.26 | 7.00 | 8.60 / 4.39 | 7.28 | 0.677 | 1.32 | PASS | 0.40759 |
| k0.28-splus | 0.28 | 7.30 | 8.60 / 4.39 | 7.19 | 0.686 | 1.31 | PASS | 0.35 |

Winner: **k0.20-splus**

Ranking: hard constraints first, then the 8 px preference, then a
6 px safety gap (the final validator measures rendered pixels, not
projections), then weights movement 0.35 / continuity 0.30 / gap 0.20 /
drift 0.15.
