---
title: "feat: prefetch recompare and pr merge readiness"
type: feat
status: completed
date: 2026-05-24
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: Prefetch Recompare + PR Merge Readiness (plan 083)

## Summary

Complete deferred prefetch re-classify from plan 082, route classify hints to `--prefetch-git`, and embed open-PR merge readiness when `lfg_track_complete`.

---

## Problem Frame

Track reports `monitoring_complete` but agents lack merge guidance for the open feature PR. `--prefetch-git` fetches without re-comparing checkpoint when `classify_fc_stale_gap` persists. Blocked hint still says manual git fetch instead of `--prefetch-git`.

---

## Requirements

- R1. After prefetch, re-run `_compare_checkpoint` + `_validate_checkpoint_doc` + `_refine_lfg_checkpoint`.
- R2. `classify_fc_stale_gap` blocked hint recommends `--prefetch-git --lfg-gate`.
- R3. When `lfg_track_complete`, embed `pr_merge_status` from `gh pr view` (number, url, mergeable, check summary).
- R4. Stderr message on `--lfg-gate` when track complete.
- R5. Tests; bump `PLAN_TRACK_CAP` to `083`; update solution doc agent loop step 6.

---

## Scope Boundaries

- Does not merge PR #308 automatically.
- No workflow YAML changes.

---

## Test scenarios

- T1. prefetch recompare updates checkpoint after mock fetch.
- T2. classify hint contains `--prefetch-git`.
- T3. pr_merge_status embedded when track complete (mocked gh).
