---
title: "verify: sync ci canonical run evidence post-293"
type: verify
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# verify: Sync CI Canonical Run Evidence Post-#293

## Summary

Plans 043–044 landed verify trigger fixes on master (`855b099ff`). Plan 020 still references superseded FC run 26363668835. Sync canonical run URLs (FC 26364669571, verify 26364391944), confirm local smoke, and record plan 044 dispatch as code-landed but not yet exercised by a publish run.

## Problem Frame

Track closeout is code-complete; CI remains queued on GitHub runners. Evidence tables drift when concurrency supersedes runs without doc updates.

## Requirements

- R1. Update plan 020 FC row to [26364669571](https://github.com/OpenKotOR/PyKotor/actions/runs/26364669571).
- R2. Note verify [26364391944](https://github.com/OpenKotOR/PyKotor/actions/runs/26364391944) unchanged (no re-dispatch).
- R3. Add plan 044 dispatch hook status: landed #293, awaits next Auto-Publish with packages.
- R4. Local discover + core import smoke pass.
- R5. Mark plan 045 completed; no workflow YAML changes.

## Implementation Units

- U1. **Docs** — plan 020, 045 verification.
- U2. **Local smoke** — discover_tools + PYTHONPATH core import.

## Verification

| Check | Expected | Result |
|-------|----------|--------|
| Plan 020 FC URL | 26364669571 | ✅ updated |
| Local smoke | pass | ✅ discover (3 CLIs) + `import pykotor` |
| No CI re-dispatch | unchanged | ✅ no workflow edits |

## Scope Boundaries

- Does not cancel or re-dispatch CI runs.
- Does not wait for runner backlog.

## Sources & References

- FC: https://github.com/OpenKotOR/PyKotor/actions/runs/26364669571
- Verify: https://github.com/OpenKotOR/PyKotor/actions/runs/26364391944
- Plan 044: `docs/plans/2026-05-24-044-dispatch-verify-after-publish-plan.md`
