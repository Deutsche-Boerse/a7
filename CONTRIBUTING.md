# Contributing to A7 Python SDK

Thank you for your interest in contributing to the A7 Python SDK! This document provides guidelines for development, testing, and publishing.

## Development Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Getting Started

```bash
# Clone the repository
git clone https://github.com/Deutsche-Boerse/a7.git
cd a7/sdk

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Code Quality

Before submitting any changes, ensure your code passes all quality checks.

### Linting with Ruff

```bash
# Check for linting issues
ruff check .

# Auto-fix issues where possible
ruff check . --fix
```

### Formatting with Ruff

```bash
# Check formatting
ruff format --check .

# Apply formatting
ruff format .
```

### Type Checking with Pyright

```bash
# Run type checker
pyright
```

### All Checks at Once

```bash
# Run all quality checks
ruff check . && ruff format . && pyright
```

## Running Tests

### Unit Tests

Unit tests mock all HTTP calls and don't require API access:

```bash
# Run unit tests only (excludes integration tests)
pytest tests/ --ignore=tests/test_integration.py -v

# Run specific test file
pytest tests/test_rdi.py -v

# Run with coverage
pytest tests/ --ignore=tests/test_integration.py --cov=a7
```

### Integration Tests (Production API)

Integration tests run against the real A7 API and validate all resources work correctly.

#### Setup

1. Create a `.env` file in the `sdk/` directory:

```bash
A7_API_TOKEN=Bearer_your_token_here
A7_BASE_URL=https://a7.deutsche-boerse.com/api/
A7_VERIFY_SSL=true
A7_INTEGRATION_TESTS=1
NO_PROXY='*'  # Required if behind corporate proxy
```

2. Run integration tests:

```bash
# Enable integration tests and run
A7_INTEGRATION_TESTS=1 pytest tests/test_integration.py -v

# Show API responses (truncated to 270 chars)
A7_INTEGRATION_TESTS=1 pytest tests/test_integration.py --show-responses -v -s

# Run specific test class
A7_INTEGRATION_TESTS=1 pytest tests/test_integration.py::TestRDI -v
A7_INTEGRATION_TESTS=1 pytest tests/test_integration.py::TestNegativeScenarios -v
```

#### Test Classes

| Test Class | Description | Tests |
|------------|-------------|-------|
| `TestRDI` | T7 reference data | 5 |
| `TestSD` | CME security details | 3 |
| `TestAlgo` | Algorithm execution | 4 |
| `TestEOBI` | T7 order book interface | 4 |
| `TestMDP` | CME market data | 3 |
| `TestOrderBook` | Constructed order books | 2 |
| `TestDataset` | Customer datasets | 3 |
| `TestInsights` | Market insights | 2 |
| `TestPrecalc` | Precalculation management | 3 |
| `TestAuction` | Xetra auctions | 3 |
| `TestNegativeScenarios` | Error handling | 4 |
| `TestAuthentication` | Auth and context manager | 2 |

**Note**: Some tests may be skipped if specific test data is unavailable on your environment.

### Running All Tests

```bash
# Run complete test suite
A7_INTEGRATION_TESTS=1 pytest tests/ -v
```

## Development Guidelines

### Code Style

- **Type hints required**: All functions must have type hints (Python 3.10+ syntax)
- **Docstrings required**: All public methods must have comprehensive docstrings
- **Keep it simple**: Prefer clarity over cleverness
- **No async**: This is a sync-only SDK

### Testing Requirements

- **Unit tests**: Required for all new features
- **Positive tests**: Test expected behavior
- **Negative tests**: Test error handling (auth failures, not found, validation)
- **Use `mock_client` fixture**: For unit tests, not `client`

### Adding New Endpoints

1. Check OpenAPI specification in `sdk/openapi/`
2. Add method to appropriate resource class in `sdk/a7/resources/`
3. Add comprehensive type hints
4. Write unit tests (positive and negative cases)
5. Write integration test if applicable
6. Update README with usage example
7. Run full quality check: `ruff check . && ruff format . && pyright && pytest tests/ -v`

## Publishing (Authorized Users Only)

Publishing to PyPI is restricted to authorized maintainers.

### Prerequisites

1. PyPI account with upload permissions for the `a7` package
2. PyPI API token stored securely

### Build Process

```bash
cd sdk/

# 1. Ensure all tests pass
pytest tests/ -v

# 2. Run quality checks
ruff check . && ruff format . && pyright

# 3. Update version in a7/_version.py
# Example: __version__ = "0.3.0"

# 4. Build the package
python -m build

# 5. Check the built package
twine check dist/*
```

### Upload to PyPI

```bash
# Install twine if not already installed
pip install twine

# Upload to PyPI (requires authentication)
twine upload dist/*

# Or upload to TestPyPI first for verification
twine upload --repository testpypi dist/*
```

### Post-Release

1. Create a git tag: `git tag v0.3.0`
2. Push the tag: `git push origin v0.3.0`
3. Update CHANGELOG in README.md

## Security

- **Never commit secrets**: Keep `.env` files out of version control
- **Token handling**: Pass tokens at client initialization only
- **No token storage**: SDK does not cache or store tokens

## Getting Help

- 🐛 [GitHub Issues](https://github.com/Deutsche-Boerse/a7/issues) for bug reports
- 📧 Contact A7 team: [hdp@deutsche-boerse.com](mailto:hdp@deutsche-boerse.com)

## Troubleshooting

### Corporate Proxy / SSL Certificate Issues

When publishing to PyPI from behind a corporate proxy or firewall with SSL inspection, you may encounter SSL certificate verification errors:

```
SSLCertVerificationError: certificate verify failed: unable to get local issuer certificate
```

**Solution**: Point to the system CA bundle that includes corporate certificates:

```bash
# Check if your system has corporate certificates installed
ls /usr/local/share/ca-certificates/

# Set REQUESTS_CA_BUNDLE to use system certificates
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Then upload with credentials (to skip OIDC check which also fails behind proxy)
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=$(grep PYPI_API_TOKEN .env | cut -d= -f2)
twine upload dist/*
```

**Tip**: Add to `~/.bashrc` to avoid setting it each time:
```bash
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

---

Thank you for contributing to the A7 Python SDK!
