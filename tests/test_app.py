from __future__ import annotations

from langchain_guardrails_demo.app import GuardrailsApplication
from langchain_guardrails_demo.config import Settings


class FakeAgent:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def invoke(self, payload: dict) -> dict:
        self.calls.append(payload)
        return {"status": "ok", "payload": payload}


def test_application_run_passes_user_input_to_agent(monkeypatch) -> None:
    fake_agent = FakeAgent()

    def fake_build_guarded_agent(settings: Settings) -> FakeAgent:
        assert settings.gemini_api_key == "test-key"
        return fake_agent

    monkeypatch.setattr(
        "langchain_guardrails_demo.app.build_guarded_agent",
        fake_build_guarded_agent,
    )

    app = GuardrailsApplication(Settings(gemini_api_key="test-key"))
    result = app.run("Explain how guardrails work.")

    assert result["status"] == "ok"
    assert fake_agent.calls == [
        {"messages": [{"role": "user", "content": "Explain how guardrails work."}]}
    ]
