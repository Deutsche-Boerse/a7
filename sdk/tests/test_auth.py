"""Tests for authentication functionality."""

import httpx
import pytest

from a7.auth import BearerAuth


def test_bearer_auth_with_prefix() -> None:
    """Test BearerAuth with Bearer prefix in token."""
    auth = BearerAuth("Bearer my_token_123")
    assert auth.token == "Bearer my_token_123"


def test_bearer_auth_without_prefix() -> None:
    """Test BearerAuth adds Bearer prefix when missing."""
    auth = BearerAuth("my_token_123")
    assert auth.token == "Bearer my_token_123"


def test_bearer_auth_flow() -> None:
    """Test BearerAuth adds Authorization header."""
    auth = BearerAuth("test_token")
    request = httpx.Request("GET", "https://example.com")

    # Process through auth flow
    for authenticated_request in auth.auth_flow(request):
        assert "Authorization" in authenticated_request.headers
        assert authenticated_request.headers["Authorization"] == "Bearer test_token"
