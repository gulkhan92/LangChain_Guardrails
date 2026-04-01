from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_guardrails_demo.config import Settings


def build_chat_model(model_name: str, settings: Settings) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=settings.gemini_api_key,
        temperature=0.2,
    )
