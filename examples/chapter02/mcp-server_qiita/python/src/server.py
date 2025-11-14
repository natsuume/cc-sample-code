#!/usr/bin/env python3
"""Qiita記事検索MCPサーバーのエントリーポイント"""

from typing import Any

from mcp.server.fastmcp import FastMCP

from .qiita import SearchQiitaParams, search_qiita

# MCPサーバーインスタンスの作成
mcp = FastMCP("qiita-search")


@mcp.tool()
async def search_articles(
    keywords: list[str],
    per_page: int = 20,
    page: int = 1,
) -> list[dict[str, Any]]:
    """Qiitaの記事をキーワードで検索します.

    Args:
        keywords: 検索キーワードのリスト
        per_page: ページあたりの記事数（デフォルト: 20、最大: 100）
        page: ページ番号（デフォルト: 1）
    """
    # SearchQiitaParamsでバリデーション
    params = SearchQiitaParams(keywords=keywords, per_page=per_page, page=page)

    articles = await search_qiita(
        keywords=params.keywords,
        per_page=params.per_page,
        page=params.page,
    )

    return [article.model_dump() for article in articles]


def main() -> None:
    """メインエントリーポイント"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
