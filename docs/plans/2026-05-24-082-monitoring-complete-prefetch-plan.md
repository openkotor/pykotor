---
title: "feat: monitoring complete gate and git prefetch"
type: feat
status: completed
date: 2026-05-24
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: Monitoring Complete Gate + Git Prefetch (plan 082)

## Summary

Stop false-positive `update_monitoring_docs` proceed signals when docs already match live gh and closeout would noop. Add `--prefetch-git` to reduce `classify_fc_stale_gap` blocked states.

---

## Problem Frame

Live `--lfg-gate` reports `lfg_proceed: true` with `proceed_hint: --lfg-closeout` while `doc_validation.doc_valid` is true and `--lfg-closeout` has `would_write: false`. Agents loop on noop closeouts. `classify_fc_stale_gap` remains manual despite hint text mentioning git fetch.

---

## Requirements

- R1. After checkpoint + doc_validation, refine terminal `update_monitoring_docs` to `monitoring_complete` when doc patch would not change files.
- R2. JSON emits `lfg_track_complete: true`; skip `lfg_proceed` for `monitoring_complete`.
- R3. `proceed_hint` for `monitoring_complete` states track complete (no closeout).
- R4. `--prefetch-git` runs `git fetch origin master` before gh compare; embed `git_prefetch` result in JSON when flag set.
- R5. Retry `_commits_since_are_docs_only` classification after successful prefetch when previously None.
- R6. Tests; bump `PLAN_TRACK_CAP` to `082`; update solution doc agent loop.

---

## Scope Boundaries

- No workflow YAML changes.
- No PR #308 merge in this plan.

---

## Implementation Units

- U1. `_doc_patch_would_change`, `_refine_lfg_checkpoint`, monitoring_complete routing
- U2. `--prefetch-git` + optional re-classify after fetch
- U3. Tests and docs

---

## Test scenarios

- T1. doc_valid + noop patch → `monitoring_complete`, `lfg_track_complete: true`.
- T2. `--prefetch-git` invokes fetch helper (mocked).
- T3. proceed_hint for monitoring_complete excludes `--lfg-closeout`.
