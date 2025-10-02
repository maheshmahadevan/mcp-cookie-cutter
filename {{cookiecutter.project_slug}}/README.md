# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Overview

This MCP server was generated using the MCP Cookie Cutter framework and provides integration with APIs through the Model Context Protocol.

### Configuration

- **SDK**: {{ cookiecutter.sdk_choice }}
- **Deployment**: {{ cookiecutter.deployment_type }}
- **Authentication**: {{ cookiecutter.auth_mechanism }}

## Features

- **Tools**: Execute API operations as MCP tools
{% if cookiecutter.include_resources == 'yes' -%}
- **Resources**: Access API data as MCP resources
{% endif -%}
{% if cookiecutter.include_prompts == 'yes' -%}
- **Prompts**: Pre-built prompt templates for common tasks
{% endif -%}

## Installation

{% if cookiecutter.sdk_choice == 'python' -%}
### Python

{% if cookiecutter.python_package_manager == 'uv' -%}
Using uv (recommended for faster installs):

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# For development
uv pip install -e ".[dev]"
```
{% else -%}
Using pip:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# For development
pip install -e ".[dev]"
```
{% endif -%}
{% else -%}
### TypeScript

```bash
# Install dependencies
npm install

# Build the project
npm run build
```
{% endif -%}

## Configuration

{% if cookiecutter.auth_mechanism == 'api_key' -%}
### API Key Authentication

Create a `.env` file in the project root:

```env
MCP_API_KEYS=your-api-key-1,your-api-key-2
```
{% elif cookiecutter.auth_mechanism == 'oauth2' -%}
### OAuth 2.1 Authentication

Configure OAuth settings in your environment or code:

- Client ID
- Client Secret (optional for public clients using PKCE)
- Authorization Endpoint
- Token Endpoint

**Note**: OAuth 2.1 is recommended for public clients. Use PKCE flow for enhanced security.
{% endif -%}

## Usage

{% if cookiecutter.deployment_type == 'local' -%}
### Local (STDIO) Mode

{% if cookiecutter.sdk_choice == 'python' -%}
{% if cookiecutter.python_package_manager == 'uv' -%}
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run the server
{{ cookiecutter.project_slug }}
```

Or run directly:
```bash
uv run {{ cookiecutter.project_slug }}
```
{% else -%}
```bash
# Activate virtual environment first
source venv/bin/activate

# Run the server
{{ cookiecutter.project_slug }}
```

Or run directly:
```bash
python -m {{ cookiecutter.project_slug }}.server
```
{% endif -%}
{% else -%}
```bash
npm start
```

Or run directly:
```bash
node dist/index.js
```
{% endif -%}

#### Claude Desktop Configuration

Add to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

{% if cookiecutter.sdk_choice == 'python' -%}
{% if cookiecutter.python_package_manager == 'uv' -%}
```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/{{ cookiecutter.project_slug }}",
        "run",
        "{{ cookiecutter.project_slug }}"
      ]
    }
  }
}
```
{% else -%}
```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "/path/to/venv/bin/{{ cookiecutter.project_slug }}"
    }
  }
}
```
{% endif -%}
{% else -%}
```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "node",
      "args": ["/path/to/{{ cookiecutter.project_slug }}/dist/index.js"]
    }
  }
}
```
{% endif -%}

{% else -%}
### Remote (SSE) Mode

{% if cookiecutter.sdk_choice == 'python' -%}
```bash
{{ cookiecutter.project_slug }}
```

The server will start on `http://0.0.0.0:8000`
{% else -%}
```bash
npm start
```

The server will start on `http://localhost:8000`
{% endif -%}

#### Connecting to Remote Server

Configure your MCP client to connect to the SSE endpoint:

```
http://your-server:8000/sse
```

{% if cookiecutter.auth_mechanism != 'none' -%}
Include authentication headers as configured.
{% endif -%}
{% endif -%}

## Development

{% if cookiecutter.sdk_choice == 'python' -%}
### Python Development

```bash
# Run tests
pytest

# Type checking
mypy src

# Format code
black src

# Lint
ruff check src
```
{% else -%}
### TypeScript Development

```bash
# Watch mode for development
npm run dev

# Run tests
npm test

# Lint
npm run lint

# Format
npm run format
```
{% endif -%}

## Project Structure

```
{{ cookiecutter.project_slug }}/
{% if cookiecutter.sdk_choice == 'python' -%}
├── src/
│   └── {{ cookiecutter.project_slug }}/
│       ├── server.py          # Main server implementation
│       ├── tools.py           # Tool definitions and handlers
{% if cookiecutter.include_resources == 'yes' -%}
│       ├── resources.py       # Resource definitions
{% endif -%}
{% if cookiecutter.include_prompts == 'yes' -%}
│       ├── prompts.py         # Prompt templates
{% endif -%}
{% if cookiecutter.auth_mechanism != 'none' -%}
│       └── auth/              # Authentication handlers
{% if cookiecutter.auth_mechanism == 'oauth2' -%}
│           └── oauth.py       # OAuth 2.1 implementation
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
│           └── api_key.py     # API key implementation
{% endif -%}
{% endif -%}
├── pyproject.toml             # Python project configuration
└── README.md
{% else -%}
├── src/
│   ├── index.ts               # Main server implementation
│   ├── tools.ts               # Tool definitions and handlers
{% if cookiecutter.include_resources == 'yes' -%}
│   ├── resources.ts           # Resource definitions
{% endif -%}
{% if cookiecutter.include_prompts == 'yes' -%}
│   ├── prompts.ts             # Prompt templates
{% endif -%}
{% if cookiecutter.auth_mechanism != 'none' -%}
│   └── auth/                  # Authentication handlers
{% if cookiecutter.auth_mechanism == 'oauth2' -%}
│       └── oauth.ts           # OAuth 2.1 implementation
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
│       └── apiKey.ts          # API key implementation
{% endif -%}
{% endif -%}
├── package.json               # Node.js project configuration
├── tsconfig.json              # TypeScript configuration
└── README.md
{% endif -%}
```

## Security Best Practices

{% if cookiecutter.deployment_type == 'local' -%}
### Local Deployment
- **STDIO Transport**: Runs locally with no network exposure
- Always log to stderr, never stdout
- Validate all input parameters
{% else -%}
### Remote Deployment
- **SSE Transport**: Exposed over HTTP/HTTPS
{% if cookiecutter.auth_mechanism == 'none' -%}
- ⚠️ **Warning**: No authentication configured - not recommended for production
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
- API key authentication enabled
- Store keys securely in environment variables
- Rotate keys regularly
- Consider upgrading to OAuth 2.1 for public clients
{% elif cookiecutter.auth_mechanism == 'oauth2' -%}
- OAuth 2.1 authentication enabled
- Use PKCE for public clients
- Implement proper token validation
- Follow the OAuth 2.1 security best practices
{% endif -%}
- Use HTTPS in production
- Implement rate limiting
- Monitor and log all requests
{% endif -%}

### General Security
- Obtain explicit user consent for data access
- Protect user data privacy
- Implement proper error handling
- Follow MCP specification guidelines

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
{% if cookiecutter.sdk_choice == 'python' -%}
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
{% else -%}
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
{% endif -%}

## License

{{ cookiecutter.license }}

## Author

{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

---

*Generated with MCP Cookie Cutter*
