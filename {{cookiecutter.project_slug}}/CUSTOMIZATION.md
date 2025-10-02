# Customizing Your MCP Server

This guide shows you how to add tools to your MCP server based on your OpenAPI/Swagger specification.

## Quick Start

The generated server includes example tools. Follow these steps to customize them for your API:

1. **Review your OpenAPI spec** - Identify the endpoints you want to expose
2. **Update tool definitions** - Modify the `list_tools()` handler
3. **Implement tool logic** - Add HTTP client code in `call_tool()` handler
4. **Test your tools** - Run the server and test with Claude

## Example: Adding a Tool from OpenAPI

### Step 1: Identify an Endpoint

From your OpenAPI spec, find an endpoint. For example:

```yaml
paths:
  /pet/{petId}:
    get:
      operationId: getPetById
      summary: Find pet by ID
      parameters:
        - name: petId
          in: path
          required: true
          schema:
            type: integer
```

### Step 2: Add Tool Definition

{% if cookiecutter.sdk_choice == 'python' -%}
In `src/{{ cookiecutter.project_slug }}/tools.py`, update the `list_tools()` function:

```python
@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="getPetById",
            description="Find pet by ID from the Petstore API",
            inputSchema={
                "type": "object",
                "properties": {
                    "petId": {
                        "type": "integer",
                        "description": "ID of the pet to retrieve"
                    }
                },
                "required": ["petId"]
            }
        )
    ]
```
{% else -%}
In `src/tools.ts`, update the `ListToolsRequestSchema` handler:

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "getPetById",
        description: "Find pet by ID from the Petstore API",
        inputSchema: {
          type: "object",
          properties: {
            petId: {
              type: "integer",
              description: "ID of the pet to retrieve",
            },
          },
          required: ["petId"],
        },
      },
    ],
  };
});
```
{% endif -%}

### Step 3: Implement Tool Logic

{% if cookiecutter.sdk_choice == 'python' -%}
Add the implementation in `call_tool()`:

```python
@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute a tool."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")

    if name == "getPetById":
        import httpx

        pet_id = arguments.get("petId")
        url = f"https://petstore.swagger.io/v2/pet/{pet_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            return [
                TextContent(
                    type="text",
                    text=response.text
                )
            ]

    raise ValueError(f"Unknown tool: {name}")
```

**Note**: Add `httpx` to dependencies in `pyproject.toml`:

```toml
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",  # Add this line
]
```
{% else -%}
Add the implementation in `CallToolRequestSchema` handler:

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  log.info(`Calling tool: ${name}`);

  switch (name) {
    case "getPetById": {
      const petId = args?.petId as number;
      const url = `https://petstore.swagger.io/v2/pet/${petId}`;

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.text();

      return {
        content: [
          {
            type: "text",
            text: data,
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});
```
{% endif -%}

## Common Patterns

### GET Request with Path Parameters

{% if cookiecutter.sdk_choice == 'python' -%}
```python
async def get_user(arguments: Dict[str, Any]) -> List[TextContent]:
    user_id = arguments.get("userId")
    url = f"https://api.example.com/users/{user_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return [TextContent(type="text", text=response.text)]
```
{% else -%}
```typescript
async function getUser(args: any): Promise<string> {
  const userId = args.userId;
  const url = `https://api.example.com/users/${userId}`;

  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.text();
}
```
{% endif -%}

### GET Request with Query Parameters

{% if cookiecutter.sdk_choice == 'python' -%}
```python
async def search_pets(arguments: Dict[str, Any]) -> List[TextContent]:
    status = arguments.get("status")
    params = {"status": status}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.example.com/pets",
            params=params
        )
        response.raise_for_status()
        return [TextContent(type="text", text=response.text)]
```
{% else -%}
```typescript
async function searchPets(args: any): Promise<string> {
  const status = args.status;
  const params = new URLSearchParams({ status });
  const url = `https://api.example.com/pets?${params}`;

  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.text();
}
```
{% endif -%}

### POST Request with Body

{% if cookiecutter.sdk_choice == 'python' -%}
```python
async def create_pet(arguments: Dict[str, Any]) -> List[TextContent]:
    pet_data = arguments.get("body")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.example.com/pets",
            json=pet_data
        )
        response.raise_for_status()
        return [TextContent(type="text", text=response.text)]
