#!/usr/bin/env python3
"""Pre-generation hook to validate inputs and parse OpenAPI specs."""

import sys
import os
import json
from typing import Dict, List, Any, Optional

def validate_project_name():
    """Validate project name."""
    project_name = "{{ cookiecutter.project_name }}"

    if not project_name or project_name.strip() == "":
        print("Error: Project name cannot be empty")
        sys.exit(1)

def validate_deployment_auth_combo():
    """Validate deployment type and auth mechanism combination."""
    deployment = "{{ cookiecutter.deployment_type }}"
    auth = "{{ cookiecutter.auth_mechanism }}"

    if deployment == "remote" and auth == "none":
        print("\n⚠️  Warning: Remote deployment without authentication is not recommended for production.")
        print("Consider using API key or OAuth 2.1 for production deployments.\n")

    if deployment == "remote" and auth == "api_key":
        print("\nℹ️  Info: API key authentication selected.")
        print("For public clients, consider OAuth 2.1 for enhanced security.\n")

def load_openapi_spec(spec_path: str) -> Optional[Dict[str, Any]]:
    """Load OpenAPI spec from file or URL with proper parsing."""
    try:
        # Try to import optional dependencies
        try:
            import yaml
        except ImportError:
            yaml = None

        try:
            import requests
        except ImportError:
            requests = None

        try:
            from openapi_pydantic import OpenAPI
            has_openapi_pydantic = True
        except ImportError:
            has_openapi_pydantic = False

        spec_dict = None

        # Load from URL
        if spec_path.startswith(('http://', 'https://')):
            if requests is None:
                print("⚠️  Warning: 'requests' library not installed. Cannot fetch from URL.")
                print("   Install with: pip install requests")
                return None

            response = requests.get(spec_path, timeout=10)
            response.raise_for_status()

            # Try JSON first
            try:
                spec_dict = response.json()
            except json.JSONDecodeError:
                # Try YAML
                if yaml:
                    spec_dict = yaml.safe_load(response.text)
                else:
                    print("⚠️  Warning: 'pyyaml' library not installed. Cannot parse YAML.")
                    print("   Install with: pip install pyyaml")
                    return None

        # Load from file
        else:
            if not os.path.exists(spec_path):
                print(f"⚠️  Warning: OpenAPI spec file not found: {spec_path}")
                return None

            with open(spec_path, 'r') as f:
                content = f.read()

                # Try JSON first
                try:
                    spec_dict = json.loads(content)
                except json.JSONDecodeError:
                    # Try YAML
                    if yaml:
                        spec_dict = yaml.safe_load(content)
                    else:
                        print("⚠️  Warning: 'pyyaml' library not installed. Cannot parse YAML.")
                        print("   Install with: pip install pyyaml")
                        return None

        # Validate with openapi-pydantic if available
        if spec_dict and has_openapi_pydantic:
            try:
                # Validate the spec using Pydantic models
                OpenAPI.model_validate(spec_dict)
            except Exception as e:
                print(f"⚠️  Warning: OpenAPI spec validation failed: {e}")
                print("   Proceeding with basic parsing...")

        return spec_dict

    except Exception as e:
        print(f"⚠️  Warning: Error loading OpenAPI spec: {e}")
        return None

