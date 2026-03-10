from __future__ import annotations

from crawl4ai_mcp.crawler import _ensure_title_h1, _looks_like_interstitial, _trim_to_first_h1


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
