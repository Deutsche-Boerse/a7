"""Main A7 client class."""

import os
from typing import Any
from urllib.parse import urlparse

import httpx

from a7.auth import BearerAuth
from a7.config import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
from a7.errors import (
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from a7.resources.algo import AlgoResource
from a7.resources.auction import AuctionResource
from a7.resources.dataset import DatasetResource
from a7.resources.eobi import EOBIResource
from a7.resources.insights import InsightsResource
from a7.resources.mdp import MDPResource
from a7.resources.orderbook import OrderBookResource
from a7.resources.precalc import PrecalcResource
from a7.resources.rdi import RDIResource
from a7.resources.sd import SDResource


def _should_bypass_proxy(url: str) -> bool:
    """
    Check if URL should bypass proxy based on NO_PROXY environment variable.

    Args:
        url: The URL to check

    Returns:
        True if proxy should be bypassed for this URL
    """
    no_proxy = os.getenv("NO_PROXY", os.getenv("no_proxy", ""))
    if not no_proxy:
        return False

    if no_proxy == "*":
        return True

    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    # Check each no_proxy pattern
    for raw_pattern in no_proxy.split(","):
        pattern = raw_pattern.strip()
        if not pattern:
            continue

        # Check if pattern matches
        if pattern.startswith("."):
            # Domain suffix match
            if hostname.endswith(pattern) or hostname.endswith(pattern[1:]):
                return True
        elif pattern == hostname:
            # Exact match
            return True
        elif hostname.endswith(f".{pattern}"):
            # Subdomain match
            return True

    return False


class A7Client:
    """
    Main client for A7 Analytics Platform API.

    Example:
        >>> client = A7Client(token="YOUR_A7_TOKEN")
        >>> markets = client.rdi.get_markets()
    """

    def __init__(
        self,
        token: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        verify_ssl: bool = True,
    ) -> None:
        """
        Initialize A7 client.

        Args:
            token: A7 API token (with or without 'Bearer ' prefix)
            base_url: Base URL for A7 API (default: production URL)
            timeout: Request timeout in seconds (default: 30.0)
            verify_ssl: Whether to verify SSL certificates (default: True)
                       Set to False for self-signed certificates in dev environments
        """
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

        # Determine transport settings based on NO_PROXY environment variable
        transport = None
        if _should_bypass_proxy(base_url):
            # Explicitly disable proxies for this URL by using custom transport
            transport = httpx.HTTPTransport(verify=verify_ssl, proxy=None)

        # Initialize HTTP client with authentication
        self._client = httpx.Client(
            auth=BearerAuth(token),
            base_url=self._base_url,
            timeout=timeout,
            headers={"User-Agent": USER_AGENT},
            verify=verify_ssl,
            transport=transport,
        )

        # Initialize resource endpoints
        self.rdi = RDIResource(self._client)
        self.algo = AlgoResource(self._client)
        self.eobi = EOBIResource(self._client)
        self.mdp = MDPResource(self._client)
        self.orderbook = OrderBookResource(self._client)
        self.dataset = DatasetResource(self._client)
        self.insights = InsightsResource(self._client)
        self.precalc = PrecalcResource(self._client)
        self.auction = AuctionResource(self._client)
        self.sd = SDResource(self._client)

    def _handle_error(self, error: httpx.HTTPStatusError) -> None:
        """
        Handle HTTP errors and raise appropriate custom exceptions.

        Args:
            error: HTTP status error from httpx

        Raises:
            AuthenticationError: For 401 status
            ForbiddenError: For 403 status
            NotFoundError: For 404 status
            ValidationError: For 400 status
            RateLimitError: For 429 status
            ServerError: For 5xx status
        """
        status_code = error.response.status_code
        message = f"HTTP {status_code}: {error.response.text}"

        if status_code == 401:
            raise AuthenticationError(message)
        elif status_code == 403:
            raise ForbiddenError(message)
        elif status_code == 404:
            raise NotFoundError(message)
        elif status_code == 400:
            raise ValidationError(message)
        elif status_code == 429:
            raise RateLimitError(message)
        elif 500 <= status_code < 600:
            raise ServerError(message)
        else:
            raise ServerError(message) from error

    def __enter__(self) -> "A7Client":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._client.close()
