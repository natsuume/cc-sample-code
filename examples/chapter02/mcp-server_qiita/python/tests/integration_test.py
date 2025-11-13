"""Qiita API統合テスト

注意: このテストは実際のQiita APIを呼び出すため、以下の点に注意してください:
- レート制限（60リクエスト/時）を考慮して実行してください
- ネットワーク接続が必要です
- テスト間に待機時間を設けています
"""

import asyncio

import pytest

from src.qiita import search_qiita


@pytest.mark.asyncio
async def test_search_single_keyword() -> None:
    """単一キーワードでの検索テスト"""
    articles = await search_qiita(keywords=["TypeScript"], per_page=5, page=1)

    assert isinstance(articles, list)

    if len(articles) > 0:
        article = articles[0]

        # 必須フィールドの存在確認
        assert hasattr(article, "id")
        assert hasattr(article, "title")
        assert hasattr(article, "url")
        assert hasattr(article, "body")
        assert hasattr(article, "created_at")
        assert hasattr(article, "updated_at")
        assert hasattr(article, "likes_count")
        assert hasattr(article, "stocks_count")
        assert hasattr(article, "user")
        assert hasattr(article, "tags")

        # ユーザー情報の確認
        assert hasattr(article.user, "id")
        assert hasattr(article.user, "name")
        assert hasattr(article.user, "profile_image_url")

        # タグ情報の確認
        assert isinstance(article.tags, list)

        if len(article.tags) > 0:
            tag = article.tags[0]
            assert hasattr(tag, "name")
            assert hasattr(tag, "versions")
            assert isinstance(tag.versions, list)

    # レート制限を考慮して待機
    await asyncio.sleep(3)


@pytest.mark.asyncio
async def test_search_multiple_keywords() -> None:
    """複数キーワードでの検索テスト"""
    articles = await search_qiita(keywords=["MCP", "API"], per_page=5, page=1)

    assert isinstance(articles, list)

    # 結果が返ってきた場合、各記事の型が正しいことを確認
    for article in articles[:3]:  # 最初の3件のみチェック
        assert hasattr(article, "id")
        assert isinstance(article.id, str)
        assert hasattr(article, "title")
        assert isinstance(article.title, str)
        assert hasattr(article, "url")
        assert isinstance(article.url, str)


@pytest.mark.asyncio
async def test_search_with_pagination() -> None:
    """ページネーションのテスト"""
    # 1ページ目を取得
    articles_page1 = await search_qiita(keywords=["Python"], per_page=3, page=1)

    await asyncio.sleep(3)

    # 2ページ目を取得
    articles_page2 = await search_qiita(keywords=["Python"], per_page=3, page=2)

    # 両方のページで結果が取得できた場合、記事IDが異なることを確認
    if len(articles_page1) > 0 and len(articles_page2) > 0:
        page1_ids = {article.id for article in articles_page1}
        page2_ids = {article.id for article in articles_page2}

        # 異なるページなので、記事が重複していないことを確認
        assert len(page1_ids & page2_ids) == 0, "Different pages should return different articles"


if __name__ == "__main__":
    print("統合テストを実行します...")
    print("注意: 実際のQiita APIを呼び出すため、レート制限に注意してください\n")

    asyncio.run(test_search_single_keyword())
    print("✓ 単一キーワードでの検索テスト完了\n")

    asyncio.run(test_search_multiple_keywords())
    print("✓ 複数キーワードでの検索テスト完了\n")

    asyncio.run(test_search_with_pagination())
    print("✓ ページネーションのテスト完了\n")

    print("すべての統合テストが完了しました")
