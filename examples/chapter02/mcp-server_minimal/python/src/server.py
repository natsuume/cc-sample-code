"""MCP Server Minimal - Python Implementation.

最小限の実装例として、入力されたメッセージをそのまま返すechoツールを提供します。
"""

from mcp.server.fastmcp import FastMCP

# MCPサーバーインスタンスの作成
mcp = FastMCP("mcp-server-minimal")


@mcp.tool()
def echo(message: str) -> str:
    """入力されたメッセージをそのまま返します.

    Args:
        message: エコーバックするメッセージ
    """
    return f"Echo: {message}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
