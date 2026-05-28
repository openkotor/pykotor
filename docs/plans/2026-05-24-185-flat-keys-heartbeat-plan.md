---
title: "feat: flat_keys heartbeat on gate-watch polls"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: flat_keys Heartbeat on Gate-Watch Polls (plan 185)

## Summary

Plan 183–184 compact unchanged **`flat_keys=`** stderr. Reuse **`--watch-heartbeat-polls`** (default 12) so every N unchanged flat-key polls re-emit full **`flat_keys=`** / **`flat_fields=`** with **`flat_keys_heartbeat=1`**.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** accepts streak + heartbeat interval; skips compact omit on heartbeat polls.
- R2. **`_watch_lfg_preflight_defer`** tracks flat-key unchanged streak and **`preflight_flat_keys_heartbeats`** count.
- R3. **`preflight_watch_summary`** + summary stderr include **`flat_keys_heartbeat_polls`** when **> 0**.
- R4. Tests; **`PLAN_TRACK_CAP`** 185; closeout bullet; plans index **019–185**.

---

## Test scenarios

- T1. Streak 12 + heartbeat 12 → **`flat_keys=`** present, **`flat_keys_heartbeat=1`**, no **`flat_unchanged=true`**.
- T2. Streak 1 unchanged → compact omit still applies.
- T3. Plan patch expects **`019–185`**.
