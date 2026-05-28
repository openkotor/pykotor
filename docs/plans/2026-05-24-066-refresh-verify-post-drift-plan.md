---
title: "verify: refresh verify dispatch post-065 drift detection"
type: verify
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# verify: Refresh Verify Dispatch (plan 066)

## Summary

Plan 065 detected `verify_sha_stale: true` (verify on `9facd78fd`, master `8916e2ffe`). Cancel stale verify [26365458400](https://github.com/OpenKotOR/PyKotor/actions/runs/26365458400); dispatch fresh `workflow_dispatch` on master; sync plan 020 + solution doc.

## Requirements

- R1. Cancel verify 26365458400.
- R2. `gh workflow run verify-pypi-regression.yml --ref master`.
- R3. Record new run ID + master SHA in plan 020 and solution doc.
- R4. FC canonical run unchanged unless new run appears.

## Scope Boundaries

- No workflow YAML changes.
