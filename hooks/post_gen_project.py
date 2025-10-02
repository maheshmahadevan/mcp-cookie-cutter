#!/usr/bin/env python3
"""Post-generation hook to set up the project."""

import os
import sys
import subprocess
from pathlib import Path

def setup_python_project():
    """Set up Python project dependencies."""
    print("\n📦 Setting up Python project...")

    package_manager = "{{ cookiecutter.python_package_manager }}"

    if package_manager == "uv":
        # Check if uv is available
        try:
            subprocess.run(["uv", "--version"], check=True, capture_output=True)
            print("Using uv for package management...")

            # Initialize uv project
            try:
                subprocess.run(["uv", "venv"], check=True)
                print("✓ Virtual environment created with uv")
            except subprocess.CalledProcessError as e:
                print(f"Warning: uv setup failed: {e}")
                print("\nTo set up manually, run:")
                print("  uv venv")
                print("  source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
                print("  uv pip install -e .")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: uv not found. Install with: pip install uv")
            print("Falling back to pip instructions...")
            package_manager = "pip"

    if package_manager == "pip":
        # Create virtual environment
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✓ Virtual environment created")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not create virtual environment: {e}")

        # Install dependencies
        print("\nTo install dependencies, run:")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("  pip install -e .")

def setup_typescript_project():
    """Set up TypeScript project dependencies."""
    print("\n📦 Setting up TypeScript project...")

    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: npm not found. Please install Node.js and npm.")
        return

    print("Installing dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True)
        print("✓ Dependencies installed")

        print("\nBuilding project...")
        subprocess.run(["npm", "run", "build"], check=True)
        print("✓ Project built")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Build step failed: {e}")
        print("\nTo install and build manually, run:")
        print("  npm install")
        print("  npm run build")

def cleanup_unused_files():
    """Remove files not needed for the selected configuration."""
    sdk_choice = "{{ cookiecutter.sdk_choice }}"
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"
    include_resources = "{{ cookiecutter.include_resources }}"
    include_prompts = "{{ cookiecutter.include_prompts }}"

    # Remove SDK-specific files
    if sdk_choice == "python":
        # Remove TypeScript files
        ts_files = ["package.json", "tsconfig.json", "src/index.ts", "src/tools.ts"]
        if include_resources == "yes":
            ts_files.append("src/resources.ts")
        if include_prompts == "yes":
            ts_files.append("src/prompts.ts")
        if auth_mechanism == "oauth2":
            ts_files.append("src/auth/oauth.ts")
        if auth_mechanism == "api_key":
            ts_files.append("src/auth/apiKey.ts")

        for file in ts_files:
            file_path = Path(file)
            if file_path.exists():
                file_path.unlink()

    elif sdk_choice == "typescript":
        # Remove Python files
        py_files = [
            "pyproject.toml",
            f"src/{{ cookiecutter.project_slug }}/server.py",
            f"src/{{ cookiecutter.project_slug }}/tools.py",
        ]
        if include_resources == "yes":
            py_files.append(f"src/{{ cookiecutter.project_slug }}/resources.py")
        if include_prompts == "yes":
            py_files.append(f"src/{{ cookiecutter.project_slug }}/prompts.py")
        if auth_mechanism == "oauth2":
            py_files.append(f"src/{{ cookiecutter.project_slug }}/auth/oauth.py")
        if auth_mechanism == "api_key":
            py_files.append(f"src/{{ cookiecutter.project_slug }}/auth/api_key.py")

        for file in py_files:
            file_path = Path(file)
            if file_path.exists():
                file_path.unlink()

    # Remove auth files if not needed
    if auth_mechanism == "none":
        auth_dir = Path("src/{{ cookiecutter.project_slug }}/auth" if sdk_choice == "python" else "src/auth")
        if auth_dir.exists():
            import shutil
            shutil.rmtree(auth_dir)

def create_env_template():
    """Create .env.example file if authentication is configured."""
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"

    if auth_mechanism == "api_key":
        env_content = """# API Key Configuration
# Add your API keys (comma-separated)
MCP_API_KEYS=your-api-key-here,another-key-here
"""
        with open(".env.example", "w") as f:
            f.write(env_content)
        print("✓ Created .env.example")

    elif auth_mechanism == "oauth2":
        env_content = """# OAuth 2.1 Configuration
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret  # Optional for public clients
OAUTH_ISSUER_URL=https://your-oauth-provider.com
"""
        with open(".env.example", "w") as f:
            f.write(env_content)
        print("✓ Created .env.example")

def print_next_steps():
    """Print next steps for the user."""
    sdk_choice = "{{ cookiecutter.sdk_choice }}"
    deployment_type = "{{ cookiecutter.deployment_type }}"
    auth_mechanism = "{{ cookiecutter.auth_mechanism }}"
    package_manager = "{{ cookiecutter.python_package_manager }}"
    openapi_spec_path = "{{ cookiecutter.openapi_spec_path }}"

    print("\n" + "="*70)
    print("🎉 MCP Server generated successfully!")
    print("="*70)

    print("\n📋 Next steps:\n")

    if openapi_spec_path:
        print("1. Customize your tools based on the OpenAPI spec:")
        print("   See CUSTOMIZATION.md for detailed guide")
        print("")

    if sdk_choice == "python":
        if package_manager == "uv":
            print("2. Activate the virtual environment:")
            print("   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
            print("\n3. Install dependencies:")
            print("   uv pip install -e .")
        else:
            print("2. Activate the virtual environment:")
            print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
            print("\n3. Install dependencies:")
            print("   pip install -e .")
    else:
        print("2. Install dependencies (if not already done):")
        print("   npm install")
        print("\n3. Build the project:")
        print("   npm run build")

    if auth_mechanism != "none":
        print(f"\n4. Configure authentication:")
        print("   cp .env.example .env")
        print("   # Edit .env with your credentials")

    print("\n5. Run the server:")
    if sdk_choice == "python":
        print("   {{ cookiecutter.project_slug }}")
    else:
        print("   npm start")

    if deployment_type == "local":
        print("\n6. Configure Claude Desktop:")
        print("   Add the server configuration to claude_desktop_config.json")
        print("   See README.md for details")

    print("\n📖 For more information:")
    print("   • README.md - Setup and usage guide")
    print("   • CUSTOMIZATION.md - How to add your API tools")
    print("\n" + "="*70)

def main():
    """Main post-generation setup."""
    print("\n🔧 Running post-generation setup...")

    sdk_choice = "{{ cookiecutter.sdk_choice }}"

    # Create environment template
    create_env_template()

    # Clean up unused files
    cleanup_unused_files()

    # SDK-specific setup
    if sdk_choice == "python":
        setup_python_project()
    elif sdk_choice == "typescript":
        setup_typescript_project()

    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
