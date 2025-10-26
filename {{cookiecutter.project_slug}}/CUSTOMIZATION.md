# Customizing Your MCP Server

This guide shows you how to add tools to your MCP server based on your OpenAPI/Swagger specification.

## Quick Start

The generated server auto-generates tools from your OpenAPI spec. You can also add custom tools:

1. **Review your OpenAPI spec** - Identify the endpoints you want to expose
2. **Custom tools are auto-generated** - Individual tool files in `src/{{ cookiecutter.project_slug }}/tools/`
3. **Test your tools** - Run the server and test with Claude or MCP Inspector

## Auto-Generated Tools

The generator creates individual Python files for each OpenAPI operation in `src/{{ cookiecutter.project_slug }}/tools/`:

```
tools/
├── __init__.py
├── addPet.py          # Auto-generated from POST /pet
├── updatePet.py       # Auto-generated from PUT /pet
├── getPetById.py      # Auto-generated from GET /pet/{petId}
└── ...
```

Each tool file follows this pattern:

```python
"""Auto-generated tool: getPetById"""

import httpx
import os
from typing import Any

# Get BASE_URL from environment or use default from OpenAPI spec
BASE_URL = os.getenv("BASE_URL", "/api/v3")

@mcp.tool()  # type: ignore
async def getPetById(
    petId: int,  # Pet id to return
) -> dict | str:
    """Find pet by ID."""
    url = f"{BASE_URL}/pet/{petId}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}
```

## Common Patterns

### GET Request with Path Parameters

```python
@mcp.tool()
async def get_user(
    userId: int,  # User ID to fetch
) -> dict | str:
    """Get user by ID."""
    url = f"{BASE_URL}/users/{userId}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}
```

### GET Request with Query Parameters

```python
@mcp.tool()
async def search_pets(
    status: str,  # Status values to filter by
) -> dict | str:
    """Find pets by status."""
    url = f"{BASE_URL}/pet/findByStatus"

    async with httpx.AsyncClient() as client:
        params = {}
        if status is not None:
            params["status"] = status

        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}
```

### POST Request with Body

```python
@mcp.tool()
async def create_pet(
    body: dict,  # Request body
) -> dict | str:
    """Add a new pet to the store."""
    url = f"{BASE_URL}/pet"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body)
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}
```

### DELETE Request

```python
@mcp.tool()
async def delete_pet(
    petId: int,  # Pet id to delete
) -> dict | str:
    """Deletes a pet."""
    url = f"{BASE_URL}/pet/{petId}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}
```

## Adding Authentication

{% if cookiecutter.auth_mechanism == 'api_key' -%}
### With API Key

Your server already has API key support. To add API key to tool requests:

```python
@mcp.tool()
async def authenticated_request() -> dict | str:
    """Make an authenticated request."""
    api_key = os.getenv("API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/data",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
```
{% endif -%}

## Error Handling

Tools should handle errors gracefully:

```python
@mcp.tool()
async def safe_request(
    petId: int,
) -> dict | str:
    """Example with error handling."""
    try:
        url = f"{BASE_URL}/pet/{petId}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json() if response.text else {"status": "success"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code}", "detail": e.response.text}
    except Exception as e:
        return {"error": str(e)}
```

## Testing Your Tools

### 1. Run the Server

```bash
source .venv/bin/activate
{{ cookiecutter.project_slug }}
```

Or use the test script with auto-reload:

```bash
python test_server.py
```

### 2. Test with MCP Inspector

MCP Inspector provides a visual interface for testing:

```bash
# Start your server first
python test_server.py

# In another terminal, run MCP Inspector
{% if cookiecutter.deployment_type == 'remote' -%}
npx @modelcontextprotocol/inspector --cli http://localhost:{{ cookiecutter.server_port }}/mcp/
{% else -%}
npx @modelcontextprotocol/inspector {{ cookiecutter.project_slug }}
{% endif -%}
```

The Inspector UI opens at `http://localhost:6274` where you can:
- Test all tools with interactive forms
- View tool schemas
- Inspect request/response messages
- Debug issues

### 3. Test with Claude Desktop

Add to your Claude Desktop config file and restart Claude:

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

Try these prompts in Claude:
- "What tools do you have available?"
- "Get pet with ID 1"
- "Search for available pets"

## Adding Custom Tools

While most tools are auto-generated from your OpenAPI spec, you can add custom tools:

1. Create a new file in `src/{{ cookiecutter.project_slug }}/tools/`
2. Use the `@mcp.tool()` decorator
3. The server auto-discovers all tools in the tools directory

Example custom tool:

```python
"""Custom tool: calculate_summary"""

from typing import Any

@mcp.tool()
async def calculate_summary(
    data: list[dict],  # List of items to summarize
) -> dict:
    """Calculate summary statistics from data."""
    total = len(data)
    # Your custom logic here
    return {
        "total": total,
        "summary": "Custom calculation complete"
    }
```

## Tips

1. **Use Auto-Generated Tools** - They're created from your OpenAPI spec automatically
2. **Check Tool Files** - Review generated files in `src/{{ cookiecutter.project_slug }}/tools/`
3. **Test with Inspector** - Use MCP Inspector for quick visual testing
4. **Watch Logs** - Check server output for errors and debugging info
5. **Environment Variables** - Use `BASE_URL` from .env to configure API endpoints
6. **Add Error Handling** - Always handle HTTP errors and exceptions

## Advanced: Custom Response Formatting

Parse and format responses for better readability:

```python
import json

@mcp.tool()
async def formatted_pet(
    petId: int,
) -> dict | str:
    """Get pet with formatted response."""
    url = f"{BASE_URL}/pet/{petId}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        data = response.json()
        # Format the response
        return {
            "name": data.get("name", "Unknown"),
            "status": data.get("status", "Unknown"),
            "formatted": f"Pet '{data.get('name')}' is {data.get('status')}"
        }
```

## Need Help?

- Check the MCP docs: https://modelcontextprotocol.io
- Review FastMCP docs: https://gofastmcp.com
- Review your OpenAPI spec for endpoint details
- Look at auto-generated tool implementations
- Test with MCP Inspector for debugging

Happy coding! 🚀
