---
title: "fix: briefing notes count on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: briefing_notes count on Defer Watch Poll stderr (plan 154)

## Summary

Plan 143 flattened **`briefing_notes`** to top-level gate JSON and added **`notes=N`** on strict exit and watch summary one-liners. Deferred watch poll stderr still omits **`notes=`**, so agents polling **`--lfg-gate-watch`** cannot see how many briefing notes apply on each poll.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** appends **`notes=N`** when **`briefing_notes`** is non-empty after **`_apply_lfg_agent_briefing`**.
- R2. Tests for preflight and gate poll lines with deferred briefing notes.
- R3. **`PLAN_TRACK_CAP`** 154; closeout doc bullet; plans index **019–154**.

---

## Test scenarios

- T1. Preflight watch poll stderr includes **`notes=1`** when deferred with checkpoint queue backlog note.
- T2. Gate watch poll stderr includes **`notes=1`** on the same fixture.
- T3. Plan patch expects **`019–154`**.
