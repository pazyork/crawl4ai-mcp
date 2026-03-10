# crawl4ai-mcp — Agent Quickstart

<div align="center">

[![Single Tool](https://img.shields.io/badge/MCP%20tools-1-0A7EA4)](./README.md)
[![Batch Only](https://img.shields.io/badge/interface-fetch__urls-2563EB)](./README.md)
[![Optional LLM](https://img.shields.io/badge/LLM-optional-7C3AED)](./README.md)

**For the AI era: when you decide sleep is optional and delegation is the real product feature.**

</div>

---

## What you get

| Item | Actual contract |
|---|---|
| Tool count | **1** |
| Tool name | `fetch_urls` |
| Single URL | pass one URL inside `urls` |
| Output | `title`, `content`, `links`, `blocked`, optional `llm_used` / `llm_error` |

---

## Tool signature

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

---

## Recommended stdio MCP config

```json
{
  "mcpServers": {
    "crawl4ai": {
      "command": "crawl4ai-mcp",
      "env": {
        "CRAWL4AI_MCP_HEADLESS": "true",

        "OPENAI_BASE_URL": "https://your-openai-compatible-host",
        "OPENAI_API_KEY": "your-api-key",
        "OPENAI_MODEL": "your-model-name"
      }
    }
  }
}
```

### Important

- `OPENAI_BASE_URL` / `OPENAI_API_KEY` / `OPENAI_MODEL` are **optional**.
- If they are missing, invalid, or the model call fails, the server **automatically falls back** to non-LLM extraction.

---

## Usage notes

| Scenario | Recommended settings |
|---|---|
| Normal web extraction | `format="markdown"`, `use_llm=false` |
| Keep only the tutorial body | `use_llm=true` + `llm_instruction` |
| Single page | `urls: ["https://example.com"]` |
| Anti-bot trouble | add proxy / cookies / persistent profile |

---

## Anti-bot env vars

- `CRAWL4AI_MCP_PROXY`
- `CRAWL4AI_MCP_COOKIES_JSON`
- `CRAWL4AI_MCP_USE_PERSISTENT_CONTEXT=true`
- `CRAWL4AI_MCP_USER_DATA_DIR=/path/to/profile`

---

## Read more

- Human docs: **[README.md](./README.md)**
- 中文文档: **[README.zh-CN.md](./README.zh-CN.md)**
