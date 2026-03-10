from __future__ import annotations

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CRAWL4AI_MCP_", extra="ignore")

    headless: bool = Field(default=True)
    user_agent: Optional[str] = Field(default=None)
    proxy: Optional[str] = Field(default=None)
    cookies_json: Optional[str] = Field(
        default=None,
        description="Playwright storage_state JSON path",
    )
    use_persistent_context: bool = Field(default=False)
    user_data_dir: Optional[str] = Field(default=None)

    navigation_timeout_ms: int = Field(default=45_000)
    page_wait_ms: int = Field(default=800)
    max_scroll_steps: int = Field(default=12)
    scroll_step_wait_ms: int = Field(default=500)
    max_content_chars: int = Field(default=200_000)

    magic: bool = Field(default=False)
    max_retries: int = Field(default=1)

    accept_language: Optional[str] = Field(default="zh-CN,zh;q=0.9,en;q=0.8")


def get_settings() -> Settings:
    return Settings()
