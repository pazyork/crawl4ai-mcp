# crawl4ai-mcp — Agent Installation & Configuration Guide

<div align="center">

[![Single Tool](https://img.shields.io/badge/MCP%20tools-1-0A7EA4)](./README.md)
[![Batch Only](https://img.shields.io/badge/interface-fetch__urls-2563EB)](./README.md)
[![Optional LLM](https://img.shields.io/badge/LLM-optional-7C3AED)](./README.md)

**For AI Agents: A complete guide to install, configure, and troubleshoot crawl4ai-mcp.**

</div>

---

## Quick Reference

| Item | Value |
|---|---|
| Tool count | **2** |
| Tool names | `fetch_urls`, `search_web` |
| Single URL | `urls: ["https://example.com"]` |
| Web search | `search_web(query="...", engine="auto")` |
| LLM default | **off** (enable with `use_llm=true`) |
| Output (fetch) | `title`, `content`, `links`, `blocked`, `llm_used`, `llm_error` |
| Output (search) | `engine`, `query`, `results[{title, url, snippet}]`, `total` |

---

## Installation Steps

### Step 1: Detect Environment

**You should automatically detect:**

```bash
# Check Python version
python3 --version

# Detect OS
uname -s  # Darwin (macOS), Linux, or check for Windows

# Find MCP config location
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
# Linux: ~/.config/Claude/claude_desktop_config.json
# Windows: %APPDATA%\Claude\claude_desktop_config.json
```

**Only ask user if:**
- Python < 3.10 or not found → "Please install Python 3.10+"
- Multiple Python environments detected → "I found both conda and venv. Which do you prefer?"

### Step 2: Clone and Install

**Guide the user through these commands:**

```bash
# Clone the repository
git clone https://github.com/pazyork/crawl4ai-mcp.git
cd crawl4ai-mcp

# For users in China: Use GitHub mirror if needed
# Option 1: Use ghproxy.com mirror
git clone https://ghproxy.com/https://github.com/pazyork/crawl4ai-mcp.git

# Option 2: Use gitclone.com mirror
git clone https://gitclone.com/github.com/pazyork/crawl4ai-mcp.git

# Option 3: Configure git to use proxy
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# Option A: Using conda
conda env create -f environment.yml
conda activate crawl4ai-mcp

# Option B: Using venv
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e '.[dev]'

# For users in China: Use pip mirror for faster installation
pip install -e '.[dev]' -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install Playwright browsers (REQUIRED)
python -m playwright install chromium

# For users in China: Set Playwright mirror
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
python -m playwright install chromium
```

**China-specific acceleration tips:**

1. **GitHub Clone Acceleration:**
   - Use `ghproxy.com` or `gitclone.com` mirrors
   - Or configure git proxy: `git config --global http.proxy http://127.0.0.1:7890`

2. **pip Installation Acceleration:**
   - Tsinghua mirror: `-i https://pypi.tuna.tsinghua.edu.cn/simple`
   - Aliyun mirror: `-i https://mirrors.aliyun.com/pypi/simple/`
   - USTC mirror: `-i https://pypi.mirrors.ustc.edu.cn/simple/`

3. **Playwright Browser Download Acceleration:**
   - Set mirror: `export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/`
   - Or use Taobao mirror: `export PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright/`

### Step 3: Verify Installation

**Test the installation:**

```bash
# Should show help message
crawl4ai-mcp --help

# Run functional tests
python tests/functional_test.py
```

**Expected output:**
```
功能测试结果
================================================================================
总结: 3/3 通过
总耗时: 12.00s (并发执行)
```

---

## Configuration Guide

### Step 4: Detect Configuration Needs

**You should automatically detect:**

```bash
# Check if proxy is needed (detect if user is in China or accessing overseas sites)
curl -s --max-time 3 https://www.google.com > /dev/null && echo "Direct access OK" || echo "May need proxy"

# Check for existing proxy settings
env | grep -i proxy

# Check for OpenAI credentials
env | grep OPENAI
```

**Only ask user for:**
- **Proxy address** if detection shows it's needed: "I detected you may need a proxy for overseas websites. What's your proxy address? (e.g., `127.0.0.1:7890`, or press Enter to skip)"
- **LLM credentials** only if user explicitly wants LLM mode: "Do you want optional LLM-based content cleanup? (y/N)"

**Default to minimal config** - don't ask unnecessary questions.

### Step 5: Generate MCP Config

**Based on user's answers, create the config:**

#### Minimal Config (No Proxy, No LLM)

```json
{
  "mcpServers": {
    "crawl4ai": {
      "command": "/absolute/path/to/crawl4ai-mcp/.venv/bin/crawl4ai-mcp",
      "env": {
        "CRAWL4AI_MCP_HEADLESS": "true"
      }
    }
  }
}
```

#### Full Config (With Proxy and LLM)

```json
{
  "mcpServers": {
    "crawl4ai": {
      "command": "/absolute/path/to/crawl4ai-mcp/.venv/bin/crawl4ai-mcp",
      "env": {
        "CRAWL4AI_MCP_HEADLESS": "true",
        "CRAWL4AI_MCP_PROXY": "127.0.0.1:7890",
        "CRAWL4AI_MCP_NAVIGATION_TIMEOUT_MS": "30000",
        "CRAWL4AI_MCP_WAIT_UNTIL": "load",
        
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "OPENAI_API_KEY": "sk-...",
        "OPENAI_MODEL": "gpt-4o-mini"
      }
    }
  }
}
```

**Important Notes:**
- Replace `/absolute/path/to/crawl4ai-mcp/` with actual path
- `OPENAI_*` vars are **optional** - omit if not using LLM mode
- Proxy formats: `http://host:port`, `socks5://host:port`, `host:port`, or just `port`

### Step 6: Apply Configuration

**Guide user to update their MCP config:**

```bash
# On macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# On Linux
nano ~/.config/Claude/claude_desktop_config.json

# On Windows
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**After editing, restart Claude Desktop.**

---

## Verification & Testing

### Step 7: Verify MCP Connection

**Ask the user to check in Claude Desktop:**

> Please restart Claude Desktop and check:
> 
> 1. Look for the 🔌 icon in the bottom-right corner
> 2. Click it - you should see "crawl4ai" listed
> 3. The status should be "Connected" (green)
> 
> If you see "Error" or "Disconnected", share the error message with me.

### Step 8: Test Basic Functionality

**Run a simple test:**

> Let's test if it works. Please ask Claude to:
> 
> "Use crawl4ai to fetch https://example.com"
> 
> Expected result:
> - Title: "Example Domain"
> - Content: Should contain "This domain is for use in illustrative examples..."
> - No errors

### Step 9: Test Advanced Features

**If user configured proxy:**

> Test overseas website:
> "Fetch https://medium.com/@sampan090611/claude-code-feels-like-a-senior-dev-heres-what-actually-makes-it-different-and-what-the-49c02b456d9c"

**If user configured LLM:**

> Test LLM mode:
> "Fetch https://example.com with use_llm=true and llm_instruction='keep only the main content, remove navigation and ads'"

---

## Troubleshooting

### Problem: "Command not found: crawl4ai-mcp"

**Diagnosis:**
- Installation incomplete or wrong path in config

**Solution:**
```bash
# Find the correct path
which crawl4ai-mcp

# Or if using venv
ls /path/to/crawl4ai-mcp/.venv/bin/crawl4ai-mcp

# Update MCP config with absolute path
```

### Problem: "Playwright browser not found"

**Diagnosis:**
- Playwright browsers not installed

**Solution:**
```bash
cd /path/to/crawl4ai-mcp
source .venv/bin/activate
python -m playwright install chromium
```

### Problem: "Connection timeout" for overseas websites

**Diagnosis:**
- No proxy configured or proxy not working

**Solution:**
1. Verify proxy is running: `curl -x http://127.0.0.1:7890 https://google.com`
2. Add proxy to MCP config: `"CRAWL4AI_MCP_PROXY": "127.0.0.1:7890"`
3. Restart Claude Desktop

### Problem: "blocked=true" in response

**Diagnosis:**
- Website detected automation (Cloudflare, etc.)

**Solution:**
1. **Use proxy** (most effective for overseas sites)
2. **Add cookies**: Save browser cookies to JSON, set `CRAWL4AI_MCP_COOKIES_JSON`
3. **Use persistent profile**: Set `CRAWL4AI_MCP_USE_PERSISTENT_CONTEXT=true`
4. **Increase timeout**: Set `CRAWL4AI_MCP_NAVIGATION_TIMEOUT_MS=60000`

### Problem: LLM mode not working

**Diagnosis:**
- Missing/invalid API credentials or model call failed

**Solution:**
1. Check `llm_error` field in response for details
2. Verify API key: `curl -H "Authorization: Bearer $OPENAI_API_KEY" $OPENAI_BASE_URL/models`
3. Check model name is correct
4. **Fallback**: Non-LLM mode still works! Just omit `use_llm=true`

### Problem: Content is empty or too short

**Diagnosis:**
- Page requires JavaScript or special wait conditions

**Solution:**
1. Increase timeout: `"CRAWL4AI_MCP_NAVIGATION_TIMEOUT_MS": "60000"`
2. Change wait strategy: `"CRAWL4AI_MCP_WAIT_UNTIL": "networkidle"`
3. Check if site is in golden URLs list (pre-configured): [golden_urls.py](./src/crawl4ai_mcp/golden_urls.py)

---

## Tool Usage Reference

### Basic Fetch

```json
{
  "urls": ["https://example.com"],
  "format": "markdown",
  "max_chars": 200000
}
```

### Batch Fetch with Concurrency

```json
{
  "urls": [
    "https://site1.com",
    "https://site2.com",
    "https://site3.com"
  ],
  "format": "markdown",
  "max_chars": 120000,
  "concurrency": 3
}
```

### LLM-Enhanced Fetch

```json
{
  "urls": ["https://blog.example.com/article"],
  "format": "markdown",
  "max_chars": 200000,
  "use_llm": true,
  "llm_instruction": "keep only the article body and code examples, remove navigation, ads, and comments"
}
```

### HTML Format

```json
{
  "urls": ["https://example.com"],
  "format": "html",
  "max_chars": 200000
}
```

### Web Search (auto fallback)

```json
{
  "query": "latest AI agent frameworks",
  "engine": "auto",
  "max_results": 10
}
```

When `engine="auto"`, tries: DuckDuckGo → Bing → Google → Baidu.

### Web Search (specific engine)

```json
{
  "query": "crawl4ai tutorial",
  "engine": "google",
  "max_results": 5,
  "lang": "en"
}
```

---

## Environment Variables Reference

| Variable | Default | Description |
|---|---|---|
| `CRAWL4AI_MCP_HEADLESS` | `true` | Run browser in headless mode |
| `CRAWL4AI_MCP_PROXY` | - | Proxy server (http/https/socks5) |
| `CRAWL4AI_MCP_COOKIES_JSON` | - | Path to Playwright storage_state JSON |
| `CRAWL4AI_MCP_USE_PERSISTENT_CONTEXT` | `false` | Reuse browser profile |
| `CRAWL4AI_MCP_USER_DATA_DIR` | - | Browser profile directory |
| `CRAWL4AI_MCP_NAVIGATION_TIMEOUT_MS` | `30000` | Page load timeout (ms) |
| `CRAWL4AI_MCP_WAIT_UNTIL` | `load` | Wait strategy: `load`, `domcontentloaded`, `networkidle` |
| `CRAWL4AI_MCP_CLOUDFLARE_BYPASS` | `false` | Enable aggressive Cloudflare bypass |
| `OPENAI_BASE_URL` | - | OpenAI-compatible API base URL |
| `OPENAI_API_KEY` | - | API key |
| `OPENAI_MODEL` | - | Model name (e.g., `gpt-4o-mini`) |

---

## Common Scenarios

### Scenario 1: Domestic websites only (China)

**Config:**
```json
{
  "command": "/path/to/.venv/bin/crawl4ai-mcp",
  "env": {
    "CRAWL4AI_MCP_HEADLESS": "true"
  }
}
```

**Works great for:** Zhihu, WeChat, CSDN, Bilibili, etc.

### Scenario 2: Overseas websites with proxy

**Config:**
```json
{
  "command": "/path/to/.venv/bin/crawl4ai-mcp",
  "env": {
    "CRAWL4AI_MCP_HEADLESS": "true",
    "CRAWL4AI_MCP_PROXY": "127.0.0.1:7890"
  }
}
```

**Works great for:** Medium, GitHub, ProductHunt, etc.

### Scenario 3: Research with LLM cleanup

**Config:**
```json
{
  "command": "/path/to/.venv/bin/crawl4ai-mcp",
  "env": {
    "CRAWL4AI_MCP_HEADLESS": "true",
    "CRAWL4AI_MCP_PROXY": "127.0.0.1:7890",
    "OPENAI_BASE_URL": "https://api.openai.com/v1",
    "OPENAI_API_KEY": "sk-...",
    "OPENAI_MODEL": "gpt-4o-mini"
  }
}
```

**Use case:** Extract clean article content, remove ads/navigation

---

## Success Checklist

- [ ] Python 3.9+ installed
- [ ] Repository cloned
- [ ] Dependencies installed (`pip install -e '.[dev]'`)
- [ ] Playwright browsers installed (`playwright install chromium`)
- [ ] Functional tests pass (`python tests/functional_test.py`)
- [ ] MCP config file updated with absolute path
- [ ] Claude Desktop restarted
- [ ] MCP connection shows "Connected" in Claude
- [ ] Test fetch works: `https://example.com`
- [ ] (Optional) Proxy configured and tested
- [ ] (Optional) LLM credentials configured and tested

---

## Getting Help

**If you encounter issues:**

1. Check the troubleshooting section above
2. Run diagnostic: `python tests/functional_test.py`
3. Check MCP logs in Claude Desktop (Help → View Logs)
4. Review [README.md](./README.md) for detailed documentation
5. Check [golden_urls.py](./src/crawl4ai_mcp/golden_urls.py) for pre-configured sites

**For human developers:**
- Full docs: [README.md](./README.md)
- 中文文档: [README.zh-CN.md](./README.zh-CN.md)
- GitHub Issues: [Report a bug](https://github.com/pazyork/crawl4ai-mcp/issues)
