"""Response formatting: JSON content, truncation, pagination helpers."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

# Recommended max response size for tool output (plan §2.4); truncate with continuation hint when exceeded
MAX_RESPONSE_CHARS = 25_000


def json_content(payload: Any, max_chars: int = MAX_RESPONSE_CHARS) -> types.CallToolResult:
    """Build MCP CallToolResult from a JSON-serializable payload.

    If serialized length exceeds max_chars, truncates and appends a continuation hint.
    """
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if len(text) > max_chars:
        hint = "\n... [truncated at {} chars; use offset/limit or filters to get more]".format(max_chars)
        text = text[: max_chars - len(hint)] + hint
    return types.CallToolResult(content=[types.TextContent(type="text", text=text)])
