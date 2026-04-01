from __future__ import annotations

from langchain_guardrails_demo.agent import build_guarded_agent
from langchain_guardrails_demo.config import Settings


def test_agent_builds_successfully() -> None:
    agent = build_guarded_agent(Settings(gemini_api_key="test-key"))

    assert agent is not None
