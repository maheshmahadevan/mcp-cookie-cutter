#!/usr/bin/env python3
"""Local test script for {{ cookiecutter.project_name }} MCP server."""

import os
import sys
import subprocess
from pathlib import Path

def print_inspector_info(deployment_type, project_slug, port):
    """Print MCP Inspector usage information."""
    print("\n" + "="*70)
    print("🔍 MCP Inspector Testing")
    print("="*70)
    print("\nYou can test this server with MCP Inspector:")
    print("\nRequires: Node.js ^22.7.5")

    if deployment_type == "remote":
        print(f"\n# Test Streamable HTTP server:")
        print(f"npx @modelcontextprotocol/inspector \\")
        print(f"  --cli http://localhost:{port}/mcp/")
    else:
        print(f"\n# Test STDIO server:")
        print(f"npx @modelcontextprotocol/inspector {project_slug}")

    print("\nInspector UI will open at: http://localhost:6274")
    print("="*70 + "\n")

def main():
    """Run the MCP server locally for testing."""
    deployment_type = "{{ cookiecutter.deployment_type }}"
    project_slug = "{{ cookiecutter.project_slug }}"

    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found.")
        print("   Creating from .env.example...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✓ Created .env file. Please edit it with your configuration.")
        else:
            print("❌ .env.example not found. Please create .env manually.")
            return 1

    print(f"\n🚀 Starting {project_slug} server in {deployment_type} mode...\n")

    if deployment_type == "remote":
        # Run HTTP server with uvicorn
        port = os.getenv("PORT", "{{ cookiecutter.server_port }}")
        host = os.getenv("HOST", "0.0.0.0")

        print(f"Starting HTTP server on {host}:{port}")
        print(f"MCP endpoint: http://localhost:{port}/mcp/")
        print("\nPress CTRL+C to stop the server.\n")

        # Print MCP Inspector info
        print_inspector_info(deployment_type, project_slug, port)

        wrapper_file = f"{project_slug}_uvicorn_wrapper.py"
        try:
            # Create a wrapper module for uvicorn
            wrapper_code = f"""
import os
os.environ['PORT'] = '{port}'
os.environ['HOST'] = '{host}'

from {project_slug}.server import create_server

mcp = create_server()
app = mcp.http_app()
"""

            # Write temporary wrapper
            with open(wrapper_file, 'w') as f:
                f.write(wrapper_code)

            # Run with uvicorn and auto-reload
            subprocess.run([
                sys.executable, "-m", "uvicorn",
                f"{wrapper_file.replace('.py', '')}:app",
                "--host", host,
                "--port", port,
                "--reload"  # Auto-reload on code changes
            ])
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped.")
        finally:
            # Clean up wrapper file
            if os.path.exists(wrapper_file):
                os.remove(wrapper_file)

        return 0
    else:
        # Run STDIO server
        print("Starting STDIO server...")
        print("This will run in stdio mode for Claude Desktop integration.")
        print("\nPress CTRL+C to stop the server.\n")

        # Print MCP Inspector info
        print_inspector_info(deployment_type, project_slug, None)

        try:
            subprocess.run([sys.executable, "-m", project_slug])
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped.")
            return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())
