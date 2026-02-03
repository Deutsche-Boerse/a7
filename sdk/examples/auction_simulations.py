"""
Auction Simulations Example - Xetra auction data and simulations

Demonstrates:
- Navigating Xetra auction hierarchy (exchanges, dates, segments, securities)
- Retrieving security reference data with tick tables
- Getting auction types available for securities
- Simulating auction outcomes with additional orders

Run with: python examples/auction_simulations.py
"""

import os
from dotenv import load_dotenv
from a7 import A7Client

# Load configuration
load_dotenv()

# Disable proxy for direct connection (required in some environments)
for key in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
    if key in os.environ:
        del os.environ[key]


def main():
    client = A7Client(
        token=os.getenv("A7_API_TOKEN"),
        base_url=os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/"),
        verify_ssl=os.getenv("A7_VERIFY_SSL", "true").lower() == "true",
    )

    print("=" * 70)
    print("XETRA AUCTION SIMULATIONS")
    print("=" * 70)

    # 1. Get available exchanges
    print("\n1. Available Exchanges for Auctions:")
    try:
        exchanges = client.auction.get_exchanges()
        print(f"   {', '.join(exchanges)}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 2. Get available dates for XETR
    print("\n2. Available Trading Days for XETR:")
    try:
        dates = client.auction.get_dates("XETR")
        print(f"   Found {len(dates)} trading days")
        if dates:
            print(f"   Latest 5: {dates[-5:]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 3. Get market segments
    print("\n3. Market Segments for XETR on 2024-01-09:")
    try:
        segments = client.auction.get_market_segments("XETR", 20240109, mode="segment")
        print(f"   Found {len(segments)} market segments")
        if segments:
            print(f"   Sample segments: {segments[:5]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 4. Get securities in a segment
    print("\n4. Securities in Segment 53007 (SDAX):")
    try:
        securities = client.auction.get_securities("XETR", 20240109, "53007")
        print(f"   Found {len(securities)} securities")
        if securities:
            print(f"   Sample security IDs: {securities[:5]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 5. Get security reference data - TPE (SDAX stock)
    print("\n5. Security Reference Data for TPE (SDAX):")
    try:
        security = client.auction.get_security(
            exchange="XETR",
            date=20240109,
            market_segment_id=53007,
            security_id=2505100
        )
        print(f"   Symbol: {security.get('Symbol')}")
        print(f"   ISIN: {security.get('ISIN')}")
        print(f"   Index: {security.get('Index')}")
        print(f"   Security ID: {security.get('SecurityID')}")
        print(f"   Market Segment ID: {security.get('MarketSegmentID')}")

        # Show tick table
        ticks = security.get("Ticks", [])
        if ticks:
            print(f"\n   Tick Table ({len(ticks)} tiers):")
            for tick in ticks[:5]:
                print(f"     {tick['From']:>10} - {tick['To']:>12}: tick = {tick['Tick']}")
            if len(ticks) > 5:
                print(f"     ... and {len(ticks) - 5} more tiers")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 6. Get security by symbol - VOW3 (DAX stock)
    print("\n6. Security Reference Data for VOW3 (DAX) by Symbol:")
    try:
        security = client.auction.get_security_by_symbol(
            exchange="XETR",
            date=20250212,
            symbol="VOW3"
        )
        print(f"   Symbol: {security.get('Symbol')}")
        print(f"   ISIN: {security.get('ISIN')}")
        print(f"   Index: {security.get('Index')}")
        print(f"   Security ID: {security.get('SecurityID')}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 7. Get available auction types
    print("\n7. Auction Types for DAX (segment 52915, security 2506257):")
    try:
        auction_types = client.auction.get_auction_types(
            exchange="XETR",
            date=20230111,
            market_segment_id=52915,
            security_id=2506257
        )
        print(f"   Available types: {', '.join(auction_types)}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 8. Get historical auction data
    print("\n8. Historical Opening Auction Data:")
    try:
        auction = client.auction.get_auction(
            exchange="XETR",
            date=20230111,
            market_segment_id=52915,
            security_id=2506257,
            auction_type="opening"
        )
        print(f"   Auction data retrieved")
        if isinstance(auction, dict):
            print(f"   Keys: {list(auction.keys())[:5]}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 9. Simulate auction with additional order
    print("\n9. Simulate Opening Auction with Additional Buy Order:")
    try:
        simulated = client.auction.get_auction(
            exchange="XETR",
            date=20230111,
            market_segment_id=52915,
            security_id=2506257,
            auction_type="opening",
            side="buy",
            px=15000.0,
            qty=100,
            prio=1
        )
        print(f"   Simulation with: side=buy, price=15000.0, qty=100, priority=1")
        if isinstance(simulated, dict):
            # The response structure depends on the API
            print(f"   Response keys: {list(simulated.keys())[:5]}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    print("\n" + "=" * 70)
    print("AUCTION SIMULATION USE CASES")
    print("=" * 70)
    print("""
Xetra Auction Simulations allow you to:
  • Analyze historical auction outcomes
  • Simulate "what-if" scenarios with your orders
  • Understand price discovery in auctions
  • Optimize order placement strategies

Auction Types:
  • opening:  Opening auction at market open
  • closing:  Closing auction at market close
  • intraday: Intraday auctions (volatility interruptions)

Simulation Parameters:
  • side: 'buy' or 'sell'
  • px: Limit price for the order
  • qty: Order quantity
  • prio: Time priority (1 = highest)
""")

    print("=" * 70)
    print("AUCTION SIMULATIONS COMPLETE")
    print("=" * 70)

    # Clean up
    client.close()


if __name__ == "__main__":
    main()
