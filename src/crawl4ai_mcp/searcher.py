from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Any, Optional
from urllib.parse import quote_plus, unquote, urlencode, urlparse

from .types import now_iso


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str

    def to_dict(self) -> dict[str, str]:
        return {"title": self.title, "url": self.url, "snippet": self.snippet}


@dataclass(frozen=True)
class SearchResponse:
    engine: str
    query: str
    results: list[SearchResult]
    fallback_engines: list[str] = field(default_factory=list)
    extracted_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, object]:
        d: dict[str, object] = {
            "engine": self.engine,
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total": len(self.results),
            "extracted_at": self.extracted_at,
        }
        if self.fallback_engines:
            d["fallback_engines_tried"] = self.fallback_engines
        return d


FALLBACK_ORDER = ("duckduckgo", "bing", "google", "baidu")

SUPPORTED_ENGINES = FALLBACK_ORDER


def build_search_url(engine: str, query: str, num: int = 10, **kwargs: Any) -> str:
    q = quote_plus(query)
    lang = kwargs.get("lang", "")

    if engine == "google":
        params: dict[str, Any] = {"q": query, "num": num}
        if lang:
            params["hl"] = lang
        return "https://www.google.com/search?" + urlencode(params)

    if engine == "bing":
        params = {"q": query, "count": num}
        return "https://www.bing.com/search?" + urlencode(params)

    if engine == "baidu":
        params = {"wd": query, "rn": num}
        return "https://www.baidu.com/s?" + urlencode(params)

    if engine == "duckduckgo":
        return f"https://html.duckduckgo.com/html/?q={q}"

    raise ValueError(
        f"Unsupported engine: {engine}. Use: {', '.join(SUPPORTED_ENGINES)}"
    )


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    s = re.sub(r"\s+", " ", text).strip()
    s = re.sub(r"^(Ad|广告|推广)\s*[·|]\s*", "", s)
    return s


def _is_ad(el_text: str) -> bool:
    ad_markers = ("Ad ·", "广告", "推广", "Sponsored")
    return any(m in el_text for m in ad_markers)


def _abs_url(href: str, base: str) -> Optional[str]:
    if not href or href.startswith("javascript:") or href.startswith("#"):
        return None
    if href.startswith("http"):
        return href
    parsed = urlparse(base)
    return f"{parsed.scheme}://{parsed.netloc}{href}"


def _extract_ddg_url(href: str) -> Optional[str]:
    if "duckduckgo.com/l/?" in href:
        m = re.search(r"uddg=([^&]+)", href)
        if m:
            return unquote(m.group(1))
    return href if href.startswith("http") else None


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = unquote(parsed.path.rstrip("/") or "/")
    return f"{parsed.scheme}://{parsed.netloc}{path}"


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(
    results: list[SearchResult],
    title_threshold: float = 0.85,
) -> list[SearchResult]:
    seen_urls: set[str] = set()
    seen_titles: list[str] = []
    unique: list[SearchResult] = []

    for r in results:
        norm = _normalize_url(r.url)
        if norm in seen_urls:
            continue

        low_title = r.title.lower()
        if any(
            SequenceMatcher(None, low_title, t).ratio() > title_threshold
            for t in seen_titles
        ):
            continue

        seen_urls.add(norm)
        seen_titles.append(low_title)
        unique.append(r)

    return unique


# ---------------------------------------------------------------------------
# CSS selectors per engine
# ---------------------------------------------------------------------------

_GOOGLE_SELECTORS = {
    "container": "#search .g, #rso .g",
    "title": "h3",
    "link": "a[href]",
    "snippet": "[data-sncf], .VwiC3b, .lEBKkf, .st",
}

_BING_SELECTORS = {
    "container": "#b_results > li.b_algo",
    "title": "h2 a",
    "link": "h2 a[href]",
    "snippet": ".b_caption p, .b_algoSlug",
}

_BAIDU_SELECTORS = {
    "container": "#content_left .result, #content_left .c-container",
    "title": "h3 a, .c-title a",
    "link": "h3 a[href], .c-title a[href]",
    "snippet": ".c-abstract, .content-right_8Zs40, .c-span-last",
}

_DDG_SELECTORS = {
    "container": ".result, .web-result",
    "title": ".result__a, .result__title a",
    "link": ".result__a[href], .result__title a[href]",
    "snippet": ".result__snippet",
}

ENGINE_SELECTORS = {
    "google": _GOOGLE_SELECTORS,
    "bing": _BING_SELECTORS,
    "baidu": _BAIDU_SELECTORS,
    "duckduckgo": _DDG_SELECTORS,
}


# ---------------------------------------------------------------------------
# Playwright page → structured results
# ---------------------------------------------------------------------------

async def parse_search_results(
    page: Any,
    engine: str,
    query: str,
    max_results: int = 10,
) -> SearchResponse:
    sels = ENGINE_SELECTORS.get(engine)
    if not sels:
        raise ValueError(f"No parser for engine: {engine}")

    results: list[SearchResult] = []
    containers = await page.query_selector_all(sels["container"])

    for el in containers:
        if len(results) >= max_results:
            break

        title_el = await el.query_selector(sels["title"])
        link_el = await el.query_selector(sels["link"])
        snippet_el = await el.query_selector(sels["snippet"])

        if not title_el or not link_el:
            continue

        title = _clean(await title_el.inner_text())
        href = await link_el.get_attribute("href") or ""
        snippet = _clean(await snippet_el.inner_text()) if snippet_el else ""

        if not title:
            continue

        full_text = await el.inner_text()
        if _is_ad(full_text):
            continue

        if engine == "duckduckgo":
            url = _extract_ddg_url(href)
        else:
            base_url = page.url if isinstance(page.url, str) else str(page.url)
            url = _abs_url(href, base_url)

        if not url or not url.startswith("http"):
            continue

        search_host = urlparse(build_search_url(engine, "")).netloc
        if urlparse(url).netloc == search_host:
            continue

        results.append(SearchResult(title=title, url=url, snippet=snippet))

    return SearchResponse(
        engine=engine, query=query, results=deduplicate(results)
    )


# ---------------------------------------------------------------------------
# Markdown fallback parser (when Playwright page object is unavailable)
# ---------------------------------------------------------------------------

def parse_search_from_markdown(
    md: str, engine: str, query: str, max_results: int
) -> SearchResponse:
    results: list[SearchResult] = []
    link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    lines = md.splitlines()
    search_domains = ("google.", "bing.com", "baidu.com", "duckduckgo.com")

    i = 0
    while i < len(lines) and len(results) < max_results:
        m = link_pattern.search(lines[i])
        if m:
            title = m.group(1).strip()
            url = m.group(2).strip()
            host = urlparse(url).netloc.lower()
            if not any(d in host for d in search_domains) and len(title) > 5:
                snippet = ""
                for j in range(i + 1, min(i + 4, len(lines))):
                    line = lines[j].strip()
                    if line and not line.startswith("[") and not line.startswith("#"):
                        snippet = line[:300]
                        break
                results.append(SearchResult(title=title, url=url, snippet=snippet))
        i += 1

    return SearchResponse(
        engine=engine, query=query, results=deduplicate(results)
    )
