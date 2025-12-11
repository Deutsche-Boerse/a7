"""
Example: Listing algorithms

Demonstrates:
- Listing all algorithm owners
- Listing algorithms for a specific owner
- Getting algorithm metadata
- Running algorithms with parameters

Run with: python examples/list_algorithms.py
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

# Helper function to show truncated output in smart way
def print_truncated(obj, indent="   "):
    if isinstance(obj, list):
        print(f"{indent}List with {len(obj)} items (showing first 5):")
        for i, item in enumerate(obj[:5]):
            print(f"{indent}Item {i+1}:")
            print_truncated(item, indent + "  ")
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'series' and isinstance(value, list):
                print(f"{indent}• series: List[{len(value)}]")
                for s in value[:3]:
                    if isinstance(s, dict) and 'name' in s:
                        content_info = ""
                        if 'content' in s and isinstance(s['content'], dict):
                            counts = [f"{k}[{len(v)}]" if isinstance(v, list) else k for k, v in s['content'].items()]
                            content_info = f", content keys: {', '.join(counts)}"
                        print(f"{indent}  - name: {s['name']}{content_info}")
                    else:
                            print(f"{indent}  - {str(s)[:50]}...")
                if len(value) > 3:
                    print(f"{indent}  - ... ({len(value)-3} more)")
            else:
                val_str = str(value)
                if len(val_str) > 100:
                    val_str = val_str[:100] + "..."
                print(f"{indent}• {key}: {val_str}")
    else:
        print(f"{indent}{obj}")


def main():
    client = A7Client(
        token=os.getenv("A7_API_TOKEN"),
        base_url=os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/"),
        verify_ssl=os.getenv("A7_VERIFY_SSL", "true").lower() == "true",
    )

    print("=" * 60)
    print("ALGORITHM MANAGEMENT")
    print("=" * 60)

    # 1. List all algorithm owners
    print("\n1. Algorithm Owners:")
    try:
        owners = client.algo.list_owners()
        print(f"   Found {len(owners)} owners")
        print(f"   Sample: {', '.join(owners[:10])}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 2. List algorithms for the public 'dbag' owner
    print("\n2. Algorithms for 'dbag' (public):")
    try:
        algos = client.algo.list_algorithms("dbag")
        print(f"   Found {len(algos)} algorithms:")
        for algo in algos:
            print(f"   • {algo}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 3. Get algorithm metadata
    print("\n3. Algorithm Metadata for 'dbag/top_level':")
    try:
        metadata = client.algo.get_metadata(
            owner="dbag",
            algorithm="top_level",
            mode="compact"
        )
        print(f"   Metadata retrieved:")
        if isinstance(metadata, dict):
            for key in list(metadata.keys())[:5]:
                print(f"   • {key}: {metadata[key]}")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 4. Run an algorithm
    print("\n4. Running 'dbag/top_level' algorithm:")
    try:
        params = {
            "marketId": "XETR",
            "date": 20230804,
            "marketSegmentId": 52885,
            "securityId": "2504978"
        }
        print(f"   Parameters: {params}")
        result = client.algo.run(
            owner="dbag",
            algorithm="top_level",
            params=params
        )
        print(f"   Algorithm executed successfully")
        print(f"   Result type: {type(result)}")
        
        # Raw truncated output
        if isinstance(result, list):
            print(f"   Result (first 5 items, truncated):")
            for item in result[:5]:
                # Truncate the string representation of the item to avoid flooding the console
                item_str = str(item)
                if len(item_str) > 100:
                    item_str = item_str[:100] + "..."
                print(f"   • {item_str}")
        else:
            print(f"   Result: {result}")

        print("\n   Smart Output:")
        print_truncated(result)
    except Exception as e:
        print(f"   (Not available: {e})")

    # Clean up
    client.close()

    print("\n" + "=" * 60)
    print("ALGORITHM MANAGEMENT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
