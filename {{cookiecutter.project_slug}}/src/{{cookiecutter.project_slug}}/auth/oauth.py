{% if cookiecutter.sdk_choice == 'python' and cookiecutter.auth_mechanism == 'oauth2' -%}
"""OAuth 2.1 authentication handler."""

import logging
from typing import Optional
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

logger = logging.getLogger(__name__)


class OAuthHandler:
    """OAuth 2.1 authentication handler following MCP best practices."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        authorization_endpoint: Optional[str] = None,
        token_endpoint: Optional[str] = None,
    ):
        """Initialize OAuth handler.

        Args:
            client_id: OAuth client ID
            client_secret: OAuth client secret (use PKCE for public clients)
            authorization_endpoint: OAuth authorization URL
            token_endpoint: OAuth token URL
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint

        # Initialize OAuth client
        self.oauth = OAuth()
        if client_id:
            self.oauth.register(
                name='mcp_provider',
                client_id=client_id,
                client_secret=client_secret,
                authorize_url=authorization_endpoint,
                access_token_url=token_endpoint,
                client_kwargs={'scope': 'openid profile email'},
            )

    async def authenticate(self, request: Request) -> bool:
        """Authenticate incoming request.

        Args:
            request: Starlette request object

        Returns:
            True if authenticated, False otherwise
        """
        # Extract bearer token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            logger.warning("Missing or invalid Authorization header")
            return False

        token = auth_header[7:]  # Remove 'Bearer ' prefix

        try:
            # Verify token (implement your token verification logic)
            # This could involve introspection endpoint or JWT validation
            await self._verify_token(token)
            return True
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return False

    async def _verify_token(self, token: str) -> None:
        """Verify OAuth token.

        Args:
            token: Bearer token to verify

        Raises:
            ValueError: If token is invalid
        """
        # Implement token verification logic here
        # Options:
        # 1. Call OAuth provider's introspection endpoint
        # 2. Validate JWT signature if using JWT tokens
        # 3. Check token against local cache/database
        pass

    def get_authorization_url(self) -> str:
        """Get OAuth authorization URL for user consent.

        Returns:
            Authorization URL for user to grant consent
        """
        if not self.authorization_endpoint:
            raise ValueError("Authorization endpoint not configured")

        # Build authorization URL with PKCE for public clients
        # This should be called from your UI to redirect users
        return f"{self.authorization_endpoint}?client_id={self.client_id}&response_type=code&scope=openid"
{%- endif %}
