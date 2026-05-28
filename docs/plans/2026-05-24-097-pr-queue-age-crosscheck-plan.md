---
title: "feat: pr queue age and checks crosscheck"
type: feat
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: PR Queue Age + Checks Crosscheck (plan 097)

## Summary

When PR CI is queue-saturated, agents need **how long** checks have waited and a **rollup vs gh pr checks** count crosscheck to interpret backlog severity.

---

## Problem Frame

PR #308 shows 26 queued / 0 in progress with no age signal. Rollup (27) vs `gh pr checks` (25) counts differ with no JSON explanation.

---

## Requirements

- R1. `pr_ci_bottlenecks.oldest_queued_started_at` and `oldest_queued_age_hours` from earliest rollup `started_at`.
- R2. `pr_checks_crosscheck` on gate JSON: gh total, rollup total, state counts, delta (best-effort; non-fatal on gh error).
- R3. Queue-backlog `merge_hint` mentions runner backlog and oldest queued age when known.
- R4. Tests; bump `PLAN_TRACK_CAP` to `097`; update docs.

---

## Scope Boundaries

- Does not replace rollup as primary source of truth.
- No workflow YAML changes.

---

## Test scenarios

- T1. Oldest queued age computed from started_at timestamps.
- T2. Crosscheck JSON when gh pr checks succeeds.
- T3. merge_hint includes backlog age when queue_backlog.
