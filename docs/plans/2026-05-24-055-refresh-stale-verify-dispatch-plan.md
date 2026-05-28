---
title: "verify: refresh stale verify dispatch and sync fc evidence"
type: verify
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# verify: Refresh Stale Verify Dispatch and Sync FC Evidence

## Summary

Monitoring-only track (plan 051). Verify [26364992933](https://github.com/OpenKotOR/PyKotor/actions/runs/26364992933) remains queued on stale SHA `4881930aa` while master is `9facd78fd`. FC canonical run is [26365415666](https://github.com/OpenKotOR/PyKotor/actions/runs/26365415666). Cancel stale verify; dispatch on master tip; sync plan 020 and solution doc.

## Problem Frame

`--ci-status-only` shows verify SHA drift. `test-cli-tools` checkout would not reflect #297–#303. Solution doc allows cancel/dispatch on stale SHA; plan 051 avoids loops—this is SHA drift, not a repeat no-op slice.

## Requirements

- R1. Cancel verify 26364992933; `workflow_dispatch` on master.
- R2. Confirm new run has Check trigger queued on `9facd78fd`.
- R3. Update plan 020 + solution doc FC URL → 26365415666.
- R4. `--ci-status-only --json` after dispatch.
- R5. No workflow YAML changes; mark plan 055 completed.

## Implementation Units

- U1. **CI hygiene** — cancel + dispatch.
- U2. **Docs** — plan 020, solution doc, plan 055.

## Verification

| Check | Expected | Result |
|-------|----------|--------|
| Stale verify cancelled | 26364992933 | ✅ cancelled |
| Fresh verify | Check trigger on `9facd78fd` | ✅ [26365458400](https://github.com/OpenKotOR/PyKotor/actions/runs/26365458400) |
| FC URL | 26365415666 | ✅ plan 020 updated |
| YAML | unchanged | ✅ no workflow edits |

## Scope Boundaries

- Does not wait for runner backlog.
- FC run not re-dispatched (already on tip).

## Sources & References

- Plan 054: `--ci-status-only`
- Solution: stale SHA cancel guidance
