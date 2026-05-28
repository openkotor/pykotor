---
title: "feat: local verify-pypi regression script"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: Local Verify-PyPI Regression Script

## Summary

Plans 041–047 repeatedly ran the same manual local steps while CI [26364756399](https://github.com/OpenKotOR/PyKotor/actions/runs/26364756399) and FC [26364669571](https://github.com/OpenKotOR/PyKotor/actions/runs/26364669571) stay queued. Add `.github/scripts/local_verify_pypi_slice.py` mirroring `verify-pypi-regression.yml` published-package checks so agents and developers can run one command.

## Problem Frame

Manual venv + inline `python -c` blocks are error-prone and duplicated across LFG slices. CI backlog is external; local parity should be one reproducible entry point.

## Requirements

- R1. Script installs `pykotor[all]` from PyPI in an ephemeral venv.
- R2. Script runs workflow-equivalent core and format import checks.
- R3. Script runs discover_tools → pip install → `--help` CLI path with documented skips (kotordiff not on PyPI; `--help` rc≠0).
- R4. Exit 0 on pass/skips; exit 1 on hard failures (imports, discovery).
- R5. Run script locally; document in plan 020; mark plan 048 completed.
- R6. No CI cancel/dispatch.

## Implementation Units

- U1. **Script** — `.github/scripts/local_verify_pypi_slice.py`
- U2. **Docs** — plan 020 usage row, plan 048 verification.

## Verification

| Check | Expected | Result |
|-------|----------|--------|
| `python3 .github/scripts/local_verify_pypi_slice.py` | exit 0 | ✅ pass |
| CI runs | unchanged | ✅ no re-dispatch |

## Scope Boundaries

- Does not replace CI matrix (single OS/Python).
- No workflow YAML changes.

## Sources & References

- Workflow: `.github/workflows/verify-pypi-regression.yml`
- Plan 047: manual vertical slice baseline
