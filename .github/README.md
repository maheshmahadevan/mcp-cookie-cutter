# GitHub Workflows

## Automated Testing Workflow (`test.yml`)

This repository includes a comprehensive GitHub Actions workflow for automated testing of the MCP Cookie Cutter template.

### What Gets Tested

The CI/CD pipeline runs automatically on:
- Push to `main`, `develop`, or `claude/**` branches
- Pull requests to `main` or `develop` branches
- Manual workflow dispatch

### Test Jobs

#### 1. **Template Generation Tests**
Tests across Python 3.10, 3.11, and 3.12:
- ✅ Basic template generation (no OpenAPI spec)
- ✅ Petstore API generation (JSON Swagger 2.0)
- ✅ Cat API generation (YAML OpenAPI 3.0)
- ✅ OpenWeather API generation (JSON with remote deployment)
- ✅ Multi-Auth API generation (OAuth 2.1)
- ✅ Remote deployment configuration (Docker/docker-compose)
- ✅ Package installation and import verification

#### 2. **Hook Tests**
- ✅ Pre-generation hook (OpenAPI parsing)
- ✅ Post-generation hook (project setup)
- ✅ Hook dependency validation

#### 3. **Lint and Format Check**
- ✅ Black formatting check (non-blocking)
- ✅ Ruff linting (non-blocking)

#### 4. **Example Validation**
- ✅ OpenAPI spec validation for all examples
- ✅ JSON/YAML parsing tests

### Running Tests Locally

You can run the same tests locally before pushing:

```bash
# Install dependencies
pip install cookiecutter
pip install -r hook_requirements.txt

# Test basic generation
cookiecutter . --no-input project_name="test_server"

# Test with Petstore API
cookiecutter . --no-input \
  project_name="test_petstore" \
  openapi_spec_path="examples/petstore-swagger.json"

# Verify generated project
cd test_petstore
uv venv && source .venv/bin/activate
uv pip install -e .
python -c "import test_petstore"
```

### Viewing Test Results

1. Navigate to the **Actions** tab in GitHub
2. Select the **MCP Cookie Cutter CI** workflow
3. View test results for each job and step

### Badge Status

Add this badge to your README to show CI status:

```markdown
[![CI Status](https://github.com/YOUR_USERNAME/mcp-cookie-cutter/workflows/MCP%20Cookie%20Cutter%20CI/badge.svg)](https://github.com/YOUR_USERNAME/mcp-cookie-cutter/actions)
```

### Troubleshooting

**Common Issues:**

1. **Template generation fails**: Check that `cookiecutter.json` is valid
2. **Hook errors**: Verify `hook_requirements.txt` dependencies are installed
3. **Import failures**: Ensure generated `pyproject.toml` includes all required dependencies
4. **YAML parsing errors**: Validate OpenAPI specs with `openapi-spec-validator`

**Debug locally:**

```bash
# Enable verbose output
cookiecutter . --no-input --verbose

# Test hooks directly
cd hooks
python pre_gen_project.py
```

### Contributing

When adding new features:
1. Ensure tests still pass locally
2. Add new test cases to `test.yml` for new functionality
3. Update this README if changing workflow behavior
4. Linting/formatting checks are non-blocking but recommended to pass
