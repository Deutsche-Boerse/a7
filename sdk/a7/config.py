"""Configuration constants for A7 SDK.

Default values - users can override via A7Client constructor or environment variables.
"""

# Default API Base URL (production)
# Note: Version paths (/v1/, /v2/, etc.) are included in resource endpoints
DEFAULT_BASE_URL = "https://a7.deutsche-boerse.com/api/"

# Request timeout in seconds
DEFAULT_TIMEOUT = 30.0

# SSL Verification (enabled by default for security)
DEFAULT_VERIFY_SSL = True

# User agent
USER_AGENT = "a7-python-sdk/0.2.3"
