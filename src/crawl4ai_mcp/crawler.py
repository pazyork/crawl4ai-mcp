from __future__ import annotations

import asyncio
import json
import random
import re
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Any, Optional, Union
from urllib.parse import urlparse

import httpx
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, ProxyConfig
from crawl4ai.cache_context import CacheMode

from .config import Settings
from .types import build_result_dict


@dataclass(frozen=True)
class FetchOptions:
    format: str
    max_chars: int


def _load_storage_state(path: Optional[str]) -> Optional[dict[str, Any]]:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"cookies_json not found: {path}")
    return json.loads(p.read_text(encoding="utf-8"))


def _scroll_js(max_steps: int, step_wait_ms: int) -> str:
    return f"""
(() => {{
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  return (async () => {{
    let last = 0;
    for (let i = 0; i < {max_steps}; i++) {{
      window.scrollTo(0, document.body.scrollHeight);
      await sleep({step_wait_ms});
      const h = document.body.scrollHeight;
      if (h === last) break;
      last = h;
    }}
    window.scrollTo(0, 0);
  }})();
}})();
""".strip()


def _domain_overrides(url: str) -> dict[str, Any]:
    host = urlparse(url).netloc.lower()
    if "medium.com" in host:
        return {
            "wait_for_fast": "css:article",
            "wait_for_hard": "css:article",
            "page_timeout": 80_000,
            "css_selector_hard": "article",
        }
    if "code.claude.com" in host:
        return {
            "wait_for_fast": "body",
            "wait_for_hard": "body",
            "page_timeout": 80_000,
            "css_selector_hard": "#content-area",
        }
    if "producthunt.com" in host:
        return {
            "wait_for_fast": "body",
            "wait_for_hard": "body",
            "page_timeout": 60_000,
            "wait_until": "networkidle",
            "delay_before_return_html": 5.0,
            "cloudflare_wait": True,
        }
    if "github.com" in host:
        return {
            "wait_for_fast": "body",
            "wait_for_hard": "body",
            "page_timeout": 50_000,
        }
    return {}


def _normalize_proxy_url(proxy: str) -> str:
    s = proxy.strip()
    if not s:
        raise ValueError("proxy must not be empty")
    if s.isdigit():
        return f"http://127.0.0.1:{s}"
    if s.startswith("socket5://"):
        return "socks5://" + s[len("socket5://") :]
    if "://" not in s:
        if re.fullmatch(r"[^:/\s]+:\d+", s):
            return f"http://{s}"
        raise ValueError("proxy must start with http://, https://, socks5://, or socks5h://")
    parsed = urlparse(s)
    if parsed.scheme not in {"http", "https", "socks5", "socks5h"}:
        raise ValueError("proxy must start with http://, https://, socks5://, or socks5h://")
    return s


def _build_proxy_config(proxy: Optional[str]) -> Optional[ProxyConfig]:
    if not proxy:
        return None
    return ProxyConfig(server=_normalize_proxy_url(proxy))


def _normalize_links(raw: Any) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    if raw is None:
        return out
    if isinstance(raw, dict):
        for _, v in raw.items():
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        href = item.get("href") or item.get("url")
                        text = item.get("text") or item.get("title") or ""
                        if href:
                            out.append({"text": str(text)[:200], "url": str(href)})
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                href = item.get("href") or item.get("url")
                text = item.get("text") or item.get("title") or ""
                if href:
                    out.append({"text": str(text)[:200], "url": str(href)})
    seen: set[tuple[str, str]] = set()
    dedup: list[dict[str, str]] = []
    for link in out:
        key = (link.get("text", ""), link.get("url", ""))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(link)
    return dedup


def _pick_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    try:
        return str(v)
    except Exception:
        return ""


def _pick_markdown(result: Any) -> str:
    v2 = getattr(result, "markdown_v2", None)
    if v2 is not None:
        for attr in ("fit_markdown", "markdown_with_citations", "raw_markdown", "markdown"):
            s = _pick_str(getattr(v2, attr, None))
            if s.strip():
                return s

    md = getattr(result, "markdown", None)
    if md is not None and not isinstance(md, str):
        for attr in ("fit_markdown", "raw_markdown", "markdown"):
            s = _pick_str(getattr(md, attr, None))
            if s.strip():
                return s
    s = _pick_str(md)
    return s


def _pick_html(result: Any) -> str:
    return _pick_str(getattr(result, "html", None))


