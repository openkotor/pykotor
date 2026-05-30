---
title: "feat: omit unchanged flat_keys on gate-watch polls"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: Omit Unchanged flat_keys on Gate-Watch Polls (plan 183)

## Summary

Plan 182 added **`flat_keys=`** stderr on every deferred poll. When populated keys are unchanged poll-to-poll, omit **`flat_keys=`** and **`flat_fields=`** and emit **`flat_unchanged=true`** instead.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line(..., previous_flat_keys=)`** compares present-keys to prior poll.
- R2. When equal and non-empty, strip **`flat_keys=`** / **`flat_fields=`** and append **`flat_unchanged=true`**.
- R3. **`_watch_lfg_preflight_defer`** tracks previous flat keys between polls.
- R4. Tests; **`PLAN_TRACK_CAP`** 183; closeout bullet; plans index **019–183**.

---

## Test scenarios

- T1. Second poll with same present-keys → no **`flat_keys=`**, has **`flat_unchanged=true`**.
- T2. Poll with changed present-keys → full **`flat_keys=`** list, no **`flat_unchanged=true`**.
- T3. Plan patch expects **`019–183`**.
