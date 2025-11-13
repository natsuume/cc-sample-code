"""Qiita API呼び出し処理のユニットテスト"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from .qiita import QiitaArticle, search_qiita


@pytest.fixture
def mock_article_data() -> dict[str, Any]:
    """モックの記事データ"""
    return {
        "id": "abc123",
        "title": "Test Article",
        "url": "https://qiita.com/user/items/abc123",
        "body": "Test body content",
        "created_at": "2024-01-01T00:00:00+09:00",
        "updated_at": "2024-01-02T00:00:00+09:00",
        "likes_count": 10,
        "stocks_count": 5,
        "user": {
            "id": "user123",
            "name": "Test User",
            "profile_image_url": "https://example.com/profile.png",
        },
        "tags": [
            {"name": "Python", "versions": ["3.10"]},
            {"name": "TypeScript", "versions": ["5.0"]},
        ],
    }


@pytest.mark.asyncio
async def test_search_qiita_success(mock_article_data: dict[str, Any]) -> None:
    """正常なAPIレスポンスの処理テスト"""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = [mock_article_data]
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = mock_client

        articles = await search_qiita(keywords=["Python"])

        assert len(articles) == 1
        assert isinstance(articles[0], QiitaArticle)
        assert articles[0].id == "abc123"
        assert articles[0].title == "Test Article"
        assert articles[0].likes_count == 10
        assert articles[0].user.name == "Test User"
        assert len(articles[0].tags) == 2


@pytest.mark.asyncio
async def test_search_qiita_multiple_articles(mock_article_data: dict[str, Any]) -> None:
    """複数記事の処理テスト"""
    article2 = mock_article_data.copy()
    article2["id"] = "def456"
    article2["title"] = "Second Article"

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = [mock_article_data, article2]
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = mock_client

        articles = await search_qiita(keywords=["Python"])

        assert len(articles) == 2
        assert articles[0].id == "abc123"
        assert articles[1].id == "def456"


@pytest.mark.asyncio
async def test_search_qiita_empty_result() -> None:
    """空の結果の処理テスト"""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = mock_client

        articles = await search_qiita(keywords=["NonExistentKeyword12345"])

        assert len(articles) == 0


@pytest.mark.asyncio
async def test_search_qiita_api_error() -> None:
    """APIエラーの処理テスト"""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=MagicMock(), response=mock_response
    )

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = mock_client

        with pytest.raises(httpx.HTTPStatusError):
            await search_qiita(keywords=["test"])


@pytest.mark.asyncio
async def test_search_qiita_query_construction() -> None:
    """URL構築のテスト"""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = mock_client

        await search_qiita(keywords=["Python", "TypeScript"], per_page=50, page=2)

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args

        assert call_args is not None
        assert call_args.args[0] == "https://qiita.com/api/v2/items"

        params = call_args.kwargs["params"]
        assert "query" in params
        assert "title:Python OR body:Python" in params["query"]
        assert "title:TypeScript OR body:TypeScript" in params["query"]
        assert params["per_page"] == "50"
        assert params["page"] == "2"
