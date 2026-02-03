"""
Basic usage example - getting started with A7 SDK

Shows the most common operations with minimal configuration.
Run with: python examples/basic_usage.py
"""

import os
from dotenv import load_dotenv
from a7 import A7Client

# Load configuration from .env file
load_dotenv()

# Disable proxy for direct connection (required in some environments)
for key in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
    if key in os.environ:
        del os.environ[key]


def main():
    # Initialize client with your token
    # Token can be obtained from: https://a7.deutsche-boerse.com/
    client = A7Client(
        token=os.getenv("A7_API_TOKEN"),
        base_url=os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/"),
        verify_ssl=os.getenv("A7_VERIFY_SSL", "true").lower() == "true",
    )

    print("=" * 60)
    print("A7 SDK - BASIC USAGE EXAMPLE")
    print("=" * 60)

    # 1. Discover available T7 markets
    print("\n1. Available T7 Markets (RDI):")
    markets = client.rdi.get_markets()
    print(f"   Found {len(markets)} markets: {', '.join(markets)}")

    # 2. Get market segments for a specific market and date
    print("\n2. Market Segments for XETR on 2023-08-04:")
    try:
        segments = client.rdi.get_market_segments("XETR", date=20230804)
        print(f"   Found {len(segments)} segments")
        if segments:
            seg = segments[0]
            if isinstance(seg, dict):
                print(f"   First segment ID: {seg.get('MarketSegmentID', seg)}")
            else:
                print(f"   First segment ID: {seg}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 3. Discover CME exchanges
    print("\n3. CME Exchanges (SD):")
    try:
        exchanges = client.sd.get_exchanges()
        print(f"   Found: {', '.join(exchanges[:5])}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 4. List algorithm owners
    print("\n4. Algorithm Owners:")
    try:
        owners = client.algo.list_owners()
        print(f"   Found {len(owners)} owners: {', '.join(owners[:5])}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 5. Get Pace of Roll market segments
    print("\n5. Insights - POR Market Segments:")
    try:
        por_segments = client.insights.get_por_market_segments()
        print(f"   Found {len(por_segments)} segments: {', '.join(por_segments[:5])}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 6. Get auction exchanges
    print("\n6. Auction Exchanges:")
    try:
        auction_exchanges = client.auction.get_exchanges()
        print(f"   Found: {', '.join(auction_exchanges)}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # Clean up
    client.close()

    print("\n" + "=" * 60)
    print("BASIC USAGE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
