# Chapter 02: MCP Server 実装ガイドライン

このディレクトリには、Model Context Protocol (MCP) サーバーの実装例が含まれています。

## プロジェクト構成

- `mcp-server_minimal/`: 最小限のMCPサーバー実装例（TypeScript/Python）
- `mcp-server_qiita/`: Qiita記事検索MCPサーバー実装例（Python）

## 実装ガイドライン

### TypeScript実装

#### ✅ 使用すべき実装パターン

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new McpServer({
  name: 'your-server-name',
  version: '1.0.0',
});

// ツールの登録
server.registerTool(
  'tool_name',
  {
    description: 'ツールの説明',
    inputSchema: YourZodSchema,
  },
  async (args) => {
    // ツールの実装
    return { content: [{ type: 'text', text: 'result' }] };
  }
);

// サーバーの起動
const transport = new StdioServerTransport();
await server.connect(transport);
```

#### ❌ 使用禁止（deprecated）

- `Server` クラス（from `@modelcontextprotocol/sdk/server/index.js`）
- `setRequestHandler(ListToolsRequestSchema, ...)` による手動実装
- `setRequestHandler(CallToolRequestSchema, ...)` による手動実装

### Python実装

#### ✅ 使用すべき実装パターン

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("your-server-name")

@mcp.tool()
def tool_name(arg1: str, arg2: int = 10) -> str:
    """ツールの説明.

    Args:
        arg1: 引数1の説明
        arg2: 引数2の説明（デフォルト: 10）
    """
    # ツールの実装
    return "result"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**重要なポイント:**
- 型ヒント（type hints）が必須
- docstringから自動的にスキーマが生成される
- 戻り値は自動的にJSONシリアライズされる

#### ❌ 使用禁止（古い実装パターン）

- `Server` クラス（from `mcp.server`）
- `@app.list_tools()` デコレータによる手動実装
- `@app.call_tool()` デコレータによる手動実装
- 手動での `Tool` オブジェクト作成
- 手動での `inputSchema` 定義
- `stdio_server()` による手動のトランスポート管理

## コーディング原則

1. **最新のベストプラクティスに準拠**
   - 公式SDKのドキュメントを参照
   - deprecatedなAPIは使用しない

2. **型安全性を重視**
   - TypeScript: strict mode を有効化
   - Python: 型ヒント（type hints）を必須化

3. **宣言的でシンプルなコード**
   - 手動実装より宣言的なAPIを優先
   - ボイラープレートコードを最小化

4. **自動生成機能の活用**
   - TypeScript: Zodスキーマからの型推論
   - Python: 型ヒントとdocstringからのスキーマ自動生成

## 参考リンク

- [MCP公式ドキュメント](https://modelcontextprotocol.io/)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 実装時の注意事項

### 型ヒントとスキーマ

**TypeScript:**
```typescript
// Zodスキーマを使用
const ArgsSchema = z.object({
  message: z.string().describe('メッセージ'),
  count: z.number().optional(),
});
```

**Python:**
```python
# 型ヒントとdocstringを使用
def tool_name(message: str, count: int = 1) -> dict[str, Any]:
    """メッセージを指定回数返す.

    Args:
        message: 返すメッセージ
        count: 繰り返し回数（デフォルト: 1）
    """
    pass
```

### エラーハンドリング

FastMCP/McpServerは自動的にエラーをハンドリングするため、過度なtry-exceptは不要です。
必要に応じて、ビジネスロジックに関連するエラーのみをハンドリングしてください。

### 非同期処理

**TypeScript:**
```typescript
// 非同期関数として実装
async ({ arg1, arg2 }) => {
  const result = await someAsyncOperation();
  return { content: [{ type: 'text', text: result }] };
}
```

**Python:**
```python
# 同期/非同期どちらでも可
@mcp.tool()
async def async_tool(arg: str) -> str:
    result = await some_async_operation()
    return result

@mcp.tool()
def sync_tool(arg: str) -> str:
    result = some_sync_operation()
    return result
```

## 更新履歴

- 2025-01-14: 初版作成。deprecated な実装から最新のベストプラクティスへの移行完了
