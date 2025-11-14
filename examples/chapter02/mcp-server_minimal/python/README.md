# MCP Server Minimal - Python版

MCP Serverの最小実装例です。入力されたメッセージをそのまま返す`echo`ツールを提供します。

## 概要

このプロジェクトは、MCP (Model Context Protocol) Serverの基本構造を理解するための最小実装例です。
外部APIを使用せず、シンプルな`echo`ツール1つのみを実装しています。

## 必要要件

- Python 3.10以上
- pip

## インストール

```bash
# 依存関係のインストール
pip install mcp

# 開発ツールのインストール（オプション）
pip install "mcp-server-minimal[dev]"
```

## Claude Codeへの登録

このMCPサーバーをClaude Codeに登録して使用できます。

### 登録方法

このディレクトリ（`python/`）で以下のコマンドを実行してください。

#### claude mcp add コマンドを使用

```bash
claude mcp add --transport stdio minimal-echo --scope project -- python -m src.server
```

#### claude mcp add-json コマンドを使用

```bash
claude mcp add-json minimal-echo '{"type":"stdio","command":"python","args":["-m","src.server"]}' --scope project
```

`--scope project` を指定することで、プロジェクトルートに `.mcp.json` ファイルが作成され、チーム全体で共有できます。

## 実行方法

```bash
# サーバーの起動
python -m src.server
```

## 提供するツール

### echo

入力されたメッセージをそのまま返します。

**パラメータ:**
- `message` (string, 必須): エコーバックするメッセージ

**使用例:**
```json
{
  "message": "Hello, MCP!"
}
```

**レスポンス:**
```
Echo: Hello, MCP!
```

## 開発

### コードフォーマット

```bash
ruff format src/
```

### リント

```bash
ruff check src/
```

### 型チェック

```bash
mypy src/
```

## プロジェクト構造

```
python/
├── src/
│   ├── __init__.py       # パッケージマーカー
│   └── server.py         # MCPサーバー実装
├── pyproject.toml        # プロジェクト設定
└── README.md             # このファイル
```

## ライセンス

このプロジェクトはサンプルコードです。
