from __future__ import annotations

from pydantic import BaseModel, Field


class AssistantResponse(BaseModel):
    topic: str = Field(..., description="Short normalized description of the user request.")
    answer: str = Field(..., description="Final safe answer for the user.")
    safety_notes: list[str] = Field(
        default_factory=list,
        description="Relevant safety or compliance notes applied by the assistant.",
    )
    sources: list[str] = Field(
        default_factory=list,
        description="Optional sources or references used in the answer.",
    )


class SafetyVerdict(BaseModel):
    is_safe: bool = Field(..., description="Whether the content is safe to return.")
    reason: str = Field(..., description="Brief explanation for the safety decision.")
