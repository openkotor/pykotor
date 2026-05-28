---
title: "feat: enrich preflight doc validation and checkpoint snippet"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: Enrich Preflight Doc Validation + Snippet (plan 069)

## Gaps

- G1. `--validate-checkpoint-doc` is a separate command from `--monitor-preflight`; agents need two gh calls for full gate context.
- G2. `_validate_checkpoint_doc` only compares run IDs — oversimplified; Last CI check text can drift on status/conclusion while IDs match.
- G3. `_format_checkpoint_snippet` prints `status` even when run is terminal; should prefer `conclusion` when present.
- G4. Solution doc plans index stops at 066; missing 067–068 tooling notes (`emit-checkpoint-snippet`, `fc_sha_stale_benign`, validate).
- G5. Human `_print_ci_status` omits `fc_sha_stale_benign` when printing checkpoint notes.

## Requirements

- R1. When `--compare-checkpoint`, embed `doc_validation` from `_validate_checkpoint_doc` in CI status JSON.
- R2. Extend validation with `status_drift` when parsed Last CI check bold status words disagree with live run state (terminal conclusion vs active status word).
- R3. Snippet uses conclusion when terminal, else status.
- R4. Update `docs/solutions/testing/verify-pypi-regression-closeout.md` Prefer/Agent sections for plans 067–069.
- R5. Optional `--include-checkpoint-snippet` adds `checkpoint_snippet` string to JSON (with compare-checkpoint).
- R6. Unit tests for status drift, snippet conclusion, embedded doc_validation.

## Test scenarios

- T1. `_validate_checkpoint_doc` reports `status_drift` when doc says **queued** but live conclusion is success.
- T2. Snippet shows **success** when verify conclusion is success.
- T3. `_ci_status(compare_checkpoint=True)` JSON includes `doc_validation`.
- T4. `--include-checkpoint-snippet` adds non-empty `checkpoint_snippet` key.
