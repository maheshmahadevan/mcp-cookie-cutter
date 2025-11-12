#!/usr/bin/env python3
"""Command-line interface for MCP Cookie Cutter."""

import sys
from pathlib import Path
from cookiecutter.main import cookiecutter


def get_template_dir():
    """Get the path to the cookiecutter template directory.

    The template files are in the same directory as the package,
    not inside the package itself.
    """
    # Package is installed, template is at package root
    package_dir = Path(__file__).parent
    # Go up one level to find the template directory
    template_root = package_dir.parent

    # Check if we're in development mode (template files are alongside the package)
    if (template_root / "cookiecutter.json").exists():
        return str(template_root)

    # If installed via pip, the template should be in package_data
    # This is the installed location
    installed_template = package_dir / "template"
    if installed_template.exists():
        return str(installed_template)

    # Fallback: try to find it relative to the current location
    # This handles editable installs
    current_dir = Path.cwd()
    if (current_dir / "cookiecutter.json").exists():
        return str(current_dir)

    raise FileNotFoundError(
        "Could not find cookiecutter template. "
        "Please ensure mcp-cookie-cutter is properly installed."
    )


def main():
    """Main entry point for the mcp-cookie-cutter CLI."""
    try:
        template_dir = get_template_dir()

        # Pass any command-line arguments to cookiecutter
        # Users can do: mcp-cookie-cutter --no-input project_name="My Server"
        cookiecutter(template_dir)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
