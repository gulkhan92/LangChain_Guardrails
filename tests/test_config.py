from __future__ import annotations

import pytest

from langchain_guardrails_demo.config import Settings


def test_settings_from_env_loads_values(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "api-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-1.5-flash")
    monkeypatch.setenv("GEMINI_SAFETY_MODEL", "gemini-1.5-pro")

    settings = Settings.from_env()

    assert settings.gemini_api_key == "api-key"
    assert settings.gemini_model == "gemini-1.5-flash"
    assert settings.safety_model == "gemini-1.5-pro"


def test_settings_from_env_uses_defaults_for_optional_models(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "api-key")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_SAFETY_MODEL", raising=False)

    settings = Settings.from_env()

    assert settings.gemini_model == "gemini-2.0-flash"
    assert settings.safety_model == "gemini-2.0-flash"


def test_settings_from_env_requires_api_key(monkeypatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="GEMINI_API_KEY is not set"):
        Settings.from_env()
