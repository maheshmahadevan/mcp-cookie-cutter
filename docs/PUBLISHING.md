# Publishing to PyPI

This guide explains how to publish the MCP Cookie Cutter package to PyPI (Python Package Index).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [One-Time Setup](#one-time-setup)
3. [Building the Package](#building-the-package)
4. [Testing the Build](#testing-the-build)
5. [Publishing to Test PyPI](#publishing-to-test-pypi)
6. [Publishing to PyPI](#publishing-to-pypi)
7. [Versioning](#versioning)
8. [Automated Publishing with GitHub Actions](#automated-publishing-with-github-actions)

## Prerequisites

- Python 3.10 or higher
- An account on [PyPI](https://pypi.org/) and [Test PyPI](https://test.pypi.org/)
- API tokens for PyPI and Test PyPI (recommended over username/password)

## One-Time Setup

### 1. Install Build Tools

```bash
pip install --upgrade pip
pip install build twine
```

### 2. Create PyPI Accounts

1. **Test PyPI** (for testing): https://test.pypi.org/account/register/
2. **PyPI** (production): https://pypi.org/account/register/

### 3. Generate API Tokens

#### For PyPI:
1. Log in to https://pypi.org/
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name it (e.g., "mcp-cookie-cutter-release")
5. Scope: "Entire account" (or specific to this project after first upload)
6. Copy the token (starts with `pypi-`)

#### For Test PyPI:
1. Log in to https://test.pypi.org/
2. Follow the same steps as above

### 4. Configure Your Credentials

Create a `~/.pypirc` file (see `.pypirc.example` in this repo):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

**Important**: Never commit `.pypirc` to version control!

## Building the Package

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info
```

### 2. Update Version

Edit `pyproject.toml` and update the version number:

```toml
[project]
version = "0.2.0"  # Update this
```

### 3. Update CHANGELOG

Update `CHANGELOG.md` with changes in this release:

```markdown
## [0.2.0] - 2025-11-XX

### Added
- New feature description

### Changed
- What changed

### Fixed
- Bug fixes
```

### 4. Build the Distribution

```bash
# Build both source distribution and wheel
python -m build
```

This creates:
- `dist/mcp-cookie-cutter-0.2.0.tar.gz` (source distribution)
- `dist/mcp_cookie_cutter-0.2.0-py3-none-any.whl` (wheel)

## Testing the Build

### 1. Check the Distribution

```bash
# Check for common issues
twine check dist/*
```

### 2. Inspect Contents

```bash
# View contents of the source distribution
tar -tzf dist/mcp-cookie-cutter-*.tar.gz

# View contents of the wheel
unzip -l dist/mcp_cookie_cutter-*.whl
```

Verify that:
- All template files are included (`{{cookiecutter.project_slug}}/`)
- Hook files are included (`hooks/`)
- Documentation is included (`README.md`, `CHANGELOG.md`, etc.)
- Examples are included (`examples/`)

### 3. Test Local Installation

```bash
# Create a test virtual environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install from the built wheel
pip install dist/mcp_cookie_cutter-*.whl

# Test that it works
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter --version

# Or test with the package directly
python -c "import pkg_resources; print(pkg_resources.get_distribution('mcp-cookie-cutter').version)"

# Clean up
deactivate
rm -rf test-env
```

## Publishing to Test PyPI

Always test on Test PyPI first!

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*
```

### Test the Installation from Test PyPI

```bash
# Create a fresh virtual environment
python -m venv test-testpypi
source test-testpypi/bin/activate

# Install from Test PyPI (with dependencies from PyPI)
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    mcp-cookie-cutter

# Test it works
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter --help

# Test generating a project
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter --no-input

# Clean up
deactivate
rm -rf test-testpypi
```

## Publishing to PyPI

Once you've verified everything works on Test PyPI:

### 1. Tag the Release

```bash
# Create a git tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

### 2. Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

### 3. Verify on PyPI

1. Visit https://pypi.org/project/mcp-cookie-cutter/
2. Check the version, description, and metadata
3. Verify the README renders correctly

### 4. Test Installation

```bash
# Install from PyPI
pip install mcp-cookie-cutter

# Test it works
cookiecutter gh:maheshmahadevan/mcp-cookie-cutter --help
```

### 5. Create GitHub Release

1. Go to https://github.com/maheshmahadevan/mcp-cookie-cutter/releases
2. Click "Draft a new release"
3. Select the tag you created (v0.2.0)
4. Title: "v0.2.0"
5. Description: Copy from CHANGELOG.md
6. Attach the distribution files (optional)
7. Publish release

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): Add functionality in a backwards compatible manner
- **PATCH** version (0.0.X): Backwards compatible bug fixes

### Version Update Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with changes
- [ ] Update any version references in documentation
- [ ] Commit changes: `git commit -m "Bump version to X.Y.Z"`
- [ ] Create git tag: `git tag -a vX.Y.Z -m "Release version X.Y.Z"`
- [ ] Push changes: `git push && git push --tags`

## Automated Publishing with GitHub Actions

You can automate PyPI publishing with GitHub Actions. Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest

    permissions:
      id-token: write  # For trusted publishing

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install build tools
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Check package
      run: twine check dist/*

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

### Setup for GitHub Actions

1. Go to your GitHub repository settings
2. Navigate to Secrets and variables → Actions
3. Add a new repository secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token (from PyPI account settings)

Now, whenever you create a new release on GitHub, it will automatically publish to PyPI!

### Alternative: Trusted Publishing (Recommended)

PyPI supports "trusted publishing" which doesn't require API tokens:

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new trusted publisher:
   - PyPI Project Name: `mcp-cookie-cutter`
   - Owner: `maheshmahadevan`
   - Repository name: `mcp-cookie-cutter`
   - Workflow name: `publish.yml`
   - Environment name: (leave blank or specify if using environments)

Then update the workflow to use trusted publishing:

```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  # No password needed with trusted publishing!
```

## Troubleshooting

### Package Already Exists

If you get an error that the version already exists on PyPI:
1. You cannot overwrite a version on PyPI (by design)
2. Increment the version number
3. Rebuild and upload again

### Missing Files in Distribution

If template files are missing:
1. Check `MANIFEST.in` includes the correct patterns
2. Verify `pyproject.toml` has correct `package-data` configuration
3. Rebuild the package
4. Use `tar -tzf dist/*.tar.gz` to verify contents

### Import Errors After Installation

If users can't import the package:
1. Verify the package structure in `pyproject.toml`
2. Ensure `__init__.py` files exist where needed
3. Check that `find_packages()` or manual package list is correct

### Authentication Errors

If upload fails with authentication errors:
1. Verify your API token is correct
2. Ensure `~/.pypirc` has the correct format
3. Try deleting and regenerating the API token
4. Make sure the token has the right scope (entire account or specific project)

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)
- [PEP 517: Build System](https://peps.python.org/pep-0517/)
- [PEP 518: pyproject.toml](https://peps.python.org/pep-0518/)

## Quick Reference

```bash
# Complete release process
rm -rf build/ dist/ *.egg-info
# Update version in pyproject.toml
# Update CHANGELOG.md
python -m build
twine check dist/*
twine upload --repository testpypi dist/*  # Test first
twine upload dist/*  # Production
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```
