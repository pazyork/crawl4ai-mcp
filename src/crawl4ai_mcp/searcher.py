from __future__ import annotations

import asyncio
import random
import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from html import unescape
from urllib.parse import quote_plus, unquote, urlencode, urlparse

import httpx
from bs4 import BeautifulSoup

from .types import now_iso


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str
    engine: str = ""

    def to_dict(self) -> dict[str, str]:
        data = {"title": self.title, "url": self.url, "snippet": self.snippet}
        if self.engine:
            data["engine"] = self.engine
        return data


@dataclass(frozen=True)
class SearchResponse:
    engine: str
    query: str
    results: list[SearchResult]
    engines_used: list[str] = field(default_factory=list)
    extracted_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {
            "engine": self.engine,
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total": len(self.results),
            "extracted_at": self.extracted_at,
        }
        if self.engines_used:
            data["engines_used"] = self.engines_used
        return data


SUPPORTED_ENGINES = (
    "auto",
    "duckduckgo",
    "bing",
    "google",
    "baidu",
    "sogou",
    "so360",
    "yandex",
)

INTERNATIONAL_ORDER = ("duckduckgo", "bing", "google", "yandex")
CHINA_ORDER = ("sogou", "so360", "baidu", "bing")


def build_search_url(engine: str, query: str, num: int = 10, lang: str = "") -> str:
    q = quote_plus(query)
    if engine == "google":
        params: dict[str, object] = {"q": query, "num": num}
        if lang:
            params["hl"] = lang
        return "https://www.google.com/search?" + urlencode(params)
    if engine == "bing":
        return "https://www.bing.com/search?" + urlencode({"q": query, "count": num})
    if engine == "duckduckgo":
        return f"https://html.duckduckgo.com/html/?q={q}"
    if engine == "baidu":
        return "https://www.baidu.com/s?" + urlencode({"wd": query, "rn": num})
    if engine == "sogou":
        return f"https://www.sogou.com/web?query={q}"
    if engine == "so360":
        return f"https://www.so.com/s?q={q}"
    if engine == "yandex":
        return f"https://yandex.com/search/?text={q}"
    raise ValueError(f"Unsupported engine: {engine}. Use: {', '.join(SUPPORTED_ENGINES)}")


def resolve_engine_plan(engine: str, query: str, lang: str = "") -> list[str]:
    if engine != "auto":
        plan = [engine]
        if engine in CHINA_ORDER:
            plan.extend([x for x in CHINA_ORDER if x != engine])
            plan.extend([x for x in INTERNATIONAL_ORDER if x not in plan])
        else:
            plan.extend([x for x in INTERNATIONAL_ORDER if x != engine])
            plan.extend([x for x in CHINA_ORDER if x not in plan])
        return plan
    if lang.lower().startswith("zh") or re.search(r"[\u4e00-\u9fff]", query):
        return list(CHINA_ORDER) + [x for x in INTERNATIONAL_ORDER if x not in CHINA_ORDER]
    return list(INTERNATIONAL_ORDER) + [x for x in CHINA_ORDER if x not in INTERNATIONAL_ORDER]


def _clean_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"^(Ad|广告|推广|Sponsored)\s*[·|:-]?\s*", "", text)


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = unquote(parsed.path.rstrip("/") or "/")
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def deduplicate(results: list[SearchResult], title_threshold: float = 0.85) -> list[SearchResult]:
    seen_urls: set[str] = set()
    seen_titles: list[str] = []
    out: list[SearchResult] = []
    for item in results:
        norm = _normalize_url(item.url)
        # Redirect URLs (sogou /link, bing /ck) are unique per result — skip URL dedup
        is_redirect = any(
            p in item.url for p in ("/link?url=", "/ck/a?", "bing.com/ck/")
        )
        if not is_redirect and norm in seen_urls:
            continue
        low = item.title.lower()
        if any(SequenceMatcher(None, low, prev).ratio() > title_threshold for prev in seen_titles):
            continue
        if not is_redirect:
            seen_urls.add(norm)
        seen_titles.append(low)
        out.append(item)
    return out


def _decode_ddg(href: str) -> str:
    m = re.search(r"uddg=([^&]+)", href)
    return unquote(m.group(1)) if m else href


def _decode_so360(href: str, data_mdurl: str | None) -> str:
    return data_mdurl or href


def _parse_duckduckgo(html_text: str, max_results: int) -> list[SearchResult]:
    soup = BeautifulSoup(html_text, "lxml")
    out: list[SearchResult] = []
    for item in soup.select(".result"):
        a = item.select_one(".result__title a, .result__a")
        if not a or not a.get("href"):
            continue
        title = _clean_text(a.get_text(" ", strip=True))
        url = _decode_ddg(a["href"])
        snippet_el = item.select_one(".result__snippet")
        snippet = _clean_text(snippet_el.get_text(" ", strip=True)) if snippet_el else ""
        if title and url.startswith("http"):
            out.append(SearchResult(title=title, url=url, snippet=snippet, engine="duckduckgo"))
        if len(out) >= max_results:
            break
    return out


