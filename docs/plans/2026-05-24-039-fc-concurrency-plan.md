---
title: "fix: forward-commits concurrency deduplication"
type: fix
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# fix: Forward Commits Concurrency Deduplication

## Summary

Two Forward Commits runs ([26363511361](https://github.com/OpenKotOR/PyKotor/actions/runs/26363511361) push, [26363563890](https://github.com/OpenKotOR/PyKotor/actions/runs/26363563890) dispatch) queue duplicate cherry-picks on `master` with no concurrency group. Add `concurrency` to `.github/workflows/commit-all-to-bleeding-edge.yml`, cancel the superseded push run, and record evidence in plan 020/039.

## Problem Frame

FC lacks concurrency (unlike verify-pypi and auto-publish). Push + manual dispatch from plan 038 doubled queue load during runner backlog.

## Requirements

- R1. Add `concurrency` group `forward-commits-${{ github.ref }}` with `cancel-in-progress: true`.
- R2. Cancel superseded FC push run 26363511361; retain dispatch 26363563890 until merge retriggers.
- R3. Local FC dry-run on master tip passes.
- R4. Update plan 020 FC row; mark plan 039 completed.

## Implementation Units

- U1. `.github/workflows/commit-all-to-bleeding-edge.yml` — add concurrency block.
- U2. Docs — plans 020, 039 verification.

## Test Scenarios

| ID | Scenario | Expected |
|----|----------|----------|
| T1 | YAML concurrency | group + cancel-in-progress true |
| T2 | Cancel duplicate push FC | 26363511361 cancelled |
| T3 | Local FC dry-run | pass |

## Verification

| Check | Evidence | Result |
|-------|----------|--------|
| Concurrency | `forward-commits-${{ github.ref }}`, cancel-in-progress true | ✅ pass |
| Duplicate FC cancelled | 26363511361 | ✅ pass |
| Retained dispatch FC | [26363563890](https://github.com/OpenKotOR/PyKotor/actions/runs/26363563890) | ⏳ queued |
| Local FC dry-run | cherry-pick dec787622 + workflow restore | ✅ pass |
| Local discovery | 3 CLI tools | ✅ pass |
| Post-merge FC | triggered by `.github/workflows` push | ⏳ pending merge |

## Scope Boundaries

- Does not change cherry-pick logic.
- Verify PyPI unchanged.

## Sources & References

- Duplicate runs: 26363511361, 26363563890
- Auto-publish pattern: `.github/workflows/publish-pypi-auto.yml`
- Plan 038: `docs/plans/2026-05-24-038-post-286-fc-evidence-plan.md`
