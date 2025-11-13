"""MCP Server Minimal - Python Implementation.

最小限の実装例として、入力されたメッセージをそのまま返すechoツールを提供します。
"""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# MCPサーバーインスタンスの作成
app = Server("mcp-server-minimal")


@app.list_tools()  # type: ignore[misc, no-untyped-call]
async def list_tools() -> list[Tool]:
    """利用可能なツールのリストを返す."""
    return [
        Tool(
            name="echo",
            description="入力されたメッセージをそのまま返します",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "エコーバックするメッセージ",
                    },
                },
                "required": ["message"],
            },
        ),
    ]


@app.call_tool()  # type: ignore[misc]
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """ツールの実行."""
    if name == "echo":
        message = arguments.get("message", "")
        return [TextContent(type="text", text=f"Echo: {message}")]

    raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    """サーバーのメインエントリーポイント."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
