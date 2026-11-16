from __future__ import annotations

from unittest.mock import patch

import pytest

from app.agent.registry import dispatch_tool


def test_unknown_tool_returns_structured_error():
    result = dispatch_tool("unknown_tool", {})
    assert result["ok"] is False
    assert result["error"]["type"] == "unknown_tool"


def test_missing_question_returns_validation_error():
    result = dispatch_tool("search_department_policies", {"department": "hr"})
    assert result["ok"] is False
    assert result["error"]["type"] == "validation_error"


def test_question_too_short_returns_validation_error():
    result = dispatch_tool(
        "search_department_policies",
        {"question": "hi", "department": "hr", "top_k": 3},
    )
    assert result["ok"] is False
    assert result["error"]["type"] == "validation_error"


def test_unsupported_department_returns_validation_error():
    result = dispatch_tool(
        "search_department_policies",
        {"question": "What is the policy?", "department": "finance", "top_k": 3},
    )
    assert result["ok"] is False
    assert result["error"]["type"] == "validation_error"


def test_top_k_zero_returns_validation_error():
    result = dispatch_tool(
        "search_department_policies",
        {"question": "What is the policy?", "department": "hr", "top_k": 0},
    )
    assert result["ok"] is False
    assert result["error"]["type"] == "validation_error"


@patch("app.agent.tools.retrieve")
def test_valid_search_with_mocked_retrieve(mock_retrieve):
    mock_retrieve.return_value = [
        {
            "text": "Annual leave is accrued monthly.",
            "source": "annual_leave_policy.md",
            "page": 1,
            "department": "hr",
            "distance": 0.12,
        }
    ]

    result = dispatch_tool(
        "search_department_policies",
        {"question": "What is the annual leave policy?", "department": "hr", "top_k": 3},
    )

    assert result["ok"] is True
    assert result["result"]["status"] == "ok"
    assert result["result"]["count"] == 1
    assert result["result"]["evidence"][0]["source"] == "annual_leave_policy.md"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
