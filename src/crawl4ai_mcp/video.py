from __future__ import annotations

import asyncio
import json
import re
import subprocess
import sys
import tempfile
from html import unescape
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import httpx

from .types import build_result_dict

_PREFERRED_SUBTITLE_EXTS = ("vtt", "srt", "json3", "ttml")
_PREFERRED_LANGS = (
    "ai-zh",
    "zh-Hans",
    "zh-CN",
    "zh",
    "zh-Hant",
    "zh-TW",
    "en",
    "en-US",
    "en-GB",
)
_SKIP_LANGS = {"live_chat", "comments", "danmaku"}


def is_supported_video_url(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if "youtube.com" in host and path == "/watch":
        return True
    if "youtu.be" in host and path.strip("/"):
        return True
    if "bilibili.com" in host and "/video/" in path:
        return True
    if "b23.tv" in host and path.strip("/"):
        return True
    return False


def _subtitle_candidates(info: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    candidates: list[tuple[str, str, dict[str, Any]]] = []
    for source_name in ("subtitles", "automatic_captions"):
        tracks = info.get(source_name) or {}
        if not isinstance(tracks, dict):
            continue
        for lang, variants in tracks.items():
            if lang in _SKIP_LANGS or not isinstance(variants, list):
                continue
            for variant in variants:
                if isinstance(variant, dict):
                    candidates.append((source_name, lang, variant))
    return candidates


def _lang_rank(lang: str) -> tuple[int, str]:
    if lang in _PREFERRED_LANGS:
        return (_PREFERRED_LANGS.index(lang), lang)
    primary = lang.split("-")[0]
    if primary in _PREFERRED_LANGS:
        return (_PREFERRED_LANGS.index(primary), lang)
    return (len(_PREFERRED_LANGS) + 1, lang)


def _ext_rank(ext: str) -> int:
    if ext in _PREFERRED_SUBTITLE_EXTS:
        return _PREFERRED_SUBTITLE_EXTS.index(ext)
    return len(_PREFERRED_SUBTITLE_EXTS) + 1


def _pick_subtitle_track(info: dict[str, Any]) -> tuple[str, str, dict[str, Any]] | None:
    candidates = _subtitle_candidates(info)
    if not candidates:
        return None
    candidates.sort(key=lambda item: (0 if item[0] == "subtitles" else 1, _lang_rank(item[1]), _ext_rank(str(item[2].get("ext") or ""))))
    return candidates[0]


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def _dedupe_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    last = ""
    for line in lines:
        normalized = line.strip()
        if not normalized or normalized == last:
            continue
        out.append(normalized)
        last = normalized
    return out


def _parse_vtt_or_srt(payload: str) -> str:
    lines: list[str] = []
    for raw_line in payload.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "WEBVTT":
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if "-->" in line:
            continue
        if line.startswith("NOTE "):
            continue
        line = _strip_tags(unescape(line))
        line = re.sub(r"\{\\.*?\}", "", line)
        if line:
            lines.append(line)
    return "\n".join(_dedupe_lines(lines)).strip()


def _parse_json3(payload: str) -> str:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return ""
    lines: list[str] = []
    for event in data.get("events", []):
        if not isinstance(event, dict):
            continue
        segs = event.get("segs") or []
        text = "".join(seg.get("utf8", "") for seg in segs if isinstance(seg, dict)).strip()
        text = _strip_tags(unescape(text))
        if text:
            lines.append(text)
    return "\n".join(_dedupe_lines(lines)).strip()


def _parse_ttml(payload: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", payload, flags=re.IGNORECASE)
    fragments = re.findall(r">([^<]+)<", text)
    lines = [unescape(fragment).strip() for fragment in fragments if fragment.strip()]
    return "\n".join(_dedupe_lines(lines)).strip()


def _normalize_subtitle_text(payload: str, ext: str) -> str:
    ext = ext.lower()
    if ext in {"vtt", "srt", "ass"}:
        return _parse_vtt_or_srt(payload)
    if ext == "json3":
        return _parse_json3(payload)
    if ext in {"ttml", "xml"}:
        return _parse_ttml(payload)
    return _parse_vtt_or_srt(payload)


def _fetch_subtitle_payload(track: dict[str, Any], proxy: Optional[str]) -> tuple[str, str] | None:
    ext = str(track.get("ext") or "vtt").lower()
    data = track.get("data")
    if isinstance(data, str) and data.strip():
        return data, ext
    url = track.get("url")
    if not isinstance(url, str) or not url.strip():
        return None
    with httpx.Client(follow_redirects=True, timeout=30.0, proxy=proxy) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text, ext


def _parse_cookies_from_browser(value: Optional[str]) -> tuple[str, str | None, str | None, str | None] | None:
    if value is None:
        return None
    raw = value.strip()
    if not raw:
        return None
    browser = raw
    profile = None
    keyring = None
    container = None

    if "::" in raw:
        raw, container = raw.split("::", 1)
        container = container or None
    if ":" in raw:
        raw, profile = raw.split(":", 1)
        profile = profile or None
    if "+" in raw:
        browser, keyring = raw.split("+", 1)
        keyring = keyring.upper() or None
    else:
        browser = raw
    return (browser.lower(), profile, keyring, container)


def _build_video_markdown(title: str | None, transcript: str, source_url: str) -> str:
    transcript = transcript.strip()
    if not transcript:
        return ""
    header = f"# {title.strip()}\n\n" if title and title.strip() else ""
    meta = f"Source: {source_url}\n\n"
    return f"{header}{meta}{transcript}\n"


def _build_ytdlp_base_command(
    *,
    proxy: Optional[str],
    cookies_from_browser: Optional[str],
    cookiefile: Optional[str],
) -> list[str]:
    command = [_resolve_ytdlp_executable()]
    if proxy:
        command.extend(["--proxy", proxy])
    if cookies_from_browser:
        command.extend(["--cookies-from-browser", cookies_from_browser])
    if cookiefile:
        command.extend(["--cookies", cookiefile])
    command.append("--ignore-no-formats-error")
    return command


def _resolve_ytdlp_executable() -> str:
    candidate = Path(sys.executable).with_name("yt-dlp")
    if candidate.exists():
        return str(candidate)
    return "yt-dlp"


def _run_ytdlp(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def _load_video_metadata_via_cli(
    *,
    url: str,
    proxy: Optional[str],
    cookies_from_browser: Optional[str],
    cookiefile: Optional[str],
) -> dict[str, Any]:
    command = _build_ytdlp_base_command(
        proxy=proxy,
        cookies_from_browser=cookies_from_browser,
        cookiefile=cookiefile,
    )
    command.extend(["--skip-download", "--dump-single-json", url])
    try:
        completed = _run_ytdlp(command)
    except Exception:
        return {}
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _subtitle_file_sort_key(path: Path) -> tuple[int, tuple[int, str], int, str]:
    name = path.name
    lang = ""
    parts = name.split(".")
    if len(parts) >= 3:
        lang = parts[-2]
    source_rank = 1 if ".auto." in name else 0
    return (source_rank, _lang_rank(lang), _ext_rank(path.suffix.lstrip(".")), name)


def _extract_subtitle_file_from_dir(output_dir: Path) -> tuple[Path, str, str] | None:
    candidates: list[tuple[Path, str, str]] = []
    for path in output_dir.iterdir():
        if not path.is_file():
            continue
        ext = path.suffix.lstrip(".").lower()
        if ext not in {"vtt", "srt", "json3", "ttml", "xml", "ass"}:
            continue
        parts = path.name.split(".")
        language = parts[-2] if len(parts) >= 3 else ""
        candidates.append((path, language, ext))
    if not candidates:
        return None
    candidates.sort(key=lambda item: _subtitle_file_sort_key(item[0]))
    return candidates[0]


def _extract_video_result_via_cli(
    *,
    url: str,
    max_chars: int,
    proxy: Optional[str],
    cookies_from_browser: Optional[str],
    cookiefile: Optional[str],
) -> dict[str, object] | None:
    metadata = _load_video_metadata_via_cli(
        url=url,
        proxy=proxy,
        cookies_from_browser=cookies_from_browser,
        cookiefile=cookiefile,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        command = _build_ytdlp_base_command(
            proxy=proxy,
            cookies_from_browser=cookies_from_browser,
            cookiefile=cookiefile,
        )
        command.extend(
            [
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs",
                ",".join(_PREFERRED_LANGS),
                "--sub-format",
                "vtt/srt/json3/best",
                "-o",
                str(output_dir / "video.%(ext)s"),
                url,
            ]
        )
        try:
            _run_ytdlp(command)
        except Exception:
            return None

        picked = _extract_subtitle_file_from_dir(output_dir)
        if picked is None:
            return None
        subtitle_path, language, ext = picked
        transcript = _normalize_subtitle_text(subtitle_path.read_text(encoding="utf-8"), ext)
        if not transcript:
            return None
        markdown = _build_video_markdown(metadata.get("title") if metadata else None, transcript, url)
        if max_chars > 0 and len(markdown) > max_chars:
            markdown = markdown[:max_chars]

        result = build_result_dict(
            url=url,
            final_url=(metadata.get("webpage_url") or url) if metadata else url,
            title=metadata.get("title") if metadata else None,
            content=markdown,
            content_format="markdown",
            links=[],
        )
        result["video_metadata"] = {
            "extractor": metadata.get("extractor_key") or metadata.get("extractor") if metadata else None,
            "video_id": metadata.get("id") if metadata else None,
            "duration": metadata.get("duration") if metadata else None,
            "language": language or None,
            "subtitle_source": "automatic_captions" if ".auto." in subtitle_path.name else "subtitles",
            "subtitle_ext": ext,
        }
        return result


def _extract_video_result_sync(
    *,
    url: str,
    max_chars: int,
    proxy: Optional[str],
    cookies_from_browser: Optional[str],
    cookiefile: Optional[str],
) -> dict[str, object] | None:
    cli_result = _extract_video_result_via_cli(
        url=url,
        max_chars=max_chars,
        proxy=proxy,
        cookies_from_browser=cookies_from_browser,
        cookiefile=cookiefile,
    )
    if cli_result is not None:
        return cli_result

    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        return None

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": list(_PREFERRED_LANGS),
        "subtitlesformat": "vtt/srt/json3/best",
    }
    if proxy:
        ydl_opts["proxy"] = proxy
    parsed_cookies_from_browser = _parse_cookies_from_browser(cookies_from_browser)
    if parsed_cookies_from_browser:
        ydl_opts["cookiesfrombrowser"] = parsed_cookies_from_browser
    if cookiefile:
        ydl_opts["cookiefile"] = cookiefile

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception:
        return None

    if not isinstance(info, dict):
        return None
    picked = _pick_subtitle_track(info)
    if picked is None:
        return None
    source_name, language, track = picked
    payload = _fetch_subtitle_payload(track, proxy)
    if payload is None:
        return None
    subtitle_payload, ext = payload
    transcript = _normalize_subtitle_text(subtitle_payload, ext)
    if not transcript:
        return None
    markdown = _build_video_markdown(info.get("title"), transcript, url)
    if max_chars > 0 and len(markdown) > max_chars:
        markdown = markdown[:max_chars]

    result = build_result_dict(
        url=url,
        final_url=info.get("webpage_url") or url,
        title=info.get("title"),
        content=markdown,
        content_format="markdown",
        links=[],
    )
    result["video_metadata"] = {
        "extractor": info.get("extractor_key") or info.get("extractor"),
        "video_id": info.get("id"),
        "duration": info.get("duration"),
        "language": language,
        "subtitle_source": source_name,
        "subtitle_ext": ext,
    }
    return result


async def extract_video_result(
    *,
    url: str,
    max_chars: int,
    proxy: Optional[str],
    cookies_from_browser: Optional[str] = None,
    cookiefile: Optional[str] = None,
) -> dict[str, object] | None:
    if not is_supported_video_url(url):
        return None
    return await asyncio.to_thread(
        _extract_video_result_sync,
        url=url,
        max_chars=max_chars,
        proxy=proxy,
        cookies_from_browser=cookies_from_browser,
        cookiefile=cookiefile,
    )
