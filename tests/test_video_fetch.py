from __future__ import annotations

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

from crawl4ai_mcp import video as video_module
from crawl4ai_mcp.config import get_settings
from crawl4ai_mcp.crawler import CrawlService, FetchOptions


class _UnexpectedCrawler:
    async def arun(self, **_: object) -> object:
        raise AssertionError("browser crawler should not run for supported video subtitles")


class _BrowserResult:
    success = True
    url = "https://www.youtube.com/watch?v=OFfwN23hR8U"
    title = "网页标题"
    html = "<html><title>网页标题</title><body>网页内容</body></html>"
    markdown = "# 网页标题\n\n网页内容\n"
    links = []


class _ExpectedCrawler:
    def __init__(self) -> None:
        self.called = False

    async def arun(self, **_: object) -> object:
        self.called = True
        return _BrowserResult()


@pytest.mark.asyncio
async def test_fetch_uses_video_subtitles_for_supported_video_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    from crawl4ai_mcp import crawler as crawler_module

    async def fake_extract_video_result(
        *,
        url: str,
        options: FetchOptions,
        proxy: str | None,
        cookies_from_browser: str | None,
        cookiefile: str | None,
    ) -> dict[str, object]:
        return {
            "url": url,
            "final_url": url,
            "title": "视频标题",
            "content": "# 视频标题\n\n第一行字幕\n第二行字幕\n",
            "content_format": "markdown",
            "links": [],
            "video_metadata": {"extractor": "youtube"},
        }

    monkeypatch.setattr(crawler_module, "_fetch_video_result", fake_extract_video_result, raising=False)

    service = CrawlService(get_settings())
    service._crawler = _UnexpectedCrawler()  # type: ignore[assignment]

    result = await service.fetch(
        url="https://www.youtube.com/watch?v=OFfwN23hR8U",
        options=FetchOptions(format="markdown", max_chars=120_000),
    )

    assert result["title"] == "视频标题"
    assert "第一行字幕" in str(result["content"])
    assert result["content_format"] == "markdown"
    assert result["final_url"] == "https://www.youtube.com/watch?v=OFfwN23hR8U"
    assert result.get("video_metadata") == {"extractor": "youtube"}


@pytest.mark.asyncio
async def test_fetch_falls_back_to_browser_when_video_subtitles_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from crawl4ai_mcp import crawler as crawler_module

    async def fake_extract_video_result(
        *,
        url: str,
        options: FetchOptions,
        proxy: str | None,
        cookies_from_browser: str | None,
        cookiefile: str | None,
    ) -> None:
        return None

    monkeypatch.setattr(crawler_module, "_fetch_video_result", fake_extract_video_result, raising=False)

    service = CrawlService(get_settings())
    browser = _ExpectedCrawler()
    service._crawler = browser  # type: ignore[assignment]

    result = await service.fetch(
        url="https://www.youtube.com/watch?v=OFfwN23hR8U",
        options=FetchOptions(format="markdown", max_chars=120_000),
    )

    assert browser.called is True
    assert result["title"] == "网页标题"
    assert "网页内容" in str(result["content"])


@pytest.mark.asyncio
async def test_extract_video_result_passes_proxy_and_cookie_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setattr(video_module, "_extract_video_result_via_cli", lambda **_: None)

    class _FakeYoutubeDL:
        def __init__(self, opts: dict[str, object]) -> None:
            captured.update(opts)

        def __enter__(self) -> _FakeYoutubeDL:
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def extract_info(self, url: str, download: bool = False) -> dict[str, object]:
            return {
                "id": "abc123",
                "title": "视频标题",
                "extractor": "youtube",
                "webpage_url": url,
                "subtitles": {
                    "en": [{"ext": "vtt", "data": "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhello"}]
                },
            }

    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=_FakeYoutubeDL))

    result = await video_module.extract_video_result(
        url="https://www.youtube.com/watch?v=OFfwN23hR8U",
        max_chars=1000,
        proxy="http://127.0.0.1:7890",
        cookies_from_browser="chrome",
        cookiefile="/tmp/cookies.txt",
    )

    assert captured["proxy"] == "http://127.0.0.1:7890"
    assert captured["cookiefile"] == "/tmp/cookies.txt"
    assert captured["cookiesfrombrowser"] == ("chrome", None, None, None)
    assert result is not None
    assert result.get("title") == "视频标题"


def test_extract_video_result_via_cli_reads_downloaded_subtitle_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "subs"
    output_dir.mkdir()
    subtitle_path = output_dir / "video.zh-Hans.vtt"
    subtitle_path.write_text(
        "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n第一句\n\n00:00:01.000 --> 00:00:02.000\n第二句\n",
        encoding="utf-8",
    )

    commands: list[list[str]] = []

    class _Completed:
        def __init__(self, stdout: str = "") -> None:
            self.stdout = stdout

    def fake_run(command: list[str], check: bool, capture_output: bool, text: bool) -> _Completed:
        commands.append(command)
        if "--dump-single-json" in command:
            return _Completed('{"id":"vid123","title":"测试视频","webpage_url":"https://example.com/watch?v=1","extractor_key":"Youtube","duration":12}')
        return _Completed("")

    class _TempDir:
        def __enter__(self) -> str:
            return str(output_dir)

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

    monkeypatch.setattr(video_module, "subprocess", types.SimpleNamespace(run=fake_run), raising=False)
    monkeypatch.setattr(video_module.tempfile, "TemporaryDirectory", lambda: _TempDir())

    result = video_module._extract_video_result_via_cli(
        url="https://www.youtube.com/watch?v=OFfwN23hR8U",
        max_chars=1000,
        proxy="http://127.0.0.1:7890",
        cookies_from_browser="chrome",
        cookiefile="/tmp/cookies.txt",
    )

    assert result is not None
    assert result.get("title") == "测试视频"
    assert "第一句" in str(result.get("content") or "")
    assert result.get("video_metadata") == {
        "extractor": "Youtube",
        "video_id": "vid123",
        "duration": 12,
        "language": "zh-Hans",
        "subtitle_source": "subtitles",
        "subtitle_ext": "vtt",
    }
    assert any("--cookies-from-browser" in command for command in commands)
