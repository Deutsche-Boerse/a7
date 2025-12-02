"""Shared pytest fixtures and configuration."""

import os
import json

import pytest
from dotenv import load_dotenv

from a7 import A7Client

# Load environment variables for integration tests
load_dotenv()


def pytest_addoption(parser):
    """Add custom pytest command line options."""
    parser.addoption(
        "--show-responses",
        action="store_true",
        default=False,
        help="Show API response bodies in test output",
    )


@pytest.fixture
def show_responses(request):
    """Return whether to show API response bodies."""
    return request.config.getoption("--show-responses")


def print_response(data, show: bool = False, truncate: int = 270):
    """
    Pretty print API response data.
    
    Args:
        data: Response data to print
        show: Whether to show responses (from --show-responses flag)
        truncate: Max length before truncating (None for no truncation)
    """
    if not show:
        return
        
    if isinstance(data, (dict, list)):
        json_str = json.dumps(data, indent=2)
        if truncate and len(json_str) > truncate:
            print(f"\n📦 Response (truncated to {truncate} chars):")
            print(json_str[:truncate] + "\n... [truncated]")
        else:
            print(f"\n📦 Response:")
            print(json_str)
    else:
        str_data = str(data)
        if truncate and len(str_data) > truncate:
            print(f"\n📦 Response: {str_data[:truncate]}... [truncated]")
        else:
            print(f"\n📦 Response: {str_data}")


@pytest.fixture
def test_token() -> str:
    """Return a test API token."""
    return "Bearer test_token_12345"


@pytest.fixture
def mock_client(test_token: str) -> A7Client:
    """Return a configured A7 client for unit testing (mock scenarios)."""
    return A7Client(token=test_token)


@pytest.fixture
def mock_base_url() -> str:
    """Return mock base URL for testing."""
    return "https://api.test.a7.com/api/v1/"


@pytest.fixture
def dev_client(test_token: str) -> A7Client:
    """Return a client configured for development environment."""
    dev_url = "https://a7.deutsche-boerse.de/api/v1/"
    return A7Client(token=test_token, base_url=dev_url, verify_ssl=False)


# ============================================================================
# Integration Test Fixtures
# ============================================================================
# These fixtures are used for integration tests against real API endpoints


@pytest.fixture(scope="session")
def client():
    """
    Create A7 client for integration tests.

    Uses environment variables from .env file:
    - A7_API_TOKEN: Your API token
    - A7_BASE_URL: API base URL (default: production)
    - A7_VERIFY_SSL: SSL verification (default: true)

    Only available when A7_INTEGRATION_TESTS=1 is set.
    """
    integration_enabled = os.getenv("A7_INTEGRATION_TESTS", "0") == "1"
    if not integration_enabled:
        pytest.skip("Integration tests not enabled. Set A7_INTEGRATION_TESTS=1")

    api_token = os.getenv("A7_API_TOKEN")
    if not api_token:
        pytest.fail("A7_API_TOKEN not set in environment")

    base_url = os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/v1/")
    verify_ssl = os.getenv("A7_VERIFY_SSL", "true").lower() == "true"

    print(f"\n🔗 Connecting to: {base_url}")
    print(f"🔒 SSL Verification: {verify_ssl}")

    # Apply NO_PROXY configuration - must be set BEFORE creating client
    no_proxy = os.getenv("NO_PROXY", "")
    if no_proxy:
        os.environ["NO_PROXY"] = no_proxy
        os.environ["no_proxy"] = no_proxy  # Set both variants
        print(f"🔧 NO_PROXY: {no_proxy}")
    
    # Unset HTTP/HTTPS_PROXY if NO_PROXY is set (for complete bypass)
    if no_proxy:
        # Save original values
        orig_http_proxy = os.environ.get("HTTP_PROXY")
        orig_https_proxy = os.environ.get("HTTPS_PROXY")
        orig_http_proxy_lower = os.environ.get("http_proxy")
        orig_https_proxy_lower = os.environ.get("https_proxy")
        
        # Temporarily unset for matching NO_PROXY patterns
        for key in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
            if key in os.environ:
                del os.environ[key]

    client_instance = A7Client(token=api_token, base_url=base_url, verify_ssl=verify_ssl)

    yield client_instance

    client_instance.close()
    
    # Restore proxy settings if they were removed
    if no_proxy:
        if orig_http_proxy:
            os.environ["HTTP_PROXY"] = orig_http_proxy
        if orig_https_proxy:
            os.environ["HTTPS_PROXY"] = orig_https_proxy
        if orig_http_proxy_lower:
            os.environ["http_proxy"] = orig_http_proxy_lower
        if orig_https_proxy_lower:
            os.environ["https_proxy"] = orig_https_proxy_lower


