---
title: "fix: merge forward-commits and verify closeout PRs"
type: fix
status: completed
date: 2026-05-24
origin: lfg-pypi-track-merge
strategy_track: test-signal-quality
---

# fix: Merge Forward-Commits and Verify Closeout PRs

## Summary

Merged PRs #273 and #270 to `master`. Post-merge Forward Commits failed because `workflows: write` is invalid in workflow YAML permissions — follow-up in plan 028.

## Verification (landed)

| Check | Evidence | Result |
|-------|----------|--------|
| PR #273 merged | `f41094d9f` | ✅ merged 2026-05-24 |
| PR #270 merged | `3928a5014` | ✅ merged 2026-05-24 |
| Forward Commits post-#273 | run 26362844673 | ❌ invalid workflow YAML (`workflows` permission) |
| Follow-up | plan 028 | ⏳ in progress |
