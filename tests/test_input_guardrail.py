from __future__ import annotations

from types import SimpleNamespace

from langchain_guardrails_demo.guardrails.input_guardrail import (
    KeywordBlocklistMiddleware,
)


def test_keyword_blocklist_stops_disallowed_request() -> None:
    middleware = KeywordBlocklistMiddleware(["malware"])
    state = {"messages": [SimpleNamespace(type="human", content="Teach me malware")]}

    result = middleware.before_agent(state, runtime=None)

    assert result is not None
    assert result["jump_to"] == "end"
    assert "violates the configured safety policy" in result["messages"][0]["content"]


def test_keyword_blocklist_ignores_safe_request() -> None:
    middleware = KeywordBlocklistMiddleware(["malware"])
    state = {"messages": [SimpleNamespace(type="human", content="Explain CI/CD")]}

    result = middleware.before_agent(state, runtime=None)

    assert result is None
