---
title: "feat: fc docs-only stale benign and checkpoint validate"
type: feat
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# feat: FC Docs-Only Stale Benign + Checkpoint Validate (plan 068)

## Gaps

- G1. `fc_sha_stale` always warns even when master-only commits are docs-only (FC paths-ignore).
- G2. `_format_checkpoint_snippet` hardcodes `2026-05-24`.
- G3. `_git_origin_master_sha` fails without fetched `origin/master`.
- G4. No way to detect solution doc drift vs live CI without manual diff.

## Requirements

- R1. `_commits_since_are_docs_only(base, head)` — true when all commits touch only `docs/**`.
- R2. When `fc_sha_stale` and docs-only gap, set `fc_sha_stale_benign: true` with clear note.
- R3. Snippet uses `date.today().isoformat()`.
- R4. Master SHA: try `origin/master` then `master`.
- R5. `--validate-checkpoint-doc` reports doc vs live run ID drift.
- R6. Tests for docs-only helper and validate flag.
