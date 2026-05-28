---
title: "feat: sha drift and active-run defer semantics"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: SHA Drift and Active-Run Defer Semantics (plan 065)

## Summary

Monitoring gate returns exit 2 but verify dispatch SHA `9facd78fd` lags `origin/master` (`8916e2ffe`). Current defer logic only checks run IDs + both `queued` — oversimplified. Add master SHA drift detection, treat `in_progress` as active, and emit `defer_reason` / `recommended_action`.

## Gaps Addressed

- G1. `defer_lfg_pr` false when verify `head_sha` != `origin/master` (`verify_sha_stale`).
- G2. Defer when run IDs match and runs are active (`queued`/`in_progress`), not terminal.
- G3. JSON: `master_sha`, `verify_sha_stale`, `defer_reason`, `recommended_action`.
- G4. Unit tests; append to PR #308.

## Requirements

- R1. `_git_origin_master_sha()` via `git rev-parse origin/master`.
- R2. `_is_active_run()` for non-terminal workflow runs.
- R3. `defer_lfg_pr` only when IDs match, runs active, not `verify_sha_stale`.
- R4. Tests for stale SHA, in_progress defer, completed no-defer.

## Scope Boundaries

- No automatic `workflow_dispatch` (agent/LFG decides).
- No Last CI check doc update this slice (tooling only).
