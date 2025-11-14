# Qiita記事検索 MCP Server (Python版)

Qiita APIを使用して記事を検索する機能を提供するModel Context Protocol (MCP) サーバーのPython実装です。

## 特徴

- Qiitaのパブリック APIを使用（認証不要）
- キーワードによる記事検索機能
- MCPサーバーとして1つのツール（`search_articles`）を提供
- 厳密な型チェック（mypy strict mode）
- Pydanticによる実行時バリデーション
- 包括的なテストカバレッジ（ユニットテスト、統合テスト）

## 必要要件

- Python 3.10以上
- pip または uv

## インストール

### 1. 依存パッケージのインストール

```bash
cd python

# pipを使用する場合
pip install -e ".[dev]"

# uvを使用する場合（推奨）
uv pip install -e ".[dev]"
```

## Claude Codeへの登録

このMCPサーバーをClaude Codeに登録して使用できます。

### 登録方法

このディレクトリ（`python/`）で以下のコマンドを実行してください。

#### claude mcp add コマンドを使用

```bash
claude mcp add --transport stdio qiita-search --scope project -- python -m src.server
```

#### claude mcp add-json コマンドを使用

```bash
claude mcp add-json qiita-search '{"type":"stdio","command":"python","args":["-m","src.server"]}' --scope project
```

`--scope project` を指定することで、プロジェクトルートに `.mcp.json` ファイルが作成され、チーム全体で共有できます。

## 使用方法

### 2. 開発ツールの確認

```bash
# ruff（リント・フォーマット）
ruff --version

# mypy（型チェック）
mypy --version

# pytest（テスト）
pytest --version
```

## 使用方法

### MCPサーバーとして起動

```bash
python -m src.server
```

または実行権限を付与して直接実行：

```bash
chmod +x src/server.py
./src/server.py
```

### テストの実行

```bash
# すべてのテストを実行
pytest

# ユニットテストのみ実行
pytest src/qiita_test.py

# 統合テストのみ実行（実APIを使用するため注意）
pytest tests/integration_test.py

# カバレッジレポート付き
pytest --cov=src --cov-report=html
```

### コード品質チェック

```bash
# ruffでリント実行
ruff check src tests

# ruffで自動修正
ruff check --fix src tests

# ruffでフォーマット
ruff format src tests

# mypyで型チェック
mypy src tests
```

## プロジェクト構造

```
python/
├── pyproject.toml          # プロジェクト設定・依存関係
├── README.md               # このファイル
├── src/
│   ├── __init__.py         # パッケージ初期化
│   ├── server.py           # MCPサーバーエントリーポイント
│   ├── qiita.py            # Qiita API呼び出し処理
│   └── qiita_test.py       # ユニットテスト
└── tests/
    ├── __init__.py
    └── integration_test.py # 統合テスト
```

## 提供ツール

### `search_articles`

Qiitaの記事をキーワードで検索します。

**パラメータ:**

- `keywords` (string[], 必須): 検索キーワードのリスト（最小1個）
- `per_page` (number, オプション): ページあたりの記事数（デフォルト: 20、最大: 100）
- `page` (number, オプション): ページ番号（デフォルト: 1）

**戻り値:**

JSON形式の記事配列。各記事には以下の情報が含まれます:

- `id`: 記事ID
- `title`: タイトル
- `url`: URL
- `body`: 本文
- `created_at`: 作成日時
- `updated_at`: 更新日時
- `likes_count`: いいね数
- `stocks_count`: ストック数
- `user`: ユーザー情報（id, name, profile_image_url）
- `tags`: タグ情報の配列（name, versions）

## API制限

Qiita APIの未認証リクエストは以下の制限があります:

- **レート制限**: 60リクエスト/時（IPアドレスごと）

統合テストを実行する際は、レート制限に注意してください。

## TypeScript版との対応関係

| TypeScript | Python |
|-----------|--------|
| zod | pydantic |
| vitest | pytest |
| eslint + typescript-eslint | ruff + mypy |
| tsx | python直接実行 |
| fetch API | httpx |
| const/arrow function | async def |

## 開発

### コーディング規約

- **型ヒント**: すべての関数に型ヒントを使用
- **非同期処理**: `async/await` を使用
- **フォーマット**: ruffで自動フォーマット（ダブルクォート、スペースインデント）
- **行の長さ**: 最大100文字
- **Docstring**: すべての公開関数にdocstringを記述

### 品質保証

1. **ruff**: コードスタイルとリント
2. **mypy**: 厳密な型チェック
3. **pydantic**: 実行時の型検証
4. **pytest**: 包括的なテストカバレッジ

すべてのコードはこれらのツールでチェックされ、品質が保証されています。

## ライセンス

このプロジェクトはサンプルコードです。
