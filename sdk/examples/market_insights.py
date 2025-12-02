"""
Market Insights Example - Pre-calculated analytics

Demonstrates:
- Pace of Roll (POR) analysis for futures contracts
- Historical roll data retrieval
- Quantile analysis across multiple rolls

Run with: python examples/market_insights.py
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
    print("MARKET INSIGHTS - PACE OF ROLL (POR) ANALYSIS")
    print("=" * 70)

    # 1. Get available market segments for POR
    print("\n1. Available Market Segments for POR:")
    try:
        segments = client.insights.get_por_market_segments()
        print(f"   Found {len(segments)} segments")
        # Show some known segments from examples
        known = ["FOAT", "FGBM", "FGBS", "FXXP", "FDAX", "FGBL"]
        found = [s for s in known if s in segments]
        print(f"   Interest rate futures: {', '.join(found)}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 2. Get available rolls for FOAT (French OAT futures)
    print("\n2. Available Rolls for FOAT:")
    try:
        rolls = client.insights.get_por_rolls("FOAT")
        print(f"   Found {len(rolls)} rolls")
        if rolls:
            print(f"   Latest 5: {rolls[-5:]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 3. Get POR data for FOAT/202406
    print("\n3. POR Data for FOAT/202406 (June 2024 roll):")
    print("   Parameters: days=10, n=20, comp='c' (consecutive)")
    try:
        data = client.insights.get_por_data(
            market_segment="FOAT",
            roll=202406,
            days=10,
            n=20,
            comp="c"
        )
        # Show structure
        print(f"\n   Data structure:")
        print(f"   • Days to expiry (dte): {data.get('dte')}")
        print(f"   • Current roll (r_0): {len(data.get('r_0', []))} data points")

        # Count historical rolls
        hist_rolls = [k for k in data.keys() if k.startswith("r_") and k != "r_0"]
        print(f"   • Historical rolls: {len(hist_rolls)} (r_1 to r_{len(hist_rolls)})")

        # Show quantiles
        quantiles = [k for k in data.keys() if k.startswith("q_")]
        print(f"   • Quantiles: {', '.join(sorted(quantiles))}")
        print(f"     (q_0=min, q_1=10%, q_2=25%, q_3=75%, q_4=90%, q_5=max)")

        # Sample data
        r0 = data.get("r_0", [])
        if r0:
            print(f"\n   Sample r_0 values (roll ratio by DTE):")
            dte = data.get("dte", [])
            for i in range(min(5, len(r0))):
                print(f"     DTE {dte[i] if i < len(dte) else 'N/A'}: {r0[i]:.4f}" if r0[i] else f"     DTE {dte[i]}: null")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 4. Get POR data for FGBM (Bobl futures)
    print("\n4. POR Data for FGBM/202412 (December 2024 roll):")
    try:
        data = client.insights.get_por_data(
            market_segment="FGBM",
            roll=202412,
            days=10,
            n=30,
            comp="c"
        )
        print(f"   Days to expiry: {data.get('dte')}")
        hist_rolls = [k for k in data.keys() if k.startswith("r_")]
        print(f"   Historical rolls available: {len(hist_rolls)}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 5. Historical data - FGBS/200306 (very old data)
    print("\n5. Historical POR Data for FGBS/200306 (March 2003):")
    try:
        data = client.insights.get_por_data(
            market_segment="FGBS",
            roll=200306,
            days=10,
            n=20,
            comp="c"
        )
        hist_rolls = [k for k in data.keys() if k.startswith("r_")]
        print(f"   Historical rolls available: {len(hist_rolls)}")
        print(f"   Quantiles available: {[k for k in data.keys() if k.startswith('q_')]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    print("\n" + "=" * 70)
    print("POR ANALYSIS USE CASES")
    print("=" * 70)
    print("""
Pace of Roll (POR) measures open interest migration during contract rolls:
  • Roll ratio = back-month OI / (front-month OI + back-month OI)
  • Value of 0 = all positions in front month
  • Value of 1 = all positions rolled to back month

Key use cases:
  • Optimize roll timing to minimize market impact
  • Benchmark your roll execution against market
  • Understand liquidity migration patterns
  • Compare roll behavior across different expiries
""")

    print("=" * 70)
    print("MARKET INSIGHTS COMPLETE")
    print("=" * 70)

    # Clean up
    client.close()


if __name__ == "__main__":
    main()
