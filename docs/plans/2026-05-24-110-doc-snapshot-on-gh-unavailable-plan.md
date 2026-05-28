---
title: "fix: doc checkpoint snapshot when gh unavailable"
type: fix
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Doc Checkpoint Snapshot When GH Unavailable (plan 110)

## Summary

When `gh` is rate-limited, agents get `gh_unavailable` but `lfg_refresh_blocked: fix_gh_lookup` and no doc context. Surface **`doc_checkpoint_snapshot`** from the solution doc and normalize blocked state to **`gh_unavailable`**.

---

## Problem Frame

Live preflight: rate limit → briefing notes only gh errors. Doc Last CI check still says FC **queued** on `bcb5586` but agents cannot see it without reading files manually.

---

## Requirements

- R1. `_build_doc_checkpoint_snapshot` from Last CI check + parsed run IDs/status words.
- R2. Attach `doc_checkpoint_snapshot` when `gh_ok` is false.
- R3. `_lfg_refresh_blocked` returns `gh_unavailable` when `gh_ok` false (not `fix_gh_lookup`).
- R4. `gh_unavailable` briefing includes doc last-ci line in notes.
- R5. Tests; `PLAN_TRACK_CAP` `110`; closeout + plan 020 docs.

---

## Scope Boundaries

- Does not skip gh when available.
- Does not auto-refresh docs from snapshot.

---

## Test scenarios

- T1. `gh_ok` false → `lfg_refresh_blocked` is `gh_unavailable`.
- T2. Snapshot includes verify/FC run IDs and last_ci_line.
- T3. Briefing notes include `doc:` prefix line.
- T4. Proceed hint unchanged for rate limit retry.
