"""
Backward compatibility setup.py

This file is kept for backward compatibility.
All package configuration is now in pyproject.toml (PEP 517/518).

For modern installations, use:
    pip install .

For development installations, use:
    pip install -e .
"""

from setuptools import setup

# All configuration is in pyproject.toml
setup()
