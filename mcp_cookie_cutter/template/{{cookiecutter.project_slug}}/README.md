# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Overview

This MCP server was generated using the MCP Cookie Cutter framework and provides integration with APIs through the Model Context Protocol.

### Configuration

- **Deployment**: {{ cookiecutter.deployment_type }}
- **Authentication**: {{ cookiecutter.auth_mechanism }}

## Features

- **Tools**: Execute API operations as MCP tools (auto-generated from OpenAPI spec)
- **Prompts**: Auto-generated help prompts for API operations

## Installation

### Python

Using uv (required):

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# For development
uv pip install -e ".[dev]"
```

### Docker (Alternative)

```bash
# Build and run with Docker
docker build -t {{ cookiecutter.project_slug }} .
docker run -p {{ cookiecutter.server_port }}:{{ cookiecutter.server_port }} --env-file .env {{ cookiecutter.project_slug }}

# Or use docker-compose
docker-compose up -d
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` to configure:
- `BASE_URL`: API endpoint (from OpenAPI spec)
{% if cookiecutter.deployment_type == 'remote' -%}
- `PORT`: Server port (default: {{ cookiecutter.server_port }})
{% endif -%}
{% if cookiecutter.auth_mechanism == 'api_key' -%}
- `MCP_SERVER_API_KEY`: API key for MCP server authentication (for clients connecting to this server)
{% elif cookiecutter.auth_mechanism == 'oauth2' -%}
- `OAUTH_CLIENT_ID`: OAuth client ID
- `OAUTH_CLIENT_SECRET`: OAuth client secret (optional for PKCE)
- `OAUTH_ISSUER_URL`: OAuth provider URL
{% endif -%}

{% if cookiecutter.auth_mechanism == 'api_key' -%}
### MCP Server API Key Authentication

Example `.env`:

```env
BASE_URL=https://api.example.com
{% if cookiecutter.deployment_type == 'remote' -%}
PORT={{ cookiecutter.server_port }}
{% endif -%}
MCP_SERVER_API_KEY=your-mcp-server-api-key
```
{% elif cookiecutter.auth_mechanism == 'oauth2' -%}
### OAuth 2.1 Authentication

Example `.env`:

```env
BASE_URL=https://api.example.com
{% if cookiecutter.deployment_type == 'remote' -%}
PORT={{ cookiecutter.server_port }}
{% endif -%}
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
OAUTH_ISSUER_URL=https://auth.example.com
```

**Note**: OAuth 2.1 is recommended for public clients. Use PKCE flow for enhanced security.
{% endif -%}

## Usage

### Quick Start (Testing)

Use the provided test script for quick local testing:

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run the test server (with auto-reload)
python test_server.py
```

This script will:
- Create .env from .env.example if needed
- Start the server with auto-reload on code changes
{% if cookiecutter.deployment_type == 'remote' -%}
- Display health check and MCP endpoint URLs
{% endif -%}

{% if cookiecutter.deployment_type == 'local' -%}
### Local (STDIO) Mode

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run the server
{{ cookiecutter.project_slug }}
```

Or run directly with uv:
```bash
uv run {{ cookiecutter.project_slug }}
```

#### Claude Desktop Configuration

Add to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/{{ cookiecutter.project_slug }}",
        "run",
        "{{ cookiecutter.project_slug }}"
      ],
      "env": {
        "BASE_URL": "{{ '${BASE_URL}' }}"
      }
    }
  }
}
```

Or if using the activated virtual environment:
```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "/path/to/{{ cookiecutter.project_slug }}/.venv/bin/{{ cookiecutter.project_slug }}"
    }
  }
}
```

{% else -%}
### Remote (HTTP/SSE) Mode

This server uses **FastMCP with uvicorn** for production-grade HTTP deployment with streamable HTTP transport support.

#### Running the Server

The server uses **uvicorn** for production-grade ASGI serving:

```bash
# Run directly (uvicorn is used internally)
{{ cookiecutter.project_slug }}

# Or use uvicorn explicitly for more control
# Note: You'll need to create a wrapper module that calls mcp.http_app()
```

The server will start on `http://0.0.0.0:{{ cookiecutter.server_port }}`

**Benefits of uvicorn:**
- Production-grade ASGI server with excellent performance
- Automatic HTTP/2 support
- Graceful shutdown and reload capabilities
- Optimized for async Python applications

#### Docker Deployment

```bash
# Build the image
docker build -t {{ cookiecutter.project_slug }} .

# Run the container
docker run -p {{ cookiecutter.server_port }}:{{ cookiecutter.server_port }} --env-file .env {{ cookiecutter.project_slug }}

# Or use docker-compose
docker-compose up -d
```

#### Health Check

Check server status:
```bash
curl http://localhost:{{ cookiecutter.server_port }}/health
```

Response includes:
- Server version and protocol version
- Active sessions and statistics
- Security features enabled
- MCP capabilities

#### MCP Protocol Endpoints

The server implements the **Streamable HTTP transport** specification:

- **POST /mcp**: Handle MCP JSON-RPC requests
  - Supports session management via `mcp-session-id` header
  - Returns SSE stream for `initialize` method with appropriate Accept header

