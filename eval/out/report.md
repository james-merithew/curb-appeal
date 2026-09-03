# Curb Appeal - Vision Accuracy Report

Model(s): claude-opus-5 | images scored: 62 | doors: 12

## 1. Accuracy vs ground truth

`not_visible` counts as an abstention, not an error - it is scored separately. door_width_adequate is excluded (appearance-only vocabulary, no strict truth).

| Criterion | Correct | Wrong | Abstained | Accuracy (of committed) |
|---|---|---|---|---|
| step_free_entry | 53 | 7 | 2 | 88% |
| ramp_present | 41 | 5 | 13 | 89% |
| handrails_present | 24 | 1 | 34 | 96% |
| auto_door_button | 5 | 0 | 54 | 100% |
| lever_or_pull_hardware | 50 | 7 | 5 | 88% |
| clear_approach | 53 | 8 | 1 | 87% |
| accessible_signage | 18 | 0 | 44 | 100% |
| **all criteria** | 244 | 28 | - | **90%** |

## 2. Cross-view consistency (does the verdict flip with the angle?)

Per door: share of views agreeing with the modal verdict, averaged over criteria. 100% = rock solid across angles.

| Door | Views | Consistency | Least stable criterion |
|---|---|---|---|
| door-01 | 5 | 92% | accessible_signage (60%) |
| door-02 | 5 | 88% | handrails_present (60%) |
| door-03 | 6 | 77% | handrails_present (50%) |
| door-04 | 5 | 90% | door_width_adequate (60%) |
| door-05 | 6 | 81% | handrails_present (50%) |
| door-06 | 7 | 80% | handrails_present (57%) |
| door-07 | 4 | 94% | handrails_present (50%) |
| door-08 | 7 | 82% | step_free_entry (71%) |
| door-09 | 3 | 75% | step_free_entry (33%) |
| door-10 | 5 | 90% | door_width_adequate (60%) |
| door-11 | 5 | 85% | step_free_entry (60%) |
| door-12 | 4 | 91% | ramp_present (50%) |

## 3. Device delta (iPhone 16 Pro vs iPhone 16)

| Device | Images | Accuracy vs truth | Median latency |
|---|---|---|---|
| iPhone 17 Pro | 62 | 90% | 10.1s |

## 4. Latency vs the 15-second demo budget

- min 6.7s / median 10.1s / p95 18.9s / max 20.5s
- over budget (>15s): 10/62 (16%)
- note: this is model latency only; the production budget must also cover upload (~2s) and geocode+render (~2s).
