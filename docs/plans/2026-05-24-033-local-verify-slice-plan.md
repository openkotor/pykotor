---
title: "verify: local pypi regression slice and stale ci cleanup"
type: verify
status: completed
date: 2026-05-24
origin: lfg-local-verify-slice
strategy_track: test-signal-quality
---

# verify: Local PyPI Regression Slice and Stale CI Cleanup

## Summary

GitHub Actions runs remain stuck **queued** (26363113375, 26362905607). Cancel stale runs, re-dispatch Verify PyPI, and run local equivalents of the workflow gate + CLI discovery + core import checks.

## Problem Frame

Runner backlog prevents CI evidence closure. Local vertical slice validates the same paths the workflow exercises without waiting on GitHub queue.

## Requirements

- R1. Cancel stale queued runs 26363113375 and 26362905607.
- R2. Re-dispatch Verify PyPI on master (26363187827).
- R3. Local: `discover_tools.py --cli-only`, core import smoke (repo `uv run` or pip pykotor).
- R4. Record outcomes in plan 031/032 verification rows.

## Verification

| Check | Expected |
|-------|----------|
| Stale runs | cancelled |
| New dispatch | gate job scheduled |
| Local discovery | 3 CLI tools |
| Local core imports | pykotor import smoke pass |

## Scope Boundaries

- Does not modify workflow YAML.
- Full PyPI matrix remains CI-dependent.

## Sources & References

- Dispatch: https://github.com/OpenKotOR/PyKotor/actions/runs/26363187827
- Plan 031: `docs/plans/2026-05-24-031-fix-verify-pypi-empty-run-cancel-plan.md`
