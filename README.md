# crawl4ai-mcp

<div align="center">

[![License: AGPL v3](https://img.shields.io/badge/license-AGPL--3.0--or--later-6f42c1)](https://www.gnu.org/licenses/agpl-3.0)
[![Python](https://img.shields.io/badge/python-3.9--3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/protocol-MCP-0A7EA4)](https://modelcontextprotocol.io)
[![Playwright](https://img.shields.io/badge/browser-Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev)
[![Crawl4AI](https://img.shields.io/badge/extractor-Crawl4AI-111827)](https://github.com/unclecode/crawl4ai)
[![GitHub stars](https://img.shields.io/github/stars/pazyork/crawl4ai-mcp?style=social)](https://github.com/pazyork/crawl4ai-mcp)

**A minimal MCP server for agent-friendly web extraction.**

It renders real pages with Playwright + Crawl4AI, returns **main-content-first Markdown**, supports **batch fetching only**, and can optionally apply **OpenAI-compatible cleanup** with a custom instruction.

</div>

---

## Quick entry

| Audience | Read this |
|---|---|
| Human developer | **[README.zh-CN.md](./README.zh-CN.md)** / **[README.md](./README.md)** |
| Living in the AI era, delegating your remaining sanity to an agent | **[README_AGENT.md](./README_AGENT.md)** |

## At a glance

| Item | Reality in this repo |
|---|---|
| MCP tools | **1 tool only**: `fetch_urls` |
| Single-page fetch | Use `urls: ["https://example.com"]` |
| Output | `title + content + links + blocked + llm_used/llm_error` |
| Non-LLM mode | First-class, default, usable without any model |
| LLM mode | **Off by default**. Enabled only with `use_llm=true` + optional `llm_instruction` |
| Fallback | Missing/failed LLM call automatically falls back to non-LLM result |
| Anti-bot realism | proxy / cookies / persistent profile / randomized browser behavior |
| License | **AGPL-3.0-or-later** |

---

## How it works

```mermaid
flowchart LR
    A[URL list input] --> B[Playwright and Crawl4AI]
    B --> C{Fast path enough}
    C -- Yes --> D[Markdown or HTML result]
    C -- No --> E[Stronger fallback]
    E --> D
    D --> F[Site-specific cleanup]
    F --> G{use_llm enabled}
    G -- No --> H[Return non-LLM result]
    G -- Yes --> I[OpenAI-compatible cleanup]
    I --> J{LLM success}
    J -- Yes --> K[Return enhanced result]
    J -- No --> H
```

---

## Why this project exists

Most generic “web fetch” tools either fail on JS-heavy pages or return too much boilerplate. This project focuses on four things:

- **Non-LLM quality first**: usable even with zero model config
- **Minimal MCP surface**: easier for agents, easier to maintain
- **Pragmatic anti-bot workflow**: proxy / cookies / persistent profile are first-class
- **Golden regression review**: full markdown outputs can be saved and inspected page by page

---

## Core capabilities

### Non-LLM mode

| Capability | Actual behavior |
|---|---|
| Rendering | Real browser rendering via Playwright |
| Extraction | Crawl4AI markdown/html extraction |
| Fallback | Fast path → stronger path when content is too thin |
| Cleanup | Remove obvious noise, compress blanks, strip data-image placeholders |
| Site tuning | Zhihu / WeChat / Medium / CSDN / Claude Docs rules |
| Block detection | `blocked=true` for likely verification/interstitial output |
| Batch control | Bounded concurrency via `concurrency` |

### Optional LLM mode

| Input | Meaning |
|---|---|
| `use_llm=true` | Turn on post-cleanup with an OpenAI-compatible model |
| `llm_instruction` | Tell the model what to keep / remove |

**Important reality check:**

- With `llm_instruction`, the prompt is **constraint-heavy** and biased toward preserving original lines.
- Without `llm_instruction`, the model does a more generic “clean readable markdown” pass.
- If the LLM call fails for any reason, the tool returns the original non-LLM extraction plus `llm_used=false` and `llm_error`.

---

## The only MCP tool

### `fetch_urls`

```json
{
  "urls": ["https://a.com", "https://b.com"],
  "format": "markdown",
  "max_chars": 200000,
  "concurrency": 3,
  "use_llm": false,
  "llm_instruction": "keep only the tutorial body and in-body references"
}
```

Use a single-element list if you only need one page.

### Return shape

| Field | Meaning |
|---|---|
| `url` | Original URL |
| `final_url` | Final resolved URL after redirects |
| `title` | Extracted title |
| `content` | Markdown or HTML |
| `content_format` | `markdown` or `html` |
| `links` | Normalized extracted links |
| `blocked` | Likely anti-bot / verification / denied result |
| `llm_used` | Whether LLM enhancement was actually applied |
| `llm_error` | Why the LLM step degraded |

---

## Anti-bot realism

The server already includes randomized browser behavior in code:

| Mechanism | Actual status |
|---|---|
| Random viewport | Yes |
| Random user agent mode | Yes, when explicit UA is not provided |
| Delay jitter | Yes |
| `override_navigator` | Yes |
| `simulate_user` | Yes, in stronger fallback mode |
| Proxy / cookies / persistent profile | Supported via env vars |
| Cloudflare bypass | Enhanced browser fingerprinting + configurable wait strategies |

**Note**: For overseas websites (Medium, ProductHunt, etc.), using a proxy is recommended. The server supports HTTP/HTTPS/SOCKS5 proxies via `CRAWL4AI_MCP_PROXY` environment variable.

### Proxy input formats

`CRAWL4AI_MCP_PROXY` accepts all of these:

| Input | Interpreted as |
|---|---|
| `http://127.0.0.1:7890` | HTTP proxy |
| `https://127.0.0.1:7890` | HTTPS proxy |
| `socks5://127.0.0.1:7890` | SOCKS5 proxy |
| `socket5://127.0.0.1:7890` | Auto-normalized to `socks5://...` |
| `127.0.0.1:7890` | Auto-normalized to `http://127.0.0.1:7890` |
| `7890` | Auto-normalized to `http://127.0.0.1:7890` |

That means the README should not claim “perfect stealth”, but it can honestly claim **human-like randomization** and **practical anti-bot knobs**.

---

## Quickstart

### Conda

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
python -m pip install -U pip
python -m pip install -e '.[dev]'
python -m playwright install
crawl4ai-mcp
```

---

## MCP server config example

```json
{
  "mcpServers": {
    "crawl4ai": {
      "command": "crawl4ai-mcp",
      "env": {
        "CRAWL4AI_MCP_HEADLESS": "true",
        "CRAWL4AI_MCP_PROXY": "127.0.0.1:7890",
        "CRAWL4AI_MCP_NAVIGATION_TIMEOUT_MS": "30000",
        "CRAWL4AI_MCP_WAIT_UNTIL": "load",

        "OPENAI_BASE_URL": "https://your-openai-compatible-host",
        "OPENAI_API_KEY": "your-api-key",
        "OPENAI_MODEL": "your-model-name"
      }
    }
  }
}
```

LLM-related env vars are **optional**. `use_llm` is still **off by default** at call time. If any LLM env is missing, invalid, or the model call fails, the server automatically falls back to non-LLM extraction.

---

## Runtime configuration

| Env var | Purpose |
|---|---|
| `CRAWL4AI_MCP_HEADLESS` | Run browser headless |
| `CRAWL4AI_MCP_PROXY` | Upstream proxy, supports `http://`, `https://`, `socks5://`, `host:port`, and `port-only` |
| `CRAWL4AI_MCP_COOKIES_JSON` | Playwright storage state JSON |
| `CRAWL4AI_MCP_USE_PERSISTENT_CONTEXT` | Reuse browser profile |
| `CRAWL4AI_MCP_USER_DATA_DIR` | Profile directory |
| `CRAWL4AI_MCP_NAVIGATION_TIMEOUT_MS` | Default max single navigation wait, default `30000` |
| `CRAWL4AI_MCP_WAIT_UNTIL` | Default page readiness strategy, default `load` |
| `OPENAI_BASE_URL` | OpenAI-compatible base URL |
| `OPENAI_API_KEY` | API key |
| `OPENAI_MODEL` | Model name |

---

## Golden smoke regression

```bash
CRAWL4AI_MCP_SMOKE_DIR=./_golden_outputs .venv/bin/python -m crawl4ai_mcp.smoke_golden
```

This writes full markdown outputs to `_golden_outputs/` so you can inspect extraction quality page by page.

The golden set now includes the earlier baseline URLs plus `ainew.me`, `openclaw`, `watcha`, `producthunt`, `mydrivers`, `caihongtu`, `openrouter`, and mobile Douban. For sites outside mainland China, proxy-based verification is recommended.

Some overseas sites may still return Cloudflare or similar verification pages even when a proxy is configured. In those cases the server now marks them with `blocked=true`. The recommended path is: better proxy quality, valid cookies, or a persistent browser profile after manual verification.

---

## Prior art

- Crawl4AI: <https://github.com/unclecode/crawl4ai>
- mcp-crawl4ai-rag: <https://github.com/coleam00/mcp-crawl4ai-rag>
- weidwonder/crawl4ai-mcp-server: <https://github.com/weidwonder/crawl4ai-mcp-server>
- WaterCrawl: <https://github.com/watercrawl/WaterCrawl>
- teracrawl: <https://github.com/BrowserCash/teracrawl>

---

## License

This project is licensed under **AGPL-3.0-or-later**.
