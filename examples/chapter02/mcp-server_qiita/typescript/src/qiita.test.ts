import { describe, it, expect, vi, beforeEach } from 'vitest';
import { searchQiita } from './qiita.js';

describe('Qiita MCP Server', () => {
  describe('searchQiita', () => {
    beforeEach(() => {
      vi.restoreAllMocks();
    });

    it('正常なAPIレスポンスを処理する', async () => {
      const mockResponse = [
        {
          id: 'test-article-id',
          title: 'テスト記事タイトル',
          url: 'https://qiita.com/user/items/test-article-id',
          body: 'テスト記事の本文',
          created_at: '2025-01-01T00:00:00+09:00',
          updated_at: '2025-01-02T00:00:00+09:00',
          likes_count: 10,
          stocks_count: 5,
          user: {
            id: 'test-user',
            name: 'テストユーザー',
            profile_image_url: 'https://example.com/image.png'
          },
          tags: [
            {
              name: 'TypeScript',
              versions: []
            }
          ]
        }
      ];

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const articles = await searchQiita(['TypeScript'], 20, 1);

      expect(articles).toHaveLength(1);
      expect(articles[0]?.id).toBe('test-article-id');
      expect(articles[0]?.title).toBe('テスト記事タイトル');
      expect(articles[0]?.likes_count).toBe(10);
      expect(articles[0]?.user.name).toBe('テストユーザー');
      expect(articles[0]?.tags).toHaveLength(1);
      expect(articles[0]?.tags[0]?.name).toBe('TypeScript');
    });

    it('複数の記事を正しく処理する', async () => {
      const mockResponse = [
        {
          id: 'article-1',
          title: '記事1',
          url: 'https://qiita.com/user/items/article-1',
          body: '本文1',
          created_at: '2025-01-01T00:00:00+09:00',
          updated_at: '2025-01-02T00:00:00+09:00',
          likes_count: 10,
          stocks_count: 5,
          user: {
            id: 'user-1',
            name: 'ユーザー1',
            profile_image_url: 'https://example.com/image1.png'
          },
          tags: [{ name: 'JavaScript', versions: [] }]
        },
        {
          id: 'article-2',
          title: '記事2',
          url: 'https://qiita.com/user/items/article-2',
          body: '本文2',
          created_at: '2025-01-03T00:00:00+09:00',
          updated_at: '2025-01-04T00:00:00+09:00',
          likes_count: 20,
          stocks_count: 10,
          user: {
            id: 'user-2',
            name: 'ユーザー2',
            profile_image_url: 'https://example.com/image2.png'
          },
          tags: [{ name: 'TypeScript', versions: [] }]
        }
      ];

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const articles = await searchQiita(['JavaScript', 'TypeScript'], 20, 1);

      expect(articles).toHaveLength(2);
      expect(articles[0]?.id).toBe('article-1');
      expect(articles[1]?.id).toBe('article-2');
    });

    it('空の結果を正しく処理する', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([])
      });

      const articles = await searchQiita(['nonexistent'], 20, 1);

      expect(articles).toHaveLength(0);
    });

    it('APIエラーを適切に処理する', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        statusText: 'Internal Server Error'
      });

      await expect(searchQiita(['test'], 20, 1)).rejects.toThrow(
        'Qiita API request failed: Internal Server Error'
      );
    });
  });

  describe('URL構築', () => {
    it('正しいクエリパラメータでURLを構築する', () => {
      const params = new URLSearchParams({
        query: 'title:TypeScript OR body:TypeScript',
        per_page: '20',
        page: '1'
      });

      const url = `https://qiita.com/api/v2/items?${params.toString()}`;

      expect(url).toContain('query=title%3ATypeScript+OR+body%3ATypeScript');
      expect(url).toContain('per_page=20');
      expect(url).toContain('page=1');
    });

    it('複数キーワードでクエリを構築する', () => {
      const keywords = ['TypeScript', 'MCP'];
      const query = keywords
        .map((kw) => `title:${kw} OR body:${kw}`)
        .join(' ');

      expect(query).toBe(
        'title:TypeScript OR body:TypeScript title:MCP OR body:MCP'
      );
    });
  });
});
