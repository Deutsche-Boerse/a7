"""Custom exceptions for A7 SDK."""


class A7Error(Exception):
    """Base exception for all A7 SDK errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize error with message and optional status code."""
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(A7Error):
    """Raised when authentication fails (401)."""

    def __init__(self, message: str = "Authentication failed. Check your API token.") -> None:
        """Initialize authentication error."""
        super().__init__(message, status_code=401)


class ForbiddenError(A7Error):
    """Raised when access is forbidden (403)."""

    def __init__(self, message: str = "Access forbidden. Check your permissions.") -> None:
        """Initialize forbidden error."""
        super().__init__(message, status_code=403)


class NotFoundError(A7Error):
    """Raised when resource is not found (404)."""

    def __init__(self, message: str = "Resource not found.") -> None:
        """Initialize not found error."""
        super().__init__(message, status_code=404)


class ValidationError(A7Error):
    """Raised when request validation fails (400)."""

    def __init__(self, message: str = "Invalid request parameters.") -> None:
        """Initialize validation error."""
        super().__init__(message, status_code=400)


class RateLimitError(A7Error):
    """Raised when rate limit is exceeded (429)."""

    def __init__(self, message: str = "Rate limit exceeded. Please retry later.") -> None:
        """Initialize rate limit error."""
        super().__init__(message, status_code=429)


class ServerError(A7Error):
    """Raised when server error occurs (5xx)."""

    def __init__(self, message: str = "Server error occurred.") -> None:
        """Initialize server error."""
        super().__init__(message, status_code=500)


class ConnectionError(A7Error):
    """Raised when connection to API fails."""

    def __init__(self, message: str = "Connection to A7 API failed.") -> None:
        """Initialize connection error."""
        super().__init__(message)
