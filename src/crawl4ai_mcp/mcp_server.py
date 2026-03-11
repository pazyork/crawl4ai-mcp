from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, Literal, Optional

from mcp.server.fastmcp import Context, FastMCP

from .config import get_settings
from .crawler import CrawlService, FetchOptions, fetch_many
from .openai_client import load_openai_config, openai_chat_completions_json
from .searcher import SUPPORTED_ENGINES


@asynccontextmanager
async def _lifespan(_: FastMCP) -> AsyncIterator[dict[str, Any]]:
    settings = get_settings()
    async with CrawlService(settings) as service:
        yield {"settings": settings, "service": service}


mcp = FastMCP("crawl4ai-mcp", lifespan=_lifespan)


def _maybe_truncate(s: str, max_chars: int) -> str:
    return s if max_chars <= 0 or len(s) <= max_chars else s[:max_chars]


async def _maybe_llm_clean(
    *,
    url: str,
    content: str,
    title: Optional[str],
    llm_instruction: Optional[str] = None,
) -> dict[str, object]:
    cfg = load_openai_config()
    if not cfg.enabled:
        msg = "OpenAI-compatible config missing (OPENAI_BASE_URL/OPENAI_API_KEY/OPENAI_MODEL)"
        return {
            "llm_used": False,
            "llm_error": msg,
        }

    instruction_text = (llm_instruction or "").strip()
    if instruction_text:
        system = (
            "You FILTER an extracted Markdown document. "
            "Return ONLY a JSON object with keys: title, markdown. "
            "CRITICAL: Preserve original content. "
            "Output markdown MUST be exact lines copied from CONTENT, in the same order. "
            "You may ONLY delete lines/blocks. "
            "Do NOT rewrite, paraphrase, translate, or reformat kept lines. "
            "Preserve code fences and code lines exactly. "
            "Remove: navigation/header/footer boilerplate and sidebars. "
            "Remove: ads/marketing/promotions, app download prompts, login prompts. "
            "Remove: share/follow/subscribe CTAs. "
            "Remove: decorative/unrelated links/images (logos/icons/social buttons). "
            "Keep: main article/tutorial text. "
            "Keep: in-body citations/references (links that support the text). "
            "Keep: meaningful in-body images supporting nearby text. "
            "If unsure, KEEP the line. "
            f"Additional instruction: {instruction_text}"
        )
    else:
        system = (
            "You extract the main readable content from a webpage crawl. "
            "Return JSON with keys: title, markdown. "
            "markdown must be clean and keep code blocks."
        )

    user = f"URL: {url}\nTITLE: {title or ''}\n\nCONTENT:\n{content}\n"
    data = await openai_chat_completions_json(cfg=cfg, system=system, user=user)
    out: dict[str, object] = {"llm_used": True}
    if isinstance(data.get("title"), str):
        out["title"] = data["title"]
    if isinstance(data.get("markdown"), str):
        out["content"] = data["markdown"]
        out["content_format"] = "markdown"
    return out


@mcp.tool(description="""
Fetch and extract content from multiple URLs with real browser rendering.

Use this when you need to:
- Scrape webpage content (articles, documentation, blogs)
- Extract main text while removing navigation/ads
- Batch fetch multiple pages concurrently
- Get clean markdown from JS-heavy sites

Recommended config:
- format: "markdown" (default) - returns clean, readable content
- concurrency: 3 - optimal for most use cases
- max_chars: 200000 - enough for long articles
- use_llm: false (default) - fast without model
- llm_instruction: only needed when use_llm=true

Example usage:
{
  "urls": ["https://example.com/docs", "https://example.com/blog"],
  "format": "markdown",
  "concurrency": 3,
  "max_chars": 200000
}

Returns: results array with {url, title, content, content_format, links, extracted_at, blocked}
""")
async def fetch_urls(
    ctx: Context,
    urls: list[str],
    format: Literal["markdown", "html"] = "markdown",
    max_chars: Optional[int] = None,
    concurrency: int = 3,
    use_llm: bool = False,
    llm_instruction: Optional[str] = None,
) -> dict[str, Any]:
    service = ctx.request_context.lifespan_context["service"]
    settings = ctx.request_context.lifespan_context["settings"]
    options = FetchOptions(format=format, max_chars=max_chars or settings.max_content_chars)
    results = await fetch_many(service=service, urls=urls, options=options, concurrency=concurrency)
    if use_llm:
        cfg = load_openai_config()
        if not cfg.enabled:
            msg = "OpenAI-compatible config missing (OPENAI_BASE_URL/OPENAI_API_KEY/OPENAI_MODEL)"
            for r in results:
                if isinstance(r, dict) and "error" not in r:
                    r["llm_used"] = False
                    r["llm_error"] = msg
            return {"results": results}
        for r in results:
            if not isinstance(r, dict) or "error" in r:
                continue
            try:
                patch = await _maybe_llm_clean(
                    url=str(r.get("final_url") or r.get("url")),
                    content=str(r.get("content", "")),
                    title=r.get("title"),
                    llm_instruction=llm_instruction,
                )
                r.update(patch)
            except Exception as e:
                r["llm_used"] = False
                r["llm_error"] = str(e)
    if max_chars is not None:
        for r in results:
            if isinstance(r, dict) and isinstance(r.get("content"), str):
                r["content"] = _maybe_truncate(r["content"], max_chars)
    return {"results": results}


@mcp.tool(description="""
Search the web across 7 search engines with intelligent fusion and fallback.

Use this when you need to:
- Find relevant pages on the internet
- Search for documentation, tutorials, news
- Get aggregated results from multiple search engines
- Research a topic with comprehensive coverage

Search engines (in order):
- International: DuckDuckGo → Bing → Google → Yandex
- Chinese: Sogou → 360Search → Baidu → Bing

Recommended config:
- engine: "auto" (default) - uses fusion mode (DuckDuckGo + Bing in parallel)
- max_results: 8-10 - optimal for most research tasks
- lang: "en" or "zh-CN" - auto-detects Chinese queries

Engine selection logic:
- engine="auto" + English query → DuckDuckGo + Bing → fallback to Google
- engine="auto" + Chinese query → Sogou + 360Search → fallback to Baidu
- engine="google" → use Google only (no fallback)
- engine="duckduckgo" → use DuckDuckGo only

Fusion mode (engine="auto"):
- Queries top 2 engines simultaneously
- Aggregates and deduplicates results
- Falls back to sequential search if needed
- Returns engine="fused" when using multiple sources

Example usage:
{
  "query": "Python web scraping best practices",
  "engine": "auto",
  "max_results": 10,
  "lang": "en"
}

Returns: {engine, query, results: [{title, url, snippet, engine}], total, engines_used}
""")
async def search_web(
    ctx: Context,
    query: str,
    engine: str = "auto",
    max_results: int = 10,
    lang: str = "",
) -> dict[str, Any]:
    try:
        service = ctx.request_context.lifespan_context["service"]
        return await service.search(
            query=query,
            engine=engine,
            max_results=max_results,
            lang=lang,
        )
    except Exception as e:
        return {
            "error": str(e)[:500],
            "engine": engine if 'engine' in locals() else "unknown",
            "query": query[:100] if 'query' in locals() else "unknown",
        }


def run_stdio() -> None:
    mcp.run()
