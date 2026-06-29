---
title: "fix: top-level briefing_command json"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level briefing_command JSON (plan 149)

## Summary

Gate JSON exposes **`wait_command`** from defer briefing, but agents scanning **`briefing_*`** top-level fields miss the primary gate-watch script. Strict exit already uses **`command=`** for **`pr_ci_recommendation`**, so briefing needs a distinct **`briefing_command`** alias. Watch poll stderr also omits **`watch=`** and **`briefing_command=`** on deferred polls.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`briefing.command`** to top-level **`briefing_command`** (alongside **`wait_command`**).
- R2. **`preflight_watch_summary`** JSON includes **`briefing_command`** on deferred watch end.
- R3. **`_emit_lfg_strict_exit_stderr`** appends truncated **`briefing_command=`** when briefing carries a command (distinct from **`pr_ci_recommendation.command`**).
- R4. Watch summary one-liner includes truncated **`briefing_command=`** when present.
- R5. Watch poll stderr adds **`watch=`** and truncated **`briefing_command=`** when deferred briefing is applied.
- R6. Tests; **`PLAN_TRACK_CAP`** 149; closeout doc bullet; plans index **019–149**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`briefing_command`** when deferred with gate-watch primary command.
- T2. Watch summary JSON includes **`briefing_command`**.
- T3. Strict exit stderr includes **`briefing_command=--lfg-gate-watch`** (truncated when long).
- T4. Watch poll stderr includes **`watch=`** and **`briefing_command=`** on deferred poll.
- T5. Plan patch expects **`019–149`**.
