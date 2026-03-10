# crawl4ai-mcp — Agent Quickstart (MCP)

This document is for **agents/tools** (Claude Code, Cursor, Windsurf, Claude Desktop, etc.) that can install an MCP server.

If you’re a human developer, read: **[README.md](./README.md)** (EN) or **[README.zh-CN.md](./README.zh-CN.md)** (中文).

---

## What you get
One stable MCP tool:

- `fetch_urls(urls=[...], format="markdown", concurrency=..., use_llm=..., llm_instruction=...)`

Outputs include:
- `title`
- `content` (Markdown or HTML)
- `blocked` (true if likely anti-bot / verification page)
- optional `llm_used` / `llm_error`

---

## Install & Run (stdio MCP server)

### Conda (recommended)
```bash
conda env create -f environment.yml
conda activate crawl4ai-mcp
python -m playwright install
crawl4ai-mcp
```

### venv
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m playwright install
crawl4ai-mcp
```

---

## Platform config (concept)
Add a stdio MCP server entry:

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

---

## Recommended usage patterns

### Batch pages
- Use `fetch_urls` with `concurrency=3` (safe default).
- Keep `max_chars` large if you need full text.
- For a single page, pass one URL in the `urls` array.

Example call (batch):
```json
{
  "urls": ["https://a.com", "https://b.com"],
  "format": "markdown",
  "concurrency": 3,
  "use_llm": false,
  "llm_instruction": "keep only the main tutorial body and in-body references"
}
```

---

## Optional LLM enhancement (OpenAI-compatible)
Set env vars:
- `OPENAI_BASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`

Then call with `use_llm=true`.

Important:
- The system will **auto-fallback** to non-LLM mode on failures (network/auth/non-JSON/etc).
- If you must preserve original wording exactly, keep `use_llm=false` or use a delete-only instruction.

---

## Anti-bot knobs (env vars)
- `CRAWL4AI_MCP_PROXY`
- `CRAWL4AI_MCP_COOKIES_JSON`
- `CRAWL4AI_MCP_USE_PERSISTENT_CONTEXT=true`
- `CRAWL4AI_MCP_USER_DATA_DIR=/path/to/profile`

More details: **[README.md](./README.md)**.
