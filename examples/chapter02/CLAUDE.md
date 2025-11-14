# Chapter 02: MCP Server 実装ガイドライン

MCP Serverの実装では、最新のベストプラクティスに従い、deprecated なAPIを使用しないこと。

## TypeScript実装

### ✅ 推奨: McpServerクラスを使用

- `McpServer` クラス（from `@modelcontextprotocol/sdk/server/mcp.js`）
- `server.registerTool()` メソッドでツールを登録
- `StdioServerTransport` でトランスポートを設定

### ❌ 非推奨: Serverクラスの手動実装

- `Server` クラス（from `@modelcontextprotocol/sdk/server/index.js`）
- `setRequestHandler(ListToolsRequestSchema, ...)` による手動実装
- `setRequestHandler(CallToolRequestSchema, ...)` による手動実装

## Python実装

### ✅ 推奨: FastMCPを使用

- `FastMCP` クラス（from `mcp.server.fastmcp`）
- `@mcp.tool()` デコレータでツールを定義
- 型ヒントとdocstringから自動的にスキーマが生成される
- `mcp.run(transport="stdio")` で起動

### ❌ 非推奨: Serverクラスの手動実装

- `Server` クラス（from `mcp.server`）
- `@app.list_tools()` デコレータによる手動実装
- `@app.call_tool()` デコレータによる手動実装
- 手動での `Tool` オブジェクト作成
- 手動での `inputSchema` 定義
- `stdio_server()` による手動のトランスポート管理
