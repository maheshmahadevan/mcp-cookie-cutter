"""Setup script to install MCP Cookie Cutter as a Python package."""

from setuptools import setup, find_packages

setup(
    name="mcp-cookie-cutter",
    version="0.1.0",
    description="Intelligent MCP server generator from OpenAPI/Swagger specs",
    author="MCP Cookie Cutter Contributors",
    python_requires=">=3.10",
    install_requires=[
        "cookiecutter>=2.1.0",
        "pyyaml>=6.0",
    ],
    packages=find_packages(),
    package_data={
        "": ["*"],
    },
    include_package_data=True,
    zip_safe=False,
)
