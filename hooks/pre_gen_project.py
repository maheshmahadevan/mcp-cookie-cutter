#!/usr/bin/env python3
"""Pre-generation hook to validate inputs."""

import sys
import os

def validate_project_name():
    """Validate project name."""
    project_name = "{{ cookiecutter.project_name }}"

    if not project_name or project_name.strip() == "":
        print("Error: Project name cannot be empty")
        sys.exit(1)

def validate_deployment_auth_combo():
    """Validate deployment type and auth mechanism combination."""
    deployment = "{{ cookiecutter.deployment_type }}"
    auth = "{{ cookiecutter.auth_mechanism }}"

    if deployment == "remote" and auth == "none":
        print("\n⚠️  Warning: Remote deployment without authentication is not recommended for production.")
        print("Consider using API key or OAuth 2.1 for production deployments.\n")

    if deployment == "remote" and auth == "api_key":
        print("\nℹ️  Info: API key authentication selected.")
        print("For public clients, consider OAuth 2.1 for enhanced security.\n")

def show_openapi_info():
    """Show information about OpenAPI spec if provided."""
    openapi_spec_path = "{{ cookiecutter.openapi_spec_path }}"

    if openapi_spec_path:
        print(f"\n📋 OpenAPI Specification: {openapi_spec_path}")
        print("You'll need to customize the generated tools based on your API.")
        print("See CUSTOMIZATION.md in the generated project for details.\n")

def main():
    """Main pre-generation validation."""
    print("\n" + "="*70)
    print("🚀 MCP Cookie Cutter - Generating Your MCP Server")
    print("="*70)

    # Validate inputs
    validate_project_name()
    validate_deployment_auth_combo()
    show_openapi_info()

    print("✓ Input validation complete")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
