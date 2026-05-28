---
title: "feat: apply checkpoint snippet dry-run and write"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: Apply Checkpoint Snippet Dry-Run + Write (plan 071)

## Gaps

- G1. Agents must hand-edit solution doc **Last CI check** and **CI canonical runs** table — error-prone duplicate updates.
- G2. Plan 020 **Last CI check** prose drifts separately from solution doc.
- G3. No safe preview before writing monitoring docs while CI is still active.
- G4. Apply should refuse noop writes when `lfg_deferred` and `doc_valid` unless `--force`.

## Requirements

- R1. `--apply-checkpoint-snippet` (requires `--ci-status-only --compare-checkpoint`) previews or writes doc updates.
- R2. Default dry-run; `--write` persists changes.
- R3. Updates `docs/solutions/testing/verify-pypi-regression-closeout.md` Last CI check + canonical table rows.
- R4. Optional plan 020 target via `--apply-targets solution,plan020` (default both).
- R5. Allow apply when `doc_update_recommended`, doc drift, or `--force`; otherwise exit 2 with reason JSON.
- R6. Unit tests for patch helpers and apply gate logic.

## Test scenarios

- T1. `_replace_last_ci_check_section` replaces body when snippet differs.
- T2. `_replace_canonical_table_row` updates run ID and notes.
- T3. Apply dry-run returns `would_write: true` without modifying file (mock/temp).
- T4. Apply blocked when deferred + doc_valid without `--force`.
