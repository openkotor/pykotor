#!/usr/bin/env python3
"""Local parity check for verify-pypi-regression.yml (published PyPI packages).

Runs core/format import blocks and the CLI discover→install→help path without
requiring GitHub Actions. Documented skips match CI continue-on-error behavior.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DISCOVER_SCRIPT = REPO_ROOT / ".github" / "scripts" / "discover_tools.py"

CORE_CHECK = """
import pykotor
print('OK: pykotor imported')
from pykotor.common.language import LocalizedString, Language, Gender
print('OK: LocalizedString imported')
from pykotor.resource.type import ResourceType
print('OK: ResourceType imported')
from pykotor.extract.installation import Installation
print('OK: Installation imported')
from pykotor.tslpatcher import patcher
print('OK: TSLPatcher imported')
ls = LocalizedString.from_english('Test')
assert ls.get(Language.ENGLISH, Gender.MALE) == 'Test'
print('OK: LocalizedString works')
assert ResourceType.UTC.extension == 'utc'
print('OK: ResourceType works')
print('All pykotor core tests passed!')
"""

FORMAT_CHECK = """
from pykotor.resource.formats import gff, tlk, twoda, erf, rim, bif
print('OK: All format modules imported')
from pykotor.resource.generics import are, git, ifo, utc, uti, utd, dlg
print('OK: All generic modules imported')
print('All resource format tests passed!')
"""


def _run(venv_python: Path, code: str, label: str) -> bool:
    print(f"=== {label} ===")
    result = subprocess.run([str(venv_python), "-c", code], cwd=REPO_ROOT)
    if result.returncode != 0:
        print(f"FAIL: {label}", file=sys.stderr)
        return False
    return True


def _pip_install(venv_python: Path, *args: str) -> bool:
    result = subprocess.run(
        [str(venv_python), "-m", "pip", "install", "--upgrade", "pip", *args],
        cwd=REPO_ROOT,
    )
    return result.returncode == 0


def _cli_slice(venv_python: Path) -> bool:
    print("=== CLI ===")
    if not DISCOVER_SCRIPT.is_file():
        print(f"FAIL: missing {DISCOVER_SCRIPT}", file=sys.stderr)
        return False

    discover = subprocess.run(
        [sys.executable, str(DISCOVER_SCRIPT), "--cli-only", "--format", "json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if discover.returncode != 0:
        print(discover.stderr, file=sys.stderr)
        print("FAIL: discover_tools", file=sys.stderr)
        return False

    tools = json.loads(discover.stdout)
    for tool in tools:
        package = tool["project_name"]
        print(f"Installing {package}...")
        install = subprocess.run(
            [str(venv_python), "-m", "pip", "install", package],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        if install.returncode != 0:
            print(f"  SKIP: {package} not available on PyPI")
            continue
        module_name = tool["package_name"]
        print(f"Testing {module_name} --help")
        help_result = subprocess.run(
            [str(venv_python), "-m", module_name, "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        if help_result.returncode != 0:
            print(f"  SKIP: {module_name} help not available (rc={help_result.returncode})")
        else:
            print(f"  OK: {module_name} --help")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local verify-pypi regression slice (published packages)",
    )
    parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="pypi-verify-") as tmp:
        venv_dir = Path(tmp) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        venv_python = venv_dir / "bin" / "python"
        if not venv_python.is_file():
            venv_python = venv_dir / "Scripts" / "python.exe"

        print("=== SETUP ===")
        if not _pip_install(venv_python, "pykotor[all]"):
            print("FAIL: pip install pykotor[all]", file=sys.stderr)
            sys.exit(1)

        ok = _run(venv_python, CORE_CHECK, "CORE")
        ok = _run(venv_python, FORMAT_CHECK, "FORMATS") and ok
        ok = _cli_slice(venv_python) and ok

        if not ok:
            sys.exit(1)
        print("=== DONE ===")
        print("Local verify-pypi slice passed (with documented CLI skips).")


if __name__ == "__main__":
    main()
