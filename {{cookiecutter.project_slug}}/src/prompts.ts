{% if cookiecutter.sdk_choice == 'typescript' and cookiecutter.include_prompts == 'yes' -%}
/**
 * Prompt implementations for {{ cookiecutter.project_name }}
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListPromptsRequestSchema, GetPromptRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const log = {
  info: (msg: string) => console.error(`[INFO] ${msg}`),
};

export function registerPrompts(server: Server): void {
  // List available prompts
  server.setRequestHandler(ListPromptsRequestSchema, async () => {
    return {
      prompts: [
        {
          name: "example_prompt",
          description: "Example prompt template",
          arguments: [
            {
              name: "topic",
              description: "Topic to generate prompt for",
              required: true,
            },
          ],
        },
      ],
    };
  });

  // Get a prompt
  server.setRequestHandler(GetPromptRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    log.info(`Getting prompt: ${name}`);

    switch (name) {
      case "example_prompt": {
        const topic = args?.topic as string || "general topic";
        return {
          messages: [
            {
              role: "user",
              content: {
                type: "text",
                text: `Please provide information about ${topic}`,
              },
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown prompt: ${name}`);
    }
  });
}
{%- endif %}
