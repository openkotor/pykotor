---
title: "refactor: relocate _mirror_lfg_flat_fields"
type: refactor
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# refactor: Relocate `_mirror_lfg_flat_fields` (plan 186)

## Summary

Move **`_mirror_lfg_flat_fields`** from the preflight-watch section to the shared **`_mirror_*`** helper cluster (after **`_mirror_briefing_notes`**) so flat-field mirroring sits with queue/briefing mirror helpers it delegates to.

---

## Requirements

- R1. No behavior change — pure relocation.
- R2. **`PLAN_TRACK_CAP`** 186; closeout index **019–186**.
- R3. Existing mirror tests still pass.

---

## Test scenarios

- T1. **`test_mirror_lfg_flat_fields_from_briefing`** unchanged behavior.
- T2. Plan patch expects **`019–186`**.
