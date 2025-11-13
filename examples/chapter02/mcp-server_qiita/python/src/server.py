#!/usr/bin/env python3
"""Qiita記事検索MCPサーバーのエントリーポイント"""

import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import ValidationError

from .qiita import SearchQiitaParams, search_qiita


async def serve() -> None:
    """MCPサーバーを起動"""
    server = Server("qiita-search")

    @server.list_tools()  # type: ignore[misc, no-untyped-call]
    async def list_tools() -> list[Tool]:
        """利用可能なツールのリストを返す"""
        return [
            Tool(
                name="search_articles",
                description="Qiitaの記事をキーワードで検索します",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "検索キーワードのリスト",
                            "minItems": 1,
                        },
                        "per_page": {
                            "type": "number",
                            "description": "ページあたりの記事数（最大100）",
                            "default": 20,
                            "maximum": 100,
                            "minimum": 1,
                        },
                        "page": {
                            "type": "number",
                            "description": "ページ番号",
                            "default": 1,
                            "minimum": 1,
                        },
                    },
                    "required": ["keywords"],
                },
            )
        ]

    @server.call_tool()  # type: ignore[misc]
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """ツールを実行"""
        if name != "search_articles":
            error_msg = f"Unknown tool: {name}"
            print(error_msg, file=sys.stderr)
            raise ValueError(error_msg)

        try:
            params = SearchQiitaParams.model_validate(arguments)
            articles = await search_qiita(
                keywords=params.keywords,
                per_page=params.per_page,
                page=params.page,
            )

            result = [article.model_dump() for article in articles]

            import json

            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

        except ValidationError as e:
            error_msg = f"Validation error: {e!s}"
            print(error_msg, file=sys.stderr)
            raise

        except Exception as e:
            error_msg = f"Error searching Qiita: {e!s}"
            print(error_msg, file=sys.stderr)
            raise

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """メインエントリーポイント"""
    asyncio.run(serve())


if __name__ == "__main__":
    main()
