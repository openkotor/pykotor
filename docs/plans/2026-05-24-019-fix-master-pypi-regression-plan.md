---
title: "fix: master Verify PyPI Regression CLI discovery"
type: fix
status: active
date: 2026-05-24
origin: lfg-master-pypi-regression
strategy_track: test-signal-quality
---

# fix: master Verify PyPI Regression CLI discovery

## Summary

`Verify PyPI Regression` failed on master @ `35d83a860` because the `test-cli-tools` job checks out without submodules and runs `discover_tools.py` without `tomli` on Python 3.10. Tools live in git submodules; empty checkouts yield zero CLI tools.

---

## Problem Frame

- Run `26360919633`: `CLI Tools - Python 3.11` → `Error: No tools discovered`
- Run `26360919633`: `CLI Tools - Python 3.10` → `tomllib (or tomli on Python <3.11) is required`
- Other workflows (`ci.yml`, `publish-pypi-auto.yml`) already use `submodules: recursive`.

---

## Requirements

- R1. Checkout tool submodules before `discover_tools.py` in verify workflow.
- R2. Ensure TOML parser available on Python 3.10 discovery step.
- R3. Minimal diff; no product code changes.

---

## Implementation Units

- U1. **Workflow fix** — `.github/workflows/verify-pypi-regression.yml`
  - Add `submodules: recursive` to checkout in `test-cli-tools`.
  - `pip install tomli` before discovery (Py3.10 matrix).
- U2. **Verify** — push fix branch; confirm `Verify PyPI Regression` CLI jobs pass.

---

## Sources

- Failed run: https://github.com/OpenKotOR/PyKotor/actions/runs/26360919633
- Merge commit: `35d83a860`
