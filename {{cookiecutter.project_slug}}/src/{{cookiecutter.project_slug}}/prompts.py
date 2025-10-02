{% if cookiecutter.sdk_choice == 'python' and cookiecutter.include_prompts == 'yes' -%}
"""Prompt implementations for {{ cookiecutter.project_name }}."""

import logging
from typing import List
from mcp.server import Server
from mcp.types import Prompt, PromptMessage, TextContent

logger = logging.getLogger(__name__)


def register_prompts(server: Server):
    """Register all prompts with the MCP server."""

    @server.list_prompts()
    async def list_prompts() -> List[Prompt]:
        """List available prompts."""
        return [
            Prompt(
                name="example_prompt",
                description="Example prompt template",
                arguments=[
                    {
                        "name": "topic",
                        "description": "Topic to generate prompt for",
                        "required": True
                    }
                ]
            )
        ]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict) -> PromptMessage:
        """Get a prompt by name."""
        logger.info(f"Getting prompt: {name} with arguments: {arguments}")

        if name == "example_prompt":
            topic = arguments.get("topic", "general topic")
            return PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Please provide information about {topic}"
                )
            )

        raise ValueError(f"Unknown prompt: {name}")
{%- endif %}
