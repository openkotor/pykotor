---
title: "feat: lfg-refresh dry-run and noop guardrails"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: lfg-refresh Dry-Run + Noop Guardrails (plan 077)

## Gaps

- G1. `--lfg-refresh` always executes write/dispatch — no safe preview mode for agents.
- G2. `classify_fc_stale_gap` proceed path runs refresh but cannot auto-fix (needs git history).
- G3. Preflight JSON lacks explicit planned action list for lfg-refresh.

## Requirements

- R1. `--dry-run` with `--lfg-refresh` previews via include-proceed-actions without write/execute/sync.
- R2. Block `--lfg-refresh` when `proceed_reason` is `classify_fc_stale_gap`.
- R3. Embed `lfg_refresh_plan` with `planned_actions` based on proceed_reason.
- R4. Set `lfg_refresh_dry_run: true` when dry-run mode active.
- R5. Unit tests; bump `PLAN_TRACK_CAP` to `077`.

## Test scenarios

- T1. Dry-run lfg-refresh leaves write/execute false after expansion logic.
- T2. classify_fc_stale_gap blocked by _lfg_refresh_blocked.
- T3. lfg_refresh_plan lists doc_apply and dispatch when applicable.
