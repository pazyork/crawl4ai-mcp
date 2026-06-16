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
    # Strong markers — always blocked
    assert _looks_like_interstitial("当前环境异常\n去验证")
    assert _looks_like_interstitial("Access Denied")
    assert _looks_like_interstitial("执行安全验证\n验证成功。正在等待 www.producthunt.com 响应")
    assert _looks_like_interstitial("Checking your browser before accessing the site")
    assert _looks_like_interstitial("Just a moment... Cloudflare")
    assert _looks_like_interstitial("Verify you are human")
    # Weak markers on short content — need >= 2 co-occurring
    assert _looks_like_interstitial("去验证\nCloudflare\n正在等待")
    # NOT blocked: normal long page with incidental "Cloudflare" (P0-1 regression)
    github_page = "# GitHub - openclaw/openclaw\n\nSome real content here...\n\n© 2024 GitHub, Inc.\nProtected by Cloudflare\n"
    assert not _looks_like_interstitial(github_page), "GitHub page with Cloudflare footer must not be blocked"
    # NOT blocked: normal content
    assert not _looks_like_interstitial("# Title\n\nHello world")
    # NOT blocked: long page with single weak marker
    long_page = "x" * 5000 + "Cloudflare"
    assert not _looks_like_interstitial(long_page), "Long page with single 'Cloudflare' must not be blocked"


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
