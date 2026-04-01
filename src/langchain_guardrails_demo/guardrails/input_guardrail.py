from __future__ import annotations

from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime


class KeywordBlocklistMiddleware(AgentMiddleware):
    """Deterministic guardrail that stops clearly disallowed requests early."""

    def __init__(self, banned_keywords: list[str]) -> None:
        super().__init__()
        self.banned_keywords = tuple(keyword.lower() for keyword in banned_keywords)

    @hook_config(can_jump_to=["end"])
    def before_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        del runtime
        messages = state.get("messages", [])
        if not messages:
            return None

        first_message = messages[0]
        if getattr(first_message, "type", "") != "human":
            return None

        content = str(first_message.content).lower()
        matched = next(
            (keyword for keyword in self.banned_keywords if keyword in content),
            None,
        )
        if not matched:
            return None

        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": (
                        "I cannot help with that request because it violates the "
                        "configured safety policy."
                    ),
                }
            ],
            "jump_to": "end",
        }