```
{% else -%}
```typescript
async function createPet(args: any): Promise<string> {
  const petData = args.body;

  const response = await fetch("https://api.example.com/pets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(petData),
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.text();
}
```
{% endif -%}

### DELETE Request

{% if cookiecutter.sdk_choice == 'python' -%}
```python
async def delete_pet(arguments: Dict[str, Any]) -> List[TextContent]:
    pet_id = arguments.get("petId")

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"https://api.example.com/pets/{pet_id}"
        )
        response.raise_for_status()
        return [TextContent(type="text", text="Pet deleted successfully")]
```
{% else -%}
```typescript
async function deletePet(args: any): Promise<string> {
  const petId = args.petId;

  const response = await fetch(`https://api.example.com/pets/${petId}`, {
    method: "DELETE",
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return "Pet deleted successfully";
}
```
{% endif -%}

## Adding Authentication

{% if cookiecutter.auth_mechanism == 'api_key' -%}
### With API Key

Your server already has API key support. To add API key to tool requests:

{% if cookiecutter.sdk_choice == 'python' -%}
```python
async def authenticated_request(arguments: Dict[str, Any]) -> List[TextContent]:
    api_key = os.getenv("API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.example.com/data",
            headers=headers
        )
        response.raise_for_status()
        return [TextContent(type="text", text=response.text)]
```
{% else -%}
```typescript
async function authenticatedRequest(args: any): Promise<string> {
  const apiKey = process.env.API_KEY;

  const response = await fetch("https://api.example.com/data", {
    headers: {
      "Authorization": `Bearer ${apiKey}`,
    },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.text();
}
```
{% endif -%}
{% endif -%}

## Error Handling

Always handle errors gracefully:

{% if cookiecutter.sdk_choice == 'python' -%}
```python
try:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return [TextContent(type="text", text=response.text)]
except httpx.HTTPStatusError as e:
    error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
    return [TextContent(type="text", text=error_msg)]
except Exception as e:
    return [TextContent(type="text", text=f"Error: {str(e)}")]
```
{% else -%}
```typescript
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return await response.text();
} catch (error) {
  return `Error: ${error.message}`;
}
```
{% endif -%}

## Testing Your Tools

### 1. Run the Server

{% if cookiecutter.sdk_choice == 'python' -%}
```bash
source venv/bin/activate  # or .venv/bin/activate for uv
{{ cookiecutter.project_slug }}
```
{% else -%}
```bash
npm start
```
{% endif -%}

### 2. Test with Claude Desktop

Add to Claude Desktop config and restart Claude:

{% if cookiecutter.sdk_choice == 'python' -%}
```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "/path/to/venv/bin/{{ cookiecutter.project_slug }}"
    }
  }
}
```
{% else -%}
```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "node",
      "args": ["/path/to/dist/index.js"]
    }
  }
}
```
{% endif -%}

### 3. Test Commands

Try these prompts in Claude:
- "What tools do you have available?"
- "Get pet with ID 1"
- "Search for available pets"

## Tips

1. **Start Simple** - Begin with GET requests, then add POST/PUT/DELETE
2. **Use Examples** - Copy the example tool and modify it
3. **Test Incrementally** - Add one tool at a time and test
4. **Check Logs** - Watch server output for errors
5. **Format Responses** - Parse JSON and format nicely for Claude
6. **Add Descriptions** - Good descriptions help Claude use tools correctly

## Advanced: Parsing Responses

Instead of returning raw JSON, parse and format it:

{% if cookiecutter.sdk_choice == 'python' -%}
```python
import json

response_data = json.loads(response.text)
formatted = f"Pet Name: {response_data['name']}\\nStatus: {response_data['status']}"
return [TextContent(type="text", text=formatted)]
```
{% else -%}
```typescript
const data = await response.json();
const formatted = `Pet Name: ${data.name}\\nStatus: ${data.status}`;
return formatted;
```
{% endif -%}

## Need Help?

- Check the MCP docs: https://modelcontextprotocol.io
- Review your OpenAPI spec for endpoint details
- Look at the example tool implementation
- Test with simple curl commands first

Happy coding! 🚀
