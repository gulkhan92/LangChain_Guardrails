from __future__ import annotations

import pytest
from pydantic import ValidationError

from langchain_guardrails_demo.schemas import AssistantResponse, SafetyVerdict


def test_assistant_response_accepts_valid_payload() -> None:
    response = AssistantResponse.model_validate(
        {
            "topic": "guardrails",
            "answer": "Guardrails constrain unsafe behavior.",
            "safety_notes": ["PII redaction enabled"],
            "sources": ["LangChain docs"],
        }
    )

    assert response.topic == "guardrails"
    assert response.safety_notes == ["PII redaction enabled"]


def test_assistant_response_rejects_missing_required_fields() -> None:
    with pytest.raises(ValidationError):
        AssistantResponse.model_validate({"topic": "guardrails"})


def test_safety_verdict_requires_boolean_flag() -> None:
    with pytest.raises(ValidationError):
        SafetyVerdict.model_validate({"reason": "Missing required flag"})
