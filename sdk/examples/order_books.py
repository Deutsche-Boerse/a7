"""
Order Book Example - Working with constructed order books

Demonstrates:
- T7 order books from EOBI data
- CME order books from MDP data
- Time range filtering
- Depth level configuration

Run with: python examples/order_books.py
"""

import os
from dotenv import load_dotenv
from a7 import A7Client

# Load configuration
load_dotenv()

# Disable proxy for direct connection
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
    print("CONSTRUCTED ORDER BOOKS")
    print("=" * 70)

    # 1. T7 Order Book for XETR
    print("\n1. T7 Order Book for XETR (Xetra):")
    try:
        ob = client.orderbook.get_t7(
            market_id="XETR",
            date=20230804,
            market_segment_id=52885,
            security_id=2504978,
            from_time="1691099685504424493",  # Known valid transact time
            limit=1,
            levels=5,
            orderbook="aggregated",
            trades=True,
            indicatives=False
        )
        if isinstance(ob, dict):
            print(f"   Retrieved order book snapshot")
            print(f"   Keys: {list(ob.keys())[:5]}...")
        elif isinstance(ob, list) and len(ob) > 0:
            print(f"   Retrieved {len(ob)} order book snapshots")
            first = ob[0]
            if isinstance(first, dict):
                print(f"   First snapshot keys: {list(first.keys())[:5]}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 2. T7 Order Book for XEUR (Eurex derivatives)
    print("\n2. T7 Order Book for XEUR (Eurex):")
    print("   Note: Data availability varies by environment")
    try:
        # First get available transact times to find valid data
        times = client.eobi.get_transact_times(
            market_id="XEUR",
            date=20200227,
            market_segment_id=187421,
            security_id=204934,
            limit=1
        )
        if times and len(times) > 0:
            from_time = times[0]
            obs = client.orderbook.get_t7(
                market_id="XEUR",
                date=20200227,
                market_segment_id=187421,
                security_id=204934,
                from_time=from_time,
                limit=5,
                levels=3,
                orderbook="aggregated",
                trades=True,
                indicatives=False
            )
            if isinstance(obs, list):
                print(f"   Retrieved {len(obs)} order book snapshots")
            else:
                print(f"   Retrieved order book data")
        else:
            print("   (No transact times available for this security)")
    except Exception as e:
        print(f"   (Not available: {type(e).__name__})")

    # 3. CME Order Book
    print("\n3. CME Order Book:")
    print("   Note: CME data availability varies by environment")
    try:
        # First check what assets are available
        assets = client.mdp.get_assets("XCME", 20220915)
        if assets and len(assets) > 0:
            sample_asset = assets[0]
            # Get securities for first asset
            securities = client.mdp.get_securities("XCME", 20220915, sample_asset)
            if securities and len(securities) > 0:
                ob = client.orderbook.get_cme(
                    exchange="XCME",
                    date=20220915,
                    asset=sample_asset,
                    security_id=str(securities[0]),
                    limit=1,
                    levels=5
                )
                if isinstance(ob, (dict, list)):
                    print(f"   CME order book retrieved for {sample_asset}")
            else:
                print(f"   (No securities found for {sample_asset})")
        else:
            print("   (No assets available for this date)")
    except Exception as e:
        print(f"   (Not available: {type(e).__name__})")

    print("\n" + "=" * 70)
    print("ORDER BOOK USE CASES")
    print("=" * 70)
    print("""
Constructed Order Books provide:
  • Full book depth reconstruction from EOBI/MDP data
  • Point-in-time snapshots at nanosecond precision
  • Aggregated or order-level views
  • Trades and indicative states

Parameters:
  • from_time/to_time: Nanosecond timestamps for time range
  • limit: Maximum number of snapshots
  • levels: Order book depth
  • orderbook: 'aggregated' or 'order' level
  • trades: Include trade events
  • indicatives: Include indicative states
""")

    print("=" * 70)
    print("ORDER BOOKS COMPLETE")
    print("=" * 70)

    # Clean up
    client.close()


if __name__ == "__main__":
    main()
