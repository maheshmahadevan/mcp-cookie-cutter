# Testing MCP Cookie Cutter with Petstore API

This guide walks you through testing the MCP cookie-cutter framework using the popular Swagger Petstore API.

## Quick Start Test

### Step 1: Install Cookiecutter

```bash
pip install cookiecutter pyyaml
```

### Step 2: Run the Cookie Cutter

```bash
cd /Users/maheshmahadevan/projects/mcp-cookie-cutter
cookiecutter .
```

### Step 3: Answer the Prompts

Use these values for a quick test:

```
project_name: Petstore MCP Server
project_slug: petstore_mcp_server (auto-generated)
project_description: MCP server for Swagger Petstore API
author_name: Your Name
author_email: your.email@example.com
openapi_spec_path: examples/petstore-swagger.json
  OR use URL: https://petstore.swagger.io/v2/swagger.json
sdk_choice: 1 - python (or 2 - typescript)
deployment_type: 1 - local (easiest for testing)
auth_mechanism: 1 - none (simplest for testing)
python_package_manager: 1 - uv (or 2 - pip)
include_resources: 2 - no (focus on tools first)
include_prompts: 2 - no (focus on tools first)
license: 1 - MIT
```

## Python Server Test

### Setup and Run (with uv)

```bash
# Navigate to generated project
cd petstore_mcp_server

# Create virtual environment with uv
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Run the server
petstore_mcp_server
```

Or use uv directly without activation:

```bash
cd petstore_mcp_server
uv run petstore_mcp_server
```

### Setup and Run (with pip)

```bash
# Navigate to generated project
cd petstore_mcp_server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the server
petstore_mcp_server
```

### Test with Claude Desktop

#### With uv (recommended):

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "petstore": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/petstore_mcp_server",
        "run",
        "petstore_mcp_server"
      ]
    }
  }
}
```

#### With pip:

```json
{
  "mcpServers": {
    "petstore": {
      "command": "/full/path/to/petstore_mcp_server/venv/bin/petstore_mcp_server"
    }
  }
}
```

Restart Claude Desktop and test with prompts like:
- "What tools are available from the petstore server?"
- "Get pet with ID 1"
- "List available pets by status"

## TypeScript Server Test

### Setup and Run

```bash
# Navigate to generated project
cd petstore_mcp_server

# Install dependencies
npm install

# Build
npm run build

# Run the server
npm start
```

### Test with Claude Desktop

Add to config:

```json
{
  "mcpServers": {
    "petstore": {
      "command": "node",
      "args": ["/full/path/to/petstore_mcp_server/dist/index.js"]
    }
  }
}
```

## Testing Remote Deployment (SSE)

### Generate Remote Server

When running cookiecutter, choose:
- `deployment_type: 2 - remote`
- `auth_mechanism: 2 - api_key` (for testing)

### Setup

```bash
cd petstore_mcp_server

# Create .env file
cp .env.example .env
echo "MCP_API_KEYS=test-key-12345" > .env

# Python
pip install -e .
petstore_mcp_server

# TypeScript
npm install && npm run build && npm start
```

Server runs on `http://localhost:8000`

### Test with curl

```bash
# Test SSE endpoint
curl -H "Authorization: Bearer test-key-12345" \
     http://localhost:8000/sse
```

## Expected Output from Pre-Generation Hook

When you provide the OpenAPI spec path, you should see:

```
Loading OpenAPI specification from: examples/petstore-swagger.json

Found 8 available tools:
1. addPet - Add a new pet to the store
2. updatePet - Update an existing pet
3. getPetById - Find pet by ID
4. deletePet - Deletes a pet
5. placeOrder - Place an order for a pet
6. getOrderById - Find purchase order by ID
7. createUser - Create user
8. getUserByName - Get user by user name

✓ Pre-generation validation complete
```

## Customizing the Generated Tools

After generation, edit the tools file to connect to the actual Petstore API:

