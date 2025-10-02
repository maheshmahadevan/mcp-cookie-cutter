{% if cookiecutter.sdk_choice == 'typescript' -%}
#!/usr/bin/env node

/**
 * {{ cookiecutter.project_name }} MCP Server
 * {{ cookiecutter.project_description }}
 */

{% if cookiecutter.deployment_type == 'local' -%}
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
{% else -%}
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";
{% endif -%}
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
{% if cookiecutter.auth_mechanism == 'oauth2' -%}
import { OAuthHandler } from "./auth/oauth.js";
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
import { APIKeyHandler } from "./auth/apiKey.js";
{% endif -%}
import { registerTools } from "./tools.js";
{% if cookiecutter.include_resources == 'yes' -%}
import { registerResources } from "./resources.js";
{% endif -%}
{% if cookiecutter.include_prompts == 'yes' -%}
import { registerPrompts } from "./prompts.js";
{% endif -%}

// Configure logging (always use stderr for STDIO servers)
const log = {
  info: (msg: string) => console.error(`[INFO] ${msg}`),
  error: (msg: string) => console.error(`[ERROR] ${msg}`),
  warn: (msg: string) => console.error(`[WARN] ${msg}`),
};

class {{ cookiecutter.project_name.replace(' ', '').replace('-', '') }}Server {
  private server: Server;
{% if cookiecutter.auth_mechanism == 'oauth2' -%}
  private authHandler: OAuthHandler;
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
  private authHandler: APIKeyHandler;
{% endif -%}

  constructor() {
    this.server = new Server(
      {
        name: "{{ cookiecutter.project_slug }}",
        version: "0.1.0",
      },
      {
        capabilities: {
          tools: {},
{% if cookiecutter.include_resources == 'yes' -%}
          resources: {},
{% endif -%}
{% if cookiecutter.include_prompts == 'yes' -%}
          prompts: {},
{% endif -%}
          logging: {},
        },
      }
    );

{% if cookiecutter.auth_mechanism == 'oauth2' -%}
    this.authHandler = new OAuthHandler();
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
    this.authHandler = new APIKeyHandler();
{% endif -%}

    this.setupHandlers();
  }

  private setupHandlers(): void {
    // Register tools
    registerTools(this.server);

{% if cookiecutter.include_resources == 'yes' -%}
    // Register resources
    registerResources(this.server);
{% endif -%}

{% if cookiecutter.include_prompts == 'yes' -%}
    // Register prompts
    registerPrompts(this.server);
{% endif -%}

    // Error handler
    this.server.onerror = (error) => {
      log.error(`Server error: ${error.message}`);
    };
  }

{% if cookiecutter.deployment_type == 'local' -%}
  async run(): Promise<void> {
    log.info("Starting {{ cookiecutter.project_name }} MCP server (STDIO)");

    const transport = new StdioServerTransport();
    await this.server.connect(transport);

    log.info("Server running on STDIO");
  }
{% else -%}
  async run(): Promise<void> {
    log.info("Starting {{ cookiecutter.project_name }} MCP server (SSE)");

    const app = express();
    const PORT = process.env.PORT || 8000;

{% if cookiecutter.auth_mechanism != 'none' -%}
    // Authentication middleware
    app.use(async (req, res, next) => {
      if (req.path === "/sse") {
        const authenticated = await this.authHandler.authenticate(req);
        if (!authenticated) {
          res.status(401).send("Unauthorized");
          return;
        }
      }
      next();
    });
{% endif -%}

    app.get("/sse", async (req, res) => {
      log.info("New SSE connection");

      const transport = new SSEServerTransport("/messages", res);
      await this.server.connect(transport);
    });

    app.listen(PORT, () => {
      log.info(`Server running on port ${PORT}`);
    });
  }
{% endif -%}
}

// Main entry point
const server = new {{ cookiecutter.project_name.replace(' ', '').replace('-', '') }}Server();
server.run().catch((error) => {
  log.error(`Fatal error: ${error.message}`);
  process.exit(1);
});
{%- endif %}
