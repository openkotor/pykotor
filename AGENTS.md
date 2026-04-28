# AGENTS.md

## Cursor Cloud specific instructions

### Overview

PyKotor is a pure-Python monorepo for modding Knights of the Old Republic I & II. It uses **uv** as the package manager with a workspace defined in the root `pyproject.toml`. Minimum supported Python is 3.8; local development may use 3.13 (per `.python-version`). See `README.md` and `CONTRIBUTING.md` for standard commands.

### Running commands

Always use `uv run` to execute commands (per `.cursorrules`), e.g. `uv run pytest`, `uv run ruff check .`, `uv run pykotor --help`.

### Lint

```
uv run ruff check .
uv run ruff format --check .
```

Pre-existing lint violations exist; 259 ruff findings are normal on the current codebase.

### Tests

```
QT_QPA_PLATFORM=offscreen uv run pytest --import-mode=importlib -m "not gui and not slow" --timeout=120 \
  --ignore=Libraries/PyKotor/tests/resource/formats/test_mdl_ascii.py \
  --ignore=Libraries/PyKotor/tests/test_utility/test_registry_strict_typing.py
```

**Gotchas:**
- **`--import-mode=importlib` is required on Linux**: Without it, pytest fails with `ModuleNotFoundError: No module named 'resource.formats'` because the test directory `Libraries/PyKotor/tests/resource/` collides with Python's stdlib `resource` module.

### System dependencies (already in snapshot)

Python 3.8–3.13, uv, g++/gfortran (for numpy build), and Qt6/OpenGL/xcb system libraries are pre-installed. The `CXX=g++` env var may be needed when `uv sync` rebuilds numpy from source.

### UI regeneration (convertui)

After changing any `.ui` file under `Tools/HolocronToolset/src/ui/`, run convertui to regenerate Python bindings under `toolset/uic/qtpy/`:

```bash
uv run python Tools/HolocronToolset/src/ui/convertui.py
```

This works after a successful `uv sync --all-packages --all-extras`. **Python 3.8 is the minimum target.** Dependencies are pinned so that on 3.8 the highest version compatible with 3.8 is used (e.g. `numpy>=1.19.0,<1.25`, `requests>=2.23.0,<2.32.5`, PyQt5 on 3.8 with PyQt5-Qt5 constrained to a version that has Windows wheels). On 3.9+ the same packages use `>=` current/min versions (e.g. `numpy>=1.25`, `requests>=2.32.4`). All such splits use `python_version < \"3.9\"` vs `python_version >= \"3.9\"` (and where needed, e.g. Pillow/PyQt6-sip, additional splits for 3.10+). This keeps 3.9–3.13 working with newer releases while 3.8 gets the latest 3.8-compatible versions.

### Git commits

- Proposed git commands must be copy-paste-ready **single-line** commands only. Do not include comments, shell prompts, or wrapped multi-line blocks.
- Use the normal PyKotor root add/commit command when only root-level files changed.
- If a submodule was updated, recommend a single one-line command that commits the PyKotor root changes including the submodule gitlink, then `cd`s into the submodule, runs `git add .`, commits with the same message, pushes when required, and `cd`s back to the PyKotor root.

### Reverse engineering (agdec-http / AgentDecompile)

Use the **MCP server `user-agdec-http`** (also referred to as agdec-http or agdec) to query **Ghidra projects** that already contain analyzed game programs. **KotOR I and II use the Odyssey engine** (Aurora-family file formats are often discussed in docs; engine behavior should still be described as **Odyssey** in KotOR context).

**Program paths are not repo paths.** The strings passed as `program_path` (e.g. `/K1/k1_win_gog_swkotor.exe`, `/TSL/k2_win_gog_aspyr_swkotor2.exe`) name programs **inside the Ghidra server**. Do not treat them as local files—do not `read_file` or `grep` those paths. Align literal spellings with `.cursorrules` and the loaded Ghidra database.

