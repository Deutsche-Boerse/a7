"""
Reference Data Example - Accessing T7 and CME market reference data

Demonstrates:
- RDI: Reference Data Interface for T7 markets (Eurex, Xetra)
- SD: Security Details for CME markets (CBCM, GLBX, XCME, etc.)
- Navigation through market hierarchy
- Security details retrieval

Run with: python examples/reference_data.py
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
    print("T7 MARKETS - REFERENCE DATA INTERFACE (RDI)")
    print("=" * 70)

    # 1. Discover T7 markets
    print("\n1. Available T7 Markets:")
    markets = client.rdi.get_markets()
    print(f"   {', '.join(markets)}")

    # 2. Get market segments for Xetra
    print("\n2. Market Segments for XETR (Xetra) on 2023-08-04:")
    try:
        segments = client.rdi.get_market_segments("XETR", date=20230804)
        print(f"   Found {len(segments)} segments")
        if segments:
            seg = segments[0]
            if isinstance(seg, dict):
                print(f"   Sample: ID={seg.get('MarketSegmentID')}, Name={seg.get('MarketSegment')}")
            else:
                print(f"   Sample segment ID: {seg}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 3. Get security details for XETR
    print("\n3. Security Details for XETR:")
    try:
        details = client.rdi.get_security_details(
            market_id="XETR",
            date=20230804,
            market_segment_id=52885,
            security_id=2504978
        )
        if isinstance(details, list) and len(details) > 0:
            d = details[0]
            print(f"   Security ID: {d.get('SecurityID')}")
            print(f"   Symbol: {d.get('Symbol', 'N/A')}")
            print(f"   ISIN: {d.get('ISIN', 'N/A')}")
        else:
            print(f"   Details retrieved")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 4. Get instrument snapshot
    print("\n4. Instrument Snapshot for XETR ETF:")
    try:
        snapshot = client.rdi.get_instrument_snapshot(
            market_id="XETR",
            date=20250212,
            market_segment_id=52242,
            security_id=2504335,
            msg_seq_num=711
        )
        if snapshot and len(snapshot) > 0:
            s = snapshot[0]
            print(f"   Template: {s.get('Template')}")
            print(f"   Security Type: {s.get('SecurityType', 'N/A')}")
    except Exception as e:
        print(f"   (Not available: {e})")

    print("\n" + "=" * 70)
    print("CME MARKETS - SECURITY DETAILS (SD v2)")
    print("=" * 70)

    # 5. Discover CME exchanges
    print("\n5. Available CME Exchanges:")
    try:
        exchanges = client.sd.get_exchanges()
        print(f"   {', '.join(exchanges)}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 6. Get trading days for CBCM
    print("\n6. Trading Days for CBCM:")
    try:
        dates = client.sd.get_dates("CBCM")
        print(f"   Found {len(dates)} trading days")
        if dates:
            print(f"   Latest 3: {dates[-3:]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 7. Get assets for CBCM
    print("\n7. Assets for CBCM on 2024-11-29:")
    try:
        assets = client.sd.get_assets("CBCM", 20241129)
        print(f"   Found {len(assets)} assets")
        print(f"   Sample: {', '.join(assets[:10])}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 8. Get securities for ZQ asset
    print("\n8. Securities for CBCM/ZQ (interest rate futures):")
    try:
        securities = client.sd.get_securities("CBCM", 20241129, "ZQ")
        print(f"   Found {len(securities)} ZQ securities")
        if securities:
            print(f"   Sample IDs: {securities[:5]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 9. Get CME security details - ZQ spread
    print("\n9. Security Details for CBCM/ZQ/42433670 (spread):")
    try:
        details = client.sd.get_security_details(
            exchange="CBCM",
            date=20241129,
            asset="ZQ",
            security_id=42433670
        )
        if isinstance(details, list) and len(details) > 0:
            d = details[0]
            print(f"   Name: {d.get('Name')}")
            print(f"   Symbol: {d.get('Symbol')}")
            print(f"   Security Type: {d.get('SecurityType')}")
            print(f"   Currency: {d.get('Currency')}")
            print(f"   Asset: {d.get('Asset')}")
            # Show legs for spread
            legs = d.get("Legs", [])
            if legs:
                print(f"   Legs: {len(legs)} leg(s)")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 10. Get FX security details from GLBX
    print("\n10. Security Details for GLBX/USDCAD FX Spot:")
    try:
        details = client.sd.get_security_details(
            exchange="GLBX",
            date=20180227,
            asset="USDCAD",
            security_id=577527
        )
        if isinstance(details, list) and len(details) > 0:
            d = details[0]
            print(f"   Name: {d.get('Name')}")
            print(f"   Symbol: {d.get('Symbol')}")
            print(f"   Security Type: {d.get('SecurityType')}")
            print(f"   Currency: {d.get('Currency')}")
            print(f"   Settle Currency: {d.get('SettlCurrency')}")
    except Exception as e:
        print(f"   (Not available: {e})")

    print("\n" + "=" * 70)
    print("REFERENCE DATA COMPLETE")
    print("=" * 70)

    # Clean up
    client.close()


if __name__ == "__main__":
    main()
