from __future__ import annotations

from langchain.messages import AIMessage

from langchain_guardrails_demo.presentation import build_console_payload
from langchain_guardrails_demo.schemas import AssistantResponse


def test_build_console_payload_uses_structured_response() -> None:
    result = {
        "structured_response": AssistantResponse(
            topic="structured output",
            answer="Use a schema-backed response contract.",
            safety_notes=["Validated output"],
            sources=["LangChain docs"],
        )
    }

    payload = build_console_payload(result)

    assert payload["topic"] == "structured output"
    assert payload["answer"] == "Use a schema-backed response contract."


def test_build_console_payload_falls_back_to_final_message() -> None:
    result = {"messages": [AIMessage(content="Fallback response")]}

    payload = build_console_payload(result)

    assert payload["message"] == "Fallback response"
    assert payload["topic"] is None
