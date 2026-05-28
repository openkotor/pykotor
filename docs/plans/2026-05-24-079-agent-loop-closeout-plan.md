---
title: "docs: agent loop closeout and lfg-gate shorthand"
type: docs
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# docs: Agent Loop Closeout + lfg-gate Shorthand (plan 079)

## Gaps

- G1. Solution closeout doc stops at plan 073; missing lfg-preflight / proceed_hint / lfg-refresh loop.
- G2. Agents must remember `--lfg-preflight --strict-defer-exit` for gate + full JSON.
- G3. Plans index in closeout still references 019–073.

## Requirements

- R1. Add **Agent loop** section to `verify-pypi-regression-closeout.md` with proceed_hint workflow.
- R2. `--lfg-gate` expands to `--lfg-preflight --strict-defer-exit`.
- R3. Update closeout Prefer section for plans 074–078 flags.
- R4. Unit test for `--lfg-gate` CLI; bump `PLAN_TRACK_CAP` to `079`.

## Test scenarios

- T1. lfg-gate sets preflight + strict-defer-exit.
- T2. lfg-gate exits 2 when deferred (live gh integration).
