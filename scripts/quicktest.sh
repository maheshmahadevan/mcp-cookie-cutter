#!/bin/bash
# Quick test script for MCP Cookie Cutter with Petstore

set -e

echo "🚀 MCP Cookie Cutter - Petstore Quick Test"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if cookiecutter is installed
if ! command -v cookiecutter &> /dev/null; then
    echo "Installing cookiecutter..."
    # Try different package managers
    if command -v uv &> /dev/null; then
        uv pip install cookiecutter pyyaml
    elif command -v pip3 &> /dev/null; then
        pip3 install cookiecutter pyyaml
    elif command -v pip &> /dev/null; then
        pip install cookiecutter pyyaml
    elif command -v python3 &> /dev/null; then
        python3 -m pip install cookiecutter pyyaml
    elif command -v python &> /dev/null; then
        python -m pip install cookiecutter pyyaml
    elif command -v conda &> /dev/null; then
        conda install -y cookiecutter pyyaml
    else
        echo "Error: No package manager found"
        echo "Please install cookiecutter manually:"
        echo "  python3 -m pip install cookiecutter pyyaml"
        exit 1
    fi
fi

# Determine package manager
PACKAGE_MANAGER="pip"
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✓ uv detected${NC}"
    PACKAGE_MANAGER="uv"
else
    echo -e "${YELLOW}! uv not found, using pip (install uv for faster builds: pip install uv)${NC}"
fi

echo ""
echo -e "${BLUE}Generating Petstore MCP Server (Python, Local, No Auth)${NC}"
echo -e "${BLUE}Using package manager: ${PACKAGE_MANAGER}${NC}"
echo ""

# Run cookiecutter with default values
cookiecutter . --no-input \
    project_name="Petstore MCP Server" \
    project_description="MCP server for Swagger Petstore API" \
    author_name="Test User" \
    author_email="test@example.com" \
    openapi_spec_path="examples/petstore-swagger.json" \
    sdk_choice="python" \
    deployment_type="local" \
    auth_mechanism="none" \
    python_package_manager="$PACKAGE_MANAGER" \
    include_resources="no" \
    include_prompts="no" \
    license="MIT"

echo ""
echo -e "${GREEN}✓ Project generated!${NC}"
echo ""

cd petstore_mcp_server

if [ "$PACKAGE_MANAGER" = "uv" ]; then
    echo -e "${BLUE}Setting up with uv...${NC}"
    uv venv
    echo ""
    echo -e "${GREEN}✓ Setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. cd petstore_mcp_server"
    echo "  2. source .venv/bin/activate"
    echo "  3. uv pip install -e ."
    echo "  4. petstore_mcp_server"
    echo ""
    echo "Or use uv directly:"
    echo "  cd petstore_mcp_server && uv run petstore_mcp_server"
else
    echo -e "${BLUE}Setting up Python virtual environment...${NC}"
    python3 -m venv venv
    echo ""
    echo -e "${GREEN}✓ Setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. cd petstore_mcp_server"
    echo "  2. source venv/bin/activate"
    echo "  3. pip install -e ."
    echo "  4. petstore_mcp_server"
fi

echo ""
echo "Or run: ./run_petstore_test.sh"
