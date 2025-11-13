# arxiv論文検索 MCP Server 実装計画

## 作成するファイル

### 0. 実装計画書（ルートディレクトリ）

#### IMPLEMENTATION_PLAN.md
- この実装計画の全内容を保存
- 作業の進捗確認や将来の参照用

### 1. プロジェクト設定ファイル（ルートディレクトリ）

#### package.json
- パッケージ名: `mcp-server-arxiv`
- type: `module`（ESモジュール使用）
- dependencies:
  - `@modelcontextprotocol/sdk` - MCP SDK
  - `zod` - スキーマ検証
  - `fast-xml-parser` - arxiv APIのXMLレスポンスをパース
- devDependencies:
  - `@types/node`
  - `typescript`（型チェック・開発用）
  - `tsx` - TypeScript直接実行用
  - `eslint`、`@eslint/js`、`typescript-eslint`
  - `@stylistic/eslint-plugin`
- scripts:
  - `start`: `tsx src/index.ts`
  - `lint`: ESLint実行
  - `lint:fix`: ESLint自動修正

#### tsconfig.json
- target: ES2022
- module: NodeNext
- moduleResolution: NodeNext
- strict: true（厳密な型チェック）
- outDir: ./dist（ビルド用、今回は使用しないが将来用）
- rootDir: ./src

#### eslint.config.js
- Flat Config形式
- TypeScript-ESLint設定:
  - `recommended-type-checked` - 型情報を使用した基本ルール
  - `stylistic-type-checked` - 型情報を使用したスタイルルール
  - `parserOptions`設定が必須（projectServiceまたはprojectを指定）
- Stylistic設定（コードフォーマット）:
  - インデント: 2スペース
  - 引用符: シングル
  - セミコロン: 必須
  - 最大行長: 100文字
  - オブジェクト/配列のスペース設定
  - **空行関連ルール**:
    - `padding-line-between-statements`: import文後、変数宣言後、return前などに空行挿入
    - `lines-between-class-members`: クラスメンバー間の空行
    - `no-multiple-empty-lines`: 連続空行の制限（最大1行）

### 2. 実装ファイル（srcディレクトリ）

#### src/index.ts
以下の機能を実装：

**MCP Serverの基本構造**
- Server初期化（name: "arxiv-search", version: "1.0.0"）
- StdioServerTransport使用

**ツール実装: `search_papers`**
- inputSchema:
  - `query` (string, 必須): 検索クエリ
  - `max_results` (number, オプション, デフォルト10): 最大結果数
  - `start` (number, オプション, デフォルト0): 開始位置
- 機能:
  1. arxiv API (`http://export.arxiv.org/api/query`) に検索リクエスト
  2. XMLレスポンスをパースして論文情報を抽出
  3. 結果を整形して返却（タイトル、著者、要約、PDF URL等）

**ヘルパー関数**
- `searchArxiv()`: arxiv APIを呼び出す関数
- `parseArxivResponse()`: XMLレスポンスをパースして構造化データに変換

**エラーハンドリング**
- ネットワークエラー
- XMLパースエラー
- 不正なパラメータエラー

### 3. ドキュメント（ルートディレクトリ）

#### README.md
以下のセクションを含む：
- プロジェクト概要
- 機能説明（search_papersツール）
- インストール方法（npm install）
- 実行方法（npm start）
- 使用例
- toolの入力スキーマ説明
- 注意事項（arxiv APIのレート制限など）

## ディレクトリ構造

```
.
├── IMPLEMENTATION_PLAN.md
├── package.json
├── tsconfig.json
├── eslint.config.js
├── README.md
└── src/
    └── index.ts
```

## ESLint設定の詳細

### TypeScript-ESLint Type-Checkedルール
- `recommended-type-checked`: 型情報を使用した推奨ルール
  - プロミスの誤用検出
  - 型アサーションの不適切な使用検出
  - async関数の戻り値チェック
- `stylistic-type-checked`: 型情報を使用したスタイルルール
  - `@typescript-eslint/naming-convention`: 命名規則の統一
  - `@typescript-eslint/consistent-type-imports`: 型インポートの統一
  - `@typescript-eslint/member-ordering`: クラスメンバーの順序
  - `@typescript-eslint/type-annotation-spacing`: 型注釈のスペース
- parserOptions:
  - `projectService: true` または `project: './tsconfig.json'`
  - `tsconfigRootDir: import.meta.dirname`

### Stylistic空行ルール
- `@stylistic/padding-line-between-statements`:
  - import文のグループ後に空行
  - 変数宣言ブロック後に空行
  - return文の前に空行
  - 関数宣言間に空行
- `@stylistic/lines-between-class-members`: クラスメンバー間に空行（シングルライン除く）
- `@stylistic/no-multiple-empty-lines`: 連続空行は最大1行に制限

## 実装の特徴

- **必要最低限**: toolは1つのみ、resourceは実装しない
- **TypeScript直接実行**: tsxを使用、ビルド不要
- **厳密な型チェック**:
  - TypeScript-ESLintのtype-checkedルールで型安全性を最大化
  - Stylisticで統一的なフォーマット（空行含む）
- **XMLパース**: fast-xml-parserで簡潔に処理
- **エラーログ**: console.error()で標準エラー出力へ

## 実装手順

1. IMPLEMENTATION_PLAN.mdを作成（この計画書を保存）
2. package.jsonを作成
3. tsconfig.jsonを作成
4. eslint.config.jsを作成
5. srcディレクトリを作成
6. src/index.tsを実装
7. README.mdを作成
8. npm installで依存関係をインストール
9. npm run lintでコードスタイルを確認
10. npm startで動作確認
