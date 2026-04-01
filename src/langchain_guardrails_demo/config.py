from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash"
    safety_model: str = "gemini-2.0-flash"

    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Create a .env file from .env.example first."
            )

        return cls(
            gemini_api_key=api_key,
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()
            or "gemini-2.0-flash",
            safety_model=os.getenv("GEMINI_SAFETY_MODEL", "gemini-2.0-flash").strip()
            or "gemini-2.0-flash",
        )
