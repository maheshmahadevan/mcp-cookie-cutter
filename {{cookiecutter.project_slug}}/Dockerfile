{% if cookiecutter.sdk_choice == 'python' -%}
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv pip install --system -e .

# Expose port for remote deployment
{% if cookiecutter.deployment_type == 'remote' -%}
EXPOSE {{ cookiecutter.server_port }}
{% endif -%}

# Run the server (FastMCP handles transport internally)
CMD ["{{ cookiecutter.project_slug }}"]
{% else -%}
FROM node:20-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build TypeScript
RUN npm run build

# Expose port for remote deployment
{% if cookiecutter.deployment_type == 'remote' -%}
EXPOSE {{ cookiecutter.server_port }}
{% endif -%}

# Run the server
CMD ["npm", "start"]
{% endif -%}
