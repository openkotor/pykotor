---
title: "feat: queue age hints and monitor preflight snippet default"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: Queue Age Hints + Monitor Preflight Snippet Default (plan 070)

## Gaps

- G1. `--include-checkpoint-snippet` is opt-in; monitor preflight should ship doc-update text by default.
- G2. `_latest_workflow_run` omits timestamps — no signal for external runner backlog vs actionable drift.
- G3. `fc_sha_stale_benign: null` when git fails still allows defer — oversimplified / unsafe.
- G4. Terminal runs recommend doc updates but JSON lacks `doc_update_recommended` flag for agents.
- G5. No queue backlog note when runs stay queued for many hours.

## Requirements

- R1. `--monitor-preflight` enables `--include-checkpoint-snippet`.
- R2. Run objects include `created_at`, `updated_at`, and `queued_hours` when status is active.
- R3. When `fc_sha_stale` and `fc_sha_stale_benign is None`, `defer_lfg_pr: false` with clear reason.
- R4. When verify or FC reaches terminal status, set `doc_update_recommended: true` on checkpoint.
- R5. When any active run `queued_hours >= 4`, add `queue_backlog_note` on checkpoint.
- R6. Unit tests for timestamps, unknown benign, doc_update_recommended, monitor preflight snippet default.

## Test scenarios

- T1. `_latest_workflow_run` parses `created_at` and computes `queued_hours`.
- T2. `_compare_checkpoint` no defer when `fc_sha_stale_benign is None`.
- T3. Terminal verify sets `doc_update_recommended: true`.
- T4. `--monitor-preflight` JSON includes `checkpoint_snippet` without extra flag.
