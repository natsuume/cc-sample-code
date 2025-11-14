# MCP Server Minimal - TypeScript版

MCP Serverの最小実装例です。入力されたメッセージをそのまま返す`echo`ツールを提供します。

## 概要

このプロジェクトは、MCP (Model Context Protocol) Serverの基本構造を理解するための最小実装例です。
外部APIを使用せず、シンプルな`echo`ツール1つのみを実装しています。

## 必要要件

- Node.js 18以上
- npm または yarn

## インストール

```bash
# 依存関係のインストール
npm install
```

## Claude Codeへの登録

このMCPサーバーをClaude Codeに登録して使用できます。

### 登録方法

このディレクトリ（`typescript/`）で以下のコマンドを実行してください。

#### claude mcp add コマンドを使用

```bash
claude mcp add --transport stdio minimal-echo --scope project -- npm start
```

#### claude mcp add-json コマンドを使用

```bash
claude mcp add-json minimal-echo '{"type":"stdio","command":"npm","args":["start"]}' --scope project
```

`--scope project` を指定することで、プロジェクトルートに `.mcp.json` ファイルが作成され、チーム全体で共有できます。

## 実行方法

### 開発モード（tsx使用）

```bash
npm run dev
```

### ビルドして実行

```bash
# ビルド
npm run build

# 実行
npm start
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

### リント

```bash
# リントチェック
npm run lint

# 自動修正
npm run lint:fix
```

### 型チェック

```bash
npm run build
```

## プロジェクト構造

```
typescript/
├── src/
│   └── index.ts          # MCPサーバー実装
├── package.json          # プロジェクト設定
├── tsconfig.json         # TypeScript設定
├── eslint.config.js      # ESLint設定
└── README.md             # このファイル
```

## ライセンス

このプロジェクトはサンプルコードです。
