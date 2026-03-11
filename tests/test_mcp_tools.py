"""Test MCP tool registration and interfaces"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_tools_registered() -> None:
    from crawl4ai_mcp.mcp_server import mcp

    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]

    assert "fetch_urls" in tool_names, "must have fetch_urls tool"
    assert "search_web" in tool_names, "must have search_web tool"
    assert "fetch_url" not in tool_names, "should not have fetch_url (removed)"
    assert len(tool_names) == 2, f"expected 2 tools, got {len(tool_names)}: {tool_names}"


@pytest.mark.asyncio
async def test_fetch_urls_has_llm_instruction_parameter() -> None:
    from crawl4ai_mcp.mcp_server import mcp

    tools = await mcp.list_tools()
    fetch_urls_tool = next((t for t in tools if t.name == "fetch_urls"), None)

    assert fetch_urls_tool is not None, "fetch_urls tool must exist"

    props = fetch_urls_tool.inputSchema.get("properties", {})
    assert "llm_instruction" in props
    assert "use_llm" in props
    assert "urls" in props
    assert "concurrency" in props
    assert props["use_llm"].get("default") is False


@pytest.mark.asyncio
async def test_search_web_has_expected_parameters() -> None:
    from crawl4ai_mcp.mcp_server import mcp

    tools = await mcp.list_tools()
    search_tool = next((t for t in tools if t.name == "search_web"), None)

    assert search_tool is not None, "search_web tool must exist"

    props = search_tool.inputSchema.get("properties", {})
    assert "query" in props
    assert "engine" in props
    assert "max_results" in props
    assert props["engine"].get("default") == "auto"
