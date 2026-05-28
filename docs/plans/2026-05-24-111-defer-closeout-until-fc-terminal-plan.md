---
title: "fix: defer closeout until all canonical runs terminal"
type: fix
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Defer Closeout Until All Canonical Runs Terminal (plan 111)

## Summary

When verify is **completed** but FC is still **queued**, `_compare_checkpoint` returns **`update_monitoring_docs`** because `runs_active = verify_active and fc_active` is false. Agents must **defer** closeout until FC reaches terminal status.

---

## Problem Frame

Live: verify success; FC queued ~1h; `fc_sha_stale_benign: true`; preflight hints `--lfg-closeout` prematurely.

---

## Requirements

- R1. Replace `if not runs_active` closeout with `verify_terminal and fc_terminal` gate.
- R2. Defer when either run still active; add `fc_active_closeout_note` / `verify_active_closeout_note`.
- R3. Extend `_resolve_lfg_defer_reason` for closeout defer kinds.
- R4. Surface closeout notes in briefing; proceed hint uses `--lfg-preflight` for FC-active closeout defer.
- R5. Tests; `PLAN_TRACK_CAP` `111`; closeout + plan 020 docs.

---

## Test scenarios

- T1. Verify terminal + FC queued + benign true → defer, not `update_monitoring_docs`.
- T2. Both terminal → still `update_monitoring_docs`.
- T3. Both active → unchanged defer (existing).
- T4. `lfg_defer_reason: fc_active_closeout` when applicable.
