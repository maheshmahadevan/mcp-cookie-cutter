# Usage Guide

## Running from Different Locations

The MCP Cookie Cutter template can be used from anywhere on your system.

### Method 1: From the Template Directory

```bash
cd /path/to/mcp-cookie-cutter
cookiecutter .
```

The generated project will be created in the same directory.

### Method 2: From Any Other Directory

```bash
# Using absolute path
cookiecutter /full/path/to/mcp-cookie-cutter

# Using relative path
cookiecutter ~/projects/mcp-cookie-cutter

# Using home directory expansion
cookiecutter ~/.local/templates/mcp-cookie-cutter
```

The generated project will be created in your **current working directory**.

### Method 3: From GitHub (Recommended for Distribution)

Once you publish the template to GitHub:

```bash
# Short form
cookiecutter gh:yourusername/mcp-cookie-cutter

# Full URL
cookiecutter https://github.com/yourusername/mcp-cookie-cutter

# Specific branch
cookiecutter gh:yourusername/mcp-cookie-cutter --checkout develop
```

### Method 4: Create Alias for Convenience

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Alias for MCP Cookie Cutter
alias mcp-create='cookiecutter /full/path/to/mcp-cookie-cutter'

# Or with gh once published
alias mcp-create='cookiecutter gh:yourusername/mcp-cookie-cutter'
```

Then just run:
```bash
mcp-create
```

## Examples

### Example 1: Generate in Current Directory

```bash
cd ~/my-projects
cookiecutter ~/templates/mcp-cookie-cutter

# Project will be created at:
# ~/my-projects/project_name/
```

### Example 2: Generate in Specific Directory

```bash
cd ~/workspace
cookiecutter /home/user/mcp-cookie-cutter

# Project will be created at:
# ~/workspace/project_name/
```

### Example 3: Non-Interactive Mode from Anywhere

```bash
cookiecutter ~/mcp-cookie-cutter --no-input \
  project_name="My API Server" \
  openapi_spec_path="https://api.example.com/openapi.json" \
  sdk_choice="python" \
  deployment_type="remote" \
  auth_mechanism="oauth2"
```

### Example 4: Using with Different OpenAPI Sources

```bash
# Local OpenAPI file
cookiecutter ~/mcp-cookie-cutter \
  openapi_spec_path="./specs/my-api.yaml"

# URL
cookiecutter ~/mcp-cookie-cutter \
  openapi_spec_path="https://petstore.swagger.io/v2/swagger.json"

# Relative path
cookiecutter ~/mcp-cookie-cutter \
  openapi_spec_path="../api-specs/openapi.json"
```

## Output Location

The generated project is always created in your **current working directory**, not in the template directory.

```bash
# You're here
/home/user/projects/

# Template is here
/home/user/templates/mcp-cookie-cutter/

# Run this
cookiecutter /home/user/templates/mcp-cookie-cutter

# Project created here
/home/user/projects/my_mcp_server/
```

## Environment-Specific Configurations

### Development Environment

```bash
# Use local OpenAPI specs
export API_SPEC_PATH="./specs/dev-api.yaml"
cookiecutter ~/mcp-cookie-cutter \
  openapi_spec_path="$API_SPEC_PATH" \
  deployment_type="local"
```

### Production Environment

```bash
# Use production OpenAPI URL
cookiecutter ~/mcp-cookie-cutter \
  openapi_spec_path="https://api.production.com/openapi.json" \
  deployment_type="remote" \
  auth_mechanism="oauth2"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Generate MCP Server

on:
  workflow_dispatch:
    inputs:
      api_url:
        description: 'OpenAPI Spec URL'
        required: true

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout template
        uses: actions/checkout@v3
        with:
          repository: yourusername/mcp-cookie-cutter
          path: template

      - name: Install cookiecutter
        run: pip install cookiecutter pyyaml

      - name: Generate server
        run: |
          cookiecutter template --no-input \
            project_name="Generated MCP Server" \
            openapi_spec_path="${{ github.event.inputs.api_url }}" \
            sdk_choice="python" \
            deployment_type="remote"

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: mcp-server
          path: generated_mcp_server/
```

## Troubleshooting

### Issue: "Template not found"

**Problem:** Running `cookiecutter mcp-cookie-cutter` fails

**Solution:** Use the full path
```bash
cookiecutter /full/path/to/mcp-cookie-cutter
# or
cookiecutter ~/mcp-cookie-cutter
```

### Issue: "OpenAPI spec not found"

**Problem:** Relative paths to OpenAPI specs don't work

**Solution:** Use absolute paths or URLs
```bash
# Instead of
openapi_spec_path: ../api-specs/openapi.json

# Use absolute path
openapi_spec_path: /home/user/api-specs/openapi.json

# Or URL
openapi_spec_path: https://example.com/openapi.json
```

### Issue: "Module not found in hooks"

**Problem:** Hooks fail with import errors

**Solution:** This is fixed in the template. The hooks use `sys.path.insert()` to find modules. If you still have issues, ensure:

1. You're using the latest version of the template
2. The `hooks/` directory contains:
   - `pre_gen_project.py`
   - `post_gen_project.py`
   - `openapi_generator.py`

### Issue: "Generated in wrong directory"

**Problem:** Project appears in unexpected location

**Solution:** Remember that cookiecutter generates in your **current working directory**:

```bash
# Check where you are
pwd

# Generate here
cookiecutter ~/mcp-cookie-cutter

# Project will be in $(pwd)/project_name/
```

## Advanced Usage

### Custom Output Directory

```bash
# Generate and specify output directory
cookiecutter ~/mcp-cookie-cutter -o /custom/output/path
```

### Replay Previous Generation

```bash
# Cookiecutter saves your inputs
cookiecutter ~/mcp-cookie-cutter --replay
```

### Override Specific Values

```bash
# Use replay but change some values
cookiecutter ~/mcp-cookie-cutter --replay \
  openapi_spec_path="https://new-api.com/spec.json"
```

### Config File

Create `~/.cookiecutterrc`:

```yaml
default_context:
  author_name: "Your Name"
  author_email: "you@example.com"
  license: "MIT"

abbreviations:
  mcp: /full/path/to/mcp-cookie-cutter
```

Then just run:
```bash
cookiecutter mcp
```

## Best Practices

1. **Use URLs for OpenAPI specs** when possible - more reliable than local paths
2. **Test generated servers** before committing to source control
3. **Version control your API specs** alongside generated servers
4. **Use the template from a fixed location** (e.g., `~/templates/`)
5. **Create shell aliases** for frequently used configurations
6. **Document your generation commands** in your project's README
7. **Use GitHub for distribution** rather than local paths when sharing with teams
