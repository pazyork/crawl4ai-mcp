# crawl4ai-mcp

基于 **crawl4ai** 的 **MCP (Model Context Protocol)** 服务：为 Agent 提供「直接可用」的网页抓取与正文提取能力。

## 目标

- 对 JS-heavy 站点也尽量稳定（Zhihu / WeChat MP / Medium / CSDN 等）
- **不配置 LLM 也能用**：默认返回干净的 Markdown / Text
- 可选配置任意 **OpenAI-compatible** 模型（base_url / api_key / model）用于增强抽取/清洗
- MCP 工具面尽量精简：Agent 无需改造提示词，直接接入就能用

## 当前能力（MCP 保持精简）

### 核心能力（不依赖 LLM，解决“非 LLM 模式”痛点）

- **动态网页抓取**：基于 Playwright 的真实浏览器渲染（crawl4ai），对 JS-heavy 页面更稳
- **正文优先的 Markdown**：默认返回更适合模型消费的 Markdown（去掉部分 CTA/噪音、压缩空行、去掉 data:image 占位）
- **图片信息不丢失（部分站点）**：例如 WeChat 文章会追加 `## Images` 列表，保留图片 URL 供后续处理
- **抗干扰与降级**：两阶段抓取（快速 → 强力重试），并返回 `blocked=true` 提示可能命中验证/反爬
- **批量抓取**：`fetch_urls` 支持并发上限（不会无限并发把自己打死）
- **伪装与随机性**（无需改 MCP 工具面）：随机 UA、随机 viewport、随机请求节奏抖动、navigator 覆盖、必要时模拟用户行为
- **可控接入**：代理 / cookies / persistent profile（解决验证码/登录态/频控场景的现实痛点）

### 可选能力（有 LLM 时能做什么）

在 `use_llm=true` 且配置了 OpenAI-compatible 参数时，会在抓取完成后做一次“内容清洗/重写”为更干净的 Markdown：

- 统一结构（标题、段落、代码块）
- 更强的噪音删除（站点 CTA、导航碎片）
- 更接近“可直接 RAG/检索”的正文

任何一个 LLM 参数缺失、非法、或模型不可用时，会自动降级回非 LLM 模式（不会影响基础抓取）。

## 协议

本项目使用 **AGPL-3.0-or-later**：如果你将本服务作为网络服务对外提供（包括修改后提供），需要向使用者提供对应的源代码。这会显著提高“免费商用并私有改造”的门槛。

## 安装

> Python 3.9 - 3.12（推荐 3.11）

### Conda

```bash
conda env create -f environment.yml
conda activate crawl4ai-mcp
```

### 中国大陆 pip 镜像（可选）

网络环境较慢时可以临时指定镜像：

```bash
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e '.[dev]'
```

### venv（可选）

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

### Playwright/浏览器依赖

`crawl4ai` 依赖浏览器环境。若首次运行报缺少浏览器/驱动，请按提示安装（不同版本可能略有差异）。

常见命令：

```bash
python -m playwright install
```

## 运行 MCP Server（stdio）

```bash
crawl4ai-mcp
```

### 配置（环境变量）

- `CRAWL4AI_MCP_HEADLESS`：`true/false`（默认 `true`）
- `CRAWL4AI_MCP_USER_AGENT`：自定义 UA（可选）
- `CRAWL4AI_MCP_PROXY`：代理（可选）
- `CRAWL4AI_MCP_COOKIES_JSON`：cookies JSON 文件路径（可选，Playwright 格式）
- `CRAWL4AI_MCP_MAX_RETRIES`：失败重试次数（默认 `1`）
- `CRAWL4AI_MCP_USE_PERSISTENT_CONTEXT`：复用浏览器 profile（默认 `false`）
- `CRAWL4AI_MCP_USER_DATA_DIR`：浏览器 profile 目录（可选，建议配合 persistent_context 用于反爬站点）

伪装/随机化（可选，默认已开启一些随机性）：

- `CRAWL4AI_MCP_VIEWPORT_WIDTH_MIN` / `CRAWL4AI_MCP_VIEWPORT_WIDTH_MAX`
- `CRAWL4AI_MCP_VIEWPORT_HEIGHT_MIN` / `CRAWL4AI_MCP_VIEWPORT_HEIGHT_MAX`
- `CRAWL4AI_MCP_LOCALE`（默认 `zh-CN`）
- `CRAWL4AI_MCP_TIMEZONE_ID`（默认 `Asia/Shanghai`）
- `CRAWL4AI_MCP_MEAN_DELAY_S` / `CRAWL4AI_MCP_MAX_DELAY_JITTER_S`（请求间隔随机抖动）

OpenAI-compatible（可选）：

- `OPENAI_BASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`

## MCP 工具

### `fetch_url`

输入：

```json
{
  "url": "https://example.com",
  "format": "markdown",
  "max_chars": 200000,
  "use_llm": false
}
```

输出（示例字段，实际以返回为准）：

```json
{
  "url": "...",
  "final_url": "...",
  "title": "...",
  "content": "...",
  "content_format": "markdown",
  "extracted_at": "2026-03-10T00:00:00Z",
  "links": [{"text": "...", "url": "..."}],
  "blocked": false
}
```

`blocked=true` 表示疑似命中反爬/验证页（例如“当前环境异常/去验证/Access Denied”）；此时建议配置代理或 cookies 再试。

### `fetch_urls`

批量抓取：

```json
{
  "urls": ["https://a.com", "https://b.com"],
  "format": "markdown",
  "max_chars": 200000,
  "concurrency": 3,
  "use_llm": false
}
```

## Claude Desktop/Windsurf 配置示例

将如下片段加入你的 MCP 配置（路径和命令按实际环境调整）：

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

## 开发

### 运行测试

```bash
ruff check .
pytest
```

### Golden URLs 烟囱测试（手动）

```bash
python -m crawl4ai_mcp.smoke_golden
```

输出完整 Markdown：

```bash
CRAWL4AI_MCP_SMOKE_FULL=1 python -m crawl4ai_mcp.smoke_golden
```

保存到目录（每个 URL 一个 `.md` 文件）：

```bash
CRAWL4AI_MCP_SMOKE_DIR=./_golden_outputs python -m crawl4ai_mcp.smoke_golden
```

> 注意：该脚本会访问网络并启动浏览器，耗时较长。
