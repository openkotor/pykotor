---
title: "feat: exit-on-defer for ci-status checkpoint"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: exit-on-defer for ci-status Checkpoint (plan 061)

## Summary

Monitoring checkpoint unchanged (`defer_lfg_pr: true`); PR #308 open with plans 059–060. Add `--exit-on-defer` so agents and LFG can short-circuit when no monitoring work remains—without another docs-only PR.

## Problem Frame

Repeated `/lfg` invocations re-run full pipeline despite `defer_lfg_pr: true`. Agents need an explicit machine/human signal and stable exit semantics.

## Requirements

- R1. `--exit-on-defer` requires `--ci-status-only --compare-checkpoint`.
- R2. When `defer_lfg_pr` is true, JSON includes `lfg_deferred: true` and stderr prints a one-line defer reason.
- R3. Exit 0 when `gh_ok` and deferred (not an error).
- R4. Unit test for defer exit path via subprocess.
- R5. Document in AGENTS.md; append to PR #308.

## Implementation Units

- U1. **Script** — flag, validation, exit path, non-JSON checkpoint line.
- U2. **Tests** — subprocess test in `test_local_verify_checkpoint.py`.
- U3. **AGENTS.md** — `--exit-on-defer` usage.

## Verification

| Check | Expected |
|-------|----------|
| `--ci-status-only --json --compare-checkpoint --exit-on-defer` | `lfg_deferred: true`, exit 0 |
| Without defer (mocked in unit test) | no `lfg_deferred` |

## Scope Boundaries

- No plan 020 / solution doc CI conclusion update (still queued).
- No new PR; extend #308.

## Sources & References

- Plans 056–060, PR #308
- `.github/scripts/local_verify_pypi_slice.py`