def extract_tools_from_spec(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract available tools from OpenAPI spec with full operation details."""
    tools = []

    # Get paths
    paths = spec.get('paths', {})

    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                continue

            # Extract operation details
            operation_id = operation.get('operationId', f"{method}_{path.replace('/', '_')}")
            summary = operation.get('summary', operation.get('description', ''))

            # Extract parameters (path, query, header, etc.)
            parameters = operation.get('parameters', [])

            # Extract request body schema reference (if any)
            request_body = operation.get('requestBody', {})
            request_schema_ref = None
            if request_body:
                content = request_body.get('content', {})
                if 'application/json' in content:
                    schema = content['application/json'].get('schema', {})
                    request_schema_ref = schema.get('$ref')

            # Extract response schema references
            responses = operation.get('responses', {})
            response_schema_refs = {}
            for status_code, response_obj in responses.items():
                content = response_obj.get('content', {})
                if 'application/json' in content:
                    schema = content['application/json'].get('schema', {})
                    schema_ref = schema.get('$ref')
                    if schema_ref:
                        response_schema_refs[status_code] = schema_ref

            tools.append({
                'name': operation_id,
                'method': method.upper(),
                'path': path,
                'description': summary,
                'parameters': parameters,
                'request_schema_ref': request_schema_ref,
                'response_schema_refs': response_schema_refs,
                'operation': operation  # Keep full operation for later use
            })

    return tools

def prompt_tool_selection(tools: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Prompt user to select which tools to implement."""
    print("\n🔧 Interactive Tool Selection")
    print("=" * 70)
    print("Select which API operations to implement as MCP tools.")
    print("You can always add more tools later using CUSTOMIZATION.md\n")

    # Show all tools with numbers
    for i, tool in enumerate(tools, 1):
        print(f"{i:2d}. [{tool['method']:6s}] {tool['path']:35s} - {tool['name']}")
        if tool['description']:
            print(f"    {tool['description'][:60]}")

    print("\n" + "=" * 70)
    print("Enter your choices:")
    print("  • Specific numbers: 1,3,5")
    print("  • Ranges: 1-5")
    print("  • All: 'all' or press Enter")
    print("  • Skip: 'none' or 'skip'")

    while True:
        try:
            choice = input("\nYour selection: ").strip().lower()

            # Handle special cases
            if not choice or choice == 'all':
                return tools

            if choice in ['none', 'skip', 'n']:
                print("\n⏭️  Skipping tool generation. You can add tools manually later.")
                return []

            # Parse selection
            selected_indices = set()
            parts = choice.split(',')

            for part in parts:
                part = part.strip()

                # Handle ranges (e.g., "1-5")
                if '-' in part:
                    start, end = part.split('-')
                    start_idx = int(start.strip()) - 1
                    end_idx = int(end.strip()) - 1

                    if 0 <= start_idx < len(tools) and 0 <= end_idx < len(tools):
                        selected_indices.update(range(start_idx, end_idx + 1))
                    else:
                        print(f"⚠️  Range {part} is out of bounds (1-{len(tools)})")
                        continue

                # Handle single numbers
                else:
                    idx = int(part) - 1
                    if 0 <= idx < len(tools):
                        selected_indices.add(idx)
                    else:
                        print(f"⚠️  Number {part} is out of bounds (1-{len(tools)})")
                        continue

            selected = [tools[i] for i in sorted(selected_indices)]

            if selected:
                print(f"\n✓ Selected {len(selected)} tool(s):")
                for tool in selected:
                    print(f"  • {tool['method']:6s} {tool['path']:35s} - {tool['name']}")

                confirm = input("\nProceed with this selection? [Y/n]: ").strip().lower()
                if confirm in ['', 'y', 'yes']:
                    return selected
            else:
                print("\n⚠️  No valid tools selected. Try again.")

        except ValueError as e:
            print(f"⚠️  Invalid input format. Please use numbers, ranges, or 'all'.")
        except KeyboardInterrupt:
            print("\n\n⏭️  Selection cancelled. Proceeding without tool generation.")
            return []

def save_selected_tools(tools: List[Dict[str, Any]], spec: Dict[str, Any]):
    """Save selected tools and spec to files for post-generation hook."""
    import json

    # Extract base URL from spec
    base_url = ""
    if 'servers' in spec and spec['servers']:
        base_url = spec['servers'][0].get('url', '')
    elif 'host' in spec:
        schemes = spec.get('schemes', ['https'])
        host = spec.get('host', '')
        base_path = spec.get('basePath', '')
        if host:
            base_url = f"{schemes[0]}://{host}{base_path}"

    # Collect all schema references needed by selected tools
    schema_refs = set()
    for tool in tools:
        if tool.get('request_schema_ref'):
            schema_refs.add(tool['request_schema_ref'])
        for schema_ref in tool.get('response_schema_refs', {}).values():
            schema_refs.add(schema_ref)

    # Save tool selection data
    tool_data = {
        'base_url': base_url,
        'tools': tools,
        'schema_refs': list(schema_refs),
        'spec_version': spec.get('openapi') or spec.get('swagger', 'unknown')
    }

    with open('.openapi_tools.json', 'w') as f:
        json.dump(tool_data, f, indent=2)

    # Save the full OpenAPI spec for datamodel-code-generator
    with open('.openapi_spec.json', 'w') as f:
        json.dump(spec, f, indent=2)

def show_openapi_info():
    """Show information about OpenAPI spec if provided."""
    openapi_spec_path = "{{ cookiecutter.openapi_spec_path }}"

    if openapi_spec_path:
        print(f"\n📋 OpenAPI Specification: {openapi_spec_path}")

        # Try to parse the spec
        spec = load_openapi_spec(openapi_spec_path)

        if spec:
            tools = extract_tools_from_spec(spec)

            if tools:
                print(f"\n✨ Found {len(tools)} available API operations:")
                print("\n" + "-" * 70)

                # Show first 10 tools as preview
                for i, tool in enumerate(tools[:10], 1):
                    print(f"{i:2d}. {tool['method']:6s} {tool['path']:30s} - {tool['name']}")
                    if tool['description']:
                        print(f"     {tool['description'][:60]}")

                if len(tools) > 10:
                    print(f"\n... and {len(tools) - 10} more operations")

                print("-" * 70)

                # Ask if user wants to select tools interactively
                print("\n💡 Would you like to select which tools to implement now?")
                print("   (You can always add more tools later using CUSTOMIZATION.md)")

                try:
                    choice = input("\nSelect tools interactively? [Y/n]: ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    # No input available (--no-input mode) or user cancelled
                    # Default to selecting all tools
                    print("n")
                    choice = 'n'

                if choice in ['', 'y', 'yes']:
                    selected_tools = prompt_tool_selection(tools)
                    if selected_tools:
                        save_selected_tools(selected_tools, spec)
                        print(f"\n✓ Will generate {len(selected_tools)} MCP tool(s)")
                    else:
                        print("\n⏭️  No tools selected. Use CUSTOMIZATION.md to add them later.")
                else:
                    # Default to selecting all tools when not doing interactive selection
                    print("\n⏭️  Skipping interactive selection. Selecting all tools by default.")
                    save_selected_tools(tools, spec)
                    print(f"✓ Will generate all {len(tools)} MCP tool(s)")
            else:
                print("   No API operations found in the spec.")
        else:
            print("   Could not parse OpenAPI spec - proceeding without tool suggestions.")

        print()

def main():
    """Main pre-generation validation."""
    print("\n" + "="*70)
    print("🚀 MCP Cookie Cutter - Generating Your MCP Server")
    print("="*70)

    # Validate inputs
    validate_project_name()
    validate_deployment_auth_combo()
    show_openapi_info()

    print("✓ Input validation complete")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
