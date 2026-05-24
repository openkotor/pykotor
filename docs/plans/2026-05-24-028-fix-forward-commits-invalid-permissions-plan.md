---
title: "fix: forward-commits invalid permissions and workflow cherry-pick"
type: fix
status: completed
date: 2026-05-24
origin: lfg-forward-commits-post-273
strategy_track: test-signal-quality
---

# fix: Forward Commits Invalid Permissions and Workflow Cherry-Pick

## Summary

PR #273 merged `workflows: write` into `.github/workflows/commit-all-to-bleeding-edge.yml`, but GitHub rejects that key in workflow `permissions` (`Unexpected value 'workflows'`). Forward Commits now fails at workflow parse time. Remove the invalid permission and retain bleeding-edge `.github/workflows` copies when forwarding master commits.

## Problem Frame

Run [26362844673](https://github.com/OpenKotOR/PyKotor/actions/runs/26362844673) failed with invalid workflow YAML. Original push rejection for workflow files cannot be solved via `workflows:` in workflow permissions scope.

## Requirements

- R1. Remove invalid `workflows: write` from forward-commits workflow permissions.
- R2. After cherry-pick, restore `.github/workflows` from pre-cherry-pick `bleeding-edge` HEAD.
- R3. Use `[skip-edge]` on restore commit message to avoid recursive workflow trigger.
- R4. Forward Commits run succeeds on next master push.

## Implementation Units

- U1. `.github/workflows/commit-all-to-bleeding-edge.yml` — fix permissions + cherry-pick script.

## Verification

| Check | Expected |
|-------|----------|
| Workflow YAML valid | no `workflows:` permission key |
| Forward Commits run | success on push |
| bleeding-edge | receives master commits minus workflow file drift |

## Scope Boundaries

- Does not use PAT/secrets for workflow updates on bleeding-edge.
- Does not change verify-pypi-regression workflow logic.

## Sources & References

- Failed run: https://github.com/OpenKotOR/PyKotor/actions/runs/26362844673
- Workflow: `.github/workflows/commit-all-to-bleeding-edge.yml`
