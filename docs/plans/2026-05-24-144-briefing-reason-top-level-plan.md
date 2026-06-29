---
title: "fix: top-level briefing reason json"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level briefing_reason JSON (plan 144)

## Summary

Defer briefing exposes **`reason: unchanged_active_runs`**, and the briefing stderr line prints **`reason=unchanged_active_runs`**, but top-level gate JSON only has the separate **`lfg_defer_reason`** key. Agents parsing briefing-shaped JSON without that mapping must drill into **`lfg_agent_briefing`**.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors briefing **`reason`** to top-level **`briefing_reason`** when set.
- R2. **`preflight_watch_summary`** JSON includes **`briefing_reason`** on deferred watch end.
- R3. **`_emit_lfg_strict_exit_stderr`** appends **`briefing_reason=`** when briefing carries reason.
- R4. Watch summary one-liner includes **`briefing_reason=`** when present.
- R5. Tests; **`PLAN_TRACK_CAP`** 144; closeout doc bullet; plans index **019–144**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`briefing_reason: unchanged_active_runs`** when deferred.
- T2. Watch summary JSON includes **`briefing_reason`**.
- T3. Strict exit stderr includes **`briefing_reason=unchanged_active_runs`**.
- T4. Plan patch expects **`019–144`**.
