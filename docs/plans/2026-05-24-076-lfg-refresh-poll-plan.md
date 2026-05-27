---
title: "feat: lfg-refresh alias and dispatch poll retry"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: lfg-refresh Alias + Dispatch Poll Retry (plan 076)

## Gaps

- G1. Agents must chain 6+ flags for full refresh (dispatch + doc sync + terminal apply).
- G2. Post-dispatch doc sync often skips because gh has not indexed the new run yet.
- G3. No guardrail blocking refresh while checkpoint is deferred.

## Requirements

- R1. `--lfg-refresh` expands to compare + include-proceed-actions + write + execute + cancel-stale + sync-docs.
- R2. Block `--lfg-refresh` with exit 2 when deferred or proceed_reason is fix_checkpoint_error / fix_gh_lookup.
- R3. Emit `lfg_refresh: true` in JSON when refresh proceeds.
- R4. Poll gh run list after dispatch (default 3 attempts, 2s interval) before doc sync skip.
- R5. `--dispatch-poll-attempts` / `--dispatch-poll-interval` override poll defaults.
- R6. Unit tests; bump `PLAN_TRACK_CAP` to `076`.

## Test scenarios

- T1. lfg-refresh expands flags and blocks when deferred.
- T2. Poll retry detects run_id change on second fetch.
- T3. CLI parser accepts --lfg-refresh.
