from __future__ import annotations

import asyncio
import os

import pytest

from crawl4ai_mcp.config import get_settings
from crawl4ai_mcp.crawler import CrawlService, FetchOptions

TEST_URLS = [
    "https://zhuanlan.zhihu.com/p/1947787094299746426",
    "https://www.zhihu.com/people/phppan",
    "https://mp.weixin.qq.com/s/vdI4M1Ly8XTnJ6PqpQcEaA",
]


@pytest.mark.asyncio
async def test_non_llm_mode() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URLS[0],
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert res.get("title"), "Title should exist"
        assert res.get("content_format") == "markdown", "Format should be markdown"
        assert res.get("llm_used") is False, "LLM should not be used"
        assert res.get("llm_error") is None, "No LLM error expected"
        assert len(content) > 1000, "Content should be substantial"


@pytest.mark.asyncio
async def test_llm_mode_without_instruction() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set, skipping LLM test")
    
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URLS[1],
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert res.get("title"), "Title should exist"
        
        if res.get("llm_used"):
            assert len(content) > 500, "LLM-cleaned content should be substantial"
            assert res.get("llm_error") is None, "No LLM error when llm_used=True"
        else:
            assert res.get("llm_error"), "Should have llm_error when llm_used=False"


@pytest.mark.asyncio
async def test_llm_mode_with_instruction() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set, skipping LLM test")
    
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URLS[2],
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert res.get("title"), "Title should exist"
        
        if res.get("llm_used"):
            assert "Claude Code" in content or "claude" in content.lower(), \
                "Content should contain relevant keywords"


@pytest.mark.asyncio
async def test_concurrent_fetches() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        tasks = [
            service.fetch(
                url=url,
                options=FetchOptions(format="markdown", max_chars=120_000),
            )
            for url in TEST_URLS
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        assert len(results) == len(TEST_URLS), "Should get all results"
        
        success_count = 0
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                print(f"URL {TEST_URLS[i]} failed: {res}")
            else:
                assert isinstance(res, dict), "Result should be a dict"
                content = str(res.get("content") or "")
                if content and len(content) > 500:
                    success_count += 1
        
        assert success_count >= 2, f"At least 2 URLs should succeed, got {success_count}"


@pytest.mark.asyncio
async def test_blocked_detection() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url="https://www.producthunt.com/",
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        
        content = str(res.get("content") or "")
        blocked = res.get("blocked")
        
        if blocked:
            assert "验证" in content or "Cloudflare" in content or len(content) < 1000, \
                "Blocked content should show verification page or be very short"
        else:
            assert len(content) > 1000, "Non-blocked content should be substantial"


@pytest.mark.asyncio
async def test_format_html() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URLS[0],
            options=FetchOptions(format="html", max_chars=120_000),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert res.get("content_format") in ["html", "markdown"], \
            "Format should be html or markdown fallback"
        assert "<" in content or "#" in content, "Should contain HTML tags or markdown"


@pytest.mark.asyncio
async def test_max_chars_limit() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URLS[0],
            options=FetchOptions(format="markdown", max_chars=5_000),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert len(content) <= 5_500, "Content should respect max_chars limit (with buffer)"


@pytest.mark.asyncio
async def test_links_extraction() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URLS[0],
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        
        links = res.get("links")
        assert isinstance(links, list), "Links should be a list"
        
        if links:
            assert isinstance(links[0], dict), "Each link should be a dict"
            assert "url" in links[0], "Link should have url field"
