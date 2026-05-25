---
title: "feat: auto apply docs on proceed and lfg_proceed signal"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: Auto-Apply Docs on Proceed + lfg_proceed Signal (plan 073)

## Gaps

- G1. When CI completes, agents must run a second `--apply-checkpoint-snippet --write` command after preflight.
- G2. Preflight JSON lacks `lfg_proceed` when gate allows work (only `lfg_deferred` on defer path).
- G3. No embedded dry-run apply preview in preflight for proceed paths.
- G4. After auto-write, `doc_validation` is stale until manual re-run.

## Requirements

- R1. `--auto-apply-on-proceed` with monitor preflight embeds `doc_apply` dry-run when `proceed_reason` is auto-apply eligible.
- R2. `--auto-apply-on-proceed --write` persists docs when apply allowed without `--force`.
- R3. Eligible reasons: `update_monitoring_docs`, `investigate_ci_drift`.
- R4. Status JSON adds `lfg_proceed: true` and `lfg_proceed_reason` when not deferred.
- R5. Re-validate `doc_validation` after successful auto-write.
- R6. Unit tests for lfg_proceed and auto-apply gate.

## Test scenarios

- T1. Terminal checkpoint sets `lfg_proceed` via helper.
- T2. Auto-apply dry-run embedded when `update_monitoring_docs`.
- T3. Auto-apply skipped when deferred.
- T4. CLI `--auto-apply-on-proceed` on mocked terminal state.
