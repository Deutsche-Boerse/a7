"""
Multi-environment configuration example

Shows how to easily switch between production, alternate, and development environments.
"""

import os

from dotenv import load_dotenv

from a7 import A7Client

# Load environment variables from .env file
load_dotenv()

# Disable proxy for direct connection
for key in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
    if key in os.environ:
        del os.environ[key]


def get_client_from_env() -> A7Client:
    """
    Create client from environment variables.

    Reads from .env file:
      A7_API_TOKEN=Bearer_your_token
      A7_BASE_URL=https://... (optional)
      A7_VERIFY_SSL=true/false (optional)
    """
    token = os.getenv("A7_API_TOKEN")
    if not token:
        raise ValueError("A7_API_TOKEN not set in environment")

    base_url = os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/")
    verify_ssl = os.getenv("A7_VERIFY_SSL", "true").lower() == "true"

    return A7Client(token=token, base_url=base_url, verify_ssl=verify_ssl)


def get_production_client(token: str) -> A7Client:
    """Create client for production environment."""
    return A7Client(
        token=token, base_url="https://a7.deutsche-boerse.com/api/", verify_ssl=True
    )


def get_alternate_client(token: str) -> A7Client:
    """Create client for alternate production environment."""
    return A7Client(
        token=token, base_url="https://a7.deutsche-boerse.de/api/", verify_ssl=True
    )


def get_dev_client(token: str) -> A7Client:
    """Create client for development environment (with self-signed cert support)."""
    return A7Client(
        token=token,
        base_url="https://a7.deutsche-boerse.de/api/",
        verify_ssl=False,  # Self-signed certificates
    )


if __name__ == "__main__":
    # Option 1: From environment variables (recommended)
    print("=== Using environment configuration ===")
    client = get_client_from_env()
    markets = client.rdi.get_markets()
    print(f"Found {len(markets)} markets")
    client.close()

    # Option 2: Explicit environment selection
    token = os.getenv("A7_API_TOKEN", "YOUR_TOKEN")

    print("\n=== Production ===")
    with get_production_client(token) as prod_client:
        # Use prod_client...
        pass

    print("=== Alternate Production ===")
    with get_alternate_client(token) as alt_client:
        # Use alt_client...
        pass

    print("=== Development ===")
    with get_dev_client(token) as dev_client:
        # Use dev_client...
        pass
