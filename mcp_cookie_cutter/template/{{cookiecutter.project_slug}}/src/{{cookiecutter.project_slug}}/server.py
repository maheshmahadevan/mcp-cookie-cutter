"""{{ cookiecutter.project_name }} FastMCP Server - Main Entry Point."""

import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    deployment_type = "{{ cookiecutter.deployment_type }}"
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"
    allow_unauthenticated = "{{ cookiecutter.allow_unauthenticated_access }}" == "y"

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

        # Add authentication middleware if API key auth is enabled
        if auth_mechanism == "api_key":
            from starlette.middleware.base import BaseHTTPMiddleware
            from starlette.responses import JSONResponse

            # Check if API key is set
            expected_key = os.getenv("MCP_SERVER_API_KEY", "")

            if not expected_key and not allow_unauthenticated:
                logger.error("SECURITY ERROR: MCP_SERVER_API_KEY not set and unauthenticated access is disabled")
                logger.error("Please set MCP_SERVER_API_KEY in your .env file or enable allow_unauthenticated_access during generation")
                raise ValueError("MCP_SERVER_API_KEY is required but not set. Server will not start.")

            if not expected_key and allow_unauthenticated:
                logger.warning("WARNING: MCP_SERVER_API_KEY not set - running WITHOUT authentication")
                logger.warning("This is a security risk. Please set MCP_SERVER_API_KEY in production.")

            class AuthMiddleware(BaseHTTPMiddleware):
                async def dispatch(self, request, call_next):
                    # Skip auth for health check endpoint
                    if request.url.path in ["/health", "/healthz"]:
                        return await call_next(request)

                    # Get API key from environment
                    api_key = os.getenv("MCP_SERVER_API_KEY", "")

                    # If no API key is set
                    if not api_key:
                        if allow_unauthenticated:
                            # Allow access without authentication (if explicitly enabled)
                            return await call_next(request)
                        else:
                            # Deny access (secure by default)
                            logger.error("Authentication required but MCP_SERVER_API_KEY not set")
                            return JSONResponse(
                                status_code=500,
                                content={"error": "Server configuration error - authentication not properly configured"}
                            )

                    # Check for API key in Authorization header
                    auth_header = request.headers.get("Authorization", "")

                    # Support both "Bearer <key>" and direct key
                    token = auth_header.replace("Bearer ", "").strip() if auth_header else ""

                    if token != api_key:
                        logger.warning(f"Unauthorized access attempt from {request.client.host}")
                        return JSONResponse(
                            status_code=401,
                            content={"error": "Unauthorized - Invalid API key"}
                        )

                    return await call_next(request)

            app.add_middleware(AuthMiddleware)
            if expected_key:
                logger.info("✓ API key authentication enabled and MCP_SERVER_API_KEY is set")
            else:
                logger.warning("⚠ Authentication disabled - unauthenticated access allowed")

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