def _extract_title_from_html(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    raw = m.group(1)
    raw = re.sub(r"\s+", " ", raw)
    t = unescape(raw).strip()
    return t


def _extract_title_from_markdown(md: str) -> str:
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return ""


async def _extract_title_via_http(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            return _extract_title_from_html(r.text)
    except Exception:
        return ""


def _need_stronger_attempt(url: str, content: str) -> bool:
    host = urlparse(url).netloc.lower()
    if not content.strip():
        return True
    hard_hosts = ("medium.com", "code.claude.com", "github.com")
    if any(x in host for x in hard_hosts):
        return len(content.strip()) < 800
    return False


def _looks_like_interstitial(content: str) -> bool:
    s = content.strip()
    if not s:
        return True
    markers = (
        "当前环境异常",
        "完成验证后即可继续访问",
        "去验证",
        "请开启 JavaScript",
        "Access Denied",
        "执行安全验证",
        "正在等待",
        "Cloudflare",
    )
    return any(m in s for m in markers)


def _trim_to_first_h1(md: str) -> str:
    lines = md.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("# "):
            return "\n".join(lines[i:]).lstrip()
    return md


def _ensure_title_h1(md: str, title: Optional[str]) -> str:
    if not title:
        return md
    s = md.lstrip()
    if s.startswith("# "):
        return md
    return f"# {title}\n\n{md.lstrip()}"


def _remove_data_image_lines(md: str) -> str:
    out: list[str] = []
    for line in md.splitlines():
        s = line.strip()
        if "data:image/svg+xml" in s and s.startswith("!"):
            continue
        out.append(line)
    return "\n".join(out)


def _strip_html_comments(md: str) -> str:
    return re.sub(r"<!--.*?-->", "", md, flags=re.DOTALL)


def _strip_zero_width(md: str) -> str:
    return md.replace("\u200b", "").replace("\ufeff", "")


def _clean_medium_markdown(md: str) -> str:
    drop_exact = {
        "Follow",
        "Subscribe",
        "Listen",
        "Share",
        "Remember me for faster sign in",
    }
    out: list[str] = []
    for line in md.splitlines():
        s = line.strip()
        if s in drop_exact:
            continue
        if "medium.com/m/signin" in s or "/m/signin" in s:
            continue
        if s.startswith("## Get ") and "stories in your inbox" in s:
            continue
        if s.startswith("Join Medium"):
            continue
        out.append(line)
    return "\n".join(out)


def _remove_markdown_links_to_domain(md: str, domain: str) -> str:
    pattern = rf"\[([^\]]*)\]\(https?://{re.escape(domain)}/[^)]+\)"

    def repl(m: re.Match[str]) -> str:
        txt = m.group(1)
        return txt if txt.strip() else ""

    return re.sub(pattern, repl, md)


def _extract_image_urls_from_html(html: str) -> list[str]:
    urls: list[str] = []
    for m in re.finditer(r"<img\b[^>]*>", html, flags=re.IGNORECASE):
        tag = m.group(0)
        m2 = re.search(r'\bdata-src\s*=\s*"([^"]+)"', tag, flags=re.IGNORECASE)
        if not m2:
            m2 = re.search(r'\bsrc\s*=\s*"([^"]+)"', tag, flags=re.IGNORECASE)
        if not m2:
            continue
        u = m2.group(1).strip()
        if not u:
            continue
        if u.startswith("data:image"):
            continue
        urls.append(u)
    out: list[str] = []
    seen: set[str] = set()
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def _squeeze_blank_lines(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    blank = False
    for line in lines:
        if line.strip() == "":
            if blank:
                continue
            blank = True
            out.append("")
        else:
            blank = False
            out.append(line.rstrip())
    return "\n".join(out).strip() + "\n"


class CrawlService:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._crawler: Optional[AsyncWebCrawler] = None

    async def __aenter__(self) -> CrawlService:
        if self._crawler is not None:
            return self
        storage_state = _load_storage_state(self._settings.cookies_json)
        vw = random.randint(
            min(self._settings.viewport_width_min, self._settings.viewport_width_max),
            max(self._settings.viewport_width_min, self._settings.viewport_width_max),
        )
        vh = random.randint(
            min(self._settings.viewport_height_min, self._settings.viewport_height_max),
            max(self._settings.viewport_height_min, self._settings.viewport_height_max),
        )
        proxy_config = _build_proxy_config(self._settings.proxy)
        browser_kwargs: dict[str, Any] = {
            "headless": self._settings.headless,
            "storage_state": storage_state,
            "use_persistent_context": self._settings.use_persistent_context,
            "viewport_width": vw,
            "viewport_height": vh,
        }
        if proxy_config:
            browser_kwargs["proxy_config"] = proxy_config
        if self._settings.user_data_dir:
            browser_kwargs["user_data_dir"] = self._settings.user_data_dir
        if self._settings.user_agent:
            browser_kwargs["user_agent"] = self._settings.user_agent
        else:
            browser_kwargs["user_agent_mode"] = "random"

        if self._settings.accept_language:
            browser_kwargs["headers"] = {"Accept-Language": self._settings.accept_language}

        browser_kwargs["extra_args"] = [
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
            "--disable-site-isolation-trials",
            "--disable-web-security",
            "--disable-features=BlockInsecurePrivateNetworkRequests",
        ]
        browser_kwargs["ignore_https_errors"] = True
        browser_cfg = BrowserConfig(**browser_kwargs)
        self._crawler = AsyncWebCrawler(config=browser_cfg)
        await self._crawler.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._crawler is None:
            return
        await self._crawler.__aexit__(exc_type, exc, tb)
        self._crawler = None

    async def fetch(self, *, url: str, options: FetchOptions) -> dict[str, object]:
        if self._crawler is None:
            raise RuntimeError("Crawler not started")

        async def run_with_retries(cfg: CrawlerRunConfig) -> Any:
            retries = max(0, int(self._settings.max_retries))
            last = None
            for i in range(retries + 1):
                try:
                    last = await self._crawler.arun(url=url, config=cfg)
                    if getattr(last, "success", False):
                        return last
                except Exception as e:
                    last = e
                if i < retries:
                    await asyncio.sleep(min(1.0 * (2**i), 4.0))
            if isinstance(last, Exception):
                raise last
            return last

        overrides = _domain_overrides(url)
        wait_for_fast = overrides.get("wait_for_fast", "body")
        wait_for_hard = overrides.get("wait_for_hard", wait_for_fast)
        css_selector_hard = overrides.get("css_selector_hard")
        page_timeout = int(overrides.get("page_timeout", self._settings.navigation_timeout_ms))
        wait_until = str(overrides.get("wait_until", self._settings.wait_until))
        wait_for_images = bool(overrides.get("wait_for_images", False))
        delay_before_return_html = float(
            overrides.get("delay_before_return_html", self._settings.page_wait_ms / 1000.0)
        )
        cloudflare_wait = bool(overrides.get("cloudflare_wait", False))
        
        # Extra delay for Cloudflare-protected sites
        if cloudflare_wait or self._settings.cloudflare_bypass:
            delay_before_return_html = max(delay_before_return_html, 5.0)
            wait_until = "networkidle"

        mean_delay = max(0.0, float(self._settings.mean_delay_s))
        max_jitter = max(0.0, float(self._settings.max_delay_jitter_s))
        mean_delay = mean_delay + random.random() * (mean_delay * 0.6)
        max_jitter = max_jitter + random.random() * (max_jitter * 0.6)

        fast_cfg = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            stream=False,
            wait_until=wait_until,
            wait_for=wait_for_fast,
            page_timeout=page_timeout,
            magic=self._settings.magic,
            remove_overlay_elements=True,
            wait_for_images=wait_for_images,
            delay_before_return_html=delay_before_return_html,
            excluded_tags=["nav", "header", "footer", "aside"],
            word_count_threshold=10,
            locale=self._settings.locale,
            timezone_id=self._settings.timezone_id,
            mean_delay=mean_delay,
            max_range=max_jitter,
            override_navigator=True,
        )

        res = await run_with_retries(fast_cfg)
        last_err = None
        if not getattr(res, "success", False):
            last_err = getattr(res, "error_message", None)
            res = None

        if res is None or not getattr(res, "success", False):
            msg = last_err or "crawl failed"
            hard_cfg = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                stream=False,
                wait_for=wait_for_hard,
                page_timeout=page_timeout,
                wait_until=wait_until,
                scan_full_page=True,
                scroll_delay=max(0.2, self._settings.scroll_step_wait_ms / 1000.0),
                magic=True,
                simulate_user=True,
                override_navigator=True,
                remove_overlay_elements=True,
                wait_for_images=wait_for_images,
                delay_before_return_html=max(0.2, delay_before_return_html),
                excluded_tags=["nav", "header", "footer", "aside"],
                word_count_threshold=10,
                locale=self._settings.locale,
                timezone_id=self._settings.timezone_id,
                mean_delay=mean_delay,
                max_range=max_jitter,
            )
            res = await run_with_retries(hard_cfg)
            if not getattr(res, "success", False):
                raise RuntimeError(msg)

        final_url = getattr(res, "url", None) or url
        title = getattr(res, "title", None)
        html = _pick_html(res)
        md = _pick_markdown(res)

        if css_selector_hard:
            extract_cfg = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                stream=False,
                wait_until=wait_until,
                wait_for=wait_for_hard,
                page_timeout=page_timeout,
                magic=self._settings.magic,
                remove_overlay_elements=True,
                wait_for_images=wait_for_images,
                delay_before_return_html=delay_before_return_html,
                excluded_tags=["nav", "header", "footer", "aside"],
                word_count_threshold=10,
                css_selector=css_selector_hard,
                locale=self._settings.locale,
                timezone_id=self._settings.timezone_id,
                mean_delay=mean_delay,
                max_range=max_jitter,
            )
            res_extract = await run_with_retries(extract_cfg)
            if getattr(res_extract, "success", False):
                md2 = _pick_markdown(res_extract)
                if md2.strip():
                    md = md2

        content_format = options.format
        if content_format == "html":
            content = html
        else:
            content = md or html
            content_format = "markdown" if md else "html"

        if _need_stronger_attempt(url, content) and getattr(res, "success", False):
            hard_cfg = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                stream=False,
                wait_for=wait_for_hard,
                page_timeout=page_timeout,
                wait_until=wait_until,
                scan_full_page=True,
                scroll_delay=max(0.2, self._settings.scroll_step_wait_ms / 1000.0),
                magic=True,
                simulate_user=True,
                override_navigator=True,
                remove_overlay_elements=True,
                wait_for_images=wait_for_images,
                delay_before_return_html=max(0.2, delay_before_return_html),
                excluded_tags=["nav", "header", "footer", "aside"],
                word_count_threshold=10,
                locale=self._settings.locale,
                timezone_id=self._settings.timezone_id,
                mean_delay=mean_delay,
                max_range=max_jitter,
            )
            res2 = await run_with_retries(hard_cfg)
            if getattr(res2, "success", False):
                final_url = getattr(res2, "url", None) or final_url
                title = getattr(res2, "title", None) or title
                html = _pick_html(res2) or html
                md = _pick_markdown(res2) or md
                if content_format == "html":
                    content = html
                else:
                    content = md or html
                    content_format = "markdown" if md else "html"

        if not isinstance(title, str) or not title.strip():
            t = _extract_title_from_html(html) if html else ""
            if not t and md:
                t = _extract_title_from_markdown(md)
            if not t:
                t = await _extract_title_via_http(final_url)
            title = t or None

        if content_format == "markdown":
            host = urlparse(final_url).netloc.lower()
            if "medium.com" in host:
                content = _trim_to_first_h1(content)
            content = _ensure_title_h1(content, title)
            content = _strip_html_comments(content)
            content = _strip_zero_width(content)
            content = _remove_data_image_lines(content)
            if "medium.com" in host:
                content = _clean_medium_markdown(content)
            content = _squeeze_blank_lines(content)

        if options.max_chars > 0 and len(content) > options.max_chars:
            content = content[: options.max_chars]

        raw_links = getattr(res, "links", None)
        links = _normalize_links(raw_links)

        result = build_result_dict(
            url=url,
            final_url=final_url,
            title=title,
            content=content,
            content_format=content_format,
            links=links,
        )
        if _looks_like_interstitial(content):
            result["blocked"] = True
        return result

    async def search(
        self,
        *,
        query: str,
        engine: str = "auto",
        max_results: int = 10,
        lang: str = "",
    ) -> dict[str, object]:
        from .searcher import search_with_fallback

        # Validate parameters
        if not query or not query.strip():
            raise ValueError("query must not be empty")
        if max_results < 1 or max_results > 100:
            raise ValueError("max_results must be between 1 and 100")

        proxy = _normalize_proxy_url(self._settings.proxy) if self._settings.proxy else None
        response = await search_with_fallback(
            query=query,
            engine=engine,
            max_results=max_results,
            lang=lang,
            proxy=proxy,
        )
        return response.to_dict()


async def fetch_many(
    *,
    service: CrawlService,
    urls: list[str],
    options: FetchOptions,
    concurrency: int,
) -> list[Union[dict[str, object], dict[str, str]]]:
    sem = asyncio.Semaphore(max(1, concurrency))

    async def one(u: str) -> Union[dict[str, object], dict[str, str]]:
        async with sem:
            try:
                return await service.fetch(url=u, options=options)
            except Exception as e:
                return {"url": u, "error": str(e)}

    return await asyncio.gather(*(one(u) for u in urls))
