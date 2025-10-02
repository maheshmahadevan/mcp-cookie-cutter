{% if cookiecutter.sdk_choice == 'typescript' -%}
/**
 * Tool implementations for {{ cookiecutter.project_name }}
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const log = {
  info: (msg: string) => console.error(`[INFO] ${msg}`),
};

export function registerTools(server: Server): void {
  // List available tools
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "example_tool",
          description: "Example tool - replace with OpenAPI-generated tools",
          inputSchema: {
            type: "object",
            properties: {
              query: {
                type: "string",
                description: "Example query parameter",
              },
            },
            required: ["query"],
          },
        },
      ],
    };
  });

  // Call a tool
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    log.info(`Calling tool: ${name}`);

    switch (name) {
      case "example_tool": {
        const query = args?.query as string;
        return {
          content: [
            {
              type: "text",
              text: `Example tool executed with query: ${query}`,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  });
}
{%- endif %}
