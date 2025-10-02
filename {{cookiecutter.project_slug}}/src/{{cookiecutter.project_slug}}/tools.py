{% if cookiecutter.sdk_choice == 'python' -%}
"""Tool implementations for {{ cookiecutter.project_name }}."""

import logging
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent

logger = logging.getLogger(__name__)


def register_tools(server: Server):
    """Register all tools with the MCP server."""

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available tools."""
        return [
            Tool(
                name="example_get_request",
                description="Example GET request - customize for your API",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resource_id": {
                            "type": "string",
                            "description": "ID of the resource to fetch"
                        }
                    },
                    "required": ["resource_id"]
                }
            ),
            Tool(
                name="example_post_request",
                description="Example POST request - customize for your API",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "object",
                            "description": "Data to send in the request body"
                        }
                    },
                    "required": ["data"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute a tool."""
        logger.info(f"Calling tool: {name} with arguments: {arguments}")

        # Example GET request
        if name == "example_get_request":
            resource_id = arguments.get("resource_id")
            # TODO: Replace with your API endpoint
            example_response = f"Fetched resource {resource_id} from your API"

            # Example of actual HTTP request (uncomment and customize):
            # import httpx
            # async with httpx.AsyncClient() as client:
            #     response = await client.get(f"https://your-api.com/resource/{resource_id}")
            #     response.raise_for_status()
            #     return [TextContent(type="text", text=response.text)]

            return [TextContent(type="text", text=example_response)]

        # Example POST request
        if name == "example_post_request":
            data = arguments.get("data")
            # TODO: Replace with your API endpoint
            example_response = f"Created resource with data: {data}"

            # Example of actual HTTP request (uncomment and customize):
            # import httpx
            # async with httpx.AsyncClient() as client:
            #     response = await client.post(
            #         "https://your-api.com/resource",
            #         json=data
            #     )
            #     response.raise_for_status()
            #     return [TextContent(type="text", text=response.text)]

            return [TextContent(type="text", text=example_response)]

        raise ValueError(f"Unknown tool: {name}")
{%- endif %}
