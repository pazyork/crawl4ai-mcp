from __future__ import annotations

from crawl4ai.async_configs import ProxyConfig

from crawl4ai_mcp.config import Settings
from crawl4ai_mcp.crawler import _build_proxy_config


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.navigation_timeout_ms == 30_000
    assert settings.wait_until == "load"


def test_build_proxy_config_accepts_http_and_socks5() -> None:
    assert isinstance(_build_proxy_config("http://127.0.0.1:8080"), ProxyConfig)
    assert _build_proxy_config("http://127.0.0.1:8080").server == "http://127.0.0.1:8080"
    assert _build_proxy_config("socks5://127.0.0.1:1080").server == "socks5://127.0.0.1:1080"
    assert _build_proxy_config("127.0.0.1:7890").server == "http://127.0.0.1:7890"
    assert _build_proxy_config("7890").server == "http://127.0.0.1:7890"
    assert _build_proxy_config("socket5://127.0.0.1:7890").server == "socks5://127.0.0.1:7890"


def test_build_proxy_config_rejects_unsupported_scheme() -> None:
    try:
        _build_proxy_config("ftp://127.0.0.1:21")
    except ValueError as exc:
        assert "proxy must start with http://, https://, socks5://, or socks5h://" in str(exc)
    else:
        raise AssertionError("unsupported proxy scheme should raise ValueError")
