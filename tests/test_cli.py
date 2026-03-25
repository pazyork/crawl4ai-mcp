from __future__ import annotations

import json
import sys
import types

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


def test_fetch_command_prints_single_json_result(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    from crawl4ai_mcp import cli as cli_module

    async def fake_fetch_command(args: object) -> dict[str, object]:
        assert args.url == "https://example.com"
        assert args.proxy == "http://127.0.0.1:7890"
        assert args.cookies_from_browser == "chrome"
        return {
            "url": "https://example.com",
            "title": "Example",
            "content": "hello",
            "content_format": "markdown",
        }

    monkeypatch.setattr(cli_module, "_run_fetch", fake_fetch_command)

    cli_module.main([
        "fetch",
        "https://example.com",
        "--proxy",
        "http://127.0.0.1:7890",
        "--cookies-from-browser",
        "chrome",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["title"] == "Example"
    assert payload["content"] == "hello"


def test_smoke_command_prints_json_array(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    from crawl4ai_mcp import cli as cli_module

    async def fake_smoke_command(args: object) -> list[dict[str, object]]:
        assert args.out_dir == "./_golden_outputs"
        return [
            {"url": "https://a.test", "title": "A", "content_format": "markdown", "chars": 12},
            {"url": "https://b.test", "title": "B", "content_format": "markdown", "chars": 34},
        ]

    monkeypatch.setattr(cli_module, "_run_smoke", fake_smoke_command)

    cli_module.main(["smoke", "--out-dir", "./_golden_outputs"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert isinstance(payload, list)
    assert payload[0]["title"] == "A"
    assert payload[1]["chars"] == 34


def test_search_command_prints_json_result(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    from crawl4ai_mcp import cli as cli_module

    async def fake_search_command(args: object) -> dict[str, object]:
        assert args.query == "agent framework"
        assert args.engine == "auto"
        assert args.max_results == 5
        assert args.lang == "en"
        return {
            "engine": "fused",
            "query": "agent framework",
            "results": [{"title": "A", "url": "https://a.test", "snippet": "x"}],
            "total": 1,
        }

    monkeypatch.setattr(cli_module, "_run_search", fake_search_command)

    cli_module.main(["search", "agent framework", "--engine", "auto", "--max-results", "5", "--lang", "en"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["engine"] == "fused"
    assert payload["total"] == 1
