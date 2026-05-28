---
title: "feat: include-proceed-actions and post-dispatch doc sync"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: Include Proceed Actions + Post-Dispatch Doc Sync (plan 075)

## Gaps

- G1. Agents must pass `--auto-apply-on-proceed` and `--dispatch-on-proceed` separately to preview all eligible LFG actions.
- G2. After `--execute` dispatch, docs still reference stale run IDs until a manual second preflight + apply.
- G3. Doc apply is blocked on dispatch paths because `proceed_reason` is not auto-apply eligible and runs may still be queued.
- G4. AGENTS.md dispatch paragraph was not committed with plan 074.

## Requirements

- R1. `--include-proceed-actions` embeds both `doc_apply` and `dispatch_on_proceed` dry-runs when each is eligible.
- R2. `--sync-docs-after-dispatch` with `--dispatch-on-proceed --execute` re-fetches gh runs and adds `post_dispatch_refresh` to JSON.
- R3. Allow doc apply with reason `post_dispatch_run_refresh` when run ID changed after successful dispatch.
- R4. `--sync-docs-after-dispatch --write` persists doc updates after refresh.
- R5. `--write` accepts `--sync-docs-after-dispatch` as a write source.
- R6. Unit tests; bump `PLAN_TRACK_CAP` to `075`.

## Test scenarios

- T1. Include-proceed-actions embeds both previews on terminal + stale verify mock.
- T2. Post-dispatch refresh detects run_id change and allows apply.
- T3. Apply blocked when run_id unchanged after dispatch.
- T4. CLI parser accepts `--include-proceed-actions`.
