from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, Literal, Optional

from mcp.server.fastmcp import Context, FastMCP

from .config import get_settings
from .crawler import CrawlService, FetchOptions, fetch_many
from .openai_client import load_openai_config, openai_chat_completions_json


@asynccontextmanager
async def _lifespan(_: FastMCP) -> AsyncIterator[dict[str, Any]]:
    settings = get_settings()
    # Delay crawler initialization to avoid stdout pollution during MCP handshake
    yield {"settings": settings, "service": None}


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
Fetch and extract content from one or more URLs with real browser rendering.

When to use:
- Scrape webpage content (articles, docs, blogs, ChatGPT shared conversations)
- Extract subtitles from supported video pages (YouTube, Bilibili)
- Extract main text while removing navigation/ads
- Batch fetch multiple pages concurrently
- Get clean markdown from JS-heavy sites

Parameters:
- urls: list of URLs to fetch (required)
- format: "markdown" (default) or "html"
- max_chars: truncate content to this length (default: 200000). Set higher for long pages.
- concurrency: parallel fetch limit (default: 3)
- use_llm: enable LLM cleanup (default: false, requires OPENAI_* env vars)
- llm_instruction: custom instruction for LLM cleanup (only when use_llm=true)

Important notes:
- Some JS-heavy pages (ChatGPT, SPAs) need extra load time — handled automatically
- Supported video URLs are handled specially and prefer subtitle/transcript extraction
- Content is truncated at max_chars. If you get incomplete content, increase max_chars
- If a page times out (default 30s), try again or check if proxy is needed
- blocked=true means the site returned a verification/CAPTCHA page
- For overseas sites, configure CRAWL4AI_MCP_PROXY env var

Returns per URL: {url, final_url, title, content, content_format, links, extracted_at, blocked}
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
    lifespan_ctx = ctx.request_context.lifespan_context
    settings = lifespan_ctx["settings"]
    
    # Initialize service on first use
    if lifespan_ctx.get("service") is None:
        lifespan_ctx["service"] = CrawlService(settings)
        await lifespan_ctx["service"].__aenter__()
    
    service = lifespan_ctx["service"]
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

When to use:
- Find relevant pages, documentation, tutorials, news
- Research a topic with comprehensive multi-engine coverage
- Get aggregated and deduplicated results from multiple sources

Parameters:
- query: search query string (required)
- engine: "auto" (default), "google", "bing", "duckduckgo", "baidu", "sogou", "so360", "yandex"
- max_results: number of results to return (default: 10, max: 100)
- lang: language hint, e.g. "en", "zh-CN" (auto-detects Chinese from query text)

Fusion mode (engine="auto"):
- Queries top 2 engines simultaneously, aggregates and deduplicates
- English queries: DuckDuckGo + Bing first, then Google, Yandex
- Chinese queries: Sogou + 360Search first, then Baidu, Bing
- Returns engine="fused" when multiple sources contribute

Important notes:
- Search may take 5-15s depending on engine availability
- If all engines fail, returns error with details per engine
- For overseas engines (Google, DuckDuckGo), proxy may be needed from China
- Results are deduplicated by URL and fuzzy title matching (85% threshold)

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
        lifespan_ctx = ctx.request_context.lifespan_context
        settings = lifespan_ctx["settings"]
        
        # Initialize service on first use
        if lifespan_ctx.get("service") is None:
            lifespan_ctx["service"] = CrawlService(settings)
            await lifespan_ctx["service"].__aenter__()
        
        service = lifespan_ctx["service"]
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
    mcp.run(transport="stdio")
