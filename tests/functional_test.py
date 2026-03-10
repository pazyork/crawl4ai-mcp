#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import sys
import time
from typing import Any

from crawl4ai_mcp.config import get_settings
from crawl4ai_mcp.crawler import CrawlService, FetchOptions

TEST_CASES = [
    {
        "name": "Basic fetch - example.com",
        "url": "https://example.com",
        "use_llm": False,
        "llm_instruction": None,
        "expected": {
            "min_length": 100,
            "llm_used": False,
            "has_title": True,
        },
    },
]


async def _test_single_case(service: CrawlService, test_case: dict[str, Any]) -> dict[str, Any]:
    start = time.time()
    try:
        res = await service.fetch(
            url=test_case["url"],
            options=FetchOptions(format="markdown", max_chars=120_000),
        )
        elapsed = time.time() - start
        
        content = str(res.get("content") or "")
        title = res.get("title")
        llm_used = res.get("llm_used")
        llm_error = res.get("llm_error")
        blocked = res.get("blocked")
        
        expected = test_case["expected"]
        checks = []
        
        if expected.get("has_title"):
            checks.append(("标题存在", bool(title), title[:50] if title else "无"))
        
        checks.append(("内容长度", len(content) >= expected["min_length"], 
                      f"{len(content)} chars (期望 >= {expected['min_length']})"))
        
        llm_check = (llm_used == expected["llm_used"]) or \
                    (expected["llm_used"] is False and llm_used in (False, None))
        checks.append(("LLM使用", llm_check, 
                      f"实际={llm_used}, 期望={expected['llm_used']}"))
        
        if llm_error:
            checks.append(("LLM错误", False, llm_error[:100]))
        
        if blocked:
            checks.append(("被阻止", False, "检测到验证页面"))
        
        all_passed = all(passed for _, passed, _ in checks)
        
        return {
            "name": test_case["name"],
            "success": all_passed,
            "elapsed": elapsed,
            "checks": checks,
            "content_length": len(content),
            "title": title,
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "name": test_case["name"],
            "success": False,
            "elapsed": elapsed,
            "error": str(e)[:200],
        }


async def test_concurrent() -> dict[str, Any]:
    start = time.time()
    settings = get_settings()
    
    async with CrawlService(settings) as service:
        tasks = [_test_single_case(service, tc) for tc in TEST_CASES]
        results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    return {
        "results": results,
        "total_elapsed": elapsed,
    }


def print_results(data: dict[str, Any]) -> None:
    print("\n" + "=" * 80)
    print("功能测试结果")
    print("=" * 80)
    
    results = data["results"]
    total_elapsed = data["total_elapsed"]
    
    success_count = sum(1 for r in results if r.get("success"))
    total_count = len(results)
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}/{total_count}] {result['name']}")
        print(f"  耗时: {result['elapsed']:.2f}s")
        
        if result.get("error"):
            print(f"  ✗ 错误: {result['error']}")
            continue
        
        if result.get("title"):
            print(f"  标题: {result['title'][:60]}")
        
        print(f"  内容长度: {result.get('content_length', 0)} chars")
        
        checks = result.get("checks", [])
        for check_name, passed, detail in checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}: {detail}")
        
        if result.get("success"):
            print("  ✓ 测试通过")
        else:
            print("  ✗ 测试失败")
    
    print("\n" + "=" * 80)
    print(f"总结: {success_count}/{total_count} 通过")
    print(f"总耗时: {total_elapsed:.2f}s (并发执行)")
    print(f"平均耗时: {total_elapsed/total_count:.2f}s per test")
    print("=" * 80 + "\n")
    
    if success_count < total_count:
        sys.exit(1)


async def main() -> None:
    print("开始功能测试...")
    print(f"测试用例数: {len(TEST_CASES)}")
    print("并发执行: 是")
    
    data = await test_concurrent()
    print_results(data)


if __name__ == "__main__":
    asyncio.run(main())
