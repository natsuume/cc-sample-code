#!/usr/bin/env node

/**
 * MCP Server Minimal - TypeScript Implementation
 *
 * 最小限の実装例として、入力されたメッセージをそのまま返すechoツールを提供します。
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';

// echoツールの入力スキーマ
const EchoArgsSchema = z.object({
  message: z.string().describe('エコーバックするメッセージ'),
});

// MCPサーバーインスタンスの作成
const server = new Server(
  {
    name: 'mcp-server-minimal',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

// 利用可能なツールのリストを返す
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'echo',
        description: '入力されたメッセージをそのまま返します',
        inputSchema: {
          type: 'object',
          properties: {
            message: {
              type: 'string',
              description: 'エコーバックするメッセージ',
            },
          },
          required: ['message'],
        },
      },
    ],
  };
});

// ツールの実行
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'echo') {
    const args = EchoArgsSchema.parse(request.params.arguments);

    return {
      content: [
        {
          type: 'text',
          text: `Echo: ${args.message}`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// サーバーのメインエントリーポイント
const main = async () => {
  const transport = new StdioServerTransport();

  await server.connect(transport);
};

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
