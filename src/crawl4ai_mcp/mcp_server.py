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


@mcp.tool(description="Fetch multiple URLs with bounded concurrency")
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


def run_stdio() -> None:
    mcp.run()
