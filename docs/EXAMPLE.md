# Example: Generating a Petstore MCP Server

This example demonstrates the intelligent code generation from an OpenAPI specification.

## Step-by-Step Walkthrough

### 1. Run Cookiecutter

```bash
cd /Users/maheshmahadevan/projects/mcp-cookie-cutter
cookiecutter .
```

### 2. Answer the Prompts

```
project_name [My MCP Server]: Petstore MCP Server
project_slug [petstore_mcp_server]:
project_description [MCP server generated from OpenAPI/Swagger specification]: MCP server for Swagger Petstore API
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
openapi_spec_path []: https://petstore.swagger.io/v2/swagger.json
Select sdk_choice:
1 - python
2 - typescript
Choose from 1, 2 [1]: 1
Select deployment_type:
1 - local
2 - remote
Choose from 1, 2 [1]: 1
Select auth_mechanism:
1 - none
2 - api_key
3 - oauth2
Choose from 1, 2, 3 [1]: 1
Select python_package_manager:
1 - uv
2 - pip
Choose from 1, 2 [1]: 1
Select include_resources:
1 - yes
2 - no
Choose from 1, 2 [1]: 2
Select include_prompts:
1 - yes
2 - no
Choose from 1, 2 [1]: 2
Select license:
1 - MIT
2 - Apache-2.0
3 - BSD-3-Clause
4 - GPL-3.0
5 - Proprietary
Choose from 1, 2, 3, 4, 5 [1]: 1
```

### 3. Interactive Tool Selection

After entering the OpenAPI spec path, you'll see:

```
🔍 Loading OpenAPI specification from: https://petstore.swagger.io/v2/swagger.json
Fetching OpenAPI spec from URL...
✓ OpenAPI spec loaded successfully

======================================================================
📋 Available API Operations
======================================================================

🏷️  pet
----------------------------------------------------------------------
   1. POST   /pet
      └─ Add a new pet to the store
   2. PUT    /pet
      └─ Update an existing pet
   3. GET    /pet/findByStatus
      └─ Finds Pets by status
   4. GET    /pet/findByTags
      └─ Finds Pets by tags
   5. GET    /pet/{petId}
      └─ Find pet by ID
   6. POST   /pet/{petId}
      └─ Updates a pet in the store with form data
   7. DELETE /pet/{petId}
      └─ Deletes a pet
   8. POST   /pet/{petId}/uploadImage
      └─ uploads an image

🏷️  store
----------------------------------------------------------------------
   9. GET    /store/inventory
      └─ Returns pet inventories by status
  10. POST   /store/order
      └─ Place an order for a pet
  11. GET    /store/order/{orderId}
      └─ Find purchase order by ID
  12. DELETE /store/order/{orderId}
      └─ Delete purchase order by ID

🏷️  user
----------------------------------------------------------------------
  13. POST   /user
      └─ Create user
  14. POST   /user/createWithArray
      └─ Creates list of users with given input array
  15. POST   /user/createWithList
      └─ Creates list of users with given input array
  16. GET    /user/login
      └─ Logs user into the system
  17. GET    /user/logout
      └─ Logs out current logged in user session
  18. GET    /user/{username}
      └─ Get user by user name
  19. PUT    /user/{username}
      └─ Updated user
  20. DELETE /user/{username}
      └─ Delete user

======================================================================
Select tools to include:
  • Enter numbers separated by commas (e.g., 1,2,5)
  • Enter 'all' to include all tools
  • Enter ranges (e.g., 1-5,8,10-12)
  • Press Enter to include all
======================================================================

Your selection: 1,3,5,9,10,11
```

**Explanation:** Here we're selecting:
- Tool 1: Add a new pet (POST)
- Tool 3: Find pets by status (GET)
- Tool 5: Get pet by ID (GET)
- Tool 9: Get store inventory (GET)
- Tool 10: Place an order (POST)
- Tool 11: Get order by ID (GET)

```
✓ Selected 6 tools
✓ Tool selection saved

======================================================================
✓ Pre-generation validation complete
======================================================================
```

### 4. Code Generation

The post-generation hook will automatically generate working code:

```
🔧 Running post-generation setup...

🔨 Generating code for 6 tools...
✓ Generated 6 tool implementations
```

### 5. Generated Code Examples

#### Python Tool Implementation (`src/petstore_mcp_server/tools.py`)

