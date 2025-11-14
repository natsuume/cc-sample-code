#!/usr/bin/env node

/**
 * MCP Server Minimal - TypeScript Implementation
 *
 * 最小限の実装例として、入力されたメッセージをそのまま返すechoツールを提供します。
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

// MCPサーバーインスタンスの作成
const server = new McpServer({
  name: 'mcp-server-minimal',
  version: '0.1.0',
});

// echoツールの登録
server.registerTool(
  'echo',
  {
    description: '入力されたメッセージをそのまま返します',
    inputSchema: {
      message: z.string().describe('エコーバックするメッセージ'),
    },
  },
  async ({ message }) => {
    return {
      content: [
        {
          type: 'text',
          text: `Echo: ${message}`,
        },
      ],
    };
  },
);

// サーバーのメインエントリーポイント
const main = async () => {
  const transport = new StdioServerTransport();

  await server.connect(transport);
};

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
