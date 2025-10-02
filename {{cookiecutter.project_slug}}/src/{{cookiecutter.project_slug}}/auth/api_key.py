{% if cookiecutter.sdk_choice == 'python' and cookiecutter.auth_mechanism == 'api_key' -%}
"""API Key authentication handler."""

import logging
import os
from typing import Optional, Set
from starlette.requests import Request
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class APIKeyHandler:
    """API Key authentication handler.

    Note: API keys are simpler but less secure than OAuth 2.1.
    Use OAuth 2.1 for public clients when possible.
    """

    def __init__(self, valid_keys: Optional[Set[str]] = None):
        """Initialize API key handler.

        Args:
            valid_keys: Set of valid API keys. If None, loads from environment.
        """
        if valid_keys is None:
            # Load API keys from environment variable
            api_keys_str = os.getenv('MCP_API_KEYS', '')
            self.valid_keys = set(key.strip() for key in api_keys_str.split(',') if key.strip())
        else:
            self.valid_keys = valid_keys

        if not self.valid_keys:
            logger.warning("No API keys configured. All requests will be rejected.")

    async def authenticate(self, request: Request) -> bool:
        """Authenticate incoming request using API key.

        Supports two methods:
        1. Authorization header: Authorization: Bearer <api_key>
        2. Query parameter: ?api_key=<api_key>

        Args:
            request: Starlette request object

        Returns:
            True if authenticated, False otherwise
        """
        # Try Authorization header first
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            api_key = auth_header[7:]  # Remove 'Bearer ' prefix
            if api_key in self.valid_keys:
                logger.info("Request authenticated via Authorization header")
                return True

        # Try query parameter
        api_key = request.query_params.get('api_key')
        if api_key and api_key in self.valid_keys:
            logger.info("Request authenticated via query parameter")
            return True

        # Try custom header
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key in self.valid_keys:
            logger.info("Request authenticated via X-API-Key header")
            return True

        logger.warning("Authentication failed: Invalid or missing API key")
        return False

    def add_key(self, api_key: str) -> None:
        """Add a new valid API key.

        Args:
            api_key: API key to add
        """
        self.valid_keys.add(api_key)
        logger.info("New API key added")

    def revoke_key(self, api_key: str) -> None:
        """Revoke an API key.

        Args:
            api_key: API key to revoke
        """
        self.valid_keys.discard(api_key)
        logger.info("API key revoked")
{%- endif %}
