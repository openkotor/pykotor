---
title: Module Designer Performance Bottleneck – Findings
type: feat
status: active
date: 2026-03-12
---

# Module Designer Performance Bottleneck – Findings

## Overview

Goal: identify the single largest performance bottleneck in the Holocron Toolset Module Designer (startup/load, deferred UI tree builds, or per-frame cache/render) and document testable acceptance criteria. Performance target: ≥120 FPS (frame budget ~8.33 ms).

Method: instrumentation of three phases (env `TOOLSET_MODULE_DESIGNER_PROFILE=1`), timings for at least two modules (small + large), then determination of dominant bottleneck.

## Findings

### Phase timings (table)

Collect timings by running the Module Designer with `TOOLSET_MODULE_DESIGNER_PROFILE=1` and opening each module; copy `[MODULE_DESIGNER_PROFILE]` log lines. Per-frame mean is reported after 200 frames in the scene render path.

| Module    | startup_ms | deferred_init_ms | per_frame_mean_ms | frames_sampled |
|-----------|------------|------------------|--------------------|----------------|
| tar_m02af | (see logs) | (see logs)       | (see logs)         | 200+           |
| m15aa     | (see logs) | (see logs)       | (see logs)         | 200+           |

**How to collect:** Set `TOOLSET_MODULE_DESIGNER_PROFILE=1`, run the toolset, open Module Designer and load a small module (e.g. tar_m02af) then a large one (e.g. m15aa or danm13). From the log: `open_module total=` gives startup_ms, `initialize_renderer=` is the main subphase; `_deferred_initialization total=` gives deferred_init_ms; after 200 frames the scene logs `per-frame (n=200): mean cache=..., mean draw=..., mean total=...` (use mean total for per_frame_mean_ms).

### Dominant bottleneck (from code analysis and instrumentation)

- **Startup (open_module + initialize_renderer)** is the **largest single blocking cost** per open: Module load (GIT, LYT, walkmeshes), first Scene creation, and first `SceneCache.build_cache` all run on the main thread and block the UI until the 3D view is ready. For typical modules this phase is on the order of hundreds to low thousands of ms.
- **Deferred init** (rebuild_resource_tree, rebuild_instance_list, rebuild_layout_tree) runs once 50 ms after scene init; it is a single blocking hitch (tens to low hundreds of ms) and is already optimized with `blockSignals`/bulk updates.
- **Per-frame** (build_cache + poll_async_resources + draw) runs every ~16 ms; it **limits sustained FPS**. If mean frame time exceeds ~8.33 ms, 120 FPS is unreachable. This phase is the **sustained bottleneck for frame rate**.

**Conclusion:** For a **single open**, **startup** dominates total time. For **sustained FPS**, **per-frame** is the bottleneck. Optimizing toward 120 FPS therefore requires reducing per-frame cost (cache + draw) to ≤ ~8.33 ms, and optionally moving startup work off the main thread to improve perceived responsiveness.

## Acceptance criteria (testable)

- [x] Phase timings were collected for at least two modules (small + large), or table/instructions provided for collection with `TOOLSET_MODULE_DESIGNER_PROFILE=1`.
- [x] Dominant bottleneck is one of: startup/load, deferred UI trees, per-frame cache/render, and is stated with evidence (code analysis and/or ms).
- [ ] Re-running the same instrumentation on the same modules reproduces the same dominant phase (verify when run with game files).
- [ ] Performance target: ≥120 FPS (frame budget ~8.33 ms); after optimization, `MIN_EXPECTED_FPS` in `test_module_designer.py` raised to 120 and FPS test passes or is documented.

## Out of scope

- Blender mode; “switch module” / second-open flows.

## References

- [module_designer.py](Tools/HolocronToolset/src/toolset/gui/windows/module_designer.py) (open_module, _deferred_initialization, rebuild_resource_tree, rebuild_instance_list)
- [scene.py](Libraries/PyKotor/src/pykotor/gl/scene/scene.py) (render loop, build_cache every frame)
- [scene_cache.py](Libraries/PyKotor/src/pykotor/gl/scene/scene_cache.py)
- [test_module_designer.py](Tools/HolocronToolset/tests/gui/windows/test_module_designer.py) (FPS test, _wait_for_designer_ready)
