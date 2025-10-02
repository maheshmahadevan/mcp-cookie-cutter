#!/usr/bin/env python3
"""OpenAPI to MCP tool generator with intelligence."""

import json
from typing import Dict, List, Any, Optional


class OpenAPIToolGenerator:
    """Generate MCP tools from OpenAPI specifications."""

    def __init__(self, spec: Dict[str, Any]):
        """Initialize with OpenAPI spec."""
        self.spec = spec
        self.base_url = self._extract_base_url()
        self.security = self._extract_security()

    def _extract_base_url(self) -> str:
        """Extract base URL from OpenAPI spec."""
        # OpenAPI 3.x
        if 'servers' in self.spec and self.spec['servers']:
            return self.spec['servers'][0].get('url', '')

        # Swagger 2.0
        schemes = self.spec.get('schemes', ['https'])
        host = self.spec.get('host', '')
        base_path = self.spec.get('basePath', '')

        if host:
            return f"{schemes[0]}://{host}{base_path}"

        return ""

    def _extract_security(self) -> Dict[str, Any]:
        """Extract security schemes from OpenAPI spec."""
        # OpenAPI 3.x
        if 'components' in self.spec and 'securitySchemes' in self.spec['components']:
            return self.spec['components']['securitySchemes']

        # Swagger 2.0
        if 'securityDefinitions' in self.spec:
            return self.spec['securityDefinitions']

        return {}

    def extract_tools(self) -> List[Dict[str, Any]]:
        """Extract all available tools from OpenAPI spec."""
        tools = []
        paths = self.spec.get('paths', {})

        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                    continue

                tool = self._operation_to_tool(path, method.upper(), operation)
                if tool:
                    tools.append(tool)

        return tools

    def _operation_to_tool(self, path: str, method: str, operation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Convert an OpenAPI operation to an MCP tool definition."""
        operation_id = operation.get('operationId', f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '')}")

        # Extract parameters
        parameters = operation.get('parameters', [])
        request_body = operation.get('requestBody', {})

        # Build input schema
        input_schema = self._build_input_schema(parameters, request_body)

        # Determine if this is a good candidate for a tool
        description = operation.get('summary', operation.get('description', ''))

        return {
            'operation_id': operation_id,
            'name': operation_id,
            'description': description or f"{method} {path}",
            'method': method,
            'path': path,
            'parameters': parameters,
            'request_body': request_body,
            'input_schema': input_schema,
            'responses': operation.get('responses', {}),
            'tags': operation.get('tags', []),
            'security': operation.get('security', []),
        }

    def _build_input_schema(self, parameters: List[Dict], request_body: Dict) -> Dict[str, Any]:
        """Build JSON schema for tool input from OpenAPI parameters."""
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }

        # Add path, query, and header parameters
        for param in parameters:
            param_name = param.get('name')
            param_in = param.get('in')
            param_schema = param.get('schema', {})

            # Handle Swagger 2.0 style
            if not param_schema and 'type' in param:
                param_schema = {
                    'type': param.get('type'),
                    'format': param.get('format'),
                    'description': param.get('description'),
                }

            schema['properties'][param_name] = {
                'type': param_schema.get('type', 'string'),
                'description': param.get('description', ''),
            }

            if 'enum' in param_schema:
                schema['properties'][param_name]['enum'] = param_schema['enum']

            if param.get('required', False):
                schema['required'].append(param_name)

        # Add request body schema
        if request_body:
            content = request_body.get('content', {})
            json_content = content.get('application/json', {})
            if json_content:
                body_schema = json_content.get('schema', {})
                schema['properties']['body'] = body_schema
                if request_body.get('required', False):
                    schema['required'].append('body')

        return schema

    def generate_python_tool_code(self, tool: Dict[str, Any]) -> str:
        """Generate Python code for a single tool."""
        method = tool['method']
        path = tool['path']
        operation_id = tool['operation_id']
        base_url = self.base_url

        # Extract path parameters
        path_params = [p['name'] for p in tool['parameters'] if p.get('in') == 'path']
        query_params = [p['name'] for p in tool['parameters'] if p.get('in') == 'query']
        has_body = 'body' in tool['input_schema']['properties']

        # Build function signature
        code = f'''
async def {operation_id}(arguments: Dict[str, Any]) -> str:
    """
    {tool['description']}

    Method: {method}
    Path: {path}
    """
    import httpx

    # Extract parameters
'''

        # Extract path parameters
        for param in path_params:
            code += f"    {param} = arguments.get('{param}')\n"

        # Extract query parameters
        if query_params:
            code += "    params = {}\n"
            for param in query_params:
                code += f"    if '{param}' in arguments:\n"
                code += f"        params['{param}'] = arguments['{param}']\n"

        # Extract body
        if has_body:
            code += "    body = arguments.get('body', {})\n"

        # Build URL
        url = f'"{base_url}{path}"'
        for param in path_params:
            url = url.replace(f'{{{param}}}', f'{{{param}}}')

        code += f"\n    url = f{url}\n"

        # Make HTTP request
        code += "\n    async with httpx.AsyncClient() as client:\n"

        if method in ['GET', 'DELETE']:
            if query_params:
                code += f"        response = await client.{method.lower()}(url, params=params)\n"
            else:
                code += f"        response = await client.{method.lower()}(url)\n"
        else:
            if query_params:
                code += f"        response = await client.{method.lower()}(url, json=body, params=params)\n"
            elif has_body:
                code += f"        response = await client.{method.lower()}(url, json=body)\n"
            else:
                code += f"        response = await client.{method.lower()}(url)\n"

        code += "        response.raise_for_status()\n"
        code += "        return response.text\n"

        return code

    def generate_typescript_tool_code(self, tool: Dict[str, Any]) -> str:
        """Generate TypeScript code for a single tool."""
        method = tool['method']
        path = tool['path']
        operation_id = tool['operation_id']
        base_url = self.base_url

        # Extract path parameters
        path_params = [p['name'] for p in tool['parameters'] if p.get('in') == 'path']
        query_params = [p['name'] for p in tool['parameters'] if p.get('in') == 'query']
        has_body = 'body' in tool['input_schema']['properties']

        code = f'''
async function {operation_id}(args: any): Promise<string> {{
  /**
   * {tool['description']}
   *
   * Method: {method}
   * Path: {path}
   */

  // Extract parameters
'''

        # Extract path parameters
        for param in path_params:
            code += f"  const {param} = args.{param};\n"

        # Build URL
        url = f'`{base_url}{path}`'
        for param in path_params:
            url = url.replace(f'{{{param}}}', f'${{{param}}}')

        code += f"\n  const url = {url};\n"

        # Build query params
        if query_params:
            code += "  const params = new URLSearchParams();\n"
            for param in query_params:
                code += f"  if (args.{param}) params.append('{param}', args.{param});\n"

        # Make HTTP request
        code += "\n  const options: RequestInit = {\n"
        code += f"    method: '{method}',\n"

        if has_body:
            code += "    headers: { 'Content-Type': 'application/json' },\n"
            code += "    body: JSON.stringify(args.body),\n"

        code += "  };\n\n"

        if query_params:
            code += "  const response = await fetch(`${url}?${params}`, options);\n"
        else:
            code += "  const response = await fetch(url, options);\n"

        code += "  if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);\n"
        code += "  return await response.text();\n"
        code += "}\n"

        return code
