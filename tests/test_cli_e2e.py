from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest

if "crawl4ai" not in sys.modules:
    crawl4ai_stub = types.ModuleType("crawl4ai")
    crawl4ai_stub.AsyncWebCrawler = object
    sys.modules["crawl4ai"] = crawl4ai_stub

if "crawl4ai.async_configs" not in sys.modules:
    async_configs_stub = types.ModuleType("crawl4ai.async_configs")

    class _DummyConfig:
        def __init__(self, **kwargs: object) -> None:
            self.kwargs = kwargs

    async_configs_stub.BrowserConfig = _DummyConfig
    async_configs_stub.CrawlerRunConfig = _DummyConfig
    async_configs_stub.ProxyConfig = _DummyConfig
    sys.modules["crawl4ai.async_configs"] = async_configs_stub

if "crawl4ai.cache_context" not in sys.modules:
    cache_context_stub = types.ModuleType("crawl4ai.cache_context")

    class _DummyCacheMode:
        BYPASS = "bypass"

    cache_context_stub.CacheMode = _DummyCacheMode
    sys.modules["crawl4ai.cache_context"] = cache_context_stub


class _FakeService:
    def __init__(self, *_: object, **__: object) -> None:
        self.urls: list[str] = []

    async def __aenter__(self) -> _FakeService:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def fetch(self, *, url: str, options: object) -> dict[str, object]:
        self.urls.append(url)
        return {
            "url": url,
            "title": f"Title for {url}",
            "content": f"Content for {url}",
            "content_format": "markdown",
        }


def test_smoke_command_uses_golden_urls_and_writes_outputs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from crawl4ai_mcp import cli as cli_module

    monkeypatch.setattr(cli_module, "CrawlService", _FakeService)
    monkeypatch.setattr(cli_module, "GOLDEN_URLS", ["https://golden.test/a", "https://golden.test/b"])

    cli_module.main(["smoke", "--out-dir", str(tmp_path), "--full-content"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert [item["url"] for item in payload] == ["https://golden.test/a", "https://golden.test/b"]
    assert payload[0]["content"] == "Content for https://golden.test/a"
    assert (tmp_path / "golden.test_a.md").exists()
    assert (tmp_path / "golden.test_b.md").exists()
