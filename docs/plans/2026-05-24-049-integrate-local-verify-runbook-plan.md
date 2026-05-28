---
title: "docs: integrate local verify-pypi script into runbook"
type: docs
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# docs: Integrate Local Verify-PyPI Script into Runbook

## Summary

Plan 048 added `local_verify_pypi_slice.py` but agents still lack a discoverable entry point. Wire the script into AGENTS.md and the verify workflow header; sync plan 020 FC URL to [26364901538](https://github.com/OpenKotOR/PyKotor/actions/runs/26364901538).

## Problem Frame

Repeated LFG slices re-ran manual verify steps before plan 048. Post-048, agents need explicit runbook guidance (use system `python3`, not `uv run`, because workspace resolution pulls unpublished kotordiff).

## Requirements

- R1. AGENTS.md: PyPI verify local parity command + gotcha (system python3).
- R2. Script: `--help` epilog with example.
- R3. `verify-pypi-regression.yml` header comment references local script.
- R4. Plan 020: FC row → 26364901538; CI monitoring updated.
- R5. Run script locally; mark plan 049 completed.

## Implementation Units

- U1. **AGENTS.md** — verify-pypi local parity section.
- U2. **Script + workflow comment** — discoverability.
- U3. **Docs** — plan 020, plan 049 verification.

## Verification

| Check | Expected | Result |
|-------|----------|--------|
| `--help` | usage + example | ✅ pass |
| Script run | exit 0 | ✅ pass |
| AGENTS.md | local verify section | ✅ added |
| FC URL | 26364901538 | ✅ plan 020 updated |

## Scope Boundaries

- No CI cancel/dispatch.
- No workflow behavior changes.

## Sources & References

- Plan 048: `.github/scripts/local_verify_pypi_slice.py`
- AGENTS.md Running commands section
