"""Tests for custom exceptions."""

import pytest

from a7 import (
    A7Error,
    AuthenticationError,
    ConnectionError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


def test_base_error() -> None:
    """Test base A7Error exception."""
    error = A7Error("Test error")
    assert str(error) == "Test error"
    assert error.status_code is None


def test_base_error_with_status() -> None:
    """Test base A7Error with status code."""
    error = A7Error("Test error", status_code=500)
    assert error.status_code == 500


def test_authentication_error() -> None:
    """Test AuthenticationError exception."""
    error = AuthenticationError()
    assert "Authentication failed" in str(error)
    assert error.status_code == 401


def test_forbidden_error() -> None:
    """Test ForbiddenError exception."""
    error = ForbiddenError()
    assert "forbidden" in str(error).lower()
    assert error.status_code == 403


def test_not_found_error() -> None:
    """Test NotFoundError exception."""
    error = NotFoundError()
    assert "not found" in str(error).lower()
    assert error.status_code == 404


def test_validation_error() -> None:
    """Test ValidationError exception."""
    error = ValidationError()
    assert "Invalid" in str(error)
    assert error.status_code == 400


def test_rate_limit_error() -> None:
    """Test RateLimitError exception."""
    error = RateLimitError()
    assert "Rate limit" in str(error)
    assert error.status_code == 429


def test_server_error() -> None:
    """Test ServerError exception."""
    error = ServerError()
    assert "Server error" in str(error)
    assert error.status_code == 500


def test_connection_error() -> None:
    """Test ConnectionError exception."""
    error = ConnectionError()
    assert "Connection" in str(error)
    assert error.status_code is None


def test_custom_messages() -> None:
    """Test exceptions with custom messages."""
    error = NotFoundError("Security XYZ not found")
    assert "Security XYZ not found" in str(error)
    assert error.status_code == 404
