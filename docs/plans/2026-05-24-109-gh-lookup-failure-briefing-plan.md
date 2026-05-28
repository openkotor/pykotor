---
title: "fix: agent briefing for gh lookup failures"
type: fix
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Agent Briefing for GH Lookup Failures (plan 109)

## Summary

When `gh run list` fails (rate limit, auth, network), preflight sets `fix_gh_lookup` with empty briefing notes and generic `gh_error` exit reason. Agents need **`gh_lookup`** details, classified error kind, and retry-oriented proceed hints.

---

## Problem Frame

Live preflight hit GitHub API rate limit (403). JSON had `gh_ok: false`, `blocked: fix_gh_lookup`, briefing with empty `notes` — no signal to wait vs fix auth.

---

## Requirements

- R1. `_classify_gh_error_message` and `_summarize_gh_lookup` on failed runs.
- R2. Attach `gh_lookup` / `gh_lookup_note` to CI status when `gh_ok` is false.
- R3. `_build_lfg_agent_briefing` returns `gh_unavailable` with error notes when `gh_ok` false.
- R4. Exit **1** `lfg_exit_reason` compounds kind (e.g. `gh_error:rate_limited`).
- R5. `proceed_hint` for rate limit suggests retry `--lfg-preflight`.
- R6. Tests; `PLAN_TRACK_CAP` `109`; closeout + plan 020 docs.

---

## Scope Boundaries

- Does not implement automatic gh retry/backoff.
- Does not change workflow YAML.

---

## Test scenarios

- T1. Rate-limit error string → `primary_kind: rate_limited`.
- T2. Briefing action `gh_unavailable` with truncated error in notes.
- T3. `_compute_lfg_exit_reason` exit 1 → `gh_error:rate_limited`.
- T4. Proceed hint mentions retry for rate limit.
