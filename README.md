# MCP Cookie Cutter

A cookiecutter template for creating Model Context Protocol (MCP) servers. Get a fully-configured MCP server in seconds, then customize it for your API.

## Features

- 🚀 **Quick Start**: Generate a working MCP server in seconds
- 🐍 **Python & TypeScript**: Choose your preferred SDK
- 🌐 **Local & Remote**: Support for STDIO (local) and SSE (remote) transports
- 🔐 **Authentication**: Built-in templates for OAuth 2.1 and API key authentication
- 📦 **Full-Featured**: Tools, Resources, and Prompts support
- 📝 **Easy Customization**: Clear examples and guides for adding your API tools
- ⚡ **Modern Tooling**: Support for uv (Python) and latest SDKs
- ✅ **Best Practices**: Follows MCP specification and security guidelines

## What You Get

- Complete MCP server project structure
- **Intelligent OpenAPI parsing** - See available API operations during generation
- Example tool implementations (GET and POST)
- Comprehensive CUSTOMIZATION.md guide
- Authentication templates
- Development environment setup
- Claude Desktop integration instructions

## Prerequisites

- Python 3.10+ (required for cookiecutter and Python servers)
- Node.js 18+ (required for TypeScript servers)
- [cookiecutter](https://github.com/cookiecutter/cookiecutter)

## Installation

```bash
# Install cookiecutter (required)
pip install cookiecutter

# Install optional dependencies for full OpenAPI parsing functionality
pip install pyyaml requests openapi-pydantic
```

Or install all at once:

```bash
pip install cookiecutter pyyaml requests openapi-pydantic
```

### Dependency Details

- **cookiecutter** (required) - Template generation engine
- **pyyaml** (optional) - For parsing YAML OpenAPI specs
- **requests** (optional) - For fetching OpenAPI specs from URLs
- **openapi-pydantic** (optional) - For validating and parsing OpenAPI schemas with type safety

Without the optional dependencies, you can still generate MCP servers, but OpenAPI spec parsing and tool suggestions will not be available.

## Quick Start

### 1. Install (Optional)

You can use the template directly without installation, but for convenience you can install it:

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-cookie-cutter.git
cd mcp-cookie-cutter
```

### 2. Generate Your MCP Server

#### From GitHub (once published):
```bash
cookiecutter gh:yourusername/mcp-cookie-cutter
```

#### From local directory:
```bash
# If you're in the template directory
cookiecutter .

# From anywhere else
cookiecutter /full/path/to/mcp-cookie-cutter

# Or using relative path
cookiecutter ~/projects/mcp-cookie-cutter
```

#### From URL (once published):
```bash
cookiecutter https://github.com/yourusername/mcp-cookie-cutter
```

### 3. Answer the Prompts

You'll be asked to configure:

- **Project name**: Name of your MCP server
- **Project description**: Brief description
- **Author information**: Your name and email
- **OpenAPI spec path**: *(Optional)* Path or URL to your OpenAPI/Swagger spec
- **SDK choice**: Python or TypeScript
- **Python package manager**: uv or pip (for Python projects)
- **Deployment type**: Local (STDIO) or Remote (SSE)
- **Authentication**: None, API key, or OAuth 2.1
- **Include resources**: Yes/No
- **Include prompts**: Yes/No
- **License**: Choose from MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, or Proprietary

### 4. Customize Your Tools

The generated server includes example tools. Follow the CUSTOMIZATION.md guide to add your API endpoints.

### 5. Run Your Server

Follow the setup instructions displayed after generation, or see the generated README.md.

## What Gets Generated

### Project Structure

```
my-mcp-server/
├── src/                    # Source code
│   ├── server.py          # Main server (Python)
│   ├── index.ts           # Main server (TypeScript)
│   ├── tools.py/ts        # Tool implementations
│   ├── resources.py/ts    # Resource implementations (optional)
│   ├── prompts.py/ts      # Prompt templates (optional)
│   └── auth/              # Authentication handlers (optional)
├── pyproject.toml         # Python config
├── package.json           # TypeScript config
├── README.md              # Generated documentation
└── .gitignore
```

### Features

- **OpenAPI Integration**: Pre-generation hook scans your OpenAPI spec and extracts available tools
- **Transport Support**:
  - **Local (STDIO)**: For Claude Desktop and local clients
  - **Remote (SSE)**: For web-based and distributed deployments
- **Authentication**:
  - **None**: Open access (local development only)
  - **API Key**: Simple bearer token or header-based auth
  - **OAuth 2.1**: Standards-compliant OAuth with PKCE support
- **MCP Features**:
  - **Tools**: Execute API operations
  - **Resources**: Access API data
  - **Prompts**: Pre-built prompt templates
  - **Logging**: Proper stderr logging (STDIO-safe)

## OpenAPI/Swagger Integration

The template includes intelligent OpenAPI parsing that:

1. **Loads your OpenAPI/Swagger specification** (from file or URL)
2. **Validates the spec** using openapi-pydantic (if installed)
3. **Extracts all available endpoints** (GET, POST, PUT, DELETE, PATCH)
4. **Displays operation details** during generation

### Supported OpenAPI Formats

- OpenAPI 3.0/3.1 (JSON or YAML)
- Swagger 2.0 (JSON or YAML)

### Example OpenAPI Flow

```bash
# Provide your OpenAPI spec path when prompted
openapi_spec_path: https://petstore.swagger.io/v2/swagger.json

# The hook will scan and display:
✨ Found 20 available API operations:
----------------------------------------------------------------------
 1. POST   /pet                           - addPet
     Add a new pet to the store
 2. GET    /pet/{petId}                   - getPetById
     Find pet by ID
...
----------------------------------------------------------------------

💡 You can implement these as MCP tools in your generated server.
```

See [OPENAPI_PARSING.md](OPENAPI_PARSING.md) for detailed documentation on OpenAPI parsing.

## Configuration Examples

### Local Python Server with No Auth

```
sdk_choice: python
deployment_type: local
auth_mechanism: none
```

Result: STDIO-based server for Claude Desktop

### Remote TypeScript Server with OAuth

```
sdk_choice: typescript
deployment_type: remote
auth_mechanism: oauth2
```

Result: SSE-based server with OAuth 2.1 authentication

### Remote Python Server with API Keys

```
sdk_choice: python
deployment_type: remote
auth_mechanism: api_key
```

Result: SSE-based server with API key authentication

## Best Practices

The generated servers follow MCP best practices:

1. **Security**:
   - OAuth 2.1 recommended for public clients
   - API keys for internal services
   - Proper user consent flows
   - Environment-based credential management

2. **Transport**:
   - STDIO for local deployments (no network exposure)
   - SSE for remote deployments (stateful connections)
   - Proper logging to stderr (never stdout)

3. **Error Handling**:
   - Comprehensive error messages
   - Input validation
   - Graceful degradation

4. **Code Quality**:
   - Type hints (Python) / TypeScript types
   - Linting and formatting configuration
   - Testing setup included

## Development

### Customizing the Template

The template uses Jinja2 templating. Key files:

- `cookiecutter.json`: Configuration options
- `hooks/pre_gen_project.py`: Pre-generation validation and OpenAPI scanning
- `hooks/post_gen_project.py`: Post-generation setup and cleanup
- `{{cookiecutter.project_slug}}/`: Template files with Jinja2 syntax

### Testing Your Template

```bash
# Generate a test project
cookiecutter . --no-input

# Or with specific values
cookiecutter . --no-input sdk_choice=python deployment_type=local
```

## Documentation

- **[EXAMPLE.md](EXAMPLE.md)** - Complete walkthrough with real code examples
- **[USAGE.md](USAGE.md)** - Detailed usage guide for running from different locations
- **[TEST_GUIDE.md](TEST_GUIDE.md)** - Testing with Petstore API

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io)

## Distribution

### Local Use

```bash
# Create alias in your shell config (~/.bashrc or ~/.zshrc)
alias mcp-create='cookiecutter /full/path/to/mcp-cookie-cutter'
```

### Team Use

```bash
# Share via GitHub
git remote add origin https://github.com/yourusername/mcp-cookie-cutter.git
git push -u origin main

# Team members use:
cookiecutter gh:yourusername/mcp-cookie-cutter
```

### Package Distribution (Future)

```bash
# Publish to PyPI (future)
pip install mcp-cookie-cutter
mcp-create
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues and discussions
- Review the MCP documentation

---

*Generate production-ready MCP servers in seconds!*
