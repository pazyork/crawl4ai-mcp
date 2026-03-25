from __future__ import annotations

import argparse
import asyncio
from contextlib import redirect_stdout
import json
from collections.abc import Sequence
from pathlib import Path
import sys
from typing import Any

from .config import Settings, get_settings
from .crawler import CrawlService, FetchOptions
from .golden_urls import GOLDEN_URLS
from .smoke_golden import _safe_slug


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crawl4agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch a single URL once and print JSON")
    _add_common_settings(fetch_parser)
    fetch_parser.add_argument("url")
    fetch_parser.add_argument("--format", choices=("markdown", "html"), default="markdown")
    fetch_parser.add_argument("--max-chars", type=int, default=200_000)

    search_parser = subparsers.add_parser("search", help="Search the web once and print JSON")
    _add_common_settings(search_parser)
    search_parser.add_argument("query")
    search_parser.add_argument("--engine", default="auto")
    search_parser.add_argument("--max-results", type=int, default=10)
    search_parser.add_argument("--lang", default="")

    smoke_parser = subparsers.add_parser("smoke", help="Run golden URLs once and print JSON")
    _add_common_settings(smoke_parser)
    smoke_parser.add_argument("--out-dir", default=None)
    smoke_parser.add_argument("--full-content", action="store_true")
    smoke_parser.add_argument("--max-chars", type=int, default=200_000)

    return parser


def _add_common_settings(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--proxy", default=None)
    parser.add_argument("--cookies-json", default=None)
    parser.add_argument("--cookies-from-browser", default=None)
    parser.add_argument("--cookiefile", default=None)
    parser.add_argument("--headless", dest="headless", action="store_true", default=None)
    parser.add_argument("--no-headless", dest="headless", action="store_false")


def _build_settings(args: argparse.Namespace) -> Settings:
    settings = get_settings()
    overrides: dict[str, Any] = {}
    if getattr(args, "proxy", None) is not None:
        overrides["proxy"] = args.proxy
    if getattr(args, "cookies_json", None) is not None:
        overrides["cookies_json"] = args.cookies_json
    if getattr(args, "cookies_from_browser", None) is not None:
        overrides["ytdlp_cookies_from_browser"] = args.cookies_from_browser
    if getattr(args, "cookiefile", None) is not None:
        overrides["ytdlp_cookiefile"] = args.cookiefile
    if getattr(args, "headless", None) is not None:
        overrides["headless"] = args.headless
    return settings.model_copy(update=overrides)


async def _run_fetch(args: argparse.Namespace) -> dict[str, object]:
    settings = _build_settings(args)
    options = FetchOptions(format=args.format, max_chars=args.max_chars)
    async with CrawlService(settings) as service:
        return await service.fetch(url=args.url, options=options)


async def _run_search(args: argparse.Namespace) -> dict[str, object]:
    settings = _build_settings(args)
    async with CrawlService(settings) as service:
        return await service.search(
            query=args.query,
            engine=args.engine,
            max_results=args.max_results,
            lang=args.lang,
        )


async def _run_smoke(args: argparse.Namespace) -> list[dict[str, object]]:
    settings = _build_settings(args)
    options = FetchOptions(format="markdown", max_chars=args.max_chars)
    out_path = Path(args.out_dir).expanduser().resolve() if args.out_dir else None
    if out_path is not None:
        out_path.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []
    async with CrawlService(settings) as service:
        for url in GOLDEN_URLS:
            result = await service.fetch(url=url, options=options)
            content = str(result.get("content") or "")
            saved_path: str | None = None
            if out_path is not None:
                file_path = out_path / f"{_safe_slug(url)}.md"
                file_path.write_text(content, encoding="utf-8")
                saved_path = str(file_path)

            item: dict[str, object] = {
                "url": url,
                "title": result.get("title"),
                "content_format": result.get("content_format"),
                "chars": len(content),
            }
            if saved_path is not None:
                item["saved_path"] = saved_path
            if args.full_content:
                item["content"] = content
            results.append(item)
    return results


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    with redirect_stdout(sys.stderr):
        if args.command == "fetch":
            payload: object = asyncio.run(_run_fetch(args))
        elif args.command == "search":
            payload = asyncio.run(_run_search(args))
        elif args.command == "smoke":
            payload = asyncio.run(_run_smoke(args))
        else:
            raise ValueError(f"Unsupported command: {args.command}")

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
