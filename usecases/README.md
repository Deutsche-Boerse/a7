# A7 SDK Use Cases & Examples

This directory contains a collection of Jupyter Notebooks demonstrating various capabilities and use cases of the Deutsche Börse A7 Analytics Platform SDK.

## Notebooks Overview

| # | Notebook | Category | Summary | API Endpoint | Market | Segment | Instrument | Security ID | Method |
|---|----------|----------|---------|--------------|--------|---------|------------|-------------|--------|
| **01** | [01_simple_example.ipynb](01_simple_example.ipynb) | Getting Started | Basic introduction to A7 API with authentication and simple data retrieval | `/algo/{owner}/top_level/run` | XEUR | 688 | FGBL | 4611674 | Direct API |
| **02** | [02_simple_rdi.ipynb](02_simple_rdi.ipynb) | Reference Data | Introduction to RDI - querying markets and retrieving market segment information | `/rdi`, `/rdi/{market}/{date}` | XEUR | - | FGBL, FDAX, OGBL | - | Direct API |
| **03** | [03_cash_rates_benchmark_hedging.ipynb](03_cash_rates_benchmark_hedging.ipynb) | Market Analytics | Cash rates and benchmark hedging analysis using PriceLevelv2 algorithm | `/algo/{owner}/PriceLevelv2/run` | XEUR | 688 | FGBL | 4611674 | Direct API |
| **04** | [04_market_insights_pace_of_roll.ipynb](04_market_insights_pace_of_roll.ipynb) | Market Insights | Pace of Roll analysis - visualizes futures contract roll transitions with liquidity migration patterns | `insights.get_por_*` | XEUR | 675 | FESX | variable | **A7 SDK** |
| **05** | [05_orderbook_reconstruction.ipynb](05_orderbook_reconstruction.ipynb) | Market Microstructure | Limit Order Book reconstruction - retrieves and analyzes T7 order book snapshots at specific timestamps | `orderbook.get_t7()`, `eobi.get_transact_times()` | XETR | 52885 | DB1 | 2504978 | **A7 SDK** |
| **06** | [06_manifold_rdi_usage.ipynb](06_manifold_rdi_usage.ipynb) | Reference Data | Comprehensive RDI navigation - explores Market → Segment → Security hierarchy with detailed metadata retrieval | `rdi.get_markets()`, `rdi.get_market_segments()`, `rdi.get_securities()`, `rdi.get_security_details()` | XEUR, XETR | 675, 52885 | FESX, DB1 | variable, 2504978 | **A7 SDK** |
| **07** | [07_algorithm_usage.ipynb](07_algorithm_usage.ipynb) | Algorithms | Algorithm execution - demonstrates simple_measures (orderbook levels & trade metrics) and Insights (trading stats, quotes, trades) algorithms | `algo.run()` with `simple_measures`, `Insights` | XETR | 52885 | DB1 | 2504978 | **A7 SDK** |
| **08** | [08_auction_analysis.ipynb](08_auction_analysis.ipynb) | Auctions | Xetra auction analysis - explores auction hierarchy, retrieves security reference data with tick tables, accesses historical auctions, and simulates auction outcomes | `auction.get_exchanges()`, `auction.get_dates()`, `auction.get_security()`, `auction.get_auction()` | XETR | 52885 | DB1 | 2504978 | **A7 SDK** |

### Key
- **Direct API**: Legacy approach using `requests` library with REST API calls
- **A7 SDK**: Modern approach using the official `a7` Python SDK (v0.2.3+)
- **Market Codes**: XEUR (Eurex), XETR (Xetra)
- **Instruments**: FGBL (German Bund Futures), FESX (EURO STOXX 50 Futures), DB1 (Deutsche Börse AG Stock)

### Notes
- Notebooks 01-03 use direct REST API calls (legacy approach) and are maintained for reference
- Notebooks 04-08 demonstrate modern SDK usage with comprehensive debugging and professional output formatting
- All SDK-based notebooks include data structure inspection suitable for technical audiences

## Running the Notebooks

To run these notebooks, ensure you have the `a7` SDK installed and your API token configured (either via environment variable `A7_API_TOKEN` or directly in the code).

```bash
pip install a7
```
