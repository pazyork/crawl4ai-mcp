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
    async with CrawlService(settings) as service:
        yield {"settings": settings, "service": service}


mcp = FastMCP("crawl4ai-mcp", lifespan=_lifespan)


def _maybe_truncate(s: str, max_chars: int) -> str:
    return s if max_chars <= 0 or len(s) <= max_chars else s[:max_chars]


async def _maybe_llm_clean(*, url: str, content: str, title: Optional[str]) -> dict[str, object]:
    cfg = load_openai_config()
    if not cfg.enabled:
        msg = "OpenAI-compatible config missing (OPENAI_BASE_URL/OPENAI_API_KEY/OPENAI_MODEL)"
        return {
            "llm_used": False,
            "llm_error": msg,
        }
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


@mcp.tool(description="Fetch a single URL and extract main content")
async def fetch_url(
    ctx: Context,
    url: str,
    format: Literal["markdown", "html"] = "markdown",
    max_chars: Optional[int] = None,
    use_llm: bool = False,
) -> dict[str, Any]:
    service = ctx.request_context.lifespan_context["service"]
    settings = ctx.request_context.lifespan_context["settings"]
    options = FetchOptions(format=format, max_chars=max_chars or settings.max_content_chars)
    res = await service.fetch(url=url, options=options)
    if use_llm:
        try:
            patch = await _maybe_llm_clean(
                url=url,
                content=str(res.get("content", "")),
                title=res.get("title"),
            )
            res.update(patch)
        except Exception as e:
            res["llm_used"] = False
            res["llm_error"] = str(e)
    if max_chars is not None and isinstance(res.get("content"), str):
        res["content"] = _maybe_truncate(res["content"], max_chars)
    return res


@mcp.tool(description="Fetch multiple URLs with bounded concurrency")
async def fetch_urls(
    ctx: Context,
    urls: list[str],
    format: Literal["markdown", "html"] = "markdown",
    max_chars: Optional[int] = None,
    concurrency: int = 3,
    use_llm: bool = False,
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


def run_stdio() -> None:
    mcp.run()
