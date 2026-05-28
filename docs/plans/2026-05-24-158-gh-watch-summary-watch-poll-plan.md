---
title: "fix: gh_watch_summary on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level gh_watch_summary on Defer Watch Poll stderr (plan 158)

## Summary

Plan 129 flattened **`gh_watch_summary`** to top-level gate JSON and poll stderr already prints **`gh_watch=`**, but only from **`_build_gh_watch_from_status`** before briefing apply. Deferred poll lines should source **`gh_watch=`** from the top-level mirror after **`_apply_lfg_agent_briefing`** for parity with strict exit and watch summary one-liners.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** emits **`gh_watch=`** from top-level **`gh_watch_summary`** after briefing apply when deferred.
- R2. Skip pre-briefing **`_build_gh_watch_from_status`** token when **`lfg_deferred`** to avoid duplicates.
- R3. Tests; **`PLAN_TRACK_CAP`** 158; closeout doc bullet; plans index **019–158**.

---

## Test scenarios

- T1. Preflight watch poll stderr includes **`gh_watch=verify:1,fc:2`** exactly once when deferred.
- T2. Gate watch poll stderr includes the same token exactly once.
- T3. Plan patch expects **`019–158`**.
