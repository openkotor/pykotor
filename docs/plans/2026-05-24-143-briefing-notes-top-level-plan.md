---
title: "fix: top-level briefing notes json"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level briefing_notes JSON (plan 143)

## Summary

Defer briefing may include checkpoint **`notes`** (e.g. **`queue_backlog_note`**, **`fc_stale_gap_pending_note`**), but top-level gate JSON omits them unless agents drill into **`lfg_agent_briefing`**. Strict exit and watch summary stderr also omit a compact notes signal.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors non-empty **`notes`** to top-level **`briefing_notes`**.
- R2. **`preflight_watch_summary`** JSON includes **`briefing_notes`** on deferred watch end when present.
- R3. **`_emit_lfg_strict_exit_stderr`** appends **`notes=N`** when briefing carries notes.
- R4. Watch summary one-liner includes **`notes=N`** when present.
- R5. Tests; **`PLAN_TRACK_CAP`** 143; closeout doc bullet; plans index **019–143**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`briefing_notes`** when checkpoint notes populate briefing.
- T2. Watch summary JSON includes **`briefing_notes`** when present.
- T3. Strict exit stderr includes **`notes=1`** when briefing has one note.
- T4. Plan patch expects **`019–143`**.
