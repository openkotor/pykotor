---
title: "fix: top-level queue flags on watch summary stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level Queue Fields on Watch Summary One-Liner stderr (plan 169)

## Summary

Plan 141 flattened queue backlog fields to top-level **`preflight_watch_summary`** JSON via **`_mirror_queue_context_fields`**. The watch summary one-liner stderr still reads **`queued=`** / queue flags only from nested **`queue_context`**, diverging from deferred poll stderr (plan 159) and top-level gate JSON.

---

## Requirements

- R1. **`_format_preflight_watch_summary_line`** emits **`queued=`** / queue flags from top-level **`max_queued_hours`** / backlog flags when present.
- R2. Fall back to nested **`queue_context`** only when top-level queue fields are absent (direct formatter tests).
- R3. Tests; **`PLAN_TRACK_CAP`** 169; closeout doc bullet; plans index **019–169**.

---

## Test scenarios

- T1. Watch summary one-liner prefers top-level **`max_queued_hours`** / **`queue_backlog_warning`** over nested **`queue_context`**.
- T2. Formatter still works when only nested **`queue_context`** is supplied.
- T3. Plan patch expects **`019–169`**.