### Python (`src/petstore_mcp_server/tools.py`)

```python
import httpx

PETSTORE_BASE_URL = "https://petstore.swagger.io/v2"

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute a tool."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")

    async with httpx.AsyncClient() as client:
        if name == "getPetById":
            pet_id = arguments.get("petId")
            response = await client.get(f"{PETSTORE_BASE_URL}/pet/{pet_id}")
            return [
                TextContent(
                    type="text",
                    text=response.text
                )
            ]

        elif name == "addPet":
            pet_data = arguments.get("body")
            response = await client.post(
                f"{PETSTORE_BASE_URL}/pet",
                json=pet_data
            )
            return [
                TextContent(
                    type="text",
                    text=f"Pet added: {response.text}"
                )
            ]

    raise ValueError(f"Unknown tool: {name}")
```

### TypeScript (`src/tools.ts`)

```typescript
const PETSTORE_BASE_URL = "https://petstore.swagger.io/v2";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "getPetById": {
      const petId = args?.petId as number;
      const response = await fetch(`${PETSTORE_BASE_URL}/pet/${petId}`);
      const data = await response.json();

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    }

    case "addPet": {
      const petData = args?.body;
      const response = await fetch(`${PETSTORE_BASE_URL}/pet`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(petData),
      });
      const data = await response.json();

      return {
        content: [
          {
            type: "text",
            text: `Pet added: ${JSON.stringify(data, null, 2)}`,
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});
```

## Test Scenarios

### 1. Basic Tool Listing
**Prompt**: "What tools do you have available?"
**Expected**: Should list getPetById, addPet, updatePet, deletePet, etc.

### 2. Get Pet by ID
**Prompt**: "Get pet with ID 1"
**Expected**: Should return pet details from the Petstore API

### 3. Create a Pet
**Prompt**: "Add a new pet named 'Buddy' with status 'available'"
**Expected**: Should create pet and return confirmation

### 4. Error Handling
**Prompt**: "Get pet with ID 99999999"
**Expected**: Should handle 404 error gracefully

## Troubleshooting

### Pre-generation hook fails
- Ensure `pyyaml` is installed: `pip install pyyaml`
- Verify OpenAPI spec path is correct
- Check that the JSON is valid

### Server won't start (Python)
- Activate virtual environment
- Install dependencies: `pip install -e .`
- Check Python version: `python --version` (need 3.10+)

### Server won't start (TypeScript)
- Install dependencies: `npm install`
- Build first: `npm run build`
- Check Node version: `node --version` (need 18+)

### Claude Desktop doesn't see the server
- Check config file path is correct
- Verify absolute paths in config
- Restart Claude Desktop after config changes
- Check Claude Desktop logs for errors

## Advanced Testing

### Test with Different OpenAPI Specs

```bash
# Download another spec
curl -o examples/my-api.json https://example.com/api/openapi.json

# Generate with it
cookiecutter . --no-input \
  openapi_spec_path=examples/my-api.json \
  project_name="My API Server"
```

### Test OAuth Flow

1. Generate with `auth_mechanism: 3 - oauth2`
2. Configure OAuth provider details
3. Test authorization flow
4. Verify token validation

### Test with Resources and Prompts

1. Generate with:
   - `include_resources: 1 - yes`
   - `include_prompts: 1 - yes`
2. Customize resources.py/ts to expose API data
3. Create useful prompt templates in prompts.py/ts

## Next Steps

1. **Enhance Tool Implementations**: Connect tools to real API endpoints
2. **Add Error Handling**: Implement robust error handling for API calls
3. **Add Validation**: Validate inputs against OpenAPI schema
4. **Auto-generate Tools**: Extend pre-generation hook to generate complete tool implementations
5. **Add Tests**: Write unit tests for your tools
6. **Deploy**: Deploy remote servers to production

## Resources

- [Petstore API Docs](https://petstore.swagger.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Claude Desktop Config](https://modelcontextprotocol.io/quickstart/user)
