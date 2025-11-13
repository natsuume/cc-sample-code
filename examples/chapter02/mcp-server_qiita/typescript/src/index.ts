#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { searchQiita } from './qiita.js';

const server = new McpServer({
  name: 'qiita-search',
  version: '1.0.0'
});

server.registerTool(
  'search_articles',
  {
    title: 'Search Qiita Articles',
    description: 'Search for articles on Qiita by keywords',
    inputSchema: {
      keywords: z.array(z.string()).min(1).describe(
        'Keywords to search for in article titles or body'
      ),
      per_page: z.number().optional().default(20).describe(
        'Number of articles per page (default: 20, max: 100)'
      ),
      page: z.number().optional().default(1).describe(
        'Page number (default: 1)'
      )
    }
  },
  async ({ keywords, per_page, page }) => {
    try {
      const articles = await searchQiita(keywords, per_page, page);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(articles, null, 2)
          }
        ]
      };
    } catch (error) {
      const errorMessage = error instanceof Error
        ? error.message
        : 'Unknown error occurred';

      throw new Error(errorMessage);
    }
  }
);

const main = async (): Promise<void> => {
  const transport = new StdioServerTransport();

  await server.connect(transport);

  console.error('Qiita MCP Server running on stdio');
};

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
