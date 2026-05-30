---
title: "fix: top-level sha_gap on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level sha_gap_short on Defer Watch Poll stderr (plan 164)

## Summary

Plan 147 flattened **`sha_gap_short`** to top-level gate JSON. Deferred watch poll stderr still emits a pre-briefing checkpoint **`sha_gap=`** from raw SHAs and a second **`sha_gap=`** from briefing after apply, duplicating or drifting from the top-level mirror.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** skips pre-briefing checkpoint **`sha_gap=`** when **`lfg_deferred`**.
- R2. Emit **`sha_gap=`** from top-level **`sha_gap_short`** after **`_apply_lfg_agent_briefing`** when deferred.
- R3. Non-deferred poll lines keep pre-briefing checkpoint **`sha_gap=`** for backward compatibility.
- R4. Tests; **`PLAN_TRACK_CAP`** 164; closeout doc bullet; plans index **019–164**.

---

## Test scenarios

- T1. Deferred preflight watch poll stderr includes **`sha_gap=7d85438:8916e2f`** exactly once.
- T2. Gate watch poll stderr matches the same dedupe behavior.
- T3. Non-deferred poll fixture still emits checkpoint **`sha_gap=`**.
- T4. Plan patch expects **`019–164`**.
