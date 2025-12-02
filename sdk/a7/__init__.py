"""A7 Python SDK - Synchronous client for Deutsche Börse A7 Analytics Platform."""

from a7.client import A7Client
from a7.errors import (
    A7Error,
    AuthenticationError,
    ConnectionError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

try:
    from a7._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = [
    "A7Client",
    "A7Error",
    "AuthenticationError",
    "ConnectionError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "__version__",
]
