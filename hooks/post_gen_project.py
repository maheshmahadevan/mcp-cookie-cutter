#!/usr/bin/env python3
"""Post-generation hook to set up the project."""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def setup_python_project():
    """Set up Python project dependencies using uv."""
    print("\n📦 Setting up Python project...")

    # Always use uv now
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("Using uv for package management...")

        # Initialize uv project
        try:
            subprocess.run(["uv", "venv"], check=True)
            print("✓ Virtual environment created with uv")
        except subprocess.CalledProcessError as e:
            print(f"Warning: uv setup failed: {e}")
            print("\nTo set up manually, run:")
            print("  uv venv")
            print("  source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
            print("  uv pip install -e .")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Warning: uv not found. Install with:")
        print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("\nThen run:")
        print("  uv venv")
        print("  source .venv/bin/activate")
        print("  uv pip install -e .")

def cleanup_unused_files():
    """Remove files not needed for the selected configuration."""
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"

    # Remove auth files if not needed
    if auth_mechanism == "none":
        auth_dir = Path("src/{{ cookiecutter.project_slug }}/auth")
        if auth_dir.exists():
            import shutil
            shutil.rmtree(auth_dir)

def create_env_template():
    """Create .env.example file with BASE_URL, PORT, and auth config."""
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"
    deployment_type = "{{ cookiecutter.deployment_type }}"
    server_port = "{{ cookiecutter.server_port }}"

    # Get base URL from OpenAPI tools if available
    base_url = ""
    if os.path.exists('./.openapi_tools.json'):
        with open('./.openapi_tools.json', 'r') as f:
            tool_data = json.load(f)
            base_url = tool_data.get('base_url', '')

    # Start building env content
    env_content = "# MCP Server Configuration\n\n"

    # Add BASE_URL from OpenAPI spec
    if base_url:
        env_content += f"# API Base URL (from OpenAPI specification)\n"
        env_content += f"BASE_URL={base_url}\n\n"
    else:
        env_content += "# API Base URL\n"
        env_content += "BASE_URL=https://api.example.com\n\n"

    # Add PORT and HOST for remote deployment
    if deployment_type == "remote":
        env_content += f"# Server Configuration\n"
        env_content += f"HOST=0.0.0.0\n"
        env_content += f"PORT={server_port}\n\n"

        # Add CORS configuration
        env_content += "# CORS Configuration (comma-separated origins, or * for all)\n"
        env_content += "CORS_ORIGINS=*\n\n"

    # Add auth configuration
    if auth_mechanism == "api_key":
        env_content += """# API Key Authentication
# Single API key for server access
API_KEY=your-api-key-here
"""
    elif auth_mechanism == "oauth2":
        env_content += """# OAuth 2.1 Configuration
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret  # Optional for public clients
OAUTH_ISSUER_URL=https://your-oauth-provider.com
"""

    with open(".env.example", "w") as f:
        f.write(env_content)
    print("✓ Created .env.example with BASE_URL and configuration")

def print_next_steps():
    """Print next steps for the user."""
    deployment_type = "{{ cookiecutter.deployment_type }}"
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"
    openapi_spec_path = "{{ cookiecutter.openapi_spec_path }}"

    print("\n" + "="*70)
    print("🎉 MCP Server generated successfully!")
    print("="*70)

    print("\n📋 Next steps:\n")

    if openapi_spec_path:
        print("1. Customize your tools based on the OpenAPI spec:")
        print("   See CUSTOMIZATION.md for detailed guide")
        print("")

    print("2. Activate the virtual environment:")
    print("   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
    print("\n3. Install dependencies:")
    print("   uv pip install -e .")

    if auth_mechanism != "none":
        print(f"\n4. Configure authentication:")
        print("   cp .env.example .env")
        print("   # Edit .env with your credentials")

    print("\n5. Run the server:")
    print("   {{ cookiecutter.project_slug }}")

    if deployment_type == "local":
        print("\n6. Configure Claude Desktop:")
        print("   Add the server configuration to claude_desktop_config.json")
        print("   See README.md for details")

    print("\n📖 For more information:")
    print("   • README.md - Setup and usage guide")
    print("   • CUSTOMIZATION.md - How to add your API tools")
    print("\n" + "="*70)

def generate_pydantic_models():
    """Generate Pydantic models from OpenAPI spec using datamodel-code-generator."""
    if not os.path.exists('./.openapi_spec.json'):
        return False

    try:
        # Check if datamodel-code-generator is available
        import subprocess
        subprocess.run(['datamodel-codegen', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n⚠️  Warning: datamodel-code-generator not installed.")
        print("   Models will not be auto-generated. Install with:")
        print("   pip install datamodel-code-generator")
        return False

    print("\n🔧 Generating Pydantic models from OpenAPI schemas...")

    project_slug = "{{ cookiecutter.project_slug }}"
    models_dir = Path(f"src/{project_slug}/models")
    models_dir.mkdir(parents=True, exist_ok=True)

    # Generate models using datamodel-code-generator
    try:
        subprocess.run([
            'datamodel-codegen',
            '--input', './.openapi_spec.json',
            '--input-file-type', 'openapi',
            '--output', str(models_dir / 'schemas.py'),
            '--target-python-version', '3.10',
            '--use-standard-collections',
            '--use-schema-description',
            '--field-constraints',
            '--snake-case-field',
            '--use-double-quotes',
            '--use-field-description',
            '--field-extra-keys-without-x-prefix', 'example'
        ], check=True, capture_output=True)

        print(f"✓ Generated Pydantic models in {models_dir}/schemas.py")

        # Fix Pydantic v2 deprecation warnings by converting example= to json_schema_extra
        schemas_file = models_dir / 'schemas.py'
        if schemas_file.exists():
            content = schemas_file.read_text()
            # Simple find and replace for example= parameter
            import re
            # Pattern: example=VALUE where VALUE can be a number, string, or identifier
            # Replace with json_schema_extra={"example": VALUE}
            content = re.sub(
                r',\s*example=([^,)]+)',
                r', json_schema_extra={"example": \1}',
                content
            )
            schemas_file.write_text(content)

        # Create __init__.py for models package
        init_file = models_dir / '__init__.py'
        init_file.write_text('"""OpenAPI schema models."""\n')

        return True

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Model generation failed")
        print(f"   This can happen with very large or complex OpenAPI specs (like GitHub's)")
        print(f"   The server will still work - you can define models manually if needed")
        if e.stderr:
            stderr_text = e.stderr.decode()
            # Only show first few lines of error to avoid clutter
            error_lines = stderr_text.split('\n')[:5]
            print(f"   Error: {error_lines[0]}")
        return False
    except Exception as e:
        print(f"⚠️  Warning: Model generation failed: {str(e)[:100]}")
        print(f"   The server will still work without generated models")
        return False

def generate_fastmcp_prompts(tools: list):
    """Generate helpful prompts from OpenAPI operations."""
    project_slug = "{{ cookiecutter.project_slug }}"
    prompts_dir = Path(f"src/{project_slug}/prompts")
    prompts_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py
    init_file = prompts_dir / "__init__.py"
    init_file.write_text("\"\"\"Auto-generated prompts from OpenAPI specification.\"\"\"\n")

    # Group tools by tags/category
    by_category = {}
    for tool in tools:
        operation = tool.get('operation', {})
        tags = operation.get('tags', ['general'])
        category = tags[0] if tags else 'general'
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(tool)

    # Generate a prompt for each category
    for category, category_tools in by_category.items():
        # Sanitize category name for use in filename and function name
        category_sanitized = sanitize_tool_name(category)

        prompt_file = prompts_dir / f"{category_sanitized}_operations.py"

        code = f'"""Auto-generated prompt for {category} operations"""\n\n'

        # Create a helpful prompt listing available operations
        code += f'@mcp.prompt()  # type: ignore\n'
        code += f'def {category_sanitized}_help() -> str:\n'
        code += f'    """Get help for {category} operations in the API."""\n'
        code += f'    return """\n'
        code += f'# {category.title()} Operations\n\n'
        code += f'Available operations:\n\n'

        for tool in category_tools:
            method = tool['method']
            path = tool['path']
            name = tool['name']
            desc_raw = tool.get('description', '')
            # Sanitize description for use in prompt text
            desc = sanitize_description(desc_raw)
            code += f'- **{name}** ({method} {path})\n'
            code += f'  {desc}\n\n'

        code += f'"""\n'

        prompt_file.write_text(code)
        print(f"   ✓ Generated {category_sanitized}_operations.py prompt")

def sanitize_tool_name(name: str) -> str:
    """Sanitize tool name to be a valid Python identifier and filename."""
    import re
    # Replace invalid characters with underscore
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = f'tool_{sanitized}'
    return sanitized or 'tool'

def sanitize_param_name(name: str, fallback: str = 'param') -> str:
    """Sanitize parameter name to be a valid Python identifier."""
    import re
    # Replace invalid characters with underscore
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = f'_{sanitized}'
    # If empty after sanitization, use fallback
    if not sanitized:
        sanitized = fallback
    # Ensure it's not a Python keyword
    import keyword
    if keyword.iskeyword(sanitized):
        sanitized = f'{sanitized}_'
    return sanitized

def sanitize_description(desc: str) -> str:
    """Sanitize description for use in Python docstrings."""
    if not desc:
        return "No description provided."
    # Replace triple quotes with single quotes to avoid breaking docstrings
    desc = desc.replace('"""', "'''")
    # Replace backslashes to avoid escape issues
    desc = desc.replace('\\', '\\\\')
    # Truncate very long descriptions
    if len(desc) > 500:
        desc = desc[:497] + "..."
    return desc

def generate_fastmcp_tools(tools: list, tool_data: dict):
    """Generate individual FastMCP tool files."""
    project_slug = "{{ cookiecutter.project_slug }}"
    tools_dir = Path(f"src/{project_slug}/tools")
    tools_dir.mkdir(parents=True, exist_ok=True)

    base_url = tool_data.get('base_url', '')

    for tool in tools:
        try:
            tool_name_raw = tool['name']
            method = tool['method']
            path = tool['path']
            description = sanitize_description(tool.get('description', ''))
            parameters = tool.get('parameters', [])

            # Sanitize tool name for filename and function name
            tool_name = sanitize_tool_name(tool_name_raw)

            # Skip if tool name is invalid after sanitization
            if not tool_name or tool_name == 'tool':
                print(f"   ⚠️  Skipping tool with invalid name: {tool_name_raw}")
                continue

            # Generate individual tool file
            tool_file = tools_dir / f"{tool_name}.py"

            code = f'"""Auto-generated tool: {tool_name}"""\n\n'
            code += 'import httpx\n'
            code += 'import os\n'
            code += 'from typing import Any\n\n'

            # Import Pydantic models if they exist
            code += f'try:\n'
            code += f'    from {project_slug}.models.schemas import *\n'
            code += f'except ImportError:\n'
            code += f'    pass\n\n'

            code += f'# Get BASE_URL from environment or use default from OpenAPI spec\n'
            code += f'BASE_URL = os.getenv("BASE_URL", "{base_url}")\n\n'

            # Extract path parameter names directly from URL template
            import re
            path_placeholders = re.findall(r'\{([^}]+)\}', path)

            # Separate path params and non-path params
            path_params = [p for p in parameters if p.get('in') == 'path']
            non_path_params = [p for p in parameters if p.get('in') != 'path']

            # Build parameter list with path params first (using URL template names)
            final_params = []
            used_param_names = set()

            # Add path parameters using names from URL template
            for placeholder in path_placeholders:
                # Create or update parameter with the placeholder name
                param_name = sanitize_param_name(placeholder)

                # Handle duplicates
                original_name = param_name
                counter = 1
                while param_name in used_param_names:
                    param_name = f'{original_name}_{counter}'
                    counter += 1
                used_param_names.add(param_name)

                # Create param dict
                path_param = {
                    'name': placeholder,
                    'sanitized_name': param_name,
                    'in': 'path',
                    'required': True,  # Path params are always required
                    'schema': {'type': 'string'},
                    'description': f'Path parameter: {placeholder}'
                }
                final_params.append(path_param)

            # Add non-path parameters
            param_counter = 0
            for param in non_path_params:
                param_name_raw = param.get('name', '')
                if not param_name_raw:
                    param_counter += 1
                    param_name_raw = f'param_{param_counter}'

                param_name = sanitize_param_name(param_name_raw)

                # Handle duplicates
                original_name = param_name
                counter = 1
                while param_name in used_param_names:
                    param_name = f'{original_name}_{counter}'
                    counter += 1
                used_param_names.add(param_name)

                param['sanitized_name'] = param_name
                if not param.get('name'):
                    param['name'] = param_name_raw
                final_params.append(param)

            # Sort by required first, then optional
            sorted_params = sorted(final_params, key=lambda p: (not p.get('required', False), p.get('name', '')))

            # Generate tool function with FastMCP decorator
            code += f'@mcp.tool()  # type: ignore\n'
            code += f'async def {tool_name}(\n'

            # Add parameters using sanitized names
            for param in sorted_params:
                param_name = param['sanitized_name']
                param_type = param.get('schema', dict()).get('type', 'str')
                python_type = dict(string='str', integer='int', boolean='bool', number='float').get(param_type, 'Any')
                param_desc_raw = param.get('description', '')
                # Sanitize param description for use in comments (simpler than docstrings)
                param_desc = param_desc_raw.replace('\n', ' ').replace('\r', '')[:200] if param_desc_raw else ''

                if param.get('required'):
                    code += f'    {param_name}: {python_type},  # {param_desc}\n'
                else:
                    code += f'    {param_name}: {python_type} | None = None,  # {param_desc}\n'

            # Add body parameter if it's a POST/PUT/PATCH
            if method in ['POST', 'PUT', 'PATCH'] and tool.get('request_schema_ref'):
                code += f'    body: dict,  # Request body\n'

            code += f') -> dict | str:\n'
            code += f'    """{description}"""\n'

            # Build URL with path parameters (use sanitized names)
            url_path = path
            for param in parameters:
                if param.get('in') == 'path':
                    original_name = param.get('name', '')
                    sanitized_name = param.get('sanitized_name', original_name)
                    if original_name:
                        # Replace the placeholder with the sanitized parameter name
                        url_path = url_path.replace('{' + original_name + '}', '{' + sanitized_name + '}')

            code += '    url = f"{BASE_URL}' + url_path + '"\n\n'

            # Handle different request methods
            code += f'    async with httpx.AsyncClient() as client:\n'

            if method == 'GET':
                code += f'        params = ' + '{}\n'
                for param in parameters:
                    if param.get('in') == 'query':
                        original_name = param.get('name', '')
                        sanitized_name = param.get('sanitized_name', original_name)
                        code += f'        if {sanitized_name} is not None:\n'
                        code += f'            params["{original_name}"] = {sanitized_name}\n'
                code += f'\n        response = await client.get(url, params=params)\n'

            elif method in ['POST', 'PUT', 'PATCH']:
                code += f'        response = await client.{method.lower()}(url, json=body)\n'

            elif method == 'DELETE':
                code += f'        response = await client.delete(url)\n'

            code += f'        response.raise_for_status()\n'
            code += '        \n'
            code += '        # Try to parse as JSON, fallback to text if not JSON\n'
            code += '        if not response.text:\n'
            code += '            return {"status": "success"}\n'
            code += '        \n'
            code += '        try:\n'
            code += '            return response.json()\n'
            code += '        except Exception:\n'
            code += '            # Response is not JSON, return as text\n'
            code += '            return {"text": response.text}\n'

            tool_file.write_text(code)
            print(f"   ✓ Generated {tool_name}.py")

        except Exception as e:
            print(f"   ⚠️  Failed to generate tool {tool_name_raw}: {str(e)[:100]}")
            continue

def generate_tool_implementations():
    """Generate tool implementations for selected OpenAPI operations."""
    if not os.path.exists('./.openapi_tools.json'):
        return

    with open('./.openapi_tools.json', 'r') as f:
        tool_data = json.load(f)

    tools = tool_data.get('tools', [])
    if not tools:
        return

    print(f"\n🔧 Generating {len(tools)} tool implementation(s)...")

    # Always use FastMCP now
    generate_fastmcp_tools(tools, tool_data)

    # Generate prompts from OpenAPI operations
    print(f"\n✨ Generating helpful prompts from API operations...")
    generate_fastmcp_prompts(tools)

def generate_python_tools(tools: List[Dict[str, Any]], tool_data: Dict[str, Any]) -> str:
    """Generate Python tool implementation code."""
    import json as json_module

    base_url = tool_data.get('base_url', 'https://api.example.com')

    code = '''"""Auto-generated tool implementations from OpenAPI spec."""

import logging
from typing import Any, Dict, List
from mcp.types import Tool, TextContent
import httpx

logger = logging.getLogger(__name__)

# Base URL from OpenAPI spec
BASE_URL = "{base_url}"

'''.format(base_url=base_url)

    # Generate list_tools function
    code += 'def get_generated_tools() -> List[Tool]:\n'
    code += '    """Get list of auto-generated tools."""\n'
    code += '    return [\n'

    for tool in tools:
        code += f'        Tool(\n'
        code += f'            name="{tool["name"]}",\n'
        code += f'            description="{tool["description"]}",\n'

        # Build input schema from parameters
        schema = dict(type='object', properties=dict(), required=[])

        for param in tool.get('parameters', []):
            param_name = param.get('name', '')
            param_schema = param.get('schema', dict())
            param_type = param_schema.get('type', 'string')

            schema['properties'][param_name] = dict(
                type=param_type,
                description=param.get('description', '')
            )

            if param.get('required', False):
                schema['required'].append(param_name)

        # Add request body if present
        if tool.get('request_schema_ref'):
            schema['properties']['body'] = dict(
                type='object',
                description='Request body'
            )
            schema['required'].append('body')

        # Use json.dumps to safely serialize the schema
        schema_str = json_module.dumps(schema)
        code += f'            inputSchema={schema_str}\n'
        code += '        ),\n'

    code += '    ]\n\n'

    # Generate call_tool implementation
    code += 'async def call_generated_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:\n'
    code += '    """Execute a generated tool."""\n'
    code += '    logger.info(f"Calling generated tool: {name}")\n\n'

    for tool in tools:
        code += f'    if name == "{tool["name"]}":\n'
        code += f'        # {tool["method"]} {tool["path"]}\n'

        # Build URL with path parameters
        path = tool['path']
        path_params = [p for p in tool.get('parameters', []) if p.get('in') == 'path']

        if path_params:
            for param in path_params:
                param_name = param['name']
                code += f'        {param_name} = arguments.get("{param_name}")\n'
                # Replace {paramName} with {paramName} in the path for f-string interpolation
                path = path.replace('{' + param_name + '}', '{' + param_name + '}')

            code += '        url = f"{BASE_URL}' + path + '"\n'
        else:
            code += '        url = f"{BASE_URL}' + path + '"\n'

        # Add query parameters
        query_params = [p for p in tool.get('parameters', []) if p.get('in') == 'query']
        if query_params:
            code += '        params = ' + '{}' + '\n'
            for param in query_params:
                param_name = param['name']
                code += f'        if "{param_name}" in arguments:\n'
                code += f'            params["{param_name}"] = arguments["{param_name}"]\n'

        # Make HTTP request
        code += '\n        async with httpx.AsyncClient() as client:\n'

        method_lower = tool['method'].lower()
        if method_lower == 'get':
            if query_params:
                code += '            response = await client.get(url, params=params)\n'
            else:
                code += '            response = await client.get(url)\n'
        elif method_lower in ['post', 'put', 'patch']:
            code += '            body = arguments.get("body", ' + '{}' + ')\n'
            code += f'            response = await client.{method_lower}(url, json=body)\n'
        elif method_lower == 'delete':
            code += f'            response = await client.delete(url)\n'

        code += '            response.raise_for_status()\n'
        code += '            return [TextContent(type="text", text=response.text)]\n\n'

    code += '    raise ValueError(f"Unknown generated tool: {name}")\n'

    return code

def setup_fastmcp_project():
    """Setup FastMCP-specific project structure (always used now)."""
    project_slug = "{{ cookiecutter.project_slug }}"

    # Create tools directory structure
    tools_dir = Path(f"src/{project_slug}/tools")
    tools_dir.mkdir(exist_ok=True)

    # Create __init__.py for tools
    tools_init = tools_dir / "__init__.py"
    tools_init.write_text("\"\"\"Auto-generated tools from OpenAPI specification.\"\"\"\n")

    # Create prompts directory structure
    prompts_dir = Path(f"src/{project_slug}/prompts")
    prompts_dir.mkdir(exist_ok=True)

    # Create __init__.py for prompts
    prompts_init = prompts_dir / "__init__.py"
    prompts_init.write_text("\"\"\"Auto-generated prompts from OpenAPI specification.\"\"\"\n")

def main():
    """Main post-generation setup."""
    print("\n🔧 Running post-generation setup...")

    # Create environment template
    create_env_template()

    # Clean up unused files
    cleanup_unused_files()

    # Generate Pydantic models if OpenAPI spec was provided
    models_generated = generate_pydantic_models()

    # Setup FastMCP project structure
    setup_fastmcp_project()

    # Generate tool implementations if tools were selected
    generate_tool_implementations()

    # Setup Python project dependencies
    setup_python_project()

    # Clean up temporary files
    for temp_file in ['./.openapi_tools.json', './.openapi_spec.json']:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
