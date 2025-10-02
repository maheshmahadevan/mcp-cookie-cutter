{% if cookiecutter.sdk_choice == 'typescript' and cookiecutter.include_resources == 'yes' -%}
/**
 * Resource implementations for {{ cookiecutter.project_name }}
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListResourcesRequestSchema, ReadResourceRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const log = {
  info: (msg: string) => console.error(`[INFO] ${msg}`),
};

export function registerResources(server: Server): void {
  // List available resources
  server.setRequestHandler(ListResourcesRequestSchema, async () => {
    return {
      resources: [
        {
          uri: "example://resource",
          name: "Example Resource",
          description: "Example resource - replace with your resources",
          mimeType: "text/plain",
        },
      ],
    };
  });

  // Read a resource
  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const { uri } = request.params;

    log.info(`Reading resource: ${uri}`);

    switch (uri) {
      case "example://resource":
        return {
          contents: [
            {
              uri,
              mimeType: "text/plain",
              text: "Example resource content",
            },
          ],
        };

      default:
        throw new Error(`Unknown resource: ${uri}`);
    }
  });
}
{%- endif %}
