---
title: "test: unit tests for checkpoint compare"
type: test
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# test: Unit Tests for Checkpoint Parse (plan 060)

## Summary

Monitoring checkpoint unchanged (`defer_lfg_pr: true`); PR #308 open. Harden plan 059 `--compare-checkpoint` with unit tests for solution-doc parsing and defer logic—no monitoring docs PR or CI dispatch.

## Problem Frame

Checkpoint parsing is regex-based with no tests; regressions would break LFG defer automation silently.

## Requirements

- R1. Unit tests for `_last_ci_check_section`, `_parse_solution_checkpoint_run_ids`, `_compare_checkpoint` using temp fixture markdown.
- R2. Tests run via `python3 -m unittest` without `gh` or PyPI venv.
- R3. Append to open PR #308; no new monitoring-only PR.
- R4. Mark plan 060 completed when tests pass.

## Implementation Units

- U1. **Tests** — `Libraries/PyKotor/tests/test_utility/test_local_verify_checkpoint.py`
- U2. **Plan status** — completed after verification.

## Test Scenarios

| Scenario | Expected |
|----------|----------|
| Valid Last CI check section | verify + FC run IDs parsed |
| Missing section | error dict |
| IDs match + both queued | `defer_lfg_pr: true` |
| IDs match + verify completed | `defer_lfg_pr: false` |
| Run ID drift | `defer_lfg_pr: false` |

## Scope Boundaries

- No solution doc or plan 020 update (CI still queued).
- No workflow YAML changes.

## Sources & References

- Plan 059, PR #308
- `.github/scripts/local_verify_pypi_slice.py`
