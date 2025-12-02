"""Authentication handling for A7 SDK."""

from typing import Generator

import httpx


class BearerAuth(httpx.Auth):
    """Bearer token authentication for httpx."""

    def __init__(self, token: str) -> None:
        """
        Initialize Bearer authentication.

        Args:
            token: API token (with or without 'Bearer ' prefix)
        """
        # Ensure token has Bearer prefix
        if token.startswith("Bearer "):
            self.token = token
        else:
            self.token = f"Bearer {token}"

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """
        Add Authorization header to request.

        Args:
            request: The HTTP request

        Yields:
            Request with Authorization header
        """
        request.headers["Authorization"] = self.token
        yield request
