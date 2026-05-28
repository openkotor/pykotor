---
title: "fix: defer briefing includes active run urls and ids"
type: fix
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Defer Briefing Active Run Refs (plan 112)

## Summary

When deferred waiting on FC (`fc_active_pending` / `fc_active_closeout`), agents get notes but no **`fc_run_url`** or **`fc_run_id`** in `lfg_agent_briefing`. Add structured run refs and stderr reason suffix.

---

## Problem Frame

Live: FC queued; defer briefing notes SHA gap but agents must parse JSON for `forward_commits.url`.

---

## Requirements

- R1. `_attach_active_run_refs` copies active run id/url/status into briefing.
- R2. Defer briefing calls attach helper for verify and FC when active.
- R3. `_emit_lfg_agent_briefing_stderr` includes `reason=` for defer action.
- R4. Tests; `PLAN_TRACK_CAP` `112`; closeout + plan 020 docs.

---

## Test scenarios

- T1. FC queued defer → briefing has `fc_run_id` and `fc_run_url`.
- T2. stderr includes `reason=fc_active_pending`.
- T3. Verify active defer includes `verify_run_url`.