**CLI / MCP outage:** The AgentDecompile repository’s **`USAGE.md`** (CLI for the same backend) is **not** part of this tree. If the MCP is down, use the upstream project’s `USAGE.md` and client docs for a non-MCP path. A copy may live in your local AgentDecompile or AD-PROXY checkout.

**Canonical tools** (MCP tool names match JSON descriptors in Cursor’s `mcps/user-agdec-http/tools/`, e.g. on a developer machine under `.cursor/projects/.../mcps/user-agdec-http/tools/`). As of the last doc sync, these tools exist:

| Group | Tool names |
| --- | --- |
| Search | `search-everything`, `search-strings`, `search-symbols`, `search-code`, `search-constants` |
| Function / flow | `get-function`, `decompile-function`, `get-call-graph`, `get-references` |
| Program / project | `open`, `import-binary`, `get-current-program`, `sync-project`, `list-project-files`, `list-processors`, `list-prompts`, `export` |
| Version control (shared projects) | `checkout-program`, `checkin-program`, `checkout-status`, `resolve-modification-conflict` |
| Annotation & types | `create-label`, `apply-data-type`, `manage-function`, `manage-function-tags`, `manage-comments`, `manage-bookmarks`, `manage-symbols`, `manage-strings`, `manage-structures`, `manage-data-types`, `manage-files` |
| Low-level / bulk | `read-bytes`, `inspect-memory`, `execute-script` |

**Deprecated or non-existent tool names in older docs** (e.g. `list-functions`, `list-exports`, `list-cross-references` as separate MCP tools): prefer **`get-references`** (cross-refs, modes include import/thunk and referrers with decomp), **`search-symbols`**, and **`search-everything`**. If you need a function list, use `search-everything` with an appropriate scope or a small `execute-script` that enumerates functions in Ghidra.

**K1 → TSL (or v.v.) function correspondence:** The bundled prompt *re-bridge-builder* may mention a **`match-function`** tool. There is **no** separate `match-function` tool in the descriptor set. **Cross-program mirroring** is done with **`manage-function`** using **`propagate: true`**, optional **`propagate_program_paths`**, and **`propagate_max_candidates` / `propagate_max_instructions`** to limit work. If propagation is insufficient, use **`execute-script`** (Ghidra script, assign results to `__result__`, set **`timeout`**) to batch-rename, tag, or bookmark on the second binary.

**`execute-script` contract:** Pass Python for Ghidra’s Jython; assign the agent-visible return value to the global **`__result__`**. Set **`program_path`** when the script should treat a specific program as `currentProgram`. See [`helper_scripts/agdec_save_load/README.md`](helper_scripts/agdec_save_load/README.md) for a concrete export example.

**Repo-side maps:** The JSON asset [`vendor/sotor/core/assets/reverse_engineering/k1_tsl_import_map.json`](vendor/sotor/core/assets/reverse_engineering/k1_tsl_import_map.json) (and its `bridgeWorkflow` section) tracks K1/TSL anchors; extend it as analysis progresses. Python parity work often lands under `Libraries/PyKotor` (e.g. extract, savedata); the Rust SotOR core under [`vendor/sotor`](vendor/sotor) shares format and RE metadata. A standalone C# “Andastra” tree is **out of this repo**—treat it as a separate project unless you add it as a submodule; until then, default engine-parity work to **PyKotor + `vendor/sotor`**.

**Second binary (follow-on):** After the main exes are mapped, use **`list-project-files`** (or the Ghidra UI) to pick another image in the same project (e.g. a game DLL) and repeat the K1↔TSL-style verification and annotation loop at a smaller scope.

**Wiki policy:** See [`wiki/reverse_engineering_findings.md`](wiki/reverse_engineering_findings.md) for conceptual engine notes; do not paste long decompilations into the wiki. Dual-address (K1 + TSL) references in code and docs follow `.cursorrules`.
