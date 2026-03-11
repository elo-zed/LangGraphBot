from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    openai_api_key: str | None
    openai_base_url: str | None
    openai_model: str
    http_timeout_seconds: float
    http_retries: int
    http_user_agent: str
    output_dir: str


def load_config() -> AppConfig:
    load_dotenv(override=False)

    def _get(name: str, default: str | None = None) -> str | None:
        v = os.getenv(name)
        if v is None or v == "":
            return default
        return v

    return AppConfig(
        openai_api_key=_get("OPENAI_API_KEY"),
        openai_base_url=_get("OPENAI_BASE_URL"),
        openai_model=_get("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini",
        http_timeout_seconds=float(_get("HTTP_TIMEOUT_SECONDS", "20") or 20),
        http_retries=int(_get("HTTP_RETRIES", "2") or 2),
        http_user_agent=_get(
            "HTTP_USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        )
        or "",
        output_dir=_get("OUTPUT_DIR", "outputs") or "outputs",
    )

