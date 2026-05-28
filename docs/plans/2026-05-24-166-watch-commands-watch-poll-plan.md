---
title: "fix: top-level watch commands on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level gh_watch_command / briefing_command on Defer Watch Poll stderr (plan 166)

## Summary

Plans 148–149 flattened **`gh_watch_command`** and **`briefing_command`** to top-level gate JSON. Deferred watch poll stderr still derives **`watch=`** via **`_extract_gh_watch_command(briefing)`** and **`briefing_command=`** from **`briefing.command`** instead of the top-level mirrors after **`_apply_lfg_agent_briefing`**.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** emits **`watch=`** from top-level **`gh_watch_command`** after briefing apply when deferred.
- R2. Emit truncated **`briefing_command=`** from top-level **`briefing_command`** after briefing apply when deferred.
- R3. Tests; **`PLAN_TRACK_CAP`** 166; closeout doc bullet; plans index **019–166**.

---

## Test scenarios

- T1. Deferred preflight watch poll stderr includes **`watch=gh run watch …`** and **`briefing_command=`** from top-level mirrors exactly once each.
- T2. Gate watch poll stderr matches the same behavior.
- T3. Plan patch expects **`019–166`**.
