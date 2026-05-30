---
title: "fix: top-level watch_recommended json and stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level watch_recommended JSON and Stderr (plan 134)

## Summary

Defer briefing sets **`watch_recommended: true`** and briefing stderr emits **`watch_recommended=true`**, but top-level gate JSON and watch summary omit it unless agents drill into **`lfg_agent_briefing`**.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`watch_recommended`** to top-level status JSON when true.
- R2. **`LFG exit:`** stderr appends **`watch_recommended=true`** when briefing recommends watch.
- R3. **`preflight_watch_summary`** JSON and one-liner include **`watch_recommended`** when set.
- R4. Tests; **`PLAN_TRACK_CAP`** 134; closeout doc bullet; plans index **019–134**.

---

## Test scenarios

- T1. Gate JSON top-level **`watch_recommended: true`** when deferred with active runs.
- T2. Strict exit stderr includes **`watch_recommended=true`**.
- T3. Watch summary one-liner includes **`watch_recommended=true`**.
- T4. Plan patch expects **`019–134`**.
