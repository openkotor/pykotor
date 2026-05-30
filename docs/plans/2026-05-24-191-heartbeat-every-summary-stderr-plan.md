---
title: "feat: heartbeat_every on preflight summary stderr"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: heartbeat_every on Preflight Summary Stderr (plan 191)

## Summary

Align preflight/gate watch **summary** stderr with poll lines: emit compact **`heartbeat_every=N`** (replacing **`watch_heartbeat_polls=`**) when unchanged flat-key polls occurred. JSON keeps **`watch_heartbeat_polls`**.

---

## Requirements

- R1. **`_format_preflight_watch_summary_line`** emits **`heartbeat_every=N`** when **`unchanged_flat_keys_polls > 0`** and interval **> 0**.
- R2. Omit legacy **`watch_heartbeat_polls=`** summary stderr token.
- R3. Tests; **`PLAN_TRACK_CAP`** 191; closeout index **019–191**.

---

## Test scenarios

- T1. Unchanged flat polls → summary stderr includes **`heartbeat_every=12`**.
- T2. No unchanged flat polls → omit **`heartbeat_every=`**.
- T3. Plan patch expects **`019–191`**.