def _parse_bing(html_text: str, max_results: int) -> list[SearchResult]:
    soup = BeautifulSoup(html_text, "lxml")
    out: list[SearchResult] = []
    for item in soup.select("li.b_algo"):
        a = item.select_one("h2 a")
        if not a or not a.get("href"):
            continue
        url = a["href"]
        if "bing.com/ck/" in url or "bing.com/search" in url:
            continue
        title = _clean_text(a.get_text(" ", strip=True))
        snippet_el = item.select_one(".b_caption p")
        snippet = _clean_text(snippet_el.get_text(" ", strip=True)) if snippet_el else ""
        if title and url.startswith("http"):
            out.append(SearchResult(title=title, url=url, snippet=snippet, engine="bing"))
        if len(out) >= max_results:
            break
    return out


def _parse_google(html_text: str, max_results: int) -> list[SearchResult]:
    soup = BeautifulSoup(html_text, "lxml")
    out: list[SearchResult] = []
    for item in soup.select("#search .g, #rso .g"):
        a = item.select_one("a[href]")
        h3 = item.select_one("h3")
        if not a or not h3 or not a.get("href"):
            continue
        url = a["href"]
        if url.startswith("/") or "google.com" in urlparse(url).netloc:
            continue
        title = _clean_text(h3.get_text(" ", strip=True))
        snippet_el = item.select_one(".VwiC3b, .lEBKkf, .st")
        snippet = _clean_text(snippet_el.get_text(" ", strip=True)) if snippet_el else ""
        if title:
            out.append(SearchResult(title=title, url=url, snippet=snippet, engine="google"))
        if len(out) >= max_results:
            break
    return out


def _parse_baidu(html_text: str, max_results: int) -> list[SearchResult]:
    soup = BeautifulSoup(html_text, "lxml")
    out: list[SearchResult] = []
    for item in soup.select("#content_left .result, #content_left .c-container"):
        a = item.select_one("h3 a, .c-title a")
        if not a or not a.get("href"):
            continue
        title = _clean_text(a.get_text(" ", strip=True))
        url = a["href"]
        snippet_el = item.select_one(".c-abstract, .c-span-last")
        snippet = _clean_text(snippet_el.get_text(" ", strip=True)) if snippet_el else ""
        if title and url:
            out.append(SearchResult(title=title, url=url, snippet=snippet, engine="baidu"))
        if len(out) >= max_results:
            break
    return out


def _decode_sogou_url(href: str) -> str | None:
    if href.startswith(("http://", "https://")):
        return href
    if href.startswith("/link?url="):
        return "https://www.sogou.com" + href
    return None


def _parse_sogou(html_text: str, max_results: int) -> list[SearchResult]:
    soup = BeautifulSoup(html_text, "lxml")
    out: list[SearchResult] = []
    for item in soup.select("div.vrwrap"):
        a = item.select_one("h3.vr-title a[href], h3 a[href]")
        if not a or not a.get("href"):
            continue
        url = _decode_sogou_url(a["href"])
        if not url:
            continue
        title = _clean_text(a.get_text(" ", strip=True))
        if not title or len(title) < 4:
            continue
        snippet_el = item.select_one(
            ".str-info, .str_info, .fz-mid, .text-layout, [id^='cacheresult_summary']"
        )
        snippet = _clean_text(snippet_el.get_text(" ", strip=True)) if snippet_el else ""
        out.append(SearchResult(title=title, url=url, snippet=snippet, engine="sogou"))
        if len(out) >= max_results:
            break
    return out


def _parse_so360(html_text: str, max_results: int) -> list[SearchResult]:
    soup = BeautifulSoup(html_text, "lxml")
    out: list[SearchResult] = []
    noise_hosts = {"fanyi.so.com", "www.so.com", "so.com"}
    for item in soup.select("li.res-list, div.res-rich"):
        a = item.select_one("h3 a[data-mdurl], h3 a[href], a[data-mdurl]")
        if not a:
            continue
        title = _clean_text(a.get_text(" ", strip=True))
        url = _decode_so360(a.get("href", ""), a.get("data-mdurl"))
        snippet_el = item.select_one(".res-list-summary, .g-c-gray2, p")
        snippet = _clean_text(snippet_el.get_text(" ", strip=True)) if snippet_el else ""
        if not title or not url:
            continue
        host = urlparse(url).netloc.lower()
        if host in noise_hosts or not url.startswith(("http://", "https://")):
            continue
        if title in {"必应搜索", "360搜索"}:
            continue
        out.append(SearchResult(title=title, url=url, snippet=snippet, engine="so360"))
        if len(out) >= max_results:
            break
    return out


