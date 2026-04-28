#!/usr/bin/env python3
"""Dynamic tool discovery for GitHub Actions workflows."""

from __future__ import annotations

import argparse
import json
import sys

from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tool_metadata import discover_tools  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover tools for CI/CD")
    parser.add_argument(
        "--format",
        choices=["json", "github"],
        default="github",
        help="Output format (json or GitHub Actions output)",
    )
    parser.add_argument("--cli-only", action="store_true", help="Only emit non-windowed tools")
    args = parser.parse_args()

    tools = discover_tools(repo_root)
    if args.cli_only:
        tools = [tool for tool in tools if tool.is_cli]

    if not tools:
        if args.format == "json":
            print("[]")
        else:
            print("tools_matrix=[]")
            print("Discovered 0 tools (workspace may lack vendored Tools/* checkouts)", file=sys.stderr)
        return

    payload = [tool.to_dict() for tool in tools]
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return

    print(f"tools_matrix={json.dumps(payload)}")
    print(f"Discovered {len(tools)} tools", file=sys.stderr)


if __name__ == "__main__":
    main()
