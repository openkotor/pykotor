---
title: "refactor: resolve preflight watch summary counters from history"
type: refactor
status: active
date: 2026-05-29
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# refactor: Resolve Preflight Watch Summary Counters (plan 207)

## Summary

Extract **`_resolve_preflight_flat_keys_heartbeats`** and **`_resolve_preflight_unchanged_flat_keys_polls`** to consolidate plan 202/206 history fallback logic used by **`_build_preflight_watch_summary`**.

---

## Requirements

- R1. Heartbeat resolve prefers status counter, then history max **`flat_hb_total`**.
- R2. Unchanged resolve prefers pairwise count, then max streak fallback.
- R3. No behavior change; tests; **`PLAN_TRACK_CAP`** 207; index **019–207**.

---

## Test scenarios

- T1. Resolve helpers unit tests for status/count preference and fallbacks.
- T2. Existing summary tests still pass.
- T3. Plan patch expects **`019–207`**.
