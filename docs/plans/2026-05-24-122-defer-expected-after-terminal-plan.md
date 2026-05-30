---
title: "fix: defer expected-after-terminal and queue warn"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Defer Expected-After-Terminal and Queue Warn (plan 122)

## Summary

During **`fc_active_pending`** defer, agents need explicit post-FC guidance and early queue warnings before the 4h severe threshold. Add **`expected_after_terminal`** to defer briefing, **`queue_backlog_warning`** at ≥2h queued, and defer-reason transition in watch summary stderr.

---

## Problem Frame

Live: FC queued 0.5h on stale SHA; agents must gate-watch then run prefetch+gate after terminal. Briefing has **`post_terminal_commands`** but no single primary **`expected_after_terminal`** field. Queue severity only surfaces at 4h.

---

## Requirements

- R1. Defer briefing includes **`expected_after_terminal`** `{action, command}` preferring `prefetch_gate` → `gate` → `preflight`.
- R2. **`queue_context.queue_backlog_warning`** when `max_queued_hours` ≥ 2 and < 4.
- R3. Defer stderr **`queue_warn=true`** when warning active.
- R4. Watch summary line includes **`reason=start->end`** when defer reasons differ across watch.
- R5. Tests; `PLAN_TRACK_CAP` `122`; closeout doc bullet.

---

## Scope Boundaries

- No change to defer exit codes or FC classification logic.
- No doc auto-apply while deferred.

---

## Test scenarios

- T1. Defer briefing with `prefetch_gate` post_terminal → `expected_after_terminal.action=prefetch_gate`.
- T2. queue_context warning at 2.5h queued, not severe.
- T3. stderr includes `queue_warn=true` and `expected_after=prefetch_gate`.
- T4. Summary line with differing start/end defer reasons includes `reason=`.
