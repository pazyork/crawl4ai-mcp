# Cloudflare Bypass Enhancement Guide

## Current Status

ProductHunt and some other sites use aggressive Cloudflare protection that blocks standard Playwright. Current success rate: **16/18 golden URLs (89%)**.

## Failed Sites

- ProductHunt.com (Cloudflare Turnstile)
- ProductHunt.com/products/* (Cloudflare Turnstile)

## Solution Options

### Option 1: Use Residential Proxy (Recommended)

**Why it works**: Cloudflare checks IP reputation. Residential IPs have high trust scores.

**Implementation**:
```bash
# Configure in MCP config
"CRAWL4AI_MCP_PROXY": "http://username:password@residential-proxy.com:8000"
```

**Providers**:
- BrightData: https://brightdata.com
- Oxylabs: https://oxylabs.io
- Smartproxy: https://smartproxy.com

### Option 2: Install Patchright (Advanced)

**What is Patchright**: A patched fork of Playwright that fixes CDP leaks and automation detection.

**Installation**:
```bash
pip install patchright
patchright install chrome
```

**Integration** (requires code changes):

1. Replace `from playwright.async_api import async_playwright` with `from patchright.async_api import async_playwright`
2. Use `channel="chrome"` instead of default Chromium
3. Set `headless=False` for better stealth

**Trade-offs**:
- ✅ Better bypass rate
- ✅ No external service needed
- ❌ Requires code fork
- ❌ Headful mode (slower, needs display)

### Option 3: Third-Party Solving Services

**Services that handle Cloudflare**:
- Scrappey.com - Provides pre-solved cookies
- Scrapeless - Cloud browser with CDP
- Bright Data Web Unlocker - Automatic solving

**Trade-offs**:
- ✅ Highest success rate
- ❌ Costs money
- ❌ Requires API integration

## Current Implementation

### What's Already Implemented

1. ✅ Random viewport (980-1480 x 640-980)
2. ✅ Random user agent mode
3. ✅ `--disable-blink-features=AutomationControlled`
4. ✅ `override_navigator=True`
5. ✅ `simulate_user=True` (human-like behavior)
6. ✅ Proxy support (HTTP/HTTPS/SOCKS5)
7. ✅ Domain-specific wait strategies
8. ✅ Cloudflare detection (`blocked=true`)
9. ✅ Extended wait for Cloudflare sites (5s + networkidle)

### What's Missing (Would Require Major Changes)

1. ❌ CDP commands for stealth
2. ❌ WebGL/Canvas fingerprint randomization
3. ❌ AudioContext spoofing
4. ❌ Automatic cookie persistence after Cloudflare clearance
5. ❌ JavaScript challenge evaluation

## Recommendations

### For Most Users

**Use residential proxy** - This solves 90% of Cloudflare issues without code changes.

```json
{
  "env": {
    "CRAWL4AI_MCP_PROXY": "127.0.0.1:7890"
  }
}
```

### For ProductHunt Specifically

ProductHunt requires **both**:
1. Residential proxy (datacenter IPs are blocked immediately)
2. Valid cookies from a real browser session

**Steps**:
1. Open ProductHunt in Chrome
2. Complete Cloudflare challenge manually
3. Export cookies using extension (EditThisCookie, Cookie-Editor)
4. Save to JSON file
5. Configure: `"CRAWL4AI_MCP_COOKIES_JSON": "/path/to/cookies.json"`

### For Developers

If you want to contribute Patchright integration:

1. Fork the repo
2. Add `patchright` as optional dependency
3. Create `PatchrightCrawlService` class
4. Add config flag: `use_patchright=true`
5. Submit PR

## Testing

Test your Cloudflare bypass:

```bash
# Test with proxy
CRAWL4AI_MCP_PROXY=127.0.0.1:7890 python -c "
import asyncio
from crawl4ai_mcp.config import get_settings
from crawl4ai_mcp.crawler import CrawlService, FetchOptions

async def test():
    settings = get_settings()
    async with CrawlService(settings) as service:
        res = await service.fetch(
            url='https://www.producthunt.com/',
            options=FetchOptions(format='markdown', max_chars=120_000),
        )
        print(f'Blocked: {res.get(\"blocked\")}')
        print(f'Content length: {len(str(res.get(\"content\") or \"\"))}')

asyncio.run(test())
"
```

**Success criteria**:
- `blocked=False`
- Content length > 5000 chars
- Content contains "Product Hunt" or product listings

## References

- Patchright: https://github.com/Kaliiiiiiiiii-Vinyzu/patchright
- HasData Cloudflare Bypass: https://github.com/HasData/cloudflare-bypass
- Playwright Stealth: https://github.com/AtuboDad/playwright_stealth
