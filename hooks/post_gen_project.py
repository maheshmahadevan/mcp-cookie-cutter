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

def setup_typescript_project():
    """Set up TypeScript project dependencies."""
    print("\n📦 Setting up TypeScript project...")

    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: npm not found. Please install Node.js and npm.")
        return

    print("Installing dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True)
        print("✓ Dependencies installed")

        print("\nBuilding project...")
        subprocess.run(["npm", "run", "build"], check=True)
        print("✓ Project built")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Build step failed: {e}")
        print("\nTo install and build manually, run:")
        print("  npm install")
        print("  npm run build")

def cleanup_unused_files():
    """Remove files not needed for the selected configuration."""
    sdk_choice = "{{ cookiecutter.sdk_choice }}"
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"

    # Remove SDK-specific files
    if sdk_choice == "python":
        # Remove TypeScript files
        ts_files = [
            "package.json",
            "tsconfig.json",
            "src/index.ts",
            "src/tools.ts",
            "src/resources.ts",
            "src/prompts.ts",
        ]
        if auth_mechanism == "oauth2":
            ts_files.append("src/auth/oauth.ts")
        if auth_mechanism == "api_key":
            ts_files.append("src/auth/apiKey.ts")

        for file in ts_files:
            file_path = Path(file)
            if file_path.exists():
                file_path.unlink()

    elif sdk_choice == "typescript":
        # Remove Python files
        py_files = [
            "pyproject.toml",
            f"src/{{ cookiecutter.project_slug }}/server.py",
        ]
        if auth_mechanism == "oauth2":
            py_files.append(f"src/{{ cookiecutter.project_slug }}/auth/oauth.py")
        if auth_mechanism == "api_key":
            py_files.append(f"src/{{ cookiecutter.project_slug }}/auth/api_key.py")

        for file in py_files:
            file_path = Path(file)
            if file_path.exists():
                file_path.unlink()

    # Remove auth files if not needed
    if auth_mechanism == "none":
        auth_dir = Path("src/{{ cookiecutter.project_slug }}/auth" if sdk_choice == "python" else "src/auth")
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
    sdk_choice = "{{ cookiecutter.sdk_choice }}"
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

    if sdk_choice == "python":
        print("2. Activate the virtual environment:")
        print("   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
        print("\n3. Install dependencies:")
        print("   uv pip install -e .")
    else:
        print("2. Install dependencies (if not already done):")
        print("   npm install")
        print("\n3. Build the project:")
        print("   npm run build")

    if auth_mechanism != "none":
        print(f"\n4. Configure authentication:")
        print("   cp .env.example .env")
        print("   # Edit .env with your credentials")

    print("\n5. Run the server:")
    if sdk_choice == "python":
        print("   {{ cookiecutter.project_slug }}")
    else:
        print("   npm start")

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

    sdk_choice = "{{ cookiecutter.sdk_choice }}"
    project_slug = "{{ cookiecutter.project_slug }}"

    if sdk_choice == "python":
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
            print(f"⚠️  Warning: Model generation failed: {e}")
            if e.stderr:
                print(f"   {e.stderr.decode()}")
            return False

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
        prompt_file = prompts_dir / f"{category}_operations.py"

        code = f'"""Auto-generated prompt for {category} operations"""\n\n'

        # Create a helpful prompt listing available operations
        code += f'@mcp.prompt()  # type: ignore\n'
        code += f'def {category}_help() -> str:\n'
        code += f'    """Get help for {category} operations in the API."""\n'
        code += f'    return """\n'
        code += f'# {category.title()} Operations\n\n'
        code += f'Available operations:\n\n'

        for tool in category_tools:
            method = tool['method']
            path = tool['path']
            name = tool['name']
            desc = tool.get('description', '')
            code += f'- **{name}** ({method} {path})\n'
            code += f'  {desc}\n\n'

        code += f'"""\n'

        prompt_file.write_text(code)
        print(f"   ✓ Generated {category}_operations.py prompt")

def generate_fastmcp_tools(tools: list, tool_data: dict):
    """Generate individual FastMCP tool files."""
    project_slug = "{{ cookiecutter.project_slug }}"
    tools_dir = Path(f"src/{project_slug}/tools")
    tools_dir.mkdir(parents=True, exist_ok=True)

    base_url = tool_data.get('base_url', '')

    for tool in tools:
        tool_name = tool['name']
        method = tool['method']
        path = tool['path']
        description = tool.get('description', '')
        parameters = tool.get('parameters', [])

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

        # Generate tool function with FastMCP decorator
        code += f'@mcp.tool()  # type: ignore\n'
        code += f'async def {tool_name}(\n'

        # Sort parameters: required first, then optional
        required_params = [p for p in parameters if p.get('required')]
        optional_params = [p for p in parameters if not p.get('required')]
        sorted_params = required_params + optional_params

        # Add parameters
        for param in sorted_params:
            param_name = param.get('name', '')
            param_type = param.get('schema', dict()).get('type', 'str')
            python_type = dict(string='str', integer='int', boolean='bool', number='float').get(param_type, 'Any')
            param_desc = param.get('description', '')

            if param.get('required'):
                code += f'    {param_name}: {python_type},  # {param_desc}\n'
            else:
                code += f'    {param_name}: {python_type} | None = None,  # {param_desc}\n'

        # Add body parameter if it's a POST/PUT/PATCH
        if method in ['POST', 'PUT', 'PATCH'] and tool.get('request_schema_ref'):
            code += f'    body: dict,  # Request body\n'

        code += f') -> dict | str:\n'
        code += f'    """{description}"""\n'

        # Build URL with path parameters
        url_path = path
        for param in parameters:
            if param.get('in') == 'path':
                param_name = param['name']
                url_path = url_path.replace('{' + param_name + '}', '{' + param_name + '}')

        code += '    url = f"{BASE_URL}' + url_path + '"\n\n'

        # Handle different request methods
        code += f'    async with httpx.AsyncClient() as client:\n'

        if method == 'GET':
            code += f'        params = ' + '{}\n'
            for param in parameters:
                if param.get('in') == 'query':
                    param_name = param['name']
                    code += f'        if {param_name} is not None:\n'
                    code += f'            params["{param_name}"] = {param_name}\n'
            code += f'\n        response = await client.get(url, params=params)\n'

        elif method in ['POST', 'PUT', 'PATCH']:
            code += f'        response = await client.{method.lower()}(url, json=body)\n'

        elif method == 'DELETE':
            code += f'        response = await client.delete(url)\n'

        code += f'        response.raise_for_status()\n'
        code += '        return response.json() if response.text else {"status": "success"}\n'

        tool_file.write_text(code)
        print(f"   ✓ Generated {tool_name}.py")

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
    return

    sdk_choice = "{{ cookiecutter.sdk_choice }}"
    project_slug = "{{ cookiecutter.project_slug }}"

    if sdk_choice == "python":
        tools_file = Path(f"src/{project_slug}/tools_generated.py")

        # Generate Python tool implementations
        tool_code = generate_python_tools(tools, tool_data)
        tools_file.write_text(tool_code)

        print(f"✓ Generated tool implementations in {tools_file}")
        print(f"   Import these in your tools.py file to use them")

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

    sdk_choice = "{{ cookiecutter.sdk_choice }}"

    # Create environment template
    create_env_template()

    # Clean up unused files
    cleanup_unused_files()

    # Generate Pydantic models if OpenAPI spec was provided
    models_generated = generate_pydantic_models()

    # Setup FastMCP project structure (always for Python)
    if sdk_choice == "python":
        setup_fastmcp_project()

    # Generate tool implementations if tools were selected
    generate_tool_implementations()

    # SDK-specific setup
    if sdk_choice == "python":
        setup_python_project()
    elif sdk_choice == "typescript":
        setup_typescript_project()

    # Clean up temporary files
    for temp_file in ['./.openapi_tools.json', './.openapi_spec.json']:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
