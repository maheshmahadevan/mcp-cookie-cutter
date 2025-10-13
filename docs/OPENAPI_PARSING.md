# OpenAPI Spec Parsing

The MCP Cookie Cutter template now includes intelligent OpenAPI specification parsing to help you understand which tools are available from your API.

## How It Works

When you provide an OpenAPI specification path during generation, the pre-generation hook will:

1. **Load the spec** from a file or URL
2. **Parse and validate** the OpenAPI document
3. **Extract all operations** (GET, POST, PUT, DELETE, PATCH)
4. **Display a summary** showing available API operations

This helps you understand what tools you can implement in your MCP server.

## Dependencies

The OpenAPI parsing feature requires these optional dependencies:

### Required for Basic Functionality
- **pyyaml** - For parsing YAML OpenAPI specs
- **requests** - For fetching OpenAPI specs from URLs

### Recommended for Enhanced Validation
- **openapi-pydantic** - For validating OpenAPI schemas with type safety

### Installation

```bash
# Install all at once
pip install pyyaml requests openapi-pydantic

# Or install individually
pip install pyyaml      # For YAML support
pip install requests    # For URL support
pip install openapi-pydantic  # For validation
```

## Usage

### From URL (Recommended)

```bash
cookiecutter /path/to/mcp-cookie-cutter
# When prompted for openapi_spec_path:
openapi_spec_path: https://petstore.swagger.io/v2/swagger.json
```

### From Local File

```bash
cookiecutter /path/to/mcp-cookie-cutter
# When prompted:
openapi_spec_path: ./my-api-spec.yaml
```

### With --no-input

```bash
cookiecutter /path/to/mcp-cookie-cutter --no-input \
  openapi_spec_path="https://petstore.swagger.io/v2/swagger.json"
```

## Example Output

When you provide an OpenAPI spec, you'll see:

```
📋 OpenAPI Specification: https://petstore.swagger.io/v2/swagger.json

✨ Found 20 available API operations:

----------------------------------------------------------------------
 1. POST   /pet/{petId}/uploadImage       - uploadFile
     uploads an image
 2. POST   /pet                           - addPet
     Add a new pet to the store
 3. PUT    /pet                           - updatePet
     Update an existing pet
 4. GET    /pet/findByStatus              - findPetsByStatus
     Finds Pets by status
 5. GET    /pet/{petId}                   - getPetById
     Find pet by ID
...
----------------------------------------------------------------------

💡 You can implement these as MCP tools in your generated server.
   See CUSTOMIZATION.md for step-by-step guide.
```

## How It Helps

The tool suggestion feature helps you:

1. **Understand your API** - See all available operations at a glance
2. **Plan implementation** - Know which tools to create in your MCP server
3. **Get operation details** - See HTTP methods, paths, and descriptions
4. **Save time** - No need to manually browse the OpenAPI spec

## Validation with openapi-pydantic

If `openapi-pydantic` is installed, the hook will validate your OpenAPI spec using Pydantic models:

- **Type safety** - Ensures spec conforms to OpenAPI 3.0/3.1 standards
- **Error detection** - Catches malformed specs early
- **Better parsing** - Leverages Pydantic's validation features

If validation fails, you'll see a warning but the generation will continue with basic parsing.

## Graceful Degradation

The system is designed to work even without all dependencies:

### Without requests
- ❌ Cannot fetch from URLs
- ✅ Can still load local files
- Shows helpful error message

### Without pyyaml
- ❌ Cannot parse YAML specs
- ✅ Can still parse JSON specs
- Shows helpful error message

### Without openapi-pydantic
- ❌ No schema validation
- ✅ Basic parsing still works
- Proceeds without validation

### Without any dependencies
- ✅ Template generation works normally
- ❌ No OpenAPI parsing or tool suggestions
- Shows informational message

## Supported Formats

- **OpenAPI 3.0** (JSON or YAML)
- **OpenAPI 3.1** (JSON or YAML)
- **Swagger 2.0** (JSON or YAML)

## Technical Details

### Parsing Libraries

The hook uses a tiered approach:

1. **Primary parser**: `openapi-pydantic` - Provides Pydantic models for OpenAPI
2. **YAML parser**: `pyyaml` - For YAML format support
3. **HTTP client**: `requests` - For fetching from URLs
4. **Fallback**: `json` (built-in) - For basic JSON parsing

### Inspiration

This implementation was inspired by `openapi-python-client` which uses:
- `openapi-pydantic` (formerly `openapi-schema-pydantic`) for parsing
- `pydantic` for data validation
- `ruamel.yaml` for YAML (we use `pyyaml` as a lighter alternative)

### Why openapi-pydantic?

We chose `openapi-pydantic` over alternatives because:

1. **Type safety** - Pydantic models provide full type hints
2. **Validation** - Automatically validates spec structure
3. **Active maintenance** - Supports both Pydantic 1.8+ and 2.x
4. **OpenAPI native** - Specifically designed for OpenAPI specs
5. **Well tested** - Used by major projects like `openapi-python-client`

## Future Enhancements (V1.0)

In V1.0, we plan to:

1. **Interactive selection** - Choose which operations to implement
2. **Automatic code generation** - Generate tool implementations automatically
3. **Smart parameter mapping** - Map OpenAPI parameters to MCP tool schemas
4. **Authentication detection** - Auto-configure auth based on security schemes
5. **Response formatting** - Generate proper response handlers

## Troubleshooting

### "requests library not installed"
```bash
pip install requests
```

### "pyyaml library not installed"
```bash
pip install pyyaml
```

### "OpenAPI spec validation failed"
- Check if your spec is valid OpenAPI 3.0/3.1 or Swagger 2.0
- Use an online validator: https://editor.swagger.io
- The generation will still proceed with basic parsing

### "No API operations found"
- Verify your OpenAPI spec has a `paths` section
- Check that operations use standard HTTP methods (GET, POST, etc.)
- Ensure the spec is properly formatted

## See Also

- [CUSTOMIZATION.md]({{cookiecutter.project_slug}}/CUSTOMIZATION.md) - How to implement the suggested tools
- [README.md](README.md) - Main documentation
- [hook_requirements.txt](hook_requirements.txt) - Full dependency list
