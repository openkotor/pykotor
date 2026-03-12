"""Installation management tools: detect, load, info."""

from __future__ import annotations

from typing import Any

from mcp import types

from pykotor.common.misc import Game

from kotormcp.schemas.inputs import LoadInstallationInput
from kotormcp.state import DEFAULT_PATH_CACHE, iter_candidate_paths, load_installation, resolve_game
from kotormcp.utils.formatting import json_content


def get_tools() -> list[types.Tool]:
    """Return tool definitions for installation management (read-only, local filesystem)."""
    return [
        types.Tool(
            name="detectInstallations",
            description="Enumerate candidate installation paths for K1/K2 by inspecting env vars and platform defaults. Read-only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="loadInstallation",
            description="Activate an installation in memory so subsequent tools can reuse cached data. Read-only; does not modify disk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string", "description": "k1, k2, or tsl"},
                    "path": {"type": "string", "description": "Optional absolute path override."},
                },
                "required": ["game"],
            },
        ),
    ]


async def handle_detect_installations(_arguments: dict[str, Any]) -> types.CallToolResult:
    """Enumerate candidate paths for K1 and K2."""
    payload = {}
    for game in (Game.K1, Game.K2):
        default_keys = {str(path).lower() for path in DEFAULT_PATH_CACHE.get(game, [])}
        details = []
        for candidate in iter_candidate_paths(game, None):
            key = str(candidate).lower()
            details.append(
                {
                    "path": str(candidate),
                    "exists": candidate.is_dir(),
                    "label": "default" if key in default_keys else "env",
                },
            )
        payload[game.name] = details
    return json_content(payload)


async def handle_load_installation(arguments: dict[str, Any]) -> types.CallToolResult:
    """Load and cache an installation for the given game."""
    inp = LoadInstallationInput.model_validate(arguments)
    game = resolve_game(inp.game)
    if game is None:
        msg = "Specify game as k1 or k2."
        raise ValueError(msg)
    installation = load_installation(game, inp.path)
    return json_content({"game": game.name, "path": str(installation.path())})
