# crawl4ai-mcp

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.9-3.12](https://img.shields.io/badge/python-3.9--3.12-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/pazyork/crawl4ai-mcp?style=social)](https://github.com/pazyork/crawl4ai-mcp)

A **Crawl4AI + Playwright** powered **MCP (Model Context Protocol)** server.

It lets agents (Claude Code / Cursor / Windsurf / Claude Desktop, etc.) reliably fetch web pages and return **main-content-first Markdown** (or HTML), with optional OpenAI-compatible LLM enhancement.

- 中文版：👉 **[README.zh-CN.md](./README.zh-CN.md)**
- Tip: just paste this link to your agent (Claude Code / Cursor) and let it do the MCP setup end-to-end: 👉 **[README_AGENT.md](./README_AGENT.md)**

> License: **AGPL-3.0-or-later** (network use + modifications must provide corresponding source code)

---

## What you can do (in one line)
Turn any URL into: **title + readable Markdown + links/images/citations + blocked/error signals**, with batching and bounded concurrency.

---

## Why this exists
Most “web fetch” tools break on JS-heavy pages or return noisy boilerplate. This project prioritizes:
- **Non-LLM quality** (works even if you don’t configure any model)
- **Minimal MCP surface** (stable tools, easy to maintain)
- **Real anti-bot knobs** (proxy/cookies/persistent profile)
- **Golden smoke outputs** (full markdown saved to files for human review)

---

## Key capabilities

### Non-LLM (default)
- Real browser rendering via Playwright (JS-heavy sites)
- Main-content-first Markdown postprocess (squeeze blanks, drop obvious noise, fix empty links, etc.)
- Fast path + strong fallback
- `blocked=true` when it likely hit an interstitial / verification / access denied
- Batch fetch with bounded concurrency

### Optional LLM enhancement (OpenAI-compatible)
- Extra knob: `llm_instruction` (requires `use_llm=true` + model configured).
  Use it to tell the model what to keep/remove while still preferring delete-only cleanup.

- Enable via `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`
- Auto-fallback to non-LLM when the LLM call fails (network/auth/non-JSON/timeout)

Important:
- If you require **strict “no rewriting”**, keep `use_llm=false`, or enforce a **delete-only** prompt policy (see “LLM delete-only policy” below).

---

## References / Prior art (respect)
- Crawl4AI: https://github.com/unclecode/crawl4ai
- mcp-crawl4ai-rag: https://github.com/coleam00/mcp-crawl4ai-rag
- weidwonder/crawl4ai-mcp-server: https://github.com/weidwonder/crawl4ai-mcp-server
- WaterCrawl / teracrawl: https://github.com/watercrawl/WaterCrawl / https://github.com/BrowserCash/teracrawl

What’s different here:
- **Minimal MCP tool surface** (one batch tool only), designed for stability
- **Non-LLM output is already usable** (not “raw HTML only”)
- **Pragmatic anti-bot workflow** (proxy/cookies/persistent context)
- **Reviewable golden outputs** (full markdown files for regression)

---

## Quickstart

> Python 3.9–3.12 (recommended 3.11)

### Conda (recommended)
```bash
conda env create -f environment.yml
conda activate crawl4ai-mcp
python -m playwright install
```

### venv
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
python -m playwright install
```

### Run MCP server (stdio)
```bash
crawl4ai-mcp
```

---

## MCP tool

### `fetch_urls`
```json
{
  "urls": ["https://a.com", "https://b.com"],
  "format": "markdown",
  "max_chars": 200000,
  "concurrency": 3,
  "use_llm": false,
  "llm_instruction": "keep only the main tutorial body and in-body references"
}
```

Use a single-element list if you only need one URL.

Typical output items:
```json
{
  "results": [
    {
      "url": "...",
      "final_url": "...",
      "title": "...",
      "content": "...",
      "content_format": "markdown",
      "links": [{"text": "...", "url": "..."}],
      "blocked": false,
      "llm_used": false,
      "llm_error": null
    }
  ]
}
```

---

## Agent integration (config concept)
Platform config locations vary. The key idea is to start `crawl4ai-mcp` as a stdio MCP server.

```json
{
  "mcpServers": {
    "crawl4ai": {
      "command": "crawl4ai-mcp",
      "env": {
        "CRAWL4AI_MCP_HEADLESS": "true"
      }
    }
  }
}
```

Agent-only quickstart: **[README_AGENT.md](./README_AGENT.md)**

---
