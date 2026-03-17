# PyKotor Monorepo

> A Python library and tooling ecosystem for reading and modifying file formats used by
> [Knights of the Old Republic](https://en.wikipedia.org/wiki/Star_Wars:_Knights_of_the_Old_Republic_(video_game))
> and its [sequel](https://en.wikipedia.org/wiki/Star_Wars_Knights_of_the_Old_Republic_II:_The_Sith_Lords).

[![LGPL-3.0](https://img.shields.io/badge/License-LGPL--3.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-brightgreen)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/GhostScripter-963%20tests-brightgreen)](Tools/HolocronToolset)
[![KotorMCP](https://img.shields.io/badge/KotorMCP-25%20tools-blue)](Tools/KotorMCP)
[![GhostScripter MCP](https://img.shields.io/badge/GhostScripter%20MCP-32%20tools-orange)](Tools/HolocronToolset)

---

## Table of Contents

- [System Architecture](#system-architecture)
  - [Full Monorepo Layout](#full-monorepo-layout)
  - [Ghostworks Pipeline](#ghostworks-pipeline)
  - [MCP Layer — AI Agent Tools](#mcp-layer--ai-agent-tools)
  - [AgentDecompile Integration](#agentdecompile-integration)
  - [Layer Responsibilities](#layer-responsibilities)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Quick Install](#quick-install)
  - [Standard Install](#standard-install)
- [Quick Start](#quick-start)
  - [Using the Library](#using-the-library)
  - [Using the Tools](#using-the-tools)
- [Available Tools](#available-tools)
- [Submodule Overview](#submodule-overview)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## System Architecture

### Full Monorepo Layout

```
PyKotor/                              ← OldRepublicDevs/PyKotor monorepo
│
├── Libraries/
│   └── PyKotor/                      ← Core I/O library (pip install pykotor)
│       └── src/pykotor/
│           ├── extract/              ← Installation / KEY-BIF / ERF / RIM readers
│           ├── resource/formats/     ← GFF, DLG, 2DA, TLK, MDL, … read/write
│           └── tools/                ← High-level helpers (module, creature, path…)
│
├── Tools/
│   ├── HolocronToolset/              ← ★ PRIMARY MODDING IDE (GhostScripter-K1-K2)
│   │   ├── ghostscripter/
│   │   │   ├── core/                 ← Hexagonal domain (services, ports, models)
│   │   │   ├── mcp/                  ← MCP server — 32 tools + AgentDecompile bridge
│   │   │   ├── ui/                   ← PyQt5 IDE (dark theme)
│   │   │   └── ipc/                  ← IPC bridges to GModular / GhostRigger
│   │   ├── tests/                    ← 963 pytest tests
│   │   ├── ROADMAP.md                ← Merge roadmap (HolocronToolset_old → new)
│   │   └── SYSTEMS_DESIGN.md        ← Coupling/cohesion, gap analysis, event bus
│   │
│   ├── HolocronToolset_old/          ← Legacy Qt5 GUI editor (reference only)
│   │   └── src/toolset/              ← 36 format editors; uses PyKotor for I/O
│   │
│   ├── KotorMCP/                     ← Standalone MCP server (25 tools, PyKotor-backed)
│   │   └── src/kotormcp/             ← Pure PyKotor, no GUI, read-mostly
│   │
│   ├── GModular/                     ← 3D module/world editor + REST API
│   ├── GhostScripter-K1-K2/          ← Mirror of HolocronToolset (same repo)
│   ├── HoloPatcher/                  ← Cross-platform TSLPatcher replacement
│   ├── HoloPazaak/                   ← Pazaak mini-game implementation
│   ├── BatchPatcher/                 ← Batch mod-patching utility
│   ├── KotorDiff/                    ← File comparison & patch generator
│   ├── HolocronAI/                   ← AI/ML experiments for KotOR assets
│   └── KitGenerator/                 ← Indoor-kit / tile-set generator
│
└── Libraries/PyKotor/                ← (same as above, uv workspace member)
```

### Ghostworks Pipeline

The **Ghostworks Pipeline** is the Ghostworks-authored three-tool pipeline that sits
alongside the broader monorepo tooling:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         Ghostworks Pipeline                                   │
│                                                                               │
│  ┌─────────────────────────┐   IPC REST   ┌──────────────────────────────┐  │
│  │  HolocronToolset        │ ←──:7002────→ │  GModular                    │  │
│  │  (GhostScripter-K1-K2) │              │  3D module/world editor       │  │
│  │                         │   CB :7003   │  LYT/VIS, walkmesh, MDL      │  │
│  │  MCP Server (32 tools)  │ ←──:7003────  │  REST API                    │  │
│  │  AgentDecompile bridge  │              └──────────────────────────────┘  │
│  │  PyQt5 IDE              │                                                 │
│  │                         │   IPC REST   ┌──────────────────────────────┐  │
│  │  port 5002 (IPC)        │ ←──:5001────→ │  GhostRigger-K1-K2           │  │
│  └─────────────────────────┘              │  MDL/MDX rigging & skinning  │  │
│                                           │  K1↔K2 model porter          │  │
│                                           └──────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘

External clients (Claude Desktop, Cursor, VS Code Copilot, any MCP agent)
  └── stdio / HTTP :6400 / SSE ──→ HolocronToolset MCP server
                               ──→ KotorMCP server (separate process)
```

**Responsibility matrix (Ghostworks Pipeline)**

| Asset class | Owner tool |
|---|---|
| NWScript (.nss/.ncs), DLG, JRL, 2DA, TLK, ERF/MOD/RIM | HolocronToolset |
| Module layout (LYT/VIS), area GIT, walkmesh (WOK/PWK/DWK) | GModular |
| 3D models (MDL/MDX), animations, textures (TPC/TGA) | GhostRigger-K1-K2 |

### MCP Layer — AI Agent Tools

Two complementary MCP servers expose KotOR assets to AI agents:

#### HolocronToolset MCP (32 tools — GhostScripter v2.2)

| Group | Tools |
|---|---|
| Installation & Discovery (5) | `detectInstallations`, `loadInstallation`, `listResources`, `describeResource`, `searchResources` |
| Reading (6) | `readGFF`, `readDLG`, `readTwoDA`, `readTLK`, `readJournal`, `journalOverview` |
| Targeted Lookups (4) | `twoDALookup`, `moduleOverview`, `nwscriptSignature`, `nwscriptCategories` |
| Writing (2) | `writeDLG`, `writeGFF` |
| Analysis & Patching (3) | `compileSummary`, `twoDAChangesINI`, `searchNWScript` |
| Composite Game-Object Accessors (5) | `getResource`, `getQuest`, `getNpc`, `getScript`, `listResType` |
| AgentDecompile Bridge (7) | `agdecStatus`, `binaryAnalyze`, `binaryDecompile`, `binarySearchSymbols`, `binaryListFunctions`, `binaryGetReferences`, `binaryListStrings` |

#### KotorMCP (25 tools — PyKotor-backed)

| Group | Tools |
|---|---|
| Installation (3) | `detectInstallations`, `loadInstallation`, `kotor_installation_info` |
| Discovery (4) | `listResources`, `describeResource`, `kotor_find_resource`, `kotor_search_resources` |
| Game Data (3) | `journalOverview`, `kotor_lookup_2da`, `kotor_lookup_tlk` |
| Modules (3) | `kotor_list_modules`, `kotor_describe_module`, `kotor_module_resources` |
| Archives (2) | `kotor_list_archive`, `kotor_extract_resource` |
| Conversion (3) | `kotor_read_gff`, `kotor_read_2da`, `kotor_read_tlk` |
| References (6) | `kotor_list_references`, `kotor_find_referrers`, `kotor_find_strref_referrers`, `kotor_describe_dlg`, `kotor_describe_jrl`, `kotor_describe_resource_refs` |
| Walkmesh (1) | `kotor_walkmesh_validation_diagram` |

> **Note on tool-name overlap**: Five tools share names between the two MCP servers
> (`detectInstallations`, `loadInstallation`, `listResources`, `describeResource`,
> `journalOverview`).  When running both servers simultaneously, use separate stdio
> transports or distinct HTTP ports to avoid AI routing ambiguity.  Tracked in
> `Tools/HolocronToolset/ROADMAP.md` Phase 3.

### AgentDecompile Integration

GhostScripter's MCP server includes a **Ghidra binary analysis bridge** via
[AgentDecompile](https://github.com/bolabaden/agentdecompile).  This lets AI agents
decompile KotOR engine functions directly from `swkotor.exe` / `swkotor2.exe`.

```
Claude Desktop
  └── MCP stdio ──→ HolocronToolset MCP server (ghostscripter/mcp/server.py)
                        └── binaryDecompile ──→ agdec_bridge.py
                                                  └── HTTP POST JSON-RPC
                                                      ──→ AgentDecompile server
                                                            └── PyGhidra / Ghidra headless
                                                                  └── C pseudocode + SSE
```

**Setup:**

```bash
# 1. Start AgentDecompile (Docker recommended)
docker run -p 8080:8080 bolabaden/agentdecompile

# 2. Set environment variable
export AGDEC_URL=http://localhost:8080

# 3. Start GhostScripter MCP
cd Tools/HolocronToolset
python -m ghostscripter.mcp
```

Available bridge tools: `agdecStatus`, `binaryAnalyze`, `binaryDecompile`,
`binarySearchSymbols`, `binaryListFunctions`, `binaryGetReferences`, `binaryListStrings`.

All bridge tools degrade gracefully if `AGDEC_URL` is not set.

### Layer Responsibilities

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Layer                 │ Location                    │ Imports from         │
│────────────────────────│─────────────────────────────│──────────────────── │
│  ① External Clients    │ Claude, Cursor, VS Code     │ — (MCP protocol)    │
│  ② KotorMCP Server     │ Tools/KotorMCP/             │ pykotor only        │
│  ③ HolocronToolset MCP │ Tools/HolocronToolset/mcp/  │ core.services       │
│  ④ Core Domain         │ …/ghostscripter/core/       │ stdlib, dataclasses │
│  ⑤ AgentDecompile Br.  │ …/mcp/agdec_bridge.py      │ httpx (async)       │
│  ⑥ GUI (IDE)           │ …/ghostscripter/ui/         │ core.services       │
│  ⑦ IPC Bridges         │ …/ghostscripter/ipc/        │ requests, flask     │
│  ⑧ PyKotor Library     │ Libraries/PyKotor/          │ stdlib, struct      │
│  ⑨ Game Data (disk)    │ K1_PATH / K2_PATH           │ — (binary files)    │
└────────────────────────────────────────────────────────────────────────────┘

Architecture invariants enforced by 38 guard tests in HolocronToolset:
  • MCP tools.py imports only ghostscripter.core.services (no direct formats)
  • Only agdec_bridge.py may import httpx
  • TLKFile lives in core.models, not elsewhere
  • No cross-layer imports from core.export or core.resource_manager
```

---

## Features

- **Complete file format support** for KotOR and TSL game files (via PyKotor)
- **Cross-platform** (Windows, macOS, Linux)
- **HolocronToolset** — MCP-first modding IDE (GhostScripter-K1-K2, v2.2)
  - 32 MCP tools, hexagonal architecture, 963 tests
  - AgentDecompile/Ghidra binary analysis bridge
  - PyQt5 dark-theme GUI: NWScript editor, dialogue node graph, quest builder,
    2DA manager, TLK editor, ERF packer, asset library
- **KotorMCP** — lightweight read-mostly MCP server (25 tools, PyKotor-backed)
- **HoloPatcher** — cross-platform TSLPatcher replacement
- **GModular** — 3D module/world editor with REST API
- **Modern Python** (3.8+), **uv** workspace, **type-annotated** API

---

## Requirements

- Python 3.8+
- Windows 7–11, macOS, or Linux
- All common architectures supported (x86, x64, arm64)
- `uv` recommended for development (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

---

## Installation

### Quick Install

Install `uv` from [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/), then:

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uvx --refresh holocrontoolset
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uvx --refresh holocrontoolset
```

### Standard Install

**Install the library:**

```bash
pip install pykotor
```

**Install tools:**

```bash
pip install holocrontoolset holopatcher kotordiff
```

**Or use pipx for isolated tool installation:**

```bash
pipx install holocrontoolset
pipx install holopatcher
pipx install kotordiff
```

**Note:** The PyKotor CLI is included with the `pykotor` package and accessible via
`pykotor` or `pykotorcli` commands.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development installation. For slow clones,
use `git clone --depth 1` then `git submodule update --init --recursive ./Tools/`.

---

## Quick Start

### Using the Library

```python
from pykotor.resource.type import ResourceType
from pykotor.extract.installation import Installation
from pykotor.resource.formats.tpc import write_tpc

# Load game installation
inst = Installation("C:/Program Files (x86)/Steam/steamapps/common/swkotor")

# Extract a texture
texture = inst.texture("C_Gammorean01")
write_tpc(texture, "./C_Gammorean01.tga", ResourceType.TGA)
```

### Using the Tools

**HolocronToolset** — MCP IDE + GUI for KotOR modding (GhostScripter v2.2):

```bash
# Run the GUI IDE
cd Tools/HolocronToolset && python -m ghostscripter

# Run the MCP server (AI agent backend — 32 tools)
cd Tools/HolocronToolset && python -m ghostscripter.mcp

# Claude Desktop config (add to claude_desktop_config.json):
# {
#   "mcpServers": {
#     "ghostscripter": {
#       "command": "python",
#       "args": ["-m", "ghostscripter.mcp"],
#       "cwd": "/path/to/Tools/HolocronToolset",
#       "env": { "K1_PATH": "/path/to/kotor1", "K2_PATH": "/path/to/kotor2" }
#     }
#   }
# }
```

**KotorMCP** — standalone PyKotor-backed MCP server (25 tools):

```bash
cd Tools/KotorMCP && kotormcp
```

**HoloPatcher** - Cross-platform TSLPatcher alternative:

```bash
uvx --refresh holopatcher --help
```

**PyKotor CLI** - Command-line build tool (included with pykotor):

```bash
uvx --refresh pykotor --help
# Example: convert 2DA to CSV
uvx --refresh pykotor 2da2csv "path/to/file.2da"
```

**KotorDiff** - Compare and generate patches:

```bash
uvx --refresh kotordiff
```

---

## Available Tools

| Tool | Description | MCP Tools | Tests | Documentation |
|------|-------------|-----------|-------|---------------|
| **HolocronToolset** | MCP-first IDE (GhostScripter v2.2) — NWScript, DLG, 2DA, TLK, ERF | **32** | **963** | [README](Tools/HolocronToolset/README.md) · [ROADMAP](Tools/HolocronToolset/ROADMAP.md) |
| **KotorMCP** | Read-mostly PyKotor-backed MCP server | **25** | — | [README](Tools/KotorMCP/README.md) |
| **HoloPatcher** | Fast, cross-platform mod installer | — | — | [README](https://github.com/OldRepublicDevs/PyKotor/tree/master/Tools/HoloPatcher#readme) |
| **GModular** | 3D module/world editor + REST API | — | — | [DEVELOPMENT](Tools/GModular/DEVELOPMENT.md) |
| **PyKotor CLI** | Command-line format conversions | — | — | [Docs](https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/docs) |
| **KotorDiff** | File comparison and TSLPatcher data generator | — | — | [README](https://github.com/OldRepublicDevs/PyKotor/tree/master/Tools/KotorDiff#readme) |
| **HolocronToolset_old** | Legacy Qt5 GUI editor (reference only) | — | — | [README](Tools/HolocronToolset_old/README.md) |

---

## Submodule Overview

Run `git submodule update --init --recursive ./Tools/` after cloning to populate all
submodules.

| Submodule path | Remote | Role |
|---|---|---|
| `Tools/HolocronToolset` | CrispyW0nton/GhostScripter-K1-K2 | ★ Primary IDE + MCP |
| `Tools/HolocronToolset_old` | OldRepublicDevs/HolocronToolset | Legacy Qt5 editor (reference) |
| `Tools/KotorMCP` | OldRepublicDevs/KotorMCP | Standalone MCP server |
| `Tools/GModular` | CrispyW0nton/GModular | 3D world editor |
| `Tools/GhostScripter-K1-K2` | CrispyW0nton/GhostScripter-K1-K2 | Mirror of HolocronToolset |
| `Tools/HoloPatcher` | OldRepublicDevs/HoloPatcher | Mod installer |
| `Tools/HoloPazaak` | OldRepublicDevs/HoloPazaak | Pazaak game |
| `Tools/BatchPatcher` | OldRepublicDevs/BatchPatcher | Batch patching |
| `Tools/KotorDiff` | OldRepublicDevs/KotorDiff | Diff & patch |
| `Tools/HolocronAI` | OldRepublicDevs/HolocronAI | AI experiments |
| `Tools/KitGenerator` | OldRepublicDevs/KitGenerator | Indoor-kit generator |

---

## Documentation

### User Documentation
- **[Installation & Usage](https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/docs)** — Detailed library documentation
- **[Contributing Guide](CONTRIBUTING.md)** — Development setup and guidelines
- **[Project Wiki](https://github.com/OldRepublicDevs/PyKotor/wiki)** — Community documentation
- **[PowerShell Setup](POWERSHELL.md)** — Windows PowerShell configuration

### Design & Architecture
- **[AGENTS.md](AGENTS.md)** — AI agent coding guidelines for this monorepo
- **[CONVENTIONS.md](CONVENTIONS.md)** — Coding conventions and type-annotation rules
- **[HolocronToolset Systems Design](Tools/HolocronToolset/SYSTEMS_DESIGN.md)** — Ghostworks Pipeline coupling/cohesion analysis, event-bus design, composite tools
- **[HolocronToolset Roadmap](Tools/HolocronToolset/ROADMAP.md)** — Merge plan from HolocronToolset_old
- **[Design System Rules](.cursor/rules/design_system_rules.md)** — UI design system documentation

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development environment setup
- Code style guidelines (see also [CONVENTIONS.md](CONVENTIONS.md))
- Testing procedures
- Pull request process

Key conventions from `AGENTS.md`:
- Use `uv run` for all commands; never bare `python`
- Explicit type hints; `X | Y` not `Optional[X]`; no `getattr`/`hasattr`
- MCP only over stdio (no shadow MCPs on open sockets)
- Commit with conventional format: `type(scope): description`

---

## License

This project is licensed under the [LGPL-3.0-or-later License](https://github.com/OldRepublicDevs/PyKotor/blob/master/LICENSE).
