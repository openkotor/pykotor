---
title: "fix: master Verify PyPI Regression workflow"
type: fix
status: in_progress
date: 2026-05-24
origin: lfg-master-pypi-blocker
strategy_track: test-signal-quality
---

# fix: Master Verify PyPI Regression

## Summary

Post-merge of PR #266 (`35d83a860`), `Verify PyPI Regression` failed on master. The `test-cli-tools` job could not run `discover_tools.py`: empty tool list on 3.11 (submodules not checked out) and missing `tomli` on 3.10.

## Root cause (run 26360919633)

| Matrix | Error |
|--------|-------|
| Python 3.11 | `Error: No tools discovered` — `Tools/*` are git submodules; checkout without `submodules: recursive` leaves empty dirs |
| Python 3.10 | `tomllib (or tomli on Python <3.11) is required` — `tool_metadata.py` needs `tomli` before discovery |

Core/extension PyPI install jobs passed; only CLI discovery failed.

## Requirements

- R1. `test-cli-tools` checks out submodules before discovery.
- R2. Install `tomli` on Python 3.10 before `discover_tools.py`.
- R3. No product code changes.

## Implementation

- U1. `.github/workflows/verify-pypi-regression.yml`: `submodules: recursive` on checkout; `pip install tomli` step before discovery.

**Fix branch:** `fix/master-pypi-regression` → PR #268

**Verification:** `Verify PyPI Regression` green on PR branch; re-run on master after merge.
