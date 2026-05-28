---
title: "verify: post-286 fc evidence and dispatch validation"
type: verify
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# verify: Post-#286 FC Evidence and Dispatch Validation

## Summary

PR #286 merged `workflow_dispatch` on Forward Commits; post-merge push run [26363511361](https://github.com/OpenKotOR/PyKotor/actions/runs/26363511361) is queued. Superseded FC [26363271048](https://github.com/OpenKotOR/PyKotor/actions/runs/26363271048) still queues. Cancel the stale run, manually dispatch FC to validate `workflow_dispatch`, update plan 020/037 verification rows, and re-run local smoke.

## Problem Frame

Plan 037 verification still says "pending merge" though #286 landed. Plan 020 FC row is stale. Two FC push runs compete in the same queue; only the post-#286 run matters.

## Requirements

- R1. Cancel superseded FC 26363271048.
- R2. `gh workflow run commit-all-to-bleeding-edge.yml --ref master`; confirm **merge** job scheduled.
- R3. Record FC runs 26363511361 + new dispatch ID in plan 020/037/038.
- R4. Local `discover_tools.py --cli-only` and core import smoke pass.
- R5. Mark plan 038 completed; note Verify PyPI 26363420578 status without cancelling (gate queued).

## Implementation Units

- U1. **CI hygiene** — cancel stale FC; manual workflow_dispatch.
- U2. **Docs evidence** — plans 020, 037, 038.

## Test Scenarios

| ID | Scenario | Expected |
|----|----------|----------|
| T1 | Cancel 26363271048 | cancelled |
| T2 | workflow_dispatch FC | merge job queued |
| T3 | Local discovery | 3 tools |

## Verification

| Check | Evidence | Result |
|-------|----------|--------|
| Stale FC 26363271048 | cancelled | ✅ pass |
| Post-#286 FC push | [26363511361](https://github.com/OpenKotOR/PyKotor/actions/runs/26363511361) — merge queued | ✅ pass |
| workflow_dispatch FC | [26363563890](https://github.com/OpenKotOR/PyKotor/actions/runs/26363563890) — merge queued | ✅ pass |
| Verify PyPI | [26363420578](https://github.com/OpenKotOR/PyKotor/actions/runs/26363420578) — Check trigger queued | ⏳ runner backlog |
| Local discovery | holopatcher, kotordiff, kotormcp | ✅ pass |
| Local core imports | pykotor smoke | ✅ pass |
| Plan 020/037 rows | updated | ✅ pass |

## Scope Boundaries

- No workflow YAML changes.
- Full matrix/FC completion deferred to runner backlog.

## Sources & References

- Post-#286 FC: https://github.com/OpenKotOR/PyKotor/actions/runs/26363511361
- Stale FC: https://github.com/OpenKotOR/PyKotor/actions/runs/26363271048
- Verify PyPI: https://github.com/OpenKotOR/PyKotor/actions/runs/26363420578
- Plan 037: `docs/plans/2026-05-24-037-fc-workflow-dispatch-plan.md`
