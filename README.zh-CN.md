# crawl4ai-mcp

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.9-3.12](https://img.shields.io/badge/python-3.9--3.12-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/pazyork/crawl4ai-mcp?style=social)](https://github.com/pazyork/crawl4ai-mcp)

一个基于 **Crawl4AI + Playwright** 的 **MCP（Model Context Protocol）** 服务。

用于让 Agent（Claude Code / Cursor / Windsurf / Claude Desktop 等）稳定抓取网页，并返回**正文优先、可直接消费**的 Markdown（或 HTML），并支持可选的 OpenAI-compatible LLM 做增强清洗（可关闭）。

- English (default): 👉 **[README.md](./README.md)**
- 推荐你直接把这个文档链接丢给你的 Agent（Claude Code / Cursor 都行），让它端到端替你把 MCP 配置和接入搞定：👉 **[README_AGENT.md](./README_AGENT.md)**

> 协议：**AGPL-3.0-or-later**（网络服务对外提供 + 修改后提供，也需提供对应源码，提高“免费商用私有改造”门槛）

---

## 你能用它做什么？（一句话）
把任意 URL 变成：**标题 + 可读 Markdown（含必要链接/引用/图片）+ blocked/错误提示**，并支持批量抓取、并发控制、抗干扰降级。

---

## 为什么做这个
很多“网页抓取工具”在 JS-heavy 页面不稳定，或者输出噪音非常多。本项目强调：
- **非 LLM 模式也要好用**（不配模型也能输出可读 Markdown）
- **MCP 工具面极简**（只保留一个批量抓取工具、稳定、可维护）
- **反爬现实主义**（代理/cookies/persistent profile）
- **golden 回归**（完整 markdown 落盘，便于逐页审查和迭代）

---

## 核心能力

### 非 LLM（默认）
- Playwright 真浏览器渲染（JS-heavy 站点）
- 正文优先 Markdown 后处理（压缩空行、去明显噪音、修复空链接等）
- 快速路径 + 强力回退
- 命中验证页/反爬时返回 `blocked=true`
- 批量抓取 + 并发上限

### 可选 LLM 增强（OpenAI-compatible）
- 额外参数：`llm_instruction`（必须 `use_llm=true` 且已配置模型）。
  用来告诉模型“保留/删除什么内容”，默认仍偏向“只删不改”的清洗。

- 通过 `OPENAI_BASE_URL` / `OPENAI_API_KEY` / `OPENAI_MODEL` 开启
- **失败自动降级**：LLM 调用失败（网络/鉴权/返回非 JSON/超时）→ 自动回退到非 LLM

重要：如果你要求**正文必须原汁原味、禁止改写**：
- 关闭 `use_llm`；或
- 使用“只删不改”的提示词策略（见下文）。

---

## 参考项目（致敬）
- Crawl4AI：<https://github.com/unclecode/crawl4ai>
- mcp-crawl4ai-rag：<https://github.com/coleam00/mcp-crawl4ai-rag>
- weidwonder/crawl4ai-mcp-server：<https://github.com/weidwonder/crawl4ai-mcp-server>
- WaterCrawl / teracrawl：<https://github.com/watercrawl/WaterCrawl> / <https://github.com/BrowserCash/teracrawl>

本项目更强调：
- **工具面极简（只保留一个批量工具）** → 更稳定、维护成本更低
- **非 LLM 输出可直接用**（不是只吐 raw HTML）
- **反爬链路可控**（代理/cookies/persistent context）
- **golden 输出可回归**（完整 markdown 文件）

---

## 快速开始

> Python 3.9–3.12（建议 3.11）

### Conda（推荐）
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

### 启动 MCP Server（stdio）
```bash
crawl4ai-mcp
```

---

## MCP 工具

### `fetch_urls`
```json
{
  "urls": ["https://a.com", "https://b.com"],
  "format": "markdown",
  "max_chars": 200000,
  "concurrency": 3,
  "use_llm": false,
  "llm_instruction": "只保留教程正文与文内引用"
}
```

如果只抓一个 URL，也统一传 `urls: ["https://example.com"]`。

---

## Agent 平台接入（概念示例）
不同平台配置文件路径不同，但核心是把 `crawl4ai-mcp` 作为 stdio MCP server 启动：

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
