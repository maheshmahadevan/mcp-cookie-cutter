"""{{ cookiecutter.project_name }} FastMCP Server - Main Entry Point."""

import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_server():
    """Create and configure the FastMCP server."""
    from fastmcp import FastMCP

    # Initialize FastMCP server
    mcp = FastMCP(
        name="{{ cookiecutter.project_slug }}"
    )

    # Auto-discover and import tools from tools directory
    tools_dir = Path(__file__).parent / "tools"
    if tools_dir.exists():
        import importlib.util
        import sys

        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name.startswith("_"):
                continue

            module_name = f"{{ cookiecutter.project_slug }}.tools.{tool_file.stem}"
            spec = importlib.util.spec_from_file_location(module_name, tool_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                # Pass mcp instance to module before executing
                module.mcp = mcp
                spec.loader.exec_module(module)
                logger.info(f"Loaded tool module: {module_name}")

    # Auto-discover and import prompts from prompts directory
    prompts_dir = Path(__file__).parent / "prompts"
    if prompts_dir.exists():
        for prompt_file in prompts_dir.glob("*.py"):
            if prompt_file.name.startswith("_"):
                continue

            module_name = f"{{ cookiecutter.project_slug }}.prompts.{prompt_file.stem}"
            spec = importlib.util.spec_from_file_location(module_name, prompt_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                module.mcp = mcp
                spec.loader.exec_module(module)
                logger.info(f"Loaded prompt module: {module_name}")

    return mcp

def main():
    """Run the FastMCP server."""
    import os
    deployment_type = "{{ cookiecutter.deployment_type }}"

    logger.info("Starting {{ cookiecutter.project_name }} FastMCP server")
    mcp = create_server()

    if deployment_type == "remote":
        # Run with HTTP transport using uvicorn for production
        port = int(os.getenv("PORT", "{{ cookiecutter.server_port }}"))
        host = os.getenv("HOST", "0.0.0.0")
        logger.info(f"Starting HTTP server on {host}:{port} with uvicorn")

        # Use uvicorn for production-grade ASGI server
        import uvicorn

        # Get the ASGI app from FastMCP (Streamable HTTP transport)
        # The endpoint will be available at /mcp/
        app = mcp.http_app()

        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    else:
        # Run with STDIO transport (default)
        mcp.run()

if __name__ == "__main__":
    main()