```python
import logging
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent

logger = logging.getLogger(__name__)


async def addPet(arguments: Dict[str, Any]) -> str:
    """
    Add a new pet to the store

    Method: POST
    Path: /pet
    """
    import httpx

    # Extract parameters
    body = arguments.get('body', {})

    url = f"https://petstore.swagger.io/v2/pet"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body)
        response.raise_for_status()
        return response.text


async def findPetsByStatus(arguments: Dict[str, Any]) -> str:
    """
    Finds Pets by status

    Method: GET
    Path: /pet/findByStatus
    """
    import httpx

    # Extract parameters
    params = {}
    if 'status' in arguments:
        params['status'] = arguments['status']

    url = f"https://petstore.swagger.io/v2/pet/findByStatus"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.text


async def getPetById(arguments: Dict[str, Any]) -> str:
    """
    Find pet by ID

    Method: GET
    Path: /pet/{petId}
    """
    import httpx

    # Extract parameters
    petId = arguments.get('petId')

    url = f"https://petstore.swagger.io/v2/pet/{petId}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


async def getInventory(arguments: Dict[str, Any]) -> str:
    """
    Returns pet inventories by status

    Method: GET
    Path: /store/inventory
    """
    import httpx

    # Extract parameters

    url = f"https://petstore.swagger.io/v2/store/inventory"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


async def placeOrder(arguments: Dict[str, Any]) -> str:
    """
    Place an order for a pet

    Method: POST
    Path: /store/order
    """
    import httpx

    # Extract parameters
    body = arguments.get('body', {})

    url = f"https://petstore.swagger.io/v2/store/order"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body)
        response.raise_for_status()
        return response.text


async def getOrderById(arguments: Dict[str, Any]) -> str:
    """
    Find purchase order by ID

    Method: GET
    Path: /store/order/{orderId}
    """
    import httpx

    # Extract parameters
    orderId = arguments.get('orderId')

    url = f"https://petstore.swagger.io/v2/store/order/{orderId}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def register_tools(server: Server):
    """Register all tools with the MCP server."""

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available tools."""
        return [
            Tool(
                name="addPet",
                description="Add a new pet to the store",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "body": {
                            "type": "object",
                            "required": ["name", "photoUrls"],
                            "properties": {
                                "id": {"type": "integer", "format": "int64"},
                                "name": {"type": "string", "example": "doggie"},
                                "photoUrls": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "status": {
                                    "type": "string",
                                    "description": "pet status in the store",
                                    "enum": ["available", "pending", "sold"]
                                }
                            }
                        }
                    },
                    "required": ["body"]
                }
            ),
            Tool(
                name="findPetsByStatus",
                description="Finds Pets by status",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "array",
                            "description": "Status values that need to be considered for filter"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="getPetById",
                description="Find pet by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "petId": {
                            "type": "integer",
                            "description": "ID of pet to return"
                        }
                    },
                    "required": ["petId"]
                }
            ),
            Tool(
                name="getInventory",
                description="Returns pet inventories by status",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="placeOrder",
                description="Place an order for a pet",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "body": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "format": "int64"},
                                "petId": {"type": "integer", "format": "int64"},
                                "quantity": {"type": "integer", "format": "int32"},
                                "status": {
                                    "type": "string",
                                    "description": "Order Status",
                                    "enum": ["placed", "approved", "delivered"]
                                }
                            }
                        }
                    },
                    "required": ["body"]
                }
            ),
            Tool(
                name="getOrderById",
                description="Find purchase order by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "orderId": {
                            "type": "integer",
                            "description": "ID of order to return"
                        }
                    },
                    "required": ["orderId"]
                }
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute a tool."""
        logger.info(f"Calling tool: {name} with arguments: {arguments}")

        if name == "addPet":
            result = await addPet(arguments)
            return [TextContent(type="text", text=result)]

        if name == "findPetsByStatus":
            result = await findPetsByStatus(arguments)
            return [TextContent(type="text", text=result)]

        if name == "getPetById":
            result = await getPetById(arguments)
            return [TextContent(type="text", text=result)]

        if name == "getInventory":
            result = await getInventory(arguments)
            return [TextContent(type="text", text=result)]

        if name == "placeOrder":
            result = await placeOrder(arguments)
            return [TextContent(type="text", text=result)]

        if name == "getOrderById":
            result = await getOrderById(arguments)
            return [TextContent(type="text", text=result)]

        raise ValueError(f"Unknown tool: {name}")
```

### 6. Run the Server

```bash
cd petstore_mcp_server

# With uv
uv venv
source .venv/bin/activate
uv pip install -e .
petstore_mcp_server

# Or directly with uv
uv run petstore_mcp_server
```

### 7. Test with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

Restart Claude Desktop and try:

**User:** "Get information about pet with ID 1"

**Claude will:**
1. See the `getPetById` tool
2. Call it with `{"petId": 1}`
3. Return the actual pet data from the Petstore API

**User:** "Find all available pets"

**Claude will:**
1. Use the `findPetsByStatus` tool
2. Call it with `{"status": ["available"]}`
3. Return the list of available pets

## What Makes This Intelligent?

### 1. **Real API Integration**
- Generated code actually calls the Petstore API
- Base URL extracted from OpenAPI spec
- Proper HTTP methods (GET, POST, etc.)

### 2. **Proper Parameter Handling**
- Path parameters: `/pet/{petId}` → extracts `petId` and builds URL
- Query parameters: `/pet/findByStatus?status=available`
- Request bodies: Properly serialized JSON

### 3. **Type-Safe Schemas**
- Input schemas generated from OpenAPI parameter definitions
- Required fields enforced
- Enum values preserved
- Descriptions included

### 4. **Error Handling**
- HTTP errors caught with `response.raise_for_status()`
- Invalid tool names rejected
- Missing parameters fail validation

### 5. **User Choice**
- Not all 20 endpoints forced on you
- Select only the tools you need
- Clean, focused MCP server

## Try Different Selections

### Minimal (Read-only)
```
Your selection: 5,9,11
```
Only GET operations for viewing data.

### Full Pet Management
```
Your selection: 1-8
```
Complete CRUD for pets.

### Everything
```
Your selection: all
```
All 20 operations available as MCP tools.

## Next Steps

1. **Add Authentication**: If API requires auth, the generator detects security schemes
2. **Add Error Formatting**: Parse JSON responses and format nicely
3. **Add Caching**: Cache frequently accessed data
4. **Add Validation**: Validate inputs against schemas before making requests
5. **Add Rate Limiting**: Protect the API from too many requests

The generated code is a **solid foundation** that you can enhance!
