from __future__ import annotations

import asyncio
import os
import re
from pathlib import Path

from .config import get_settings
from .crawler import CrawlService, FetchOptions
from .golden_urls import GOLDEN_URLS


def _safe_slug(url: str) -> str:
    s = re.sub(r"^https?://", "", url)
    s = re.sub(r"[^a-zA-Z0-9._-]+", "_", s)
    return s[:140]


async def _main() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        full = os.getenv("CRAWL4AI_MCP_SMOKE_FULL") == "1"
        out_dir = os.getenv("CRAWL4AI_MCP_SMOKE_DIR")
        out_path = Path(out_dir).expanduser().resolve() if out_dir else None
        if out_path:
            out_path.mkdir(parents=True, exist_ok=True)
        for url in GOLDEN_URLS:
            res = await service.fetch(
                url=url,
                options=FetchOptions(format="markdown", max_chars=200_000),
            )
            print("\n===", url)
            title = res.get("title")
            content = str(res.get("content") or "")
            print("title:", title)
            print("format:", res.get("content_format"), "chars:", len(content))
            if out_path:
                p = out_path / f"{_safe_slug(url)}.md"
                p.write_text(content, encoding="utf-8")
                print("saved:", str(p))
            if full:
                print(content)
            else:
                print(content[:800].replace("\n", "\\n"))


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
