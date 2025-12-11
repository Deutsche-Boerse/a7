"""
A7 Python SDK - Usage Example

This script demonstrates how to use the A7 SDK to access
market data from Deutsche Börse's A7 Analytics Platform.

Before running:
1. Copy .env.example to .env
2. Add your A7 API token to the .env file
3. Run: python manifold_usage.py
"""

import os
from dotenv import load_dotenv
from a7 import (
    A7Client,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError
)

# Load environment variables from .env file
load_dotenv()


def main():
    # Initialize the A7 client
    token = os.getenv("A7_API_TOKEN")
    if not token:
        print("Error: A7_API_TOKEN not found in environment variables.")
        print("Please create a .env file with your token (see .env.example)")
        return

    # Create client with configuration from environment
    client = A7Client(
        token=token,
        base_url=os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/"),
        verify_ssl=os.getenv("A7_VERIFY_SSL", "true").lower() == "true"
    )

    print("=" * 60)
    print("A7 Analytics Platform - SDK Example")
    print("=" * 60)

    try:
        # ============================================================
        # 1. Reference Data Interface (RDI) - T7 Markets
        # ============================================================
        print("\n📊 Reference Data Interface (RDI)")
        print("-" * 40)

        # Get available markets
        print("\n1. Discovering available markets")
        markets = client.rdi.get_markets()
        print(f"   Available markets: {markets}")

        # Get market segments for Eurex (XEUR) - using a historical date with data
        print("\n2. Getting market segments for XEUR")
        segments = client.rdi.get_market_segments("XEUR", ref_date=20241017)
        print(f"   Found {len(segments)} market segments")
        if segments:
            print(f"   First 3 segments: {segments[:3]}")

        # Get detailed security information
        print("\n3. Getting security details for a specific instrument")
        try:
            details = client.rdi.get_security_details(
                market_id="XEUR",
                ref_date=20241017,
                segment_id=688,
                security_id="204934"
            )
            print(f"   Security details: {details}")
        except NotFoundError:
            print("   Security not found for this date/segment")

        # ============================================================
        # 2. CME Security Details (SD)
        # ============================================================
        print("\n\n📈 CME Security Details (SD)")
        print("-" * 40)

        # Get available CME exchanges
        print("\n1. Getting CME exchanges")
        exchanges = client.sd.get_exchanges()
        print(f"   Available exchanges: {exchanges}")

        # ============================================================
        # 3. Algorithm Execution
        # ============================================================
        print("\n\n🔧 Algorithm Execution")
        print("-" * 40)

        # List algorithm owners
        print("\n1. Listing algorithm owners")
        owners = client.algo.list_owners()
        print(f"   Algorithm owners: {owners}")

        # List algorithms for first available owner
        if owners:
            first_owner = owners[0]
            print(f"\n2. Listing algorithms for '{first_owner}' owner")
            algos = client.algo.list_algorithms(first_owner)
            print(f"   Available algorithms: {algos[:5] if len(algos) > 5 else algos}")
        else:
            print("\n2. No algorithm owners available")

        # ============================================================
        # 4. Enhanced Order Book Interface (EOBI)
        # ============================================================
        print("\n\n📖 Enhanced Order Book Interface (EOBI)")
        print("-" * 40)

        # Get available markets for EOBI
        print("\n1. Getting EOBI markets")
        eobi_markets = client.eobi.get_markets()
        print(f"   EOBI markets: {eobi_markets}")

        # Get available dates for a market
        print("\n2. Getting first available dates for XEUR")
        dates = client.eobi.get_dates("XEUR")
        print(f"   Available dates: {dates[:5] if len(dates) > 5 else dates}")

        # Get market segments for EOBI
        print("\n3. Getting EOBI market segments for XEUR on 20241017")
        eobi_segments = client.eobi.get_market_segments("XEUR", 20241017)
        print(f"   Found {len(eobi_segments)} EOBI segments")
        if eobi_segments:
            print(f"   First 3 segments: {eobi_segments[:3]}")

        # Get securities for a specific segment (using 589 - FDAX futures for 20261218 )
        test_segment = 589
        print(f"\n4. Getting securities for segment {test_segment} (FDAX 20261218 futures)")
        securities = client.eobi.get_securities("XEUR", 20241017, test_segment)
        print(f"   Found {len(securities)} securities")
        if securities:
            print(f"   First 3 securities: {securities[:3]}")

            # Get transaction times for a security
            test_security = 10404970
            print(f"\n5. Getting transaction times for security {test_security}")
            try:
                times = client.eobi.get_transact_times(
                    market_id="XEUR",
                    date=20241017,
                    market_segment_id=test_segment,
                    security_id=test_security
                )
                print(f"   Transaction times (first 5): {times[:5] if len(times) > 5 else times}")
            except Exception as e:
                print(f"   Could not get transaction times: {e}")

        # ============================================================
        # 5. Market Insights - Pace of Roll (POR)
        # ============================================================
        print("\n\n📊 Market Insights - Pace of Roll (POR)")
        print("-" * 40)

        # Get Pace of Roll market segments
        print("\n1. Getting Pace of Roll market segments")
        por_segments = client.insights.get_por_market_segments()
        print(f"   POR segments: {por_segments}")

        # Get rolls for a specific segment (e.g., FDAX)
        if por_segments:
            test_por_segment = por_segments[0] if "FDAX" not in por_segments else "FDAX"
            print(f"\n2. Getting rolls for segment '{test_por_segment}'")
            try:
                rolls = client.insights.get_por_rolls(test_por_segment)
                print(f"   Available rolls: {rolls[:5] if len(rolls) > 5 else rolls}")

                # Get POR data for a specific roll
                if rolls:
                    first_roll = rolls[0]
                    print(f"\n3. Getting POR data for roll '{first_roll}'")
                    por_data = client.insights.get_por_data(
                        market_segment=test_por_segment,
                        roll=first_roll,
                        days=10,
                        n=20,
                        comp="c"  # 'c' for concurrent, 's' for serial
                    )
                    print(f"   POR data: {por_data}")
            except Exception as e:
                print(f"   Could not get POR data: {e}")

        # ============================================================
        # 6. Auction Simulations
        # ============================================================
        print("\n\n🔨 Auction Simulations")
        print("-" * 40)

        # Get available exchanges for auctions
        print("\n1. Getting auction exchanges")
        auction_exchanges = client.auction.get_exchanges()
        print(f"   Auction exchanges: {auction_exchanges}")

        print("\n" + "=" * 60)
        print("✅ Example completed successfully!")
        print("=" * 60)

    except AuthenticationError:
        print("\n❌ Authentication Error: Invalid API token")
        print("   Please check your A7_API_TOKEN in the .env file")
    except NotFoundError as e:
        print(f"\n❌ Not Found Error: {e}")
    except ValidationError as e:
        print(f"\n❌ Validation Error: {e}")
    except RateLimitError:
        print("\n❌ Rate Limit Error: Too many requests")
        print("   Please wait and try again later")
    except ServerError as e:
        print(f"\n❌ Server Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
