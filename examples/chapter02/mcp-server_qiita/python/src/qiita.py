"""Qiita API呼び出し処理"""

import sys
from typing import Any

import httpx
from pydantic import BaseModel, Field


class QiitaUser(BaseModel):
    """Qiitaユーザー情報"""

    id: str
    name: str
    profile_image_url: str


class QiitaTag(BaseModel):
    """Qiitaタグ情報"""

    name: str
    versions: list[str]


class QiitaArticle(BaseModel):
    """Qiita記事情報"""

    id: str
    title: str
    url: str
    body: str
    created_at: str
    updated_at: str
    likes_count: int
    stocks_count: int
    user: QiitaUser
    tags: list[QiitaTag]


class SearchQiitaParams(BaseModel):
    """Qiita検索パラメータ"""

    keywords: list[str] = Field(min_length=1)
    per_page: int = Field(default=20, le=100, ge=1)
    page: int = Field(default=1, ge=1)


async def search_qiita(
    keywords: list[str],
    per_page: int = 20,
    page: int = 1,
) -> list[QiitaArticle]:
    """Qiita APIを使用して記事を検索

    Args:
        keywords: 検索キーワードのリスト
        per_page: ページあたりの記事数（デフォルト: 20、最大: 100）
        page: ページ番号（デフォルト: 1）

    Returns:
        検索結果の記事リスト

    Raises:
        httpx.HTTPStatusError: APIリクエストが失敗した場合
    """
    query_parts = [f"title:{keyword} OR body:{keyword}" for keyword in keywords]
    query = " ".join(query_parts)

    params = {
        "query": query,
        "per_page": str(per_page),
        "page": str(page),
    }

    url = "https://qiita.com/api/v2/items"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data: list[dict[str, Any]] = response.json()

            return [QiitaArticle.model_validate(article) for article in data]

    except httpx.HTTPStatusError as e:
        error_message = f"Qiita API error: {e.response.status_code} - {e.response.text}"
        print(error_message, file=sys.stderr)
        raise

    except Exception as e:
        error_message = f"Unexpected error: {e!s}"
        print(error_message, file=sys.stderr)
        raise
