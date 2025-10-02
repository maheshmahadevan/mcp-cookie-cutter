#!/bin/bash
# Run the generated Petstore MCP server

set -e

echo "🏃 Running Petstore MCP Server"
echo "=============================="

if [ ! -d "petstore_mcp_server" ]; then
    echo "Error: petstore_mcp_server directory not found"
    echo "Run ./quicktest.sh first to generate the project"
    exit 1
fi

cd petstore_mcp_server

# Check if uv is available and .venv exists (uv project)
if command -v uv &> /dev/null && [ -d ".venv" ]; then
    echo "Using uv..."

    # Install dependencies if needed
    if [ ! -f ".venv/bin/petstore_mcp_server" ]; then
        echo "Installing dependencies with uv..."
        source .venv/bin/activate
        uv pip install -e . > /dev/null 2>&1
        echo "✓ Dependencies installed"
    fi

    echo ""
    echo "🚀 Starting Petstore MCP Server (uv)..."
    echo "   Press Ctrl+C to stop"
    echo ""

    # Run with uv
    uv run petstore_mcp_server

# Otherwise use pip/venv
else
    # Activate virtual environment
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    echo "Activating virtual environment..."
    source venv/bin/activate

    # Install dependencies
    if [ ! -f "venv/bin/petstore_mcp_server" ]; then
        echo "Installing dependencies..."
        pip install -e . > /dev/null 2>&1
        echo "✓ Dependencies installed"
    fi

    echo ""
    echo "🚀 Starting Petstore MCP Server (pip)..."
    echo "   Press Ctrl+C to stop"
    echo ""

    # Run the server
    petstore_mcp_server
fi
