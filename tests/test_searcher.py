from __future__ import annotations

import pytest

from crawl4ai_mcp.searcher import (
    SearchResult,
    _build_headers,
    _is_blocked,
    _normalize_url,
    deduplicate,
    parse_search_html,
    resolve_engine_plan,
)

BING_SAMPLE = """
<html><body>
<ol id="b_results">
  <li class="b_algo">
    <h2><a href="https://docs.crawl4ai.com/">Crawl4AI Docs</a></h2>
    <div class="b_caption"><p>Open-source LLM-friendly web crawler.</p></div>
  </li>
  <li class="b_algo">
    <h2><a href="https://github.com/unclecode/crawl4ai">GitHub - crawl4ai</a></h2>
    <div class="b_caption"><p>Star the repo on GitHub.</p></div>
  </li>
</ol>
</body></html>
"""

DDG_SAMPLE = """
<html><body>
  <div class="result">
    <a class="result__a" href="https://duckduckgo.com/l/?uddg=https%3A%2F%2Fdocs.crawl4ai.com%2F">Crawl4AI Docs</a>
    <div class="result__snippet">Open-source LLM-friendly web crawler.</div>
  </div>
  <div class="result">
    <a class="result__a" href="https://duckduckgo.com/l/?uddg=https%3A%2F%2Fgithub.com%2Funclecode%2Fcrawl4ai">GitHub crawl4ai</a>
    <div class="result__snippet">Star the repo.</div>
  </div>
</body></html>
"""

SOGOU_SAMPLE = """
<html><body>
  <div class="vrwrap">
    <h3><a href="https://docs.crawl4ai.com/">Crawl4AI 文档</a></h3>
    <p class="str-info">开源 LLM 友好的网页爬虫。</p>
  </div>
  <div class="vrwrap">
    <h3><a href="https://github.com/unclecode/crawl4ai">GitHub - crawl4ai</a></h3>
    <p class="str-info">在 GitHub 上 Star 这个项目。</p>
  </div>
</body></html>
"""

SO360_SAMPLE = """
<html><body>
  <li class="res-list">
    <h3><a href="https://www.so.com/link?m=abc" data-mdurl="https://docs.crawl4ai.com/">Crawl4AI 文档</a></h3>
    <span class="res-list-summary">开源爬虫框架。</span>
  </li>
  <li class="res-list">
    <h3><a href="https://www.so.com/link?m=xyz" data-mdurl="https://github.com/unclecode/crawl4ai">GitHub crawl4ai</a></h3>
    <span class="res-list-summary">Star 这个项目。</span>
  </li>
</body></html>
"""


def test_parse_bing():
    results = parse_search_html("bing", BING_SAMPLE, 10)
    assert len(results) == 2
    assert results[0].url == "https://docs.crawl4ai.com/"
    assert "Crawl4AI" in results[0].title
    assert "crawler" in results[0].snippet


def test_parse_duckduckgo():
    results = parse_search_html("duckduckgo", DDG_SAMPLE, 10)
    assert len(results) == 2
    assert results[0].url == "https://docs.crawl4ai.com/"
    assert results[0].engine == "duckduckgo"


def test_parse_sogou():
    results = parse_search_html("sogou", SOGOU_SAMPLE, 10)
    assert len(results) == 2
    assert results[0].url == "https://docs.crawl4ai.com/"
    assert "爬虫" in results[0].snippet


def test_parse_so360():
    results = parse_search_html("so360", SO360_SAMPLE, 10)
    assert len(results) == 2
    assert results[0].url == "https://docs.crawl4ai.com/"


def test_parse_max_results():
    results = parse_search_html("bing", BING_SAMPLE, 1)
    assert len(results) == 1


def test_deduplicate_by_url():
    items = [
        SearchResult(title="A", url="https://example.com/page", snippet=""),
        SearchResult(title="A copy", url="https://example.com/page/", snippet=""),
        SearchResult(title="B", url="https://other.com/", snippet=""),
    ]
    out = deduplicate(items)
    assert len(out) == 2
    assert out[0].url == "https://example.com/page"


def test_deduplicate_by_title_similarity():
    items = [
        SearchResult(title="Crawl4AI Documentation", url="https://a.com/", snippet=""),
        SearchResult(title="Crawl4AI Documentation Page", url="https://b.com/", snippet=""),
        SearchResult(title="Totally Different Result", url="https://c.com/", snippet=""),
    ]
    out = deduplicate(items, title_threshold=0.85)
    assert len(out) == 2
    assert out[-1].title == "Totally Different Result"


def test_normalize_url():
    assert _normalize_url("https://example.com/path/") == "https://example.com/path"
    assert _normalize_url("https://example.com/path") == "https://example.com/path"


def test_is_blocked():
    assert _is_blocked("Please complete the CAPTCHA to continue")
    assert _is_blocked("Unusual traffic from your network")
    assert _is_blocked("请输入验证码")
    assert not _is_blocked("Welcome to our website")


def test_build_headers_rotates_ua():
    seen = set()
    for _ in range(20):
        h = _build_headers("bing", "en")
        seen.add(h["user-agent"])
    assert len(seen) > 1


def test_build_headers_chinese_engines():
    h = _build_headers("baidu", "")
    assert "zh-CN" in h["accept-language"]
    h2 = _build_headers("bing", "")
    assert "en-US" in h2["accept-language"]


def test_resolve_engine_plan_auto_english():
    plan = resolve_engine_plan("auto", "python web scraping", "en")
    assert plan[0] in ("duckduckgo", "bing", "google", "yandex")
    assert "sogou" in plan
    assert "so360" in plan


def test_resolve_engine_plan_auto_chinese():
    plan = resolve_engine_plan("auto", "AI Agent 开发框架", "")
    assert plan[0] in ("sogou", "so360", "baidu")
    assert "bing" in plan


def test_resolve_engine_plan_specific():
    plan = resolve_engine_plan("google", "test", "en")
    assert plan[0] == "google"
    assert len(plan) > 1


def test_parse_unknown_engine():
    with pytest.raises(ValueError, match="No parser"):
        parse_search_html("unknown_engine", "<html></html>", 10)
