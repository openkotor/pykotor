---
title: "feat: lfg gate-watch and defer post-terminal commands"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: LFG Gate-Watch + Post-Terminal Commands (plan 118)

## Summary

Agents repeatedly run `--lfg-gate` (exit 2) while FC is queued. Add **`--lfg-gate-watch`** (gate + preflight-watch) and defer **`post_terminal_commands`** for after FC completes.

---

## Problem Frame

Live: `fc_active_pending` with watch_recommended; gate exits 2 without polling; no structured next steps after FC terminal.

---

## Requirements

- R1. `--lfg-gate-watch` enables `--lfg-gate --lfg-preflight-watch`.
- R2. `_build_defer_post_terminal_commands` with preflight/prefetch-gate hints.
- R3. Defer briefing attaches `post_terminal_commands`; monitor_commands includes `gate_watch`.
- R4. `preflight_watch_summary.next_hint` from proceed_hint after watch.
- R5. `lfg_mode` `gate_watch`; tests; `PLAN_TRACK_CAP` `118`; docs.

---

## Test scenarios

- T1. `--lfg-gate-watch` sets gate + preflight-watch flags.
- T2. Defer briefing includes post_terminal_commands.prefetch_gate when fc_sha_stale.
- T3. Watch summary includes next_hint when defer clears.
