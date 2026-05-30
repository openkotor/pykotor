---
title: "refactor: co-locate preflight flat stderr helpers and reuse interval resolver"
type: refactor
status: active
date: 2026-05-29
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# refactor: Co-locate Flat Stderr Helpers and Reuse Interval Resolver (plan 208)

## Summary

Co-locate **`_preflight_watch_poll_flat_stderr_parts`** with **`_preflight_watch_summary_flat_stderr_parts`**, and have the summary helper reuse **`_preflight_watch_heartbeat_interval`** for **`heartbeat_every=`** tokens.

---

## Requirements

- R1. Poll and summary flat stderr helpers are adjacent.
- R2. Summary flat stderr uses **`_preflight_watch_heartbeat_interval`** (no inline duplicate).
- R3. No behavior change; tests; **`PLAN_TRACK_CAP`** 208; index **019–208**.

---

## Test scenarios

- T1. Summary flat stderr resolves **`heartbeat_every`** from **`watch_heartbeat_polls`** alias.
- T2. Existing poll/summary stderr tests pass.
- T3. Plan patch expects **`019–208`**.
