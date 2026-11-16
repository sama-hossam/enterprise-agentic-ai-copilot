from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from app.agent.tools import PolicySearchInput, search_department_policies

TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "search_department_policies": {
        "function": search_department_policies,
        "input_model": PolicySearchInput,
    }
}


def dispatch_tool(name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        return {
            "ok": False,
            "error": {
                "type": "unknown_tool",
                "message": f"Unknown tool: {name}",
            },
        }

    payload = arguments if isinstance(arguments, dict) else {}

    try:
        validated = tool["input_model"](**payload)
    except TypeError as exc:
        return {
            "ok": False,
            "error": {
                "type": "validation_error",
                "message": "Invalid arguments for tool.",
                "details": str(exc),
            },
        }
    except ValidationError as exc:
        return {
            "ok": False,
            "error": {
                "type": "validation_error",
                "message": "Invalid arguments for tool.",
                "details": exc.errors(),
            },
        }

    try:
        result = tool["function"](validated)
    except Exception as exc:  # pragma: no cover - execution fallback
        return {
            "ok": False,
            "error": {
                "type": "execution_error",
                "message": "Tool execution failed.",
                "details": str(exc),
            },
        }

    return {"ok": True, "result": result}
