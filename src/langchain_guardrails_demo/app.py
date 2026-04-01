from __future__ import annotations

from langchain_guardrails_demo.agent import build_guarded_agent
from langchain_guardrails_demo.config import Settings


class GuardrailsApplication:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        self.agent = build_guarded_agent(self.settings)

    def run(self, user_input: str) -> dict:
        return self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
