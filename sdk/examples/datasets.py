"""
Dataset Management Example - Customer datasets

Demonstrates:
- Listing dataset owners
- Listing datasets for an owner
- Querying dataset data
- Precalculation job management

Note: Dataset access requires appropriate permissions.

Run with: python examples/datasets.py
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
    print("DATASET MANAGEMENT")
    print("=" * 70)

    # 1. List dataset owners
    print("\n1. Dataset Owners:")
    try:
        owners = client.dataset.list_owners(mode="compact")
        print(f"   Found {len(owners)} owners")
        if owners:
            print(f"   Sample: {', '.join(owners[:5])}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 2. List precalc owners (similar but for jobs)
    print("\n2. Precalc Job Owners:")
    try:
        owners = client.precalc.list_owners()
        print(f"   Found {len(owners)} precalc owners")
        if owners:
            print(f"   Sample: {', '.join(owners[:5])}...")
    except Exception as e:
        print(f"   (Not available: {e})")

    # 3. List precalc jobs for an owner
    print("\n3. Precalc Jobs:")
    try:
        # Try to find an owner with jobs
        if owners and len(owners) > 0:
            for owner in owners[:3]:  # Check first 3 owners
                jobs = client.precalc.get_jobs(owner)
                if jobs and len(jobs) > 0:
                    print(f"   Owner: {owner}")
                    print(f"   Jobs: {len(jobs)}")
                    for job in jobs[:5]:
                        print(f"   • {job}")
                    break
            else:
                print("   (No jobs found for available owners)")
        else:
            print("   (No precalc owners available)")
    except Exception as e:
        print(f"   (Not available: {type(e).__name__})")

    print("\n" + "=" * 70)
    print("DATASET OPERATIONS")
    print("=" * 70)
    print("""
Dataset API Operations:
  • list_owners(): Get all dataset owners
  • get_datasets(owner): List datasets for an owner
  • get_metadata(owner, dataset): Get dataset schema and info
  • get_data(owner, dataset, ...): Query with SQL-like filters
  • delete(owner, dataset): Remove a dataset

Query Parameters:
  • select: List of columns to return
  • where: SQL WHERE clause
  • order_by: SQL ORDER BY clause
  • format: 'json' or 'csv'
  • limit: Max rows to return

Precalc API Operations:
  • list_owners(): Get precalc job owners
  • get_jobs(owner): List jobs for owner
  • get_definition(owner, job): Get job configuration
  • get_dates(owner, job): Get available result dates
  • create/activate/deactivate/delete jobs
""")

    print("=" * 70)
    print("DATASET MANAGEMENT COMPLETE")
    print("=" * 70)

    # Clean up
    client.close()


if __name__ == "__main__":
    main()
