---
title: "fix: land forward-commits workflows permission (PR #273)"
type: fix
status: completed
date: 2026-05-24
origin: lfg-post-pypi-closeout
strategy_track: test-signal-quality
---

# fix: Land Forward-Commits Workflows Permission (PR #273)

## Summary

PR #273 adds `workflows: write` to `.github/workflows/commit-all-to-bleeding-edge.yml` so Forward Commits can push cherry-picks that touch workflow files. Master advanced with #275/#276; rebase #273 and close duplicate PR #274 (superseded by merged #275).

## Problem Frame

Forward Commits run 26361732290 failed on workflow push permission after bleeding-edge `.gitmodules` was fixed. PR #273 is MERGEABLE but based on pre-#275 master.

## Requirements

- R1. Rebase `fix/forward-commits-workflows-permission` onto current `origin/master`.
- R2. Confirm one-line YAML change intact: `workflows: write` under `permissions`.
- R3. Close PR #274 as superseded by merged PR #275 (duplicate concurrency fix).
- R4. Push branch; PR #273 remains MERGEABLE.

## Implementation Units

- U1. Rebase branch onto `origin/master`; resolve conflicts if any.
- U2. Update plan 021 post-merge note if rebase changes verification context.
- U3. `gh pr close 274 --comment` documenting supersession by #275.

## Verification

| Check | Expected |
|-------|----------|
| `gh pr view 273 --json mergeable` | `MERGEABLE` |
| Diff vs master | only workflow permission + plan docs |
| PR #274 | `CLOSED` |

## Scope Boundaries

- Does not merge PR #273 (await CI/user).
- Does not modify product code.

## Sources & References

- PR #273: https://github.com/OpenKotOR/PyKotor/pull/273
- PR #274: https://github.com/OpenKotOR/PyKotor/pull/274
- PR #275: https://github.com/OpenKotOR/PyKotor/pull/275
- Plan 021: `docs/plans/2026-05-24-021-fix-forward-commits-workflows-permission-plan.md`
