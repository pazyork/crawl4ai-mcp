from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional


def _as_str_or_none(v: object) -> Optional[str]:
    if v is None:
        return None
    s = str(v)
    return s if s.strip() else None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_result_dict(
    *,
    url: str,
    final_url: object,
    title: object,
    content: str,
    content_format: str,
    links: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "url": url,
        "final_url": _as_str_or_none(final_url),
        "title": _as_str_or_none(title),
        "content": content,
        "content_format": content_format,
        "extracted_at": now_iso(),
        "links": links,
    }