@pytest.fixture(scope="session")
def test_data():
    """
    Test data configuration for integration tests.

    Customize these values based on your environment's available data.
    These values are validated against the A7 dev environment.
    """
    return {
        # T7 Markets (Eurex/Xetra) - XETR with known working data
        "t7": {
            "market_id": "XETR",
            "date": 20230804,
            "market_segment_id": 52885,
            "security_id": 2504978,
            # Known working transact times from EOBI
            "transact_time": "1691099685504424493",
            "transact_time_end": "1691127000575050335",
        },
        # T7 Markets - XEUR for Eurex derivatives
        "t7_eurex": {
            "market_id": "XEUR",
            "date": 20250102,
            "market_segment_id": 371699,
            "security_id": 12517592,
        },
        # CME Markets - SD v2 endpoints
        "cme": {
            "exchange": "XCME",
            "date": 20220915,
            "asset": "BZ",
            "security_id": "12345",
        },
        # CME Markets - Additional test cases from examples
        "cme_cbcm": {
            "exchange": "CBCM",
            "date": 20241129,
            "asset": "ZQ",
            "security_id": "42433670",
        },
        "cme_glbx": {
            "exchange": "GLBX",
            "date": 20180227,
            "asset": "USDCAD",
            "security_id": "577527",
        },
        # Algorithm testing - dbag/top_level is a public algo
        "algo": {
            "owner": "dbag",
            "algorithm": "top_level",
            "test_owner": "lp124",
            # Alternative algo that works without params
            "simple_algo": "DBAG",
        },
        # Dataset testing
        "dataset": {
            "owner": "lp124",
        },
        # Auction testing - multiple test cases from examples
        "auction": {
            "exchange": "XETR",
            "date": 20230111,
            "market_segment_id": "52915",
            "security_id": 2506257,
            "symbol": "DAX",
        },
        "auction_cases": [
            # TPE - SDAX security
            {"exchange": "XETR", "date": 20240109, "market_segment_id": "53007", "security_id": 2505100, "symbol": "TPE", "index": "SDAX"},
            # SZU - SDAX security
            {"exchange": "XETR", "date": 20241204, "market_segment_id": "53002", "security_id": 2505095, "symbol": "SZU", "index": "SDAX"},
            # VOW3 - DAX security
            {"exchange": "XETR", "date": 20250212, "market_segment_id": "53021", "security_id": 2505114, "symbol": "VOW3", "index": "DAX"},
            # BNR - DAX security
            {"exchange": "XETR", "date": 20220915, "market_segment_id": "52360", "security_id": 2504453, "symbol": "BNR", "index": "DAX"},
        ],
        # Insights - Pace of Roll testing - multiple segments and rolls from examples
        "insights": {
            "market_segment": "FOAT",
            "roll": 202406,
        },
        "insights_cases": [
            # FOAT rolls
            {"market_segment": "FOAT", "roll": 202406},
            {"market_segment": "FOAT", "roll": 202506},
            # FXXP rolls (smaller data)
            {"market_segment": "FXXP", "roll": 201012},
            {"market_segment": "FXXP", "roll": 201109},
            {"market_segment": "FXXP", "roll": 201206},
            # FGBM rolls
            {"market_segment": "FGBM", "roll": 202412},
            {"market_segment": "FGBM", "roll": 202509},
            # FGBS rolls (historical)
            {"market_segment": "FGBS", "roll": 200203},
            {"market_segment": "FGBS", "roll": 200306},
        ],
    }


def skip_if_not_found(func):
    """
    Decorator to skip test if resource not found or API error occurs.

    Use for tests that depend on specific data availability.
    Handles NotFoundError, 404/500 HTTP errors gracefully.
    """
    import functools
    import httpx
    from a7.errors import NotFoundError

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundError as e:
            pytest.skip(f"Resource not available in environment: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Resource not found (404): {e.request.url}")
            elif e.response.status_code >= 500:
                pytest.skip(f"Server error ({e.response.status_code}): API unavailable")
            raise

    return wrapper
