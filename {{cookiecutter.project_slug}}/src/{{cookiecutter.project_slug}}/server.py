{% if cookiecutter.sdk_choice == 'python' -%}
"""{{ cookiecutter.project_name }} MCP Server."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

{% if cookiecutter.deployment_type == 'local' -%}
from mcp.server import Server
from mcp.server.stdio import stdio_server
{% else -%}
from mcp.server import Server
from mcp.server.sse import sse_server
from starlette.applications import Starlette
from starlette.routing import Route
{% endif -%}
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
{% if cookiecutter.auth_mechanism == 'oauth2' -%}
from .auth.oauth import OAuthHandler
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
from .auth.api_key import APIKeyHandler
{% endif -%}
from .tools import register_tools
{% if cookiecutter.include_resources == 'yes' -%}
from .resources import register_resources
{% endif -%}
{% if cookiecutter.include_prompts == 'yes' -%}
from .prompts import register_prompts
{% endif -%}

# Configure logging to stderr (never stdout for STDIO servers)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Goes to stderr by default
)
logger = logging.getLogger(__name__)


class {{ cookiecutter.project_name.replace(' ', '').replace('-', '') }}Server:
    """MCP Server for {{ cookiecutter.project_name }}."""

    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server("{{ cookiecutter.project_slug }}")
{%- if cookiecutter.auth_mechanism == 'oauth2' %}
        self.auth_handler = OAuthHandler()
{%- elif cookiecutter.auth_mechanism == 'api_key' %}
        self.auth_handler = APIKeyHandler()
{%- endif %}

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register all MCP protocol handlers."""
        # Register tools
        register_tools(self.server)
{% if cookiecutter.include_resources == 'yes' %}

        # Register resources
        register_resources(self.server)
{%- endif %}
{% if cookiecutter.include_prompts == 'yes' %}

        # Register prompts
        register_prompts(self.server)
{%- endif %}

        # Logging handler
        @self.server.set_logging_level()
        async def set_logging_level(level: LoggingLevel) -> None:
            """Set logging level."""
            logger.setLevel(level.upper())
            logger.info(f"Logging level set to {level}")

{% if cookiecutter.deployment_type == 'local' %}
    async def run(self):
        """Run the server using STDIO transport."""
        logger.info("Starting {{ cookiecutter.project_name }} MCP server (STDIO)")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )
{%- else %}
    def create_app(self) -> Starlette:
        """Create Starlette app for SSE transport."""
        async def handle_sse(request):
            """Handle SSE connections."""
{%- if cookiecutter.auth_mechanism != 'none' %}
            # Authenticate request
            if not await self.auth_handler.authenticate(request):
                return Response("Unauthorized", status_code=401)

{%- endif %}
            async with sse_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )

        app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
            ],
        )
        return app

    async def run(self):
        """Run the server using SSE transport."""
        import uvicorn
        logger.info("Starting {{ cookiecutter.project_name }} MCP server (SSE)")
        app = self.create_app()
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()
{%- endif %}


def main():
    """Main entry point."""
    server = {{ cookiecutter.project_name.replace(' ', '').replace('-', '') }}Server()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
{%- endif %}
