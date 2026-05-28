---
title: "fix: strict-exit stderr without nested briefing"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Strict-Exit Stderr Without Nested Briefing (plan 180)

## Summary

**`_emit_lfg_strict_exit_stderr`** only appended mirror tokens when **`lfg_agent_briefing`** was present. After plans 174–179, top-level flat fields and **`lfg_flat_field_values`** may exist without nested briefing. Emit mirror stderr when flat fields are populated.

---

## Requirements

- R1. **`_should_attach_lfg_mirror_stderr(status)`** true when nested briefing exists or flat-field count **> 0**.
- R2. **`_emit_lfg_strict_exit_stderr`** uses helper instead of briefing-only guard.
- R3. Tests; **`PLAN_TRACK_CAP`** 180; closeout bullet; plans index **019–180**.

---

## Test scenarios

- T1. Strict exit with top-level flat fields, no **`lfg_agent_briefing`** → mirror tokens including **`flat_fields=`**.
- T2. Existing strict-exit briefing tests unchanged.
- T3. Plan patch expects **`019–180`**.
