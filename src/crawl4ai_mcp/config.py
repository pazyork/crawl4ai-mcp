from __future__ import annotations

import tempfile
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CRAWL4AI_MCP_", extra="ignore")

    base_directory: str = Field(
        default_factory=tempfile.gettempdir,
        description="Writable base directory used by Crawl4AI for cache/log/robots state",
    )
    headless: bool = Field(default=True)
    user_agent: Optional[str] = Field(default=None)
    proxy: Optional[str] = Field(default=None)
    cookies_json: Optional[str] = Field(
        default=None,
        description="Playwright storage_state JSON path",
    )
    ytdlp_cookies_from_browser: Optional[str] = Field(
        default=None,
        description="yt-dlp browser cookie source, e.g. chrome, firefox:default",
    )
    ytdlp_cookiefile: Optional[str] = Field(
        default=None,
        description="yt-dlp Netscape cookies.txt path",
    )
    use_persistent_context: bool = Field(default=False)
    user_data_dir: Optional[str] = Field(default=None)

    viewport_width_min: int = Field(default=980)
    viewport_width_max: int = Field(default=1480)
    viewport_height_min: int = Field(default=640)
    viewport_height_max: int = Field(default=980)

    navigation_timeout_ms: int = Field(default=30_000)
    wait_until: str = Field(default="load")
    page_wait_ms: int = Field(default=800)
    max_scroll_steps: int = Field(default=12)
    scroll_step_wait_ms: int = Field(default=500)
    max_content_chars: int = Field(default=200_000)

    magic: bool = Field(default=False)
    max_retries: int = Field(default=1)

    accept_language: Optional[str] = Field(default="zh-CN,zh;q=0.9,en;q=0.8")

    locale: Optional[str] = Field(default="zh-CN")
    timezone_id: Optional[str] = Field(default="Asia/Shanghai")

    mean_delay_s: float = Field(default=0.12)
    max_delay_jitter_s: float = Field(default=0.25)

    cloudflare_bypass: bool = Field(
        default=False,
        description="Enable aggressive Cloudflare bypass mode with longer waits",
    )

    verbose: bool = Field(
        default=False,
        description=(
            "Emit crawl4ai's per-URL FETCH/SCRAPE/COMPLETE progress lines on stderr. "
            "Off by default — they are noise for MCP hosts and obscure real errors."
        ),
    )


def get_settings() -> Settings:
    return Settings()
