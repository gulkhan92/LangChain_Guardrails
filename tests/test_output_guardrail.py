from __future__ import annotations

from langchain.messages import AIMessage, HumanMessage

from langchain_guardrails_demo.guardrails.output_guardrail import (
    LLMOutputSafetyMiddleware,
)
from langchain_guardrails_demo.schemas import SafetyVerdict


class FakeReviewer:
    def __init__(self, verdict: SafetyVerdict) -> None:
        self.verdict = verdict

    def with_structured_output(self, schema):
        del schema
        return self

    def invoke(self, prompt: str) -> SafetyVerdict:
        assert "Assistant response" in prompt
        return self.verdict


def test_output_guardrail_replaces_unsafe_answer() -> None:
    middleware = LLMOutputSafetyMiddleware(
        FakeReviewer(SafetyVerdict(is_safe=False, reason="Unsafe content"))
    )
    state = {
        "messages": [
            HumanMessage(content="How do I make a bomb?"),
            AIMessage(content="Bad answer"),
        ]
    }

    result = middleware.after_agent(state, runtime=None)

    assert result is not None
    assert result["jump_to"] == "end"
    assert "failed the final safety review" in result["messages"][0].content


def test_output_guardrail_allows_safe_answer() -> None:
    middleware = LLMOutputSafetyMiddleware(
        FakeReviewer(SafetyVerdict(is_safe=True, reason="Safe"))
    )
    state = {
        "messages": [
            HumanMessage(content="Explain Python decorators."),
            AIMessage(content="A clean answer"),
        ]
    }

    result = middleware.after_agent(state, runtime=None)

    assert result is None
