from __future__ import annotations

import os

import pytest

from crawl4ai_mcp.config import get_settings
from crawl4ai_mcp.crawler import CrawlService, FetchOptions
from crawl4ai_mcp.golden_urls import GOLDEN_URLS


@pytest.mark.integration
@pytest.mark.asyncio
async def test_golden_urls_smoke() -> None:
    if os.getenv("RUN_GOLDEN") != "1":
        pytest.skip("set RUN_GOLDEN=1 to run network/browser golden tests")

    settings = get_settings()
    async with CrawlService(settings) as service:
        for url in GOLDEN_URLS:
            res = await service.fetch(
                url=url,
                options=FetchOptions(format="markdown", max_chars=120_000),
            )
            content = str(res.get("content") or "")
            title = res.get("title")
            assert content, f"empty content for {url}"
            assert (isinstance(title, str) and title.strip()) or ("#" in content or "\n" in content)
