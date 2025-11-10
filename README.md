# MCP Cookie Cutter

A cookiecutter template for creating Model Context Protocol (MCP) servers. Get a fully-configured MCP server in seconds, then customize it for your API.

## Features

- 🚀 **Quick Start**: Generate a working MCP server in seconds
- 🐍 **Python with FastMCP**: Modern Python-based MCP servers with FastMCP framework
- 🔧 **OpenAPI Auto-Generation**: Automatically generates tools from OpenAPI/Swagger specs
- 🌐 **Local & Remote**: Support for STDIO (local) and Streamable HTTP (remote) transports
- 🔐 **Authentication**: Built-in templates for OAuth 2.1 and API key authentication
- 📦 **Full-Featured**: Auto-generated tools, prompts, and Pydantic models
- 📝 **Easy Customization**: Clear examples and guides for adding your API tools
- ⚡ **Modern Tooling**: Uses uv for package management and uvicorn for production
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

- Python 3.10+ (required)
- [cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [uv](https://docs.astral.sh/uv/) (recommended for package management)

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

### 1. Install from PyPI (Recommended)

```bash
# Install cookiecutter if you haven't already
pip install cookiecutter

# Install optional dependencies for full OpenAPI parsing
pip install pyyaml requests openapi-pydantic

# Use the template directly from PyPI
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter
```

### 2. Generate Your MCP Server

#### From GitHub (Recommended):
```bash
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter
```

#### From URL:
```bash
cookiecutter https://github.com/maheshmahadevan/mcp-cookie-cutter
```

#### From local directory:
```bash
# Clone the repository first
git clone https://github.com/maheshmahadevan/mcp-cookie-cutter.git
cd mcp-cookie-cutter

# Then use the template
cookiecutter .

# Or from anywhere else using full path
cookiecutter /full/path/to/mcp-cookie-cutter

# Or using relative path
cookiecutter ~/projects/mcp-cookie-cutter
```

### 3. Answer the Prompts

You'll be asked to configure:

- **Project name**: Name of your MCP server
- **Project description**: Brief description
- **Author information**: Your name and email
- **OpenAPI spec path**: *(Optional)* Path or URL to your OpenAPI/Swagger spec
- **Deployment type**: Local (STDIO) or Remote (Streamable HTTP)
- **Server port**: Port for remote deployment (default: 8000)
- **Authentication**: None, API key, or OAuth 2.1
- **License**: Choose from MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, or Proprietary

### 4. Customize Your Tools

The generated server includes example tools. Follow the CUSTOMIZATION.md guide to add your API endpoints.

### 5. Run Your Server

Follow the setup instructions displayed after generation, or see the generated README.md.

## What Gets Generated

### Project Structure

```
my-mcp-server/
├── src/
│   └── my_mcp_server/
│       ├── server.py          # FastMCP server with auto-discovery
│       ├── tools/             # Individual tool files (auto-generated)
│       │   ├── __init__.py
│       │   ├── addPet.py      # Example: POST /pet
│       │   ├── getPetById.py  # Example: GET /pet/{petId}
│       │   └── ...
│       ├── prompts/           # Auto-generated prompts from OpenAPI
│       │   ├── __init__.py
│       │   └── pet_operations.py
│       └── models/            # Pydantic models from OpenAPI
│           ├── __init__.py
│           └── schemas.py
├── test_server.py         # Development testing with auto-reload
├── pyproject.toml         # Python project configuration
├── .env.example           # Environment variables template
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker compose for easy deployment
├── README.md              # Generated documentation
├── CUSTOMIZATION.md       # Guide for adding custom tools
└── .gitignore
```

### Features

- **OpenAPI Integration**: Auto-generates tools, prompts, and Pydantic models from OpenAPI specs
- **FastMCP Framework**: Modern Python MCP framework with decorator-based tool definitions
- **Transport Support**:
  - **Local (STDIO)**: For Claude Desktop and local clients
  - **Remote (Streamable HTTP)**: Production-grade HTTP server with uvicorn
- **Authentication**:
  - **None**: Open access (local development only)
  - **API Key**: Bearer token authentication
  - **OAuth 2.1**: Standards-compliant OAuth with PKCE support
- **MCP Features**:
  - **Tools**: Auto-generated from OpenAPI operations (individual files per tool)
  - **Prompts**: Auto-generated helpful prompts from API operations
  - **Models**: Pydantic models from OpenAPI schemas
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

### Local Server with No Auth

```
deployment_type: local
auth_mechanism: none
openapi_spec_path: https://petstore3.swagger.io/api/v3/openapi.json
```

Result: STDIO-based server for Claude Desktop with auto-generated tools

### Remote Server with API Keys

```
deployment_type: remote
server_port: 9090
auth_mechanism: api_key
openapi_spec_path: https://petstore3.swagger.io/api/v3/openapi.json
```

Result: Streamable HTTP server with API key authentication and auto-generated tools

### Remote Server with OAuth

```
deployment_type: remote
server_port: 8000
auth_mechanism: oauth2
openapi_spec_path: https://api.github.com/openapi.json
```

Result: Streamable HTTP server with OAuth 2.1 authentication

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
cookiecutter . --no-input deployment_type=local auth_mechanism=none

# Test with OpenAPI spec
cookiecutter . --no-input \
  openapi_spec_path="https://petstore3.swagger.io/api/v3/openapi.json" \
  deployment_type="remote" \
  server_port="9090"
```

## Documentation

- **[EXAMPLE.md](EXAMPLE.md)** - Complete walkthrough with real code examples
- **[USAGE.md](USAGE.md)** - Detailed usage guide for running from different locations
- **[TEST_GUIDE.md](TEST_GUIDE.md)** - Testing with Petstore API

## Testing Resources

Test your MCP Cookie Cutter template with these verified APIs that have OpenAPI 3.0 specifications:

### 1. **Swagger Petstore** ⭐ Recommended for Testing
- **OpenAPI Spec**: https://petstore3.swagger.io/api/v3/openapi.json
- **Base URL**: https://petstore3.swagger.io/api/v3
- **Auth**: None required
- **Resources**: Pets, Store, Users
- **Why**: Gold standard for API testing, fully functional, no auth needed

### 2. **JSONPlaceholder** - Simple & Free
- **OpenAPI Spec**: https://gist.githubusercontent.com/oshevtsov/7d17f88f74730ce9c95b6d7bb3e03c3d/raw/jsonplaceholder-openapi-3.0.yaml
- **Base URL**: https://jsonplaceholder.typicode.com
- **Auth**: None required
- **Resources**: Posts, Comments, Albums, Photos, Todos, Users
- **Why**: Free fake REST API, perfect for quick testing

### 3. **GitHub REST API** - Real-World Example
- **OpenAPI Spec**: https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json
- **Base URL**: https://api.github.com
- **Auth**: Optional (higher rate limits with token)
- **Resources**: Repos, Issues, Users, Pull Requests
- **Why**: Real production API, comprehensive operations
- **Note**: Very large spec (~15MB) - Pydantic model generation may fail, but tools will still be generated

### 4. **Stripe API** - Payment Processing
- **OpenAPI Spec**: https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json
- **Base URL**: https://api.stripe.com
- **Auth**: API Key (free test mode available)
- **Resources**: Payments, Customers, Products, Subscriptions
- **Why**: Well-documented, production-grade API

### 5. **APIs-guru Collection** - 300+ Public APIs
- **Repository**: https://github.com/APIs-guru/openapi-directory
- **Popular APIs**:
  - **OpenWeatherMap**: https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/openweathermap.org/2.5/openapi.yaml
  - **Spotify**: https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/spotify.com/openapi.yaml
  - **Twilio**: https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/twilio.com/openapi.yaml

### Quick Test Commands

**Test with Petstore (Recommended):**
```bash
cookiecutter . \
  project_name="petstore_server" \
  openapi_spec_path="https://petstore3.swagger.io/api/v3/openapi.json" \
  deployment_type="remote" \
  server_port="9090" \
  auth_mechanism="none"
```

**Test with JSONPlaceholder:**
```bash
cookiecutter . \
  project_name="jsonplaceholder_server" \
  openapi_spec_path="https://gist.githubusercontent.com/oshevtsov/7d17f88f74730ce9c95b6d7bb3e03c3d/raw/jsonplaceholder-openapi-3.0.yaml" \
  deployment_type="remote" \
  server_port="9090" \
  auth_mechanism="none"
```

**Test with GitHub API:**
```bash
# Note: GitHub API spec is very large, may take a minute to process
cookiecutter . \
  project_name="github_server" \
  openapi_spec_path="https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json" \
  deployment_type="remote" \
  server_port="9090" \
  auth_mechanism="api_key"
```

### Self-Hosted Testing Options

**Quick Docker Deploy - Petstore:**
```bash
docker run -d -p 8080:8080 swaggerapi/petstore3:unstable
# OpenAPI spec available at: http://localhost:8080/api/v3/openapi.json
```

**Prism Mock Server (Mock ANY OpenAPI spec):**
```bash
npm install -g @stoplight/prism-cli
prism mock https://petstore3.swagger.io/api/v3/openapi.json
# Creates a mock API server on http://localhost:4010
```

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [FastMCP Documentation](https://gofastmcp.com)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
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
git remote add origin https://github.com/maheshmahadevan/mcp-cookie-cutter.git
git push -u origin main

# Team members use:
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter
```

### Package Distribution

This package is available on PyPI for easy distribution:

```bash
# Anyone can use the template directly from GitHub
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter
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
