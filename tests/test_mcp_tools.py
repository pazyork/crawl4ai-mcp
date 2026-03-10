"""测试 MCP 工具注册和接口"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_only_fetch_urls_tool_registered() -> None:
    """验证只注册了 fetch_urls 工具，没有 fetch_url"""
    from crawl4ai_mcp.mcp_server import mcp

    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]

    assert "fetch_urls" in tool_names, "必须有 fetch_urls 工具"
    assert "fetch_url" not in tool_names, "不应该有 fetch_url 工具（已移除）"
    assert len(tool_names) == 1, f"只应该有1个工具，实际有 {len(tool_names)} 个: {tool_names}"


@pytest.mark.asyncio
async def test_fetch_urls_has_llm_instruction_parameter() -> None:
    """验证 fetch_urls 工具支持 llm_instruction 参数"""
    from crawl4ai_mcp.mcp_server import mcp

    tools = await mcp.list_tools()
    fetch_urls_tool = next((t for t in tools if t.name == "fetch_urls"), None)

    assert fetch_urls_tool is not None, "fetch_urls 工具必须存在"

    # 检查参数
    props = fetch_urls_tool.inputSchema.get("properties", {})
    assert "llm_instruction" in props, "必须支持 llm_instruction 参数"
    assert "use_llm" in props, "必须支持 use_llm 参数"
    assert "urls" in props, "必须支持 urls 参数"
    assert "concurrency" in props, "必须支持 concurrency 参数"
