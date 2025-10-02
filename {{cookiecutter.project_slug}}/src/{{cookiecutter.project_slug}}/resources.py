{% if cookiecutter.sdk_choice == 'python' and cookiecutter.include_resources == 'yes' -%}
"""Resource implementations for {{ cookiecutter.project_name }}."""

import logging
from typing import List
from mcp.server import Server
from mcp.types import Resource, TextContent

logger = logging.getLogger(__name__)


def register_resources(server: Server):
    """Register all resources with the MCP server."""

    @server.list_resources()
    async def list_resources() -> List[Resource]:
        """List available resources."""
        return [
            Resource(
                uri="example://resource",
                name="Example Resource",
                description="Example resource - replace with your resources",
                mimeType="text/plain"
            )
        ]

    @server.read_resource()
    async def read_resource(uri: str) -> str:
        """Read a resource by URI."""
        logger.info(f"Reading resource: {uri}")

        if uri == "example://resource":
            return "Example resource content"

        raise ValueError(f"Unknown resource: {uri}")
{%- endif %}
