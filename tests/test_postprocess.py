from __future__ import annotations

from crawl4ai_mcp.crawler import (
    _ensure_title_h1,
    _extract_image_urls_from_html,
    _looks_like_interstitial,
    _remove_data_image_lines,
    _remove_markdown_links_to_domain,
    _squeeze_blank_lines,
    _trim_to_first_h1,
)


def test_looks_like_interstitial() -> None:
    assert _looks_like_interstitial("当前环境异常\n去验证")
    assert _looks_like_interstitial("Access Denied")
    assert not _looks_like_interstitial("# Title\n\nHello world")


def test_trim_to_first_h1() -> None:
    md = "intro\nmore\n# Title\n\nbody"
    assert _trim_to_first_h1(md).startswith("# Title\n\nbody")


def test_ensure_title_h1() -> None:
    md = "hello"
    assert _ensure_title_h1(md, "T").startswith("# T\n\n")
    assert _ensure_title_h1("# Already\n\nX", "T").startswith("# Already")


def test_remove_data_image_lines() -> None:
    md = "a\n![x](data:image/svg+xml,abc)\n![](data:image/svg+xml,def)\nB"
    out = _remove_data_image_lines(md)
    assert "data:image/svg+xml" not in out
    assert out.splitlines() == ["a", "B"]


def test_squeeze_blank_lines() -> None:
    md = "a\n\n\n\nB\n\n"
    assert _squeeze_blank_lines(md) == "a\n\nB\n"


def test_remove_markdown_links_to_domain() -> None:
    md = "a [X](https://zhida.zhihu.com/search?q=1) b"
    assert _remove_markdown_links_to_domain(md, "zhida.zhihu.com") == "a X b"


def test_extract_image_urls_from_html() -> None:
    html = '<img data-src="https://a.com/1.png"/><img src="data:image/png,abc"/><img src="https://b.com/2.jpg">'
    assert _extract_image_urls_from_html(html) == ["https://a.com/1.png", "https://b.com/2.jpg"]
