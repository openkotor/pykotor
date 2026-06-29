---
title: "fix: top-level briefing action json"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level briefing_action JSON (plan 142)

## Summary

Defer briefing exposes **`action: defer`**, and the briefing stderr line prints **`action=defer`**, but top-level gate JSON omits the action word unless agents drill into **`lfg_agent_briefing`**. Strict exit stderr also omits **`action=`** even though **`lfg_defer_reason`** is present separately.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`action`** to top-level **`briefing_action`** when set.
- R2. **`preflight_watch_summary`** JSON includes **`briefing_action`** on deferred watch end.
- R3. **`_emit_lfg_strict_exit_stderr`** appends **`action=`** when briefing carries it.
- R4. Watch summary one-liner includes **`action=`** when present.
- R5. Tests; **`PLAN_TRACK_CAP`** 142; closeout doc bullet; plans index **019–142**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`briefing_action: defer`** when deferred.
- T2. Watch summary JSON includes **`briefing_action`**.
- T3. Strict exit stderr includes **`action=defer`**.
- T4. Plan patch expects **`019–142`**.
