"""Repository tool discovery and PyKotor library path constants (CI + compile scripts)."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore[assignment, misc]

LIBRARY_SOURCE_PATHS: list[str] = [
    "Libraries/PyKotor/src",
    "Libraries/bioware-kaitai-formats",
]
LIBRARY_TEST_PATHS: list[str] = [
    "Libraries/PyKotor/tests",
    "Libraries/bioware-kaitai-formats",
]


@dataclass
class ToolInfo:
    """Metadata for a package under `Tools/`."""

    directory: str
    name: str
    build_name: str
    display_name: str
    path: str
    src_path: str
    module_name: str
    requires_qt: bool
    is_cli: bool
    tests_path: str | None = field(default=None)

    @property
    def relative_path(self) -> str:
        return f"Tools/{self.directory}"

    def to_dict(self) -> dict[str, object | str | bool | None]:
        return {
            "directory": self.directory,
            "name": self.name,
            "build_name": self.build_name,
            "display_name": self.display_name,
            "path": self.path,
            "src_path": self.src_path,
            "module_name": self.module_name,
            "requires_qt": self.requires_qt,
            "is_cli": self.is_cli,
        }


def _read_pyproject_data(tool_dir: Path) -> dict[str, object]:
    pyproject = tool_dir / "pyproject.toml"
    if not pyproject.is_file() or tomllib is None:
        return {}
    try:
        return tomllib.load(pyproject.read_bytes())  # type: ignore[no-untyped-call]
    except (OSError, TypeError, ValueError, UnicodeError):
        return {}


def _script_module(data: dict[str, object]) -> str:
    project = data.get("project")
    if not isinstance(project, dict):
        return ""
    scripts = project.get("scripts")
    if not isinstance(scripts, dict) or not scripts:
        return ""
    for v in scripts.values():
        if isinstance(v, str) and ":" in v:
            return v.split(":", 1)[0].strip()
    return ""


def _infer_requires_qt(text: str) -> bool:
    low = text.lower()
    return "pyqt" in low or "pyside" in low or "qt5" in low or "qt6" in low


def _one_tool(repo_root: Path, tool_dir: Path) -> ToolInfo | None:
    if not (tool_dir / "pyproject.toml").is_file():
        return None
    directory = tool_dir.name
    data = _read_pyproject_data(tool_dir)
    project = data.get("project") if isinstance(data.get("project"), dict) else {}
    proj_name = str(project.get("name", directory))
    build_name = re.sub(r"[^0-9a-zA-Z]+", "-", proj_name).lower().strip("-")
    if not build_name:
        build_name = directory.lower()
    toml_text = (tool_dir / "pyproject.toml").read_text(encoding="utf-8", errors="replace")
    requires_qt = _infer_requires_qt(toml_text)
    is_cli = not requires_qt
    if (tool_dir / "src").is_dir():
        src = tool_dir / "src"
    else:
        src = tool_dir
    src_path = str(src.relative_to(repo_root))
    tests: Path | None = None
    for tname in ("tests", "test"):
        tpath = tool_dir / tname
        if tpath.is_dir():
            tests = tpath
            break
    tests_path = str(tests.relative_to(repo_root)) if tests is not None else None
    mod = _script_module(data)
    if not mod:
        if (src / "toolset").is_dir():
            mod = "toolset"
        elif (src / "pykotor").is_dir():
            mod = "pykotor"
        else:
            mod = directory
    return ToolInfo(
        directory=directory,
        name=build_name,
        build_name=build_name,
        display_name=proj_name,
        path=f"Tools/{directory}",
        src_path=src_path,
        module_name=mod,
        requires_qt=requires_qt,
        is_cli=is_cli,
        tests_path=tests_path,
    )


def discover_tools(repo_root: Path | str) -> list[ToolInfo]:
    """List each `Tools/*/` that contains a `pyproject.toml`."""
    root = Path(repo_root).resolve()
    tools_base = root / "Tools"
    if not tools_base.is_dir():
        return []
    out: list[ToolInfo] = []
    for child in sorted(tools_base.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        t = _one_tool(root, child)
        if t is not None:
            out.append(t)
    return out


def resolve_tool(name: str, repo_root: Path | str) -> ToolInfo:
    """Return tool metadata; *name* matches directory, build name, or project name (casefold)."""
    n = (name or "").strip().casefold()
    for tool in discover_tools(repo_root):
        if n in {
            tool.directory.casefold(),
            tool.build_name.casefold(),
            tool.name.casefold(),
            tool.display_name.casefold(),
        }:
            return tool
    msg = f"Unknown tool: {name!r}"
    raise KeyError(msg)
