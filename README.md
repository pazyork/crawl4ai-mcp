# crawl4ai-mcp

基于 **crawl4ai** 的 **MCP (Model Context Protocol)** 服务：为 Agent 提供「直接可用」的网页抓取与正文提取能力。

## 目标

- 对 JS-heavy 站点也尽量稳定（Zhihu / WeChat MP / Medium / CSDN 等）
- **不配置 LLM 也能用**：默认返回干净的 Markdown / Text
- 可选配置任意 **OpenAI-compatible** 模型（base_url / api_key / model）用于增强抽取/清洗
- MCP 工具面尽量精简：Agent 无需改造提示词，直接接入就能用

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
  "links": [{"text": "...", "url": "..."}]
}
```

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

> 注意：该脚本会访问网络并启动浏览器，耗时较长。
