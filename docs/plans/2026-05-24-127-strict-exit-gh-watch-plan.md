---
title: "fix: strict exit gh_watch and watch summary active_runs stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Strict Exit gh_watch and Watch Summary active_runs Stderr (plan 127)

## Summary

Plan 126 added **`gh_watch=verify:ID,fc:ID`** to briefing stderr and **`active_runs`** in watch summary JSON. Agents reading only **`LFG exit:`** or the one-line watch summary still miss multi-run watch IDs. Propagate **`gh_watch`** to strict exit stderr, structured briefing JSON, and the watch summary one-liner.

---

## Requirements

- R1. Defer/drift briefing JSON includes **`gh_watch_summary`** when monitor watch commands exist.
- R2. **`LFG exit:`** stderr appends **`gh_watch=`** from briefing (parity with briefing stderr).
- R3. **`_format_preflight_watch_summary_line`** appends **`active_runs=`** when summary dict carries **`active_runs`**.
- R4. Tests; **`PLAN_TRACK_CAP`** 127; closeout doc bullet; plans index **019–127**.

---

## Test scenarios

- T1. Strict exit defer briefing → stderr contains **`gh_watch=verify:1,fc:2`**.
- T2. Defer briefing JSON includes **`gh_watch_summary`**.
- T3. Watch summary line includes **`active_runs=verify,fc`**.
- T4. Plan patch expects **`019–127`**.
