# OpenAPI Dependencies Summary

## What Was Added

We've enhanced the MCP Cookie Cutter template with intelligent OpenAPI spec parsing capabilities.

### New Dependencies

Added to both `hook_requirements.txt` and `setup.py`:

1. **pyyaml>=6.0** - For parsing YAML OpenAPI specs
2. **requests>=2.31.0** - For fetching OpenAPI specs from URLs
3. **openapi-pydantic>=0.4.0** - For validating and parsing OpenAPI schemas

### Why These Dependencies?

#### Research from openapi-python-client

We researched how `openapi-python-client` (a popular OpenAPI code generator) handles parsing:

- Uses **openapi-pydantic** (formerly openapi-schema-pydantic) for OpenAPI parsing
- Leverages **Pydantic models** for type-safe spec validation
- Uses **ruamel.yaml** for YAML (we chose pyyaml as a lighter alternative)
- Built with **Jinja2** for code generation (same as cookiecutter)

#### Why openapi-pydantic?

We chose `openapi-pydantic` because:

1. **Type Safety** - Pydantic models provide full type hints
2. **Validation** - Automatically validates OpenAPI spec structure
3. **Active Maintenance** - Supports both Pydantic 1.8+ and 2.x
4. **OpenAPI Native** - Specifically designed for OpenAPI 3.0/3.1 specs
5. **Industry Standard** - Used by major projects like openapi-python-client
6. **Modern Fork** - Actively maintained fork of openapi-schema-pydantic

## How It Works

### Pre-Generation Hook Enhancement

The `hooks/pre_gen_project.py` file now:

1. **Loads OpenAPI specs** from files or URLs
2. **Validates specs** using openapi-pydantic (if available)
3. **Extracts API operations** (GET, POST, PUT, DELETE, PATCH)
4. **Displays tool suggestions** showing available endpoints

### Graceful Degradation

The system works with or without optional dependencies:

| Dependency | If Missing | Impact |
|------------|-----------|--------|
| requests | Warning shown | Cannot fetch from URLs, local files still work |
| pyyaml | Warning shown | Cannot parse YAML, JSON still works |
| openapi-pydantic | Silent fallback | No validation, basic parsing works |
| All | No error | Template generation works, no OpenAPI parsing |

## Installation

### For Users

```bash
# Install all dependencies
pip install cookiecutter pyyaml requests openapi-pydantic

# Or minimal install
pip install cookiecutter
# OpenAPI parsing will be limited but generation works
```

### For Development

```bash
# Install from setup.py
pip install -e .

# Or install hook requirements
pip install -r hook_requirements.txt
```

## Testing

### Test OpenAPI Parsing

```bash
# Test with Petstore API
cd /tmp
cookiecutter /path/to/mcp-cookie-cutter --no-input \
  openapi_spec_path="https://petstore.swagger.io/v2/swagger.json"
```

Expected output:
```
📋 OpenAPI Specification: https://petstore.swagger.io/v2/swagger.json

✨ Found 20 available API operations:
----------------------------------------------------------------------
 1. POST   /pet                           - addPet
     Add a new pet to the store
 2. GET    /pet/{petId}                   - getPetById
     Find pet by ID
...
----------------------------------------------------------------------
```

### Test Without Dependencies

```bash
# Uninstall optional deps
pip uninstall pyyaml requests openapi-pydantic -y

# Should still work with warnings
cookiecutter /path/to/mcp-cookie-cutter --no-input
```

## Benefits

1. **See Available Tools** - Instantly know which API operations exist
2. **Plan Implementation** - Understand what to build before coding
3. **Save Time** - No manual OpenAPI spec browsing
4. **Type Safety** - Validation catches malformed specs early
5. **Flexibility** - Works with or without all dependencies

## Files Modified

1. `hook_requirements.txt` - Added pyyaml, requests, openapi-pydantic
2. `setup.py` - Added same dependencies to install_requires
3. `hooks/pre_gen_project.py` - Added OpenAPI parsing logic
4. `README.md` - Updated installation and features sections
5. `OPENAPI_PARSING.md` - Created comprehensive documentation

## Future Enhancements (V1.0)

The V1.0 standalone CLI will use these same dependencies to:

1. **Interactive selection** - Choose which operations to implement
2. **Automatic code generation** - Generate tool implementations
3. **Smart parameter mapping** - Convert OpenAPI params to MCP schemas
4. **Auth detection** - Auto-configure based on security schemes
5. **Response formatting** - Generate proper response handlers

## References

- [openapi-python-client](https://github.com/openapi-generators/openapi-python-client) - Inspiration for parsing approach
- [openapi-pydantic](https://pypi.org/project/openapi-pydantic/) - OpenAPI parsing library
- [pyyaml](https://pypi.org/project/PyYAML/) - YAML parsing
- [requests](https://pypi.org/project/requests/) - HTTP client
