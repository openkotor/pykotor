---
title: "verify: master post-pr266 merge readiness"
type: verify
status: active
date: 2026-05-24
origin: lfg-master-post-merge
strategy_track: test-signal-quality
---

# verify: master post-PR #266 merge readiness

## Summary

PR #266 (TSLPatcher parity harness MVP + CI fixes from plans 001–017) merged to `master` at `35d83a860`. Confirm required CI on master is green; fix only if a required check fails after queue drain.

---

## Problem Frame

Prior LFG slices landed parity harness, pytest/skip fixes, tomli venv install, urllib3/Pillow Py3.8 pins, and KotorMCP `validate_py38` skip. PR #266 is **merged**; this slice verifies master health, not an open PR.

---

## Requirements

- R1. **Python application** passes flake8 + pytest on `master` HEAD.
- R2. TSLPatcher parity harness tests pass in CI default slice.
- R3. PR Build Validation tool builds pass (Windows + Ubuntu where applicable).
- R4. Pylint matrix green on Py3.8–3.11.
- R5. No product code changes unless a required check fails.

---

## Scope Boundaries

- Do not reopen PR #266 or duplicate it.
- Do not fix wiki markdown link debt (slow lane).
- Do not refresh TLK ReplaceFile golden test in this slice.

---

## Implementation Units

- U1. **Monitor master CI** on HEAD `35d83a860` (or later if fast-forwarded).

**Goal:** Confirm all required checks pass.

**Requirements:** R1–R4

**Dependencies:** None

**Files:** None (verify-only unless regression)

**Test scenarios:**
- Happy path: `gh run list --branch master` shows success for Python application, Python package matrix, PR Build Validation, Pylint.
- Error path: If a required job fails, diagnose from logs and apply minimal fix per prior plans 011–017 patterns.

**Verification:** Required master CI green on latest HEAD.

- U2. **Fix regressions only if required checks fail**

**Goal:** Minimal targeted fix for any failing required check.

**Requirements:** R5

**Dependencies:** U1 failure signal

**Files:** TBD from failure logs (likely `.github/workflows/`, `scripts/build-tool`, or submodule gitlinks)

**Verification:** Re-run failed job green after fix.

---

## Sources & References

- PR #266 (merged): https://github.com/OpenKotOR/PyKotor/pull/266
- Plans `2026-05-24-001` through `2026-05-24-017`
- Merge commit: `35d83a860`
