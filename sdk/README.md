# A7 Python SDK

[![PyPI](https://img.shields.io/pypi/v/a7.svg)](https://pypi.org/project/a7/)
[![Python](https://img.shields.io/pypi/pyversions/a7.svg)](https://pypi.org/project/a7/)
[![License](https://img.shields.io/github/license/Deutsche-Boerse/a7.svg)](https://github.com/Deutsche-Boerse/a7/blob/master/LICENSE)

A simple, synchronous Python SDK for the **A7 Analytics Platform** by Deutsche Börse. Access co-location quality market data from Eurex (XEUR) and Xetra (XETR) exchanges with a clean, resource-oriented API.

## Features

- 🚀 **Simple & Synchronous** - No async complexity, just straightforward Python
- 🔒 **Type-Safe** - Full type hints for better IDE support and fewer bugs
- 🎯 **Resource-Oriented** - Intuitive API structure (`client.rdi.get_markets()`)
- ⚡ **Minimal Dependencies** - Only essential packages (httpx)
- 🧪 **Well-Tested** - Comprehensive unit and integration tests
- 📚 **Professional** - Clean, maintainable, production-ready code

## Installation

```bash
pip install a7
```

### Development Installation

For contributing or running examples:

```bash
# Clone the repository
git clone https://github.com/Deutsche-Boerse/a7.git
cd a7/sdk

# Install in editable mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

**Note**: Examples require the package to be installed. Use `pip install -e .` from the `sdk/` directory.

## Quick Start

```python
from a7 import A7Client

# Initialize client with your API token
client = A7Client(token="YOUR_A7_TOKEN")

# Discover available markets
markets = client.rdi.get_markets()
print("Available markets:", markets)

# Get market segments for a specific date
segments = client.rdi.get_market_segments("XEUR", ref_date=20250101)
print(f"Found {len(segments)} segments")

# Get detailed security information
details = client.rdi.get_security_details(
    market_id="XEUR",
    ref_date=20250101,
    segment_id=688,
    security_id="204934"  # Note: parameter is security_id, not instrument_id
)
print("Security details:", details)
```

> 📁 **More examples**: See the [examples/](https://github.com/Deutsche-Boerse/a7/tree/master/sdk/examples) folder for complete working scripts covering all resources.

### Proxy Configuration

For development/test environments behind a corporate proxy:

```bash
# Bypass proxy for local/internal A7 instances
export NO_PROXY='*'

# Then run examples
python examples/reference_data.py
```

## Authentication

Get your API token from the [A7 Analytics Platform](https://a7.deutsche-boerse.com/).

```python
from a7 import A7Client

# Direct token passing
client = A7Client(token="YOUR_A7_TOKEN")

# Or use environment variable
import os
client = A7Client(token=os.getenv("A7_API_TOKEN"))

# For development environments with self-signed certificates
client = A7Client(
    token="YOUR_A7_TOKEN",
    base_url="https://a7-dev.deutsche-boerse.com/api/",
    verify_ssl=False
)
```

### Environment Configuration

Create a `.env` file in your project root:

```bash
# API Token
A7_API_TOKEN=Bearer_your_token_here

# Optional: Custom base URL (note: no version in base URL)
A7_BASE_URL=https://a7.deutsche-boerse.com/api/

# Optional: Disable SSL verification for dev environments
A7_VERIFY_SSL=false

# Optional: Enable integration tests
A7_INTEGRATION_TESTS=1

# Optional: Bypass proxy for local/internal instances
NO_PROXY='*'
```

Load environment variables:

```python
import os
from dotenv import load_dotenv
from a7 import A7Client

load_dotenv()

client = A7Client(
    token=os.getenv("A7_API_TOKEN"),
    base_url=os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/"),
    verify_ssl=os.getenv("A7_VERIFY_SSL", "true").lower() == "true"
)
```

## API Overview

The A7 SDK provides comprehensive access to Deutsche Börse's market data and analytics platform through ten specialized resource modules.

### Reference Data Interface (RDI)

Access reference data for Eurex and Xetra markets:

```python
# Discover available markets
markets = client.rdi.get_markets()

# Get market segments for a trading day
segments = client.rdi.get_market_segments(
    market_id="XEUR",
    ref_date=20250101
)

# Get detailed security information
details = client.rdi.get_security_details(
    market_id="XEUR",
    ref_date=20250101,
    segment_id=688,
    security_id="204934"  # Note: uses security_id parameter per OpenAPI spec
)

# Get instrument snapshot
snapshot = client.rdi.get_instrument_snapshot(
    market_id="XETR",
    date=20201104,
    segment_id=52162,
    security_id=2504233,
    msg_seq_num=106
)
```

### CME Security Details (SD)

Access reference data for CME Group markets:

```python
# Get available CME exchanges
exchanges = client.sd.get_exchanges()

# Get trading days
dates = client.sd.get_dates("XCME")

# Get assets for a trading day
assets = client.sd.get_assets("XCME", 20200106)

# Get security details
details = client.sd.get_security_details(
    exchange="XCME",
    date=20200106,
    asset="GE",
    security_id="12345678"
)
```

### Algorithm Execution & Management

Execute custom algorithms and manage algorithm lifecycle:

```python
# List algorithm owners
owners = client.algo.list_owners()

# List algorithms for an owner
algos = client.algo.list_algorithms("a7")

# Get algorithm metadata
metadata = client.algo.get_metadata("a7", "top_level", mode="detailed")

# Run algorithm with parameters
result = client.algo.run(
    owner="a7",
    algorithm="top_level",
    params={
        "marketId": "XEUR",
        "date": 20250101,
        "securityId": "204934"
    }
)

# Upload custom algorithm
with open("my_algorithm.yaml", "r") as f:
    client.algo.upload("myuser", "my_algorithm", f.read())

# Download algorithm definition
yaml_content = client.algo.download("myuser", "my_algorithm")

# Delete algorithm
client.algo.delete("myuser", "my_algorithm")
```

### Enhanced Order Book Interface (EOBI)

Access T7 market raw order book data with complete message hierarchy:

```python
# Navigate the hierarchy
markets = client.eobi.get_markets()
dates = client.eobi.get_dates("XEUR")
segments = client.eobi.get_market_segments("XEUR", 20200227)
securities = client.eobi.get_securities("XEUR", 20200227, 187421)

# Get transaction times
times = client.eobi.get_transact_times(
    market_id="XEUR",
    date=20200227,
    market_segment_id=187421,
    security_id=204934,
    limit=100,
    mode="compact"
)

# Get specific message
message = client.eobi.get_message(
    market_id="XEUR",
    date=20200227,
    market_segment_id=187421,
    security_id=204934,
    transact_time=1582821000143045889,
    applseq_num=14687296,
    msg_seq_num=23
)
```

### Market Data Platform (MDP)

Access CME market raw order book data:

```python
# Navigate the hierarchy
exchanges = client.mdp.get_exchanges()
dates = client.mdp.get_dates("XCME")
assets = client.mdp.get_assets("XCME", 20220915)
securities = client.mdp.get_securities("XCME", 20220915, "BZ")

# Get sending times
times = client.mdp.get_sending_times(
    exchange="XCME",
    date=20220915,
    asset="BZ",
    security_id="12345",
    mode="compact"
)

# Get specific message
message = client.mdp.get_message(
    exchange="XCME",
    date=20220915,
    asset="BZ",
    security_id="12345",
    sending_time=1663191900206448987,
    msg_seq_num=86054
)
```

### Constructed Order Books

Access reconstructed order books from EOBI/MDP data:

```python
# Get T7 order book
orderbook = client.orderbook.get_t7(
    market_id="XEUR",
    date=20200227,
    market_segment_id=187421,
    security_id=204934,
    from_time=1582821000000000000,
    to_time=1582821100000000000,
    limit=10,
    levels=5,
    orderbook=True,
    trades=True,
    indicatives=False
)

# Get CME order book
orderbook = client.orderbook.get_cme(
    exchange="XCME",
    date=20220915,
    asset="BZ",
    security_id="12345",
    limit=10,
    levels=10
)
```

### Customer Datasets

Manage and access datasets generated by precalculation jobs:

```python
# List dataset owners
owners = client.dataset.list_owners(mode="compact")

# Get datasets for an owner
datasets = client.dataset.get_datasets("myuser")

# Get dataset metadata
metadata = client.dataset.get_metadata("myuser", "my_dataset")

# Query dataset with filters
data = client.dataset.get_data(
    owner="myuser",
    dataset="my_dataset",
    select=["column1", "column2"],
    where="column1 > 100",
    order_by="column2 DESC",
    format="json",
    limit=1000
)

# Delete dataset
client.dataset.delete("myuser", "my_dataset")
```

### Market Insights

Access pre-calculated market analytics:

```python
# Pace of Roll (POR) insights
segments = client.insights.get_por_market_segments()
rolls = client.insights.get_por_rolls("segment_id")
data = client.insights.get_por_data(
    market_segment="segment_id",
    roll="roll_id",
    days=10,
    n=20,
    comp="c"  # 'c' for concurrent, 's' for serial
)

# Latency histogram analysis
histogram = client.insights.get_latency_histogram(
    date=20200227,
    trigger="FDAX",
    target="FESX",
    regime="fast",
    target_action="new_order",
    format="json"
)
```

### Precalculation Management

Manage scheduled jobs that generate datasets:

```python
# List owners and jobs
owners = client.precalc.list_owners()
jobs = client.precalc.get_jobs("myuser")

# Get job definition
definition = client.precalc.get_definition("myuser", "my_job")

# Create new precalc job
client.precalc.create(
    owner="myuser",
    precalc="new_job",
    definition={
        "algo": "my_algorithm",
        "params": {"marketId": "XEUR"},
        "schedule": "daily"
    }
)

# Activate/deactivate job
client.precalc.activate("myuser", "my_job")
client.precalc.deactivate("myuser", "my_job")

# Access generated data
dates = client.precalc.get_dates("myuser", "my_job")
tasks = client.precalc.get_tasks("myuser", "my_job", 20250101)
results = client.precalc.get_results("myuser", "my_job", 20250101, "task1")
data = client.precalc.get_data(
    owner="myuser",
    precalc="my_job",
    date=20250101,
    task="task1",
    result="result1",
    mode="json"
)

# Delete job
client.precalc.delete("myuser", "my_job")
```

### Auction Simulations

Simulate Xetra auction outcomes:

```python
# Navigate hierarchy
exchanges = client.auction.get_exchanges()
dates = client.auction.get_dates("XETR")
segments = client.auction.get_market_segments("XETR", 20230111, mode="segment")
securities = client.auction.get_securities("XETR", 20230111, "52915")

# Get auction types for a security
types = client.auction.get_auction_types(
    exchange="XETR",
    date=20230111,
    market_segment_id="52915",
    security_id=2506257
)

# Get historical auction data
auction = client.auction.get_auction(
    exchange="XETR",
    date=20230111,
    market_segment_id="52915",
    security_id=2506257,
    auction_type="opening"
)

# Simulate auction with additional order
simulated = client.auction.get_auction(
    exchange="XETR",
    date=20230111,
    market_segment_id="52915",
    security_id=2506257,
    auction_type="opening",
    side="buy",
    px=100.50,
    qty=1000,
    prio=1
)

# Alternative: Use symbol instead of IDs
auction = client.auction.get_auction_by_symbol(
    exchange="XETR",
    date=20230111,
    symbol="DAX",
    auction_type="opening"
)
```

## Error Handling

The SDK provides custom exceptions for different error scenarios:

```python
from a7 import (
    A7Client,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError
)

client = A7Client(token="YOUR_A7_TOKEN")

try:
    data = client.rdi.get_security_details("XEUR", 20250101, 688, "invalid_id")
except AuthenticationError:
    print("Invalid API token")
except NotFoundError:
    print("Security not found")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except RateLimitError:
    print("Rate limit exceeded, please retry later")
except ServerError as e:
    print(f"Server error: {e}")
```

## Development Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Install for Development

```bash
# Clone the repository
git clone https://github.com/Deutsche-Boerse/a7.git
cd a7/sdk

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=a7

# Run specific test file
pytest tests/test_rdi.py

# Run with verbose output
pytest -v -s

# Run integration tests (requires .env configuration)
A7_INTEGRATION_TESTS=1 pytest tests/test_integration.py -v

# Show API responses (270 char limit)
pytest tests/test_integration.py --show-responses -v -s

# Run specific test class
pytest tests/test_integration.py::TestRDI -v
pytest tests/test_integration.py::TestNegativeScenarios -v
```

**Note**: Integration tests require `NO_PROXY='*'` for dev/test environments behind corporate proxy.

### Integration Tests

Integration tests run against real A7 API instances and validate all resources comprehensively.

**Test Organization**:
- `tests/test_integration.py` - Health check suite for all resources
  - TestRDI: 5 tests for T7 reference data
  - TestSD: 3 tests for CME security details
  - TestAlgo: 4 tests for algorithm execution
  - TestEOBI: 4 tests for T7 order book interface
  - TestMDP: 3 tests for CME market data
  - TestOrderBook: 2 tests for constructed order books
  - TestDataset: 3 tests for customer datasets
  - TestInsights: 2 tests for market insights
  - TestPrecalc: 3 tests for precalculation management
  - TestAuction: 3 tests for Xetra auctions
  - TestNegativeScenarios: 4 tests for error handling
  - TestAuthentication: 2 tests for auth and context manager

To enable integration tests:

1. Create a `.env` file with your credentials:
   ```bash
   A7_API_TOKEN=Bearer_your_token
   A7_BASE_URL=https://a7.deutsche-boerse.com/api/
   A7_VERIFY_SSL=true
   A7_INTEGRATION_TESTS=1
   NO_PROXY='*'  # Required for dev/test environments
   ```

2. Run integration tests:
   ```bash
   pytest tests/test_integration.py -v
   
   # Show API responses (270 char truncation)
   pytest tests/test_integration.py --show-responses -v -s
   
   # Run specific test class
   pytest tests/test_integration.py::TestRDI -v
   ```

**Note**: Some tests may be skipped if specific data is unavailable on the configured environment.

### Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
pyright
```

## Project Structure

```
sdk/
├── a7/                      # Main package
│   ├── __init__.py         # Package exports
│   ├── _version.py         # Version info
│   ├── client.py           # Main A7Client
│   ├── config.py           # Configuration
│   ├── auth.py             # Authentication
│   ├── errors.py           # Custom exceptions
│   └── resources/          # API resources
│       ├── rdi.py          # Reference Data Interface (T7)
│       ├── sd.py           # Security Details (CME)
│       ├── algo.py         # Algorithm execution & management
│       ├── eobi.py         # Enhanced Order Book (T7)
│       ├── mdp.py          # Market Data Platform (CME)
│       ├── orderbook.py    # Constructed order books
│       ├── dataset.py      # Customer datasets
│       ├── insights.py     # Market insights & analytics
│       ├── precalc.py      # Precalculation job management
│       └── auction.py      # Xetra auction simulations
├── tests/                   # Test suite
├── examples/                # Usage examples (see link below)
├── openapi/                 # OpenAPI specifications
└── pyproject.toml          # Package configuration
```

> 📁 **Examples**: [github.com/Deutsche-Boerse/a7/tree/master/sdk/examples](https://github.com/Deutsche-Boerse/a7/tree/master/sdk/examples)

## API Coverage

### Implemented Resources (v0.2.0)

#### Core Market Data
- ✅ **RDI** - Reference Data Interface (T7 markets)
  - Available markets, segments, security details
  - Instrument snapshots
- ✅ **SD** - Security Details v2 (CME markets)
  - Exchanges, assets, security reference data

#### Raw Market Data
- ✅ **EOBI** - Enhanced Order Book Interface (T7)
  - Complete message hierarchy navigation
  - Transaction times, ApplSeqNums, MsgSeqNums
  - Individual message retrieval
- ✅ **MDP** - Market Data Platform (CME)
  - Complete message hierarchy navigation
  - Sending times with filtering
  - Individual message retrieval

#### Constructed Data
- ✅ **OrderBook** - Reconstructed order books
  - T7 order books from EOBI data
  - CME order books from MDP data
  - Configurable depth levels and time ranges

#### Analytics & Execution
- ✅ **Algo** - Algorithm execution and management
  - Run custom algorithms with parameters
  - Upload, download, delete algorithms
  - List owners and algorithm metadata
- ✅ **Insights** - Pre-calculated market insights
  - Pace of Roll (POR) analysis
  - Latency histogram analysis
- ✅ **Auction** - Xetra auction simulations
  - Historical auction data
  - Simulate auction outcomes with additional orders
  - Support for symbol-based and ID-based queries

#### Data Management
- ✅ **Dataset** - Customer datasets
  - List, query, and manage datasets
  - SQL-like filtering and ordering
  - CSV and JSON export formats
- ✅ **Precalc** - Precalculation job management
  - Create, activate, deactivate jobs
  - Access generated results hierarchy
  - Job lifecycle management

### Configuration Options
- ✅ Multiple base URLs (production, alternate, development)
- ✅ SSL verification control
- ✅ Environment variable configuration
- ✅ Integration test support

## API Methods Reference

Complete list of all available methods organized by resource:

### RDI (Reference Data Interface - T7)
| Method | Description |
|--------|-------------|
| `get_markets()` | List available T7 markets |
| `get_market_segments(market_id, ref_date)` | Get segments for a market |
| `get_security_details(market_id, ref_date, segment_id, security_id)` | Get security details |
| `get_instrument_snapshot(market_id, date, segment_id, security_id, msg_seq_num)` | Get instrument snapshot |

### SD (Security Details - CME)
| Method | Description |
|--------|-------------|
| `get_exchanges()` | List available CME exchanges |
| `get_dates(exchange)` | Get trading dates for exchange |
| `get_assets(exchange, date)` | Get assets for a trading day |
| `get_security_details(exchange, date, asset, security_id)` | Get CME security details |

### Algo (Algorithm Execution)
| Method | Description |
|--------|-------------|
| `list_owners()` | List algorithm owners |
| `list_algorithms(owner)` | List algorithms for an owner |
| `get_metadata(owner, algorithm, mode)` | Get algorithm metadata |
| `run(owner, algorithm, params)` | Execute algorithm with parameters |
| `upload(owner, algorithm, definition)` | Upload algorithm definition |
| `download(owner, algorithm)` | Download algorithm YAML |
| `delete(owner, algorithm)` | Delete an algorithm |

### EOBI (Enhanced Order Book Interface - T7)
| Method | Description |
|--------|-------------|
| `get_markets()` | List available markets |
| `get_dates(market_id)` | Get dates for a market |
| `get_market_segments(market_id, date)` | Get market segments |
| `get_securities(market_id, date, market_segment_id)` | Get securities |
| `get_transact_times(market_id, date, market_segment_id, security_id)` | Get transaction times |
| `get_applseq_nums(market_id, date, market_segment_id, security_id, transact_time)` | Get application sequence numbers |
| `get_msg_seq_nums(market_id, date, market_segment_id, security_id, transact_time, applseq_num)` | Get message sequence numbers |
| `get_message(market_id, date, market_segment_id, security_id, transact_time, applseq_num, msg_seq_num)` | Get specific message |

### MDP (Market Data Platform - CME)
| Method | Description |
|--------|-------------|
| `get_exchanges()` | List available exchanges |
| `get_dates(exchange)` | Get dates for exchange |
| `get_assets(exchange, date)` | Get assets for a date |
| `get_securities(exchange, date, asset)` | Get securities |
| `get_sending_times(exchange, date, asset, security_id)` | Get sending times |
| `get_message(exchange, date, asset, security_id, sending_time, msg_seq_num)` | Get specific message |

### OrderBook (Constructed Order Books)
| Method | Description |
|--------|-------------|
| `get_t7(market_id, date, market_segment_id, security_id)` | Get T7 constructed order book |
| `get_cme(exchange, date, asset, security_id)` | Get CME constructed order book |

### Dataset (Customer Datasets)
| Method | Description |
|--------|-------------|
| `list_owners(mode)` | List dataset owners |
| `get_datasets(owner)` | Get datasets for an owner |
| `get_metadata(owner, dataset)` | Get dataset metadata |
| `get_data(owner, dataset, select, where, order_by, format, limit)` | Query dataset with filters |
| `delete(owner, dataset)` | Delete a dataset |

### Insights (Market Insights)
| Method | Description |
|--------|-------------|
| `get_por_market_segments()` | Get POR market segments |
| `get_por_rolls(market_segment)` | Get POR rolls |
| `get_por_data(market_segment, roll, days, n, comp)` | Get POR data |
| `get_latency_histogram(date, trigger, target, regime, target_action, format)` | Get latency histogram |

### Precalc (Precalculation Management)
| Method | Description |
|--------|-------------|
| `list_owners()` | List precalc owners |
| `get_jobs(owner)` | Get jobs for an owner |
| `get_definition(owner, precalc)` | Get job definition |
| `create(owner, precalc, definition)` | Create new job |
| `activate(owner, precalc)` | Activate a job |
| `deactivate(owner, precalc)` | Deactivate a job |
| `get_dates(owner, precalc)` | Get dates with results |
| `get_tasks(owner, precalc, date)` | Get tasks for a date |
| `get_results(owner, precalc, date, task)` | Get results for a task |
| `get_data(owner, precalc, date, task, result, mode)` | Get result data |
| `delete(owner, precalc)` | Delete a job |

### Auction (Xetra Auction Simulations)
| Method | Description |
|--------|-------------|
| `get_exchanges()` | List available exchanges |
| `get_dates(exchange)` | Get dates for exchange |
| `get_market_segments(exchange, date, mode)` | Get market segments |
| `get_securities(exchange, date, market_segment_id)` | Get securities |
| `get_auction_types(...)` | Get auction types for security |
| `get_auction(...)` | Get/simulate auction data |
| `get_auction_by_symbol(...)` | Get auction by symbol |

## Contributing

This is an educational project demonstrating the A7 API. Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- **Type hints required** for all functions
- **Tests required** for all new features (positive and negative cases)
- **Code must pass** `ruff check`, `ruff format`, and `pyright`
- **Keep it simple** - clarity over cleverness
- **No async** - this is a sync-only SDK

## Changelog

### Version 0.2.3 (2025-12-11)

**Bug Fixes & Documentation Improvements**

#### Bug Fixes
- **EOBI & MDP Resources**: Fixed `mode` parameter default value. Changed from `"compact"` to `"reference"` to align with OpenAPI specifications. This affects:
  - `eobi.get_transact_times()`
  - `eobi.get_applseq_nums()`
  - `eobi.get_msg_seq_nums()`
  - `mdp.get_sending_times()`

#### Documentation
- Added more verbose and comprehensive usage examples to better demonstrate SDK capabilities.

### Version 0.2.0 (2025-11-02)

**Major Release - Complete API Coverage**

This release implements comprehensive coverage of the A7 Analytics Platform API with 10 specialized resource modules.

#### New Resources
- **SD (Security Details)** - CME Group reference data
  - Exchange, asset, and security hierarchy navigation
  - Complete CME market reference data access
- **OrderBook** - Constructed order books
  - T7 order books from EOBI data
  - CME order books from MDP data
  - Configurable depth levels and time ranges
- **Dataset** - Customer dataset management
  - SQL-like query capabilities (SELECT, WHERE, ORDER BY)
  - JSON and CSV export formats
  - Full dataset lifecycle management
- **Insights** - Pre-calculated market analytics
  - Pace of Roll (POR) analysis
  - Latency histogram analysis with HPT timestamps
- **Precalc** - Precalculation job management
  - Job creation, activation, and scheduling
  - Complete results hierarchy access
  - Automated dataset generation
- **Auction** - Xetra auction simulations
  - Historical auction data retrieval
  - Simulate auction outcomes with additional orders
  - Symbol-based and ID-based queries

#### Enhanced Resources
- **Algo** - Algorithm management expanded
  - Added `list_owners()` for algorithm discovery
  - Added `upload()`, `download()`, `delete()` for algorithm lifecycle
  - Fixed `run()` method to use GET with query parameters (breaking change)
  - Added URL encoding for algorithm names with special characters
- **EOBI** - Complete hierarchy navigation
  - Added `get_markets()`, `get_dates()`, `get_market_segments()`, `get_securities()`
  - Added `get_transact_times()`, `get_applseq_nums()`, `get_msg_seq_nums()`
  - Enhanced filtering capabilities with mode parameters
- **MDP** - Complete CME data access
  - Added `get_exchanges()`, `get_dates()`, `get_assets()`, `get_securities()`
  - Added `get_sending_times()` with comprehensive filtering
  - Updated parameter names to match OpenAPI specification

#### Documentation & Examples
- Comprehensive README with all 10 resources documented
- New example files:
  - `reference_data.py` - T7 and CME reference data
  - `order_books.py` - Constructed order book access
  - `market_insights.py` - POR and latency analysis
  - `datasets.py` - Dataset management and querying
- Enhanced examples README with usage patterns
- Professional docstrings for all methods

#### Breaking Changes
- `algo.run()` changed from POST to GET (affects all algorithm execution)
- EOBI and MDP parameter names updated to match OpenAPI specs

### Version 0.1.0 (2025-10)

**Initial Release**

- Core client with Bearer authentication
- RDI (Reference Data Interface) for T7 markets
- Basic algorithm execution capabilities
- EOBI and MDP message retrieval
- Comprehensive error handling
- Type-safe API with full type hints

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Deutsche-Boerse/a7/blob/master/LICENSE) file for details.

## Resources

- [A7 Analytics Platform](https://a7.deutsche-boerse.com/)
- [Documentation](https://a7.deutsche-boerse.com/docs)
- [GitHub Repository](https://github.com/Deutsche-Boerse/a7)
- [PyPI Package](https://pypi.org/project/a7/)

## Support

For issues and questions:
- 🐛 [GitHub Issues](https://github.com/Deutsche-Boerse/a7/issues)
- 📧 Contact A7 team: [hdp@deutsche-boerse.com](mailto:hdp@deutsche-boerse.com)

## Acknowledgments

Built by the Deutsche Börse team for the financial analytics community.

---

**Note**: This SDK is for educational and research purposes.
