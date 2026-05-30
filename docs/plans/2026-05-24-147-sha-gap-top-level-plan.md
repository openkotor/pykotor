---
title: "fix: top-level sha gap json"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level sha_gap JSON (plan 147)

## Summary

When FC SHA lag is active, defer briefing includes structured **`sha_gap`**, and briefing stderr prints **`sha_gap=`**, but top-level gate JSON omits the object unless agents drill into **`lfg_agent_briefing`**. Strict exit stderr also omits **`sha_gap=`**.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`sha_gap`** and **`sha_gap_short`** to top-level status JSON when set.
- R2. **`preflight_watch_summary`** JSON includes both when deferred with SHA gap.
- R3. **`_emit_lfg_strict_exit_stderr`** appends **`sha_gap=`** when briefing carries **`sha_gap.short`**.
- R4. Watch summary one-liner includes **`sha_gap=`** when present.
- R5. Tests; **`PLAN_TRACK_CAP`** 147; closeout doc bullet; plans index **019–147**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`sha_gap`** / **`sha_gap_short`** when FC SHA gap is active.
- T2. Watch summary JSON includes both fields.
- T3. Strict exit stderr includes **`sha_gap=7d85438:8916e2f`** style token.
- T4. Plan patch expects **`019–147`**.
