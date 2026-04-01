from __future__ import annotations

from typing import Any

from langchain.messages import AIMessage

from langchain_guardrails_demo.schemas import AssistantResponse


def extract_structured_response(result: dict[str, Any]) -> AssistantResponse | None:
    structured = result.get("structured_response")
    if isinstance(structured, AssistantResponse):
        return structured
    if isinstance(structured, dict):
        return AssistantResponse.model_validate(structured)
    return None


def extract_final_message(result: dict[str, Any]) -> str | None:
    messages = result.get("messages", [])
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            return str(message.content)
        if isinstance(message, dict) and message.get("role") == "assistant":
            return str(message.get("content", ""))
    return None


def build_console_payload(result: dict[str, Any]) -> dict[str, Any]:
    structured = extract_structured_response(result)
    if structured:
        return structured.model_dump()

    message = extract_final_message(result)
    return {
        "topic": None,
        "answer": None,
        "safety_notes": [],
        "sources": [],
        "message": message,
    }
