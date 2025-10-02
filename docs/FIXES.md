# Template Indentation Fixes

## Issue
The Python server.py template had indentation problems caused by Jinja2 template directives not preserving proper Python indentation.

## Problems Fixed

### 1. Authentication Handler Indentation (Lines 52-56)
**Problem**: The `{%- endif -%}` directive was consuming newlines, causing the auth handler initialization to lose indentation.

**Before**:
```jinja2
self.server = Server("{{ cookiecutter.project_slug }}")
{% if cookiecutter.auth_mechanism == 'oauth2' -%}
        self.auth_handler = OAuthHandler()
{% elif cookiecutter.auth_mechanism == 'api_key' -%}
        self.auth_handler = APIKeyHandler()
{% endif -%}
```

**After**:
```jinja2
self.server = Server("{{ cookiecutter.project_slug }}")
{%- if cookiecutter.auth_mechanism == 'oauth2' %}
        self.auth_handler = OAuthHandler()
{%- elif cookiecutter.auth_mechanism == 'api_key' %}
        self.auth_handler = APIKeyHandler()
{%- endif %}
```

**Fix**: Changed from `-%}` to `%}` on the if/elif statements and moved the `-` to the closing tag (`{%-`).

### 2. Resource Registration Indentation (Lines 65-69)
**Problem**: Conditional blocks for optional resources were creating inconsistent spacing.

**Before**:
```jinja2
{% if cookiecutter.include_resources == 'yes' -%}
        # Register resources
        register_resources(self.server)
{% endif -%}
```

**After**:
```jinja2
{% if cookiecutter.include_resources == 'yes' %}

        # Register resources
        register_resources(self.server)
{%- endif %}
```

**Fix**: Added explicit blank line and moved `-` to closing tag to control whitespace better.

### 3. Prompt Registration Indentation (Lines 70-74)
Same fix as resources registration.

### 4. Deployment Type Methods (Lines 83-127)
**Problem**: The local vs remote deployment blocks had inconsistent whitespace stripping.

**Before**:
```jinja2
{% if cookiecutter.deployment_type == 'local' -%}
    async def run(self):
...
{% else -%}
    def create_app(self) -> Starlette:
...
{% endif -%}
```

**After**:
```jinja2
{% if cookiecutter.deployment_type == 'local' %}
    async def run(self):
...
{%- else %}
    def create_app(self) -> Starlette:
...
{%- endif %}
```

**Fix**: Consistent use of `{%-` on closing/else tags only.

### 5. Authentication Check in SSE Handler (Lines 98-103)
**Problem**: Extra blank line when auth is enabled.

**Fixed**: Adjusted whitespace control to prevent extra newlines.

## Testing Results

All 8 major configuration combinations now generate valid Python syntax:

```
✓ local + none + no resources/prompts
✓ local + none + resources + prompts
✓ remote + api_key + no resources/prompts
✓ remote + api_key + resources + prompts
✓ remote + oauth2 + prompts only
✓ remote + oauth2 + resources only
✓ remote + none + resources + prompts
✓ local + api_key + resources only
```

## Jinja2 Whitespace Control Rules Used

- `{%-` strips whitespace **before** the tag
- `-%}` strips whitespace **after** the tag
- Use `{%-` on closing tags (`endif`, `else`) to prevent extra blank lines
- Use plain `%}` on opening tags to preserve indentation
- Explicitly add blank lines in template where needed for readability

## Files Modified

- `{{cookiecutter.project_slug}}/src/{{cookiecutter.project_slug}}/server.py`

## Validation

All generated Python files now pass:
- `python3 -m py_compile` (syntax check)
- `ast.parse()` (AST validation)
