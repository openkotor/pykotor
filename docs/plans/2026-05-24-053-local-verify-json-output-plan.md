---
title: "feat: json output for local verify-pypi script"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: JSON Output for Local Verify-PyPI Script

## Summary

Track is monitoring-only; CI [26364992933](https://github.com/OpenKotOR/PyKotor/actions/runs/26364992933) and FC [26365113919](https://github.com/OpenKotOR/PyKotor/actions/runs/26365113919) remain queued. Add `--json` structured output to `local_verify_pypi_slice.py` for agent-friendly automation instead of another evidence-only docs slice.

## Problem Frame

Repeated monitoring LFG passes re-run the same script and parse stdout. Agents need machine-readable pass/skip/fail summary without scraping log lines.

## Requirements

- R1. `--json` flag prints final summary object to stdout (checks + overall status).
- R2. Default human-readable output unchanged.
- R3. Exit 0 on pass/skips; exit 1 on hard failures.
- R4. AGENTS.md documents `--json` option.
- R5. Run script with and without `--json`; mark plan 053 completed.
- R6. No CI cancel/dispatch.

## Implementation Units

- U1. **Script** — collect results; emit JSON when requested.
- U2. **AGENTS.md** — document flag.

## Verification

| Check | Expected | Result |
|-------|----------|--------|
| Default run | exit 0 | ✅ pass |
| `--json` run | valid JSON, exit 0 | ✅ `status: pass` |
| AGENTS.md | `--json` documented | ✅ pass |

## Scope Boundaries

- No workflow YAML changes.
- CI URLs unchanged (still queued).

## Sources & References

- Script: `.github/scripts/local_verify_pypi_slice.py`
- Plan 051: monitoring-only
