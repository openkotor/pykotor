---
title: "feat: extend apply to plan020 table and proceed reason"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: Extend Apply to Plan 020 Table + Proceed Reason (plan 072)

## Gaps

- G1. `--apply-checkpoint-snippet` updates plan 020 Last CI line only — verification table rows still hand-edited.
- G2. Solution doc `last_verified` frontmatter stale after apply.
- G3. Checkpoint JSON lacks `proceed_reason` when `defer_lfg_pr: false` — agents must infer from `defer_reason`.
- G4. Plan 020 **Plans:** index line not refreshed on apply.

## Requirements

- R1. `_patch_plan020` updates Verify PyPI CI + Forward Commits verification table rows from live gh.
- R2. `_patch_solution_closeout` updates YAML `last_verified: YYYY-MM-DD` on apply.
- R3. `_compare_checkpoint` sets `proceed_reason` whenever `defer_lfg_pr: false`.
- R4. Plan 020 **Plans:** line updated to current plan index cap (071→072).
- R5. Unit tests for plan020 table patch, frontmatter, proceed_reason.

## Test scenarios

- T1. `_patch_plan020` updates verify/FC verification rows.
- T2. Frontmatter `last_verified` replaced.
- T3. Terminal checkpoint includes `proceed_reason: update_monitoring_docs`.
