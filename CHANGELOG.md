# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **CLI tool support** - Install as `pip install mcp-cookie-cutter` and use `mcp-cookie-cutter` command
- Command-line interface entry point (`mcp_cookie_cutter.cli:main`)
- PyPI packaging support with modern `pyproject.toml`
- Comprehensive PUBLISHING.md documentation for PyPI releases
- CHANGELOG.md for version tracking
- MIT LICENSE file
- MANIFEST.in for proper package distribution
- mcp_cookie_cutter Python package with CLI module

### Changed
- Updated README.md with CLI usage examples and correct repository URLs
- Enhanced installation instructions with CLI tool option and PyPI workflow
- Updated pyproject.toml with [project.scripts] entry point

## [0.1.0] - 2025-11-10

### Added
- Initial release of MCP Cookie Cutter
- Cookiecutter template for MCP server generation
- OpenAPI/Swagger automatic parsing and tool generation
- FastMCP framework integration
- Support for local (STDIO) and remote (HTTP/SSE) deployments
- Authentication templates (None, API Key, OAuth 2.1)
- Auto-generation of tools, prompts, and Pydantic models
- Interactive tool selection during project generation
- Pre-generation and post-generation hooks
- Comprehensive documentation:
  - README.md with quick start guide
  - EXAMPLE.md with complete walkthrough
  - USAGE.md for different deployment scenarios
  - TEST_GUIDE.md for Petstore API testing
  - OPENAPI_PARSING.md for OpenAPI integration details
  - CUSTOMIZATION.md in generated projects
- Example OpenAPI specifications for testing
- Docker and docker-compose support in generated projects
- Development testing with auto-reload
- Environment variable configuration

### Features
- **Template Variables**:
  - Project name and description
  - Author information
  - OpenAPI spec path (URL or local file)
  - Deployment type (local/remote)
  - Server port configuration
  - Authentication mechanism selection
  - License selection (MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, Proprietary)

- **OpenAPI Integration**:
  - JSON and YAML format support
  - OpenAPI 3.0/3.1 and Swagger 2.0 compatibility
  - Automatic endpoint discovery
  - Operation metadata extraction
  - Interactive tool selection
  - Pydantic model generation

- **Generated Project Features**:
  - FastMCP server with auto-discovery
  - Individual tool files for each operation
  - Auto-generated prompts from API operations
  - Pydantic models from OpenAPI schemas
  - Docker containerization
  - Environment-based configuration
  - Type hints and validation
  - Proper logging (stderr for STDIO compliance)

### Dependencies
- cookiecutter>=2.1.0
- pyyaml>=6.0
- requests>=2.31.0
- openapi-pydantic>=0.4.0
- datamodel-code-generator>=0.25.0

### Known Issues
- Jinja2 template parsing conflicts with complex embedded Python code (workaround implemented)
- Interactive tool selection only works in terminal mode, not with `--no-input` flag
- Very large OpenAPI specs (e.g., GitHub API ~15MB) may cause Pydantic model generation to fail, though tools will still be generated

[Unreleased]: https://github.com/maheshmahadevan/mcp-cookie-cutter/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/maheshmahadevan/mcp-cookie-cutter/releases/tag/v0.1.0
