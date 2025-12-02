"""Tests for A7Client initialization and basic functionality."""

import pytest

from a7 import A7Client


def test_client_initialization(test_token: str) -> None:
    """Test client initializes with valid token."""
    client = A7Client(token=test_token)

    assert client is not None
    assert client.rdi is not None
    assert client.algo is not None
    assert client.eobi is not None
    assert client.mdp is not None


def test_client_with_bearer_prefix() -> None:
    """Test client handles Bearer prefix correctly."""
    client = A7Client(token="Bearer my_token")
    assert client is not None


def test_client_without_bearer_prefix() -> None:
    """Test client adds Bearer prefix when missing."""
    client = A7Client(token="my_token")
    assert client is not None


def test_client_context_manager(test_token: str) -> None:
    """Test client can be used as context manager."""
    with A7Client(token=test_token) as client:
        assert client is not None


def test_client_close(test_token: str) -> None:
    """Test client close method."""
    client = A7Client(token=test_token)
    client.close()
    # No exception should be raised


def test_client_custom_base_url(test_token: str, mock_base_url: str) -> None:
    """Test client with custom base URL."""
    client = A7Client(token=test_token, base_url=mock_base_url)
    assert client is not None


def test_client_custom_timeout(test_token: str) -> None:
    """Test client with custom timeout."""
    client = A7Client(token=test_token, timeout=60.0)
    assert client is not None


def test_client_ssl_verification_enabled(test_token: str) -> None:
    """Test client with SSL verification enabled (default)."""
    client = A7Client(token=test_token)
    assert client is not None


def test_client_ssl_verification_disabled(test_token: str) -> None:
    """Test client with SSL verification disabled for dev environments."""
    client = A7Client(token=test_token, verify_ssl=False)
    assert client is not None


def test_client_dev_url(test_token: str) -> None:
    """Test client with development URL."""
    dev_url = "https://a7.deutsche-boerse.de/api/v1/"
    client = A7Client(token=test_token, base_url=dev_url, verify_ssl=False)
    assert client is not None


def test_client_alternate_url(test_token: str) -> None:
    """Test client with alternate production URL."""
    alt_url = "https://a7.deutsche-boerse.de/api/v1/"
    client = A7Client(token=test_token, base_url=alt_url)
    assert client is not None
