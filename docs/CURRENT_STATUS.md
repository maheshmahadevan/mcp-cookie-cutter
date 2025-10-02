# Current Status & Known Issues

## ✅ What Works

1. **Project Structure** - Complete cookiecutter template with:
   - Python and TypeScript MCP server templates
   - Local (STDIO) and Remote (SSE) deployment options
   - OAuth 2.1 and API key authentication templates
   - uv and pip package manager support

2. **OpenAPI Integration** - Basic functionality:
   - Loads OpenAPI specs from URLs or local files
   - Parses Swagger 2.0 and OpenAPI 3.x
   - Extracts endpoints and parameters
   - JSON specs work reliably (YAML requires pyyaml)

3. **Documentation**:
   - `README.md` - Main documentation
   - `EXAMPLE.md` - Complete walkthrough
   - `USAGE.md` - Multi-location usage guide
   - `TEST_GUIDE.md` - Testing instructions

## ⚠️  Known Issues

### Issue: Cookiecutter Hook Jinja2 Parsing

**Problem**: The hooks (`pre_gen_project.py` and `post_gen_project.py`) use Jinja2 templates for cookiecutter variables like `{{ cookiecutter.project_name }}`. However, the OpenAPIToolGenerator class and code generation functions also contain many curly braces (`{}`) which Jinja2 tries to parse, causing template syntax errors.

**Error**:
```
jinja2.exceptions.TemplateSyntaxError: expected token 'end of print statement', got ':'
```

**Attempted Solutions**:
1. ❌ Importing openapi_generator.py - Doesn't work because cookiecutter copies hooks to temp dir
2. ❌ Using sys.path.insert() - Module not found in temp directory
3. ❌ Using importlib.util.spec_from_file_location() - File not found in temp directory
4. ❌ Inlining with exec() - Jinja2 parses the code inside exec string
5. ❌ {% raw %} blocks - Still has issues with nested structures
6. ❌ Manual escaping of {{}} - Too many places, gets complex

**Recommended Solutions**:

### Option 1: Simplify for V1 (Quick Win)
Remove the interactive tool selection and automatic code generation for the initial release:
- Keep basic template generation working
- Provide example tool implementations
- Users manually customize the generated tools
- Document how to add tools based on OpenAPI spec

### Option 2: Use Python Script Instead of Hooks (Better Long-term)
Create a standalone Python CLI tool that:
1. Runs outside cookiecutter
2. Reads OpenAPI spec
3. Shows interactive tool selection
4. Generates cookiecutter context file
5. Calls cookiecutter with the generated context
6. Post-processes the generated files

Example:
```bash
mcp-generate --openapi https://petstore.swagger.io/v2/swagger.json
```

### Option 3: Use Cookiecutter Extensions (Advanced)
Write a cookiecutter extension that handles OpenAPI parsing outside of Jinja2 context.

## 🎯 Immediate Next Steps

### For Quick Release (V0.1):

1. **Remove complex hooks** - Keep only basic validation
2. **Provide template tools** - Include example implementations
3. **Document customization** - Clear guide on adapting tools
4. **Test basic flow** - Ensure template generation works from any directory

Files to modify:
```bash
# Simplify hooks
hooks/pre_gen_project.py  # Just validate inputs, no OpenAPI parsing
hooks/post_gen_project.py # Just setup venv, no code generation

# Enhance templates
{{cookiecutter.project_slug}}/src/.../tools.py  # Add more example tools
{{cookiecutter.project_slug}}/CUSTOMIZATION.md  # New guide
```

### For Full Release (V1.0):

1. **Create standalone CLI tool** (`mcp-generator`)
2. **Implement interactive selection** outside cookiecutter
3. **Generate code** before calling cookiecutter
4. **Full OpenAPI support** with all HTTP methods, auth schemes, etc.

## 📝 How to Test Current State

```bash
# This will fail due to Jinja2 issues:
cookiecutter . --no-input openapi_spec_path="https://petstore.swagger.io/v2/swagger.json"

# This works (no OpenAPI spec):
cookiecutter . --no-input project_name="Test" openapi_spec_path=""

# Manual testing:
cd generated_project
# Edit tools.py manually based on OpenAPI spec
# Follow README.md for setup
```

## 🔧 Quick Fix to Make It Work Now

Remove the problematic code:

```python
# In hooks/pre_gen_project.py - remove lines 23-104 (the exec block)
# Replace with simple validation only

# In hooks/post_gen_project.py - remove lines 10-46 and 245-475
# Remove generate_tool_implementations() and related functions
```

This will make cookiecutter work, but without automatic code generation.

## 💡 Recommendation

**Ship V0.1 without intelligent code generation**, with clear documentation on:
1. How to manually create tools from OpenAPI specs
2. Examples of common patterns (GET, POST, path params, query params)
3. Promise V1.0 with full automatic generation

This gets something useful in users' hands quickly while we architect the proper solution.