def _parse_yandex(html_text: str, max_results: int) -> list[SearchResult]:
    soup = BeautifulSoup(html_text, "lxml")
    out: list[SearchResult] = []
    for item in soup.select(".serp-item"):
        a = item.select_one("a.Link, a.organic__url")
        if not a or not a.get("href"):
            continue
        title_el = item.select_one(".OrganicTitle-LinkText, h2")
        if title_el:
            title = _clean_text(title_el.get_text(" ", strip=True))
        else:
            title = _clean_text(a.get_text(" ", strip=True))
        url = a["href"]
        snippet_el = item.select_one(".OrganicText, .text-container")
        snippet = _clean_text(snippet_el.get_text(" ", strip=True)) if snippet_el else ""
        if title and url.startswith("http"):
            out.append(SearchResult(title=title, url=url, snippet=snippet, engine="yandex"))
        if len(out) >= max_results:
            break
    return out


PARSERS = {
    "duckduckgo": _parse_duckduckgo,
    "bing": _parse_bing,
    "google": _parse_google,
    "baidu": _parse_baidu,
    "sogou": _parse_sogou,
    "so360": _parse_so360,
    "yandex": _parse_yandex,
}


def parse_search_html(engine: str, html_text: str, max_results: int) -> list[SearchResult]:
    parser = PARSERS.get(engine)
    if not parser:
        raise ValueError(f"No parser for engine: {engine}")
    return deduplicate(parser(html_text, max_results))


_UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

_ENGINE_REFERERS: dict[str, str] = {
    "google": "https://www.google.com/",
    "bing": "https://www.bing.com/",
    "duckduckgo": "https://duckduckgo.com/",
    "baidu": "https://www.baidu.com/",
    "sogou": "https://www.sogou.com/",
    "so360": "https://www.so.com/",
    "yandex": "https://yandex.com/",
}

_BLOCKED_MARKERS = (
    "unusual traffic",
    "captcha",
    "verify you are human",
    "access denied",
    "403 forbidden",
    "too many requests",
    "robot",
    "automated queries",
    "请输入验证码",
    "安全验证",
)


def _is_blocked(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in _BLOCKED_MARKERS)


def _build_headers(engine: str, lang: str) -> dict[str, str]:
    ua = random.choice(_UA_POOL)
    accept_lang = lang or ("zh-CN,zh;q=0.9,en;q=0.8" if engine in ("baidu", "sogou", "so360") else "en-US,en;q=0.9,zh-CN;q=0.8")
    return {
        "user-agent": ua,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "accept-language": accept_lang,
        "accept-encoding": "gzip, deflate, br",
        "dnt": "1",
        "upgrade-insecure-requests": "1",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "referer": _ENGINE_REFERERS.get(engine, "https://www.google.com/"),
    }


async def fetch_engine_results(
    *,
    engine: str,
    query: str,
    max_results: int,
    lang: str,
    proxy: str | None,
    timeout: float = 20.0,
    max_retries: int = 2,
) -> list[SearchResult]:
    url = build_search_url(engine, query, num=max_results, lang=lang)
    last_exc: Exception = RuntimeError("no attempt")

    for attempt in range(max_retries + 1):
        if attempt > 0:
            await asyncio.sleep(random.uniform(1.5, 3.5))

        headers = _build_headers(engine, lang)
        try:
            async with httpx.AsyncClient(
                headers=headers,
                timeout=timeout,
                follow_redirects=True,
                proxy=proxy or None,
            ) as client:
                resp = await client.get(url)

            if resp.status_code == 429:
                raise RuntimeError(f"{engine} rate-limited (429)")
            if resp.status_code >= 400:
                raise RuntimeError(f"{engine} HTTP {resp.status_code}")

            if _is_blocked(resp.text[:2000]):
                raise RuntimeError(f"{engine} blocked (anti-bot page detected)")

            results = parse_search_html(engine, resp.text, max_results)
            if not results and attempt < max_retries:
                raise RuntimeError(f"{engine} returned 0 results, retrying")
            return results

        except (httpx.TimeoutException, httpx.ConnectError) as e:
            last_exc = RuntimeError(f"{engine} connection error: {e}")
        except RuntimeError:
            raise
        except Exception as e:
            last_exc = e

    raise last_exc


async def search_with_fallback(
    *,
    query: str,
    engine: str,
    max_results: int,
    lang: str,
    proxy: str | None,
) -> SearchResponse:
    plan = resolve_engine_plan(engine, query, lang)
    aggregate: list[SearchResult] = []
    engines_used: list[str] = []
    errors: list[str] = []

    for name in plan:
        try:
            items = await fetch_engine_results(
                engine=name,
                query=query,
                max_results=max_results,
                lang=lang,
                proxy=proxy,
            )
            if not items:
                errors.append(f"{name}: 0 results")
                continue
            engines_used.append(name)
            aggregate = deduplicate(aggregate + items)
            if len(aggregate) >= max_results:
                break
        except Exception as e:
            errors.append(f"{name}: {e}")
            continue

    if not aggregate:
        raise RuntimeError(f"All engines failed: {'; '.join(errors)}")

    return SearchResponse(
        engine="aggregated" if len(engines_used) > 1 else engines_used[0],
        query=query,
        results=aggregate[:max_results],
        engines_used=engines_used,
    )
