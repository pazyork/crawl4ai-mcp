from __future__ import annotations

import os

import pytest

from crawl4ai_mcp.config import get_settings
from crawl4ai_mcp.crawler import CrawlService, FetchOptions

GOLDEN_URLS = [
    "https://zhuanlan.zhihu.com/p/1947787094299746426",
    "https://www.zhihu.com/people/phppan",
    "https://mp.weixin.qq.com/s/vdI4M1Ly8XTnJ6PqpQcEaA",
    "https://code.claude.com/docs/zh-CN/hooks",
    "https://medium.com/@sampan090611/claude-code-feels-like-a-senior-dev-heres-what-actually-makes-it-different-and-what-the-49c02b456d9c",
    "https://blog.csdn.net/Dontla/article/details/150590085",
]


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
