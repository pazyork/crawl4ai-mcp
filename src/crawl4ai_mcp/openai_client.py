from __future__ import annotations

import json
from dataclasses import dataclass
from os import getenv
from typing import Any, Optional

import httpx


@dataclass(frozen=True)
class OpenAIConfig:
    base_url: Optional[str]
    api_key: Optional[str]
    model: Optional[str]

    @property
    def enabled(self) -> bool:
        return bool(self.base_url and self.api_key and self.model)


def load_openai_config() -> OpenAIConfig:
    return OpenAIConfig(
        base_url=getenv("OPENAI_BASE_URL"),
        api_key=getenv("OPENAI_API_KEY"),
        model=getenv("OPENAI_MODEL"),
    )


async def openai_chat_completions_json(
    *,
    cfg: OpenAIConfig,
    system: str,
    user: str,
    timeout_s: float = 60.0,
) -> dict[str, Any]:
    if not cfg.enabled:
        raise RuntimeError("OpenAI-compatible config not set (OPENAI_BASE_URL/KEY/MODEL)")

    url = cfg.base_url.rstrip("/") + "/v1/chat/completions"
    headers = {"Authorization": f"Bearer {cfg.api_key}"}
    payload = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=timeout_s) as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise RuntimeError("Unexpected OpenAI response content type")
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError("OpenAI returned non-JSON content") from e
        if not isinstance(parsed, dict):
            raise RuntimeError("OpenAI returned non-object JSON")
        return parsed
