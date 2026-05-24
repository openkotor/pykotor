---
title: "feat: strict-defer-exit code for LFG gate"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: strict-defer-exit for LFG Gate (plan 064)

## Summary

`lfg_deferred: true`; PR #308 open. Add `--strict-defer-exit` so `--monitor-preflight` returns exit code **2** when deferred (0 = proceed, 1 = gh error), enabling shell/LFG to stop before noop work.

## Requirements

- R1. `--strict-defer-exit` requires defer path (`--exit-on-defer` or `--monitor-preflight`).
- R2. Exit 2 when `lfg_deferred`; exit 0 when not deferred and `gh_ok`; exit 1 on gh failure.
- R3. Unit tests for exit codes (mock defer path where possible).
- R4. Document in AGENTS.md and solution doc; append to PR #308.

## Implementation Units

- U1. Script exit logic
- U2. Tests (subprocess with real monitor-preflight → expect 2 today)
- U3. Docs

## Scope Boundaries

- No Last CI check update (still queued).
