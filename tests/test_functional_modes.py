from __future__ import annotations

import os

import pytest

from crawl4ai_mcp.config import get_settings
from crawl4ai_mcp.crawler import CrawlService, FetchOptions


TEST_URL = "https://example.com"


@pytest.mark.asyncio
async def test_non_llm_mode() -> None:
    """Test basic non-LLM mode with a stable website."""
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URL,
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert res.get("title"), "Title should exist"
        assert res.get("content_format") == "markdown", "Format should be markdown"
        assert "Example Domain" in content, "Should contain expected content"
        assert len(content) > 100, "Content should be substantial"


@pytest.mark.asyncio
async def test_html_format() -> None:
    """Test HTML format output."""
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URL,
            options=FetchOptions(format="html", max_chars=120_000),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert res.get("content_format") in ["html", "markdown"], \
            "Format should be html or markdown fallback"


@pytest.mark.asyncio
async def test_max_chars_limit() -> None:
    """Test max_chars limit is respected."""
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URL,
            options=FetchOptions(format="markdown", max_chars=500),
        )
        content = str(res.get("content") or "")
        
        assert content, "Content should not be empty"
        assert len(content) <= 600, "Content should respect max_chars limit (with buffer)"


@pytest.mark.asyncio
async def test_links_extraction() -> None:
    """Test that links are extracted."""
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url=TEST_URL,
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        
        links = res.get("links")
        assert isinstance(links, list), "Links should be a list"
        
        if links:
            assert isinstance(links[0], dict), "Each link should be a dict"
            assert "url" in links[0], "Link should have url field"
