from __future__ import annotations

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain.agents.middleware import PIIMiddleware

from langchain_guardrails_demo.config import Settings
from langchain_guardrails_demo.guardrails.input_guardrail import (
    KeywordBlocklistMiddleware,
)
from langchain_guardrails_demo.guardrails.output_guardrail import (
    LLMOutputSafetyMiddleware,
)
from langchain_guardrails_demo.prompts import SYSTEM_PROMPT
from langchain_guardrails_demo.schemas import AssistantResponse
from langchain_guardrails_demo.services.model_factory import build_chat_model


DEFAULT_BANNED_KEYWORDS = [
    "hack",
    "malware",
    "phishing",
    "bomb",
    "explosive",
    "bypass security",
]


class EmailRedactionMiddleware(PIIMiddleware):
    def __init__(self) -> None:
        super().__init__("email", strategy="redact", apply_to_input=True, apply_to_output=True)


class CreditCardMaskMiddleware(PIIMiddleware):
    def __init__(self) -> None:
        super().__init__("credit_card", strategy="mask", apply_to_input=True)


def build_guarded_agent(settings: Settings):
    llm = build_chat_model(settings.gemini_model, settings)
    reviewer = build_chat_model(settings.safety_model, settings)

    middleware = [
        KeywordBlocklistMiddleware(DEFAULT_BANNED_KEYWORDS),
        EmailRedactionMiddleware(),
        CreditCardMaskMiddleware(),
        LLMOutputSafetyMiddleware(reviewer),
    ]

    return create_agent(
        model=llm,
        tools=[],
        system_prompt=SYSTEM_PROMPT,
        middleware=middleware,
        response_format=ProviderStrategy(schema=AssistantResponse),
    )
