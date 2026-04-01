from __future__ import annotations

from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain.messages import AIMessage
from langgraph.runtime import Runtime

from langchain_guardrails_demo.prompts import SAFETY_REVIEW_PROMPT
from langchain_guardrails_demo.schemas import SafetyVerdict


class LLMOutputSafetyMiddleware(AgentMiddleware):
    """Model-based guardrail that reviews the final answer before it is returned."""

    def __init__(self, reviewer) -> None:
        super().__init__()
        self.reviewer = reviewer.with_structured_output(SafetyVerdict)

    @hook_config(can_jump_to=["end"])
    def after_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        del runtime
        messages = state.get("messages", [])
        if not messages:
            return None

        user_request = ""
        for message in messages:
            if getattr(message, "type", "") == "human":
                user_request = str(message.content)
                break

        last_message = messages[-1]
        if not isinstance(last_message, AIMessage):
            return None

        verdict = self.reviewer.invoke(
            SAFETY_REVIEW_PROMPT.format(
                user_request=user_request,
                assistant_response=last_message.content,
            )
        )

        if verdict.is_safe:
            return None

        return {
            "messages": [
                AIMessage(
                    content=(
                        "I cannot return that response because it failed the final "
                        f"safety review. Reason: {verdict.reason}"
                    )
                )
            ],
            "jump_to": "end",
        }