- **GET /mcp**: SSE stream for server-to-client communication
  - Requires `mcp-session-id` header
  - Keeps connection alive with periodic pings

- **DELETE /mcp**: Terminate session
  - Requires `mcp-session-id` header
  - Closes all active SSE connections for the session

- **GET /health**: Health check endpoint
  - No authentication required
  - Returns server status and statistics

#### Session Management

The server automatically manages sessions with:
- Unique session IDs per API key
- Session timeout (1 hour of inactivity)
- Rate limiting (100 requests per minute per session)
- Support for multiple SSE connections per session

#### Connecting to Remote Server

{% if cookiecutter.auth_mechanism == 'api_key' -%}
Example using curl:

```bash
# Initialize session
curl -X POST http://localhost:{{ cookiecutter.server_port }}/mcp \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}}}'

# The response includes mcp-session-id header

# Call a tool
curl -X POST http://localhost:{{ cookiecutter.server_port }}/mcp \
  -H "Authorization: Bearer your-api-key" \
  -H "mcp-session-id: <session-id>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"tool_name","arguments":{}}}'
```
{% else -%}
Configure your MCP client to connect to:
```
http://your-server:{{ cookiecutter.server_port }}/mcp
```
{% endif -%}

{% if cookiecutter.auth_mechanism != 'none' -%}
Include authentication headers as configured.
{% endif -%}
{% endif -%}

## Testing with MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a visual testing tool for debugging and testing MCP servers.

**Requirements**: Node.js ^22.7.5

{% if cookiecutter.deployment_type == 'remote' -%}
### Test Streamable HTTP Server

```bash
# Start your server first (in another terminal)
python test_server.py

# Then run MCP Inspector (it will auto-detect Streamable HTTP transport)
npx @modelcontextprotocol/inspector \
  --cli http://localhost:{{ cookiecutter.server_port }}/mcp/
```

{% if cookiecutter.auth_mechanism == 'api_key' -%}
**Note**: You may need to configure authentication headers in the Inspector UI.
{% endif -%}
{% else -%}
### Test STDIO Server

```bash
# Run MCP Inspector with your server
npx @modelcontextprotocol/inspector {{ cookiecutter.project_slug }}
```
{% endif -%}

The Inspector UI will open at `http://localhost:6274` where you can:
- Test all available tools with interactive forms
- View and execute prompts
- Inspect server capabilities
- Debug JSON-RPC messages

**Tip**: The `test_server.py` script automatically displays the Inspector command for your configuration.

## Development

### Python Development

```bash
# Run tests
pytest

# Type checking
mypy src

# Format code
black src

# Lint
ruff check src
```

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/
│   └── {{ cookiecutter.project_slug }}/
│       ├── server.py          # FastMCP server with auto-discovery
│       ├── tools/             # Individual tool files (auto-generated)
│       │   ├── __init__.py
│       │   ├── updatePet.py   # Example tool
│       │   └── ...
│       ├── prompts/           # Auto-generated prompts from OpenAPI
│       │   ├── __init__.py
│       │   └── pet_operations.py
│       └── models/            # Pydantic models from OpenAPI
│           ├── __init__.py
│           └── schemas.py
├── .env.example               # Environment variables template
{% if cookiecutter.deployment_type == 'remote' -%}
├── Dockerfile                 # Docker container configuration
├── docker-compose.yml         # Docker compose for easy deployment
{% endif -%}
├── pyproject.toml             # Python project configuration
└── README.md
```

## Security Best Practices

{% if cookiecutter.deployment_type == 'local' -%}
### Local Deployment
- **STDIO Transport**: Runs locally with no network exposure
- Always log to stderr, never stdout
- Validate all input parameters
{% else -%}
### Remote Deployment (HTTP/SSE Transport)

**Built with FastMCP + uvicorn** for production-grade deployment:

- **Streamable HTTP Transport**: Implements MCP protocol over HTTP with SSE
- **Session Management**: Automatic session tracking with `mcp-session-id` headers
- **Rate Limiting**: 100 requests per minute per session
- **Session Timeout**: 1 hour of inactivity
- **CORS Support**: Configurable via `CORS_ORIGINS` environment variable
- **Health Checks**: `/health` endpoint for monitoring
{% if cookiecutter.auth_mechanism == 'none' -%}
- ⚠️ **Warning**: No authentication configured - not recommended for production
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
- **API Key Authentication**: Bearer token validation
- **Session Isolation**: Each API key gets separate sessions
- Store keys securely in environment variables
- Rotate keys regularly
{% elif cookiecutter.auth_mechanism == 'oauth2' -%}
- **OAuth 2.1 Authentication**: Modern authentication flow
- Use PKCE for public clients
- Implement proper token validation
- Follow OAuth 2.1 security best practices
{% endif -%}
- Use HTTPS in production (configure reverse proxy)
- Monitor and log all requests
- Docker-ready with multi-stage builds
{% endif -%}

### General Security
- Obtain explicit user consent for data access
- Protect user data privacy
- Implement proper error handling
- Follow MCP specification guidelines

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [FastMCP Documentation](https://gofastmcp.com)

## License

{{ cookiecutter.license }}

## Author

{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

---

*Generated with MCP Cookie Cutter*
