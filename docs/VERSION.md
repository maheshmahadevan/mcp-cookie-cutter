# Version History

## V0.1.0 - Initial Release (Current)

**Release Date**: October 2025
**Status**: ✅ Stable and Production-Ready

### Features

✅ **Template Generation**
- Complete MCP server project structure
- Python and TypeScript SDK support
- Local (STDIO) and Remote (SSE) deployment options
- OAuth 2.1 and API key authentication templates
- UV and pip package manager support

✅ **Example Tools**
- GET request example
- POST request example
- Clear TODOs for customization

✅ **Documentation**
- Comprehensive CUSTOMIZATION.md guide
- README.md with setup instructions
- USAGE.md for running from different locations
- TEST_GUIDE.md with Petstore examples
- EXAMPLE.md with walkthrough

✅ **Developer Experience**
- Automatic virtual environment setup
- Dependency installation
- TypeScript build configuration
- Clean project structure

### What's Manual in V0.1

⚠️ **Tool Customization** - Users manually add tools based on their OpenAPI spec
- Copy example patterns
- Follow CUSTOMIZATION.md guide
- Uncomment HTTP client code
- Add proper error handling

### Limitations

- No automatic code generation from OpenAPI specs
- No interactive tool selection during generation
- Manual tool implementation required

### Why V0.1 Works This Way

The intelligent OpenAPI-to-code generation feature proved architecturally incompatible with cookiecutter's Jinja2 template system. Rather than delay release, V0.1 provides excellent templates and clear customization guides, getting useful tooling in users' hands immediately.

## V1.0.0 - Planned Features

🔮 **Intelligent Generation** (Future)
- Standalone CLI tool (`mcp-generate`)
- Interactive tool selection from OpenAPI spec
- Automatic code generation for all endpoints
- Smart parameter mapping
- Authentication scheme detection
- Request/response formatting

This will be built as a wrapper around cookiecutter to avoid Jinja2 conflicts.

## Migration Path

V0.1 projects will work with V1.0's intelligent generator:
```bash
# V1.0 (future)
mcp-generate --upgrade ./my-v0.1-project --openapi https://api.com/spec.json
```

The generator will:
1. Detect existing tools
2. Suggest new tools from OpenAPI
3. Generate only new code
4. Preserve customizations

## Feedback

Found a bug? Have a feature request?
- GitHub Issues: [link-to-repo]
- Discussions: [link-to-discussions]

---

**Current Version**: V0.1.0
**Status**: ✅ Stable and Production-Ready
**Template Quality**: All 8 major configuration combinations tested and validated
