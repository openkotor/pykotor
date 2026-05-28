---
title: "verify: finalize post-277 CI and forward-commits dry-run"
type: verify
status: completed
date: 2026-05-24
origin: lfg-ci-evidence-finalize
strategy_track: test-signal-quality
---

# verify: Finalize Post-#277 CI and Forward-Commits Dry-Run

## Summary

CI runs remain queued/pending on GitHub runner backlog. Supplement with local forward-commits dry-run on `origin/bleeding-edge` and poll manual Verify PyPI dispatch for final evidence.

## Problem Frame

Runs 26362905607 (Forward Commits) and 26362999987 (Verify PyPI manual) have not started jobs. Plan 029 recorded URLs but not outcomes.

## Requirements

- R1. Local dry-run cherry-pick of `bf8656653` onto `origin/bleeding-edge` using #277 script logic.
- R2. Local `discover_tools.py --cli-only` smoke test.
- R3. Poll Verify PyPI run 26362999987; record conclusion if available.
- R4. Update plans 028/029 verification tables with dry-run + CI status.

## Verification

| Check | Expected |
|-------|----------|
| FC dry-run | cherry-pick + workflow restore succeeds |
| Local discovery | 3 CLI tools |
| Verify PyPI 26362999987 | success, failure, or still pending with note |

## Scope Boundaries

- No workflow YAML changes unless dry-run exposes a script bug.
- Does not force-push bleeding-edge.

## Sources & References

- FC run: https://github.com/OpenKotOR/PyKotor/actions/runs/26362905607
- Verify run: https://github.com/OpenKotOR/PyKotor/actions/runs/26362999987
- Plan 028: `docs/plans/2026-05-24-028-fix-forward-commits-invalid-permissions-plan.md`
