# Qiita記事検索 MCP Server

Qiita APIを用いて記事を検索するMCP (Model Context Protocol) Serverです。

## 概要

このMCP Serverは、QiitaのパブリックAPIを使用して記事を検索する機能を提供します。
書籍のサンプルコードとして、必要最低限の機能を実装しています。

## 機能

### `search_articles` ツール

Qiita上の記事を検索します。

**入力パラメータ:**

- `keywords` (string[], 必須): 検索キーワードの配列
  - 例: `["TypeScript"]`、`["MCP", "API"]`
  - 各キーワードはタイトルまたは本文から検索されます
- `per_page` (number, オプション): ページあたりの記事数 (デフォルト: 20、最大: 100)
- `page` (number, オプション): ページ番号 (デフォルト: 1)

**出力:**

記事情報の配列（JSON形式）
- `id`: 記事ID
- `title`: 記事タイトル
- `url`: 記事URL
- `body`: 記事本文（Markdown形式）
- `created_at`: 作成日時
- `updated_at`: 更新日時
- `likes_count`: いいね数
- `stocks_count`: ストック数
- `user`: 投稿者情報（id, name, profile_image_url）
- `tags`: タグ情報の配列

## インストール

```bash
npm install
```

## Claude Codeへの登録

このMCPサーバーをClaude Codeに登録して使用できます。

### 登録方法

このディレクトリ（`typescript/`）で以下のコマンドを実行してください。

#### claude mcp add コマンドを使用

```bash
claude mcp add --transport stdio qiita-search --scope project -- npm start
```

#### claude mcp add-json コマンドを使用

```bash
claude mcp add-json qiita-search '{"type":"stdio","command":"npm","args":["start"]}' --scope project
```

`--scope project` を指定することで、プロジェクトルートに `.mcp.json` ファイルが作成され、チーム全体で共有できます。

## 実行

```bash
npm start
```

## 開発

### Lint実行

```bash
npm run lint
```

### Lint自動修正

```bash
npm run lint:fix
```

## 技術仕様

- **言語**: TypeScript
- **実行環境**: Node.js (tsx使用)
- **MCP SDK**: @modelcontextprotocol/sdk
- **バリデーション**: Zod
- **コードスタイル**: ESLint + @stylistic/eslint-plugin

## 注意事項

### Qiita APIのレート制限

Qiita APIには以下のレート制限があります：

**未認証リクエスト（このサーバーの実装）:**
- **制限**: 60リクエスト/時
- **単位**: IPアドレスごと

**認証済みリクエスト（未実装）:**
- **制限**: 1,000リクエスト/時
- **単位**: ユーザーごと

頻繁にリクエストを送信する場合は、レート制限に注意してください。
より高いレート制限が必要な場合は、[Qiitaの設定ページ](https://qiita.com/settings/tokens)からアクセストークンを取得し、
実装を拡張することを検討してください。

### ページネーション

- ページ番号は1から開始します
- `per_page`は最大100まで指定可能です
- 最大100ページまで取得可能です

## ライセンス

MIT
