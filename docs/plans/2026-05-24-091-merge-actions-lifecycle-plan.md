---
title: "feat: merge actions and pr lifecycle states"
type: feat
status: active
date: 2026-05-24
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: Merge Actions + PR Lifecycle States (plan 091)

## Summary

Add structured `merge_actions`, `next_pending_check`, and handle PR `MERGED`/`CLOSED` states in merge gate rollup.

---

## Problem Frame

Agents parse long `merge_hint` strings for gh commands. No pointer to the next pending job URL. Merged/closed PRs fall through to generic hints.

---

## Requirements

- R1. `merge_actions` object with watch/failed/merge gh commands when track complete.
- R2. `next_pending_check` from first pending detail (name + details_url).
- R3. PR state `MERGED`/`CLOSED` sets `lfg_merge_blocked` and specific hints.
- R4. Watch stops on merged/closed; strict exit **3**.
- R5. Tests; bump `PLAN_TRACK_CAP` to `091`; update docs.

---

## Scope Boundaries

- Does not run gh commands automatically.
- No workflow YAML changes.

---

## Test scenarios

- T1. merge_actions includes watch command with PR number.
- T2. MERGED state sets pr_merged blocked.
- T3. next_pending_check populated from details.
