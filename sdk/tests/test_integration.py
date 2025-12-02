"""
Integration Tests for A7 SDK

Tests all resources against real A7 API endpoints with 2-3 tests per endpoint.
Requires valid credentials in .env file and A7_INTEGRATION_TESTS=1

Run with:
    pytest tests/test_integration.py -v
    pytest tests/test_integration.py -v --show-responses  # Show API responses
    pytest tests/test_integration.py::TestRDI -v  # Test specific class
"""

import os
import yaml
import pytest
from pathlib import Path
from conftest import skip_if_not_found, print_response

from a7.errors import NotFoundError, AuthenticationError


# ============================================================================
# RDI (Reference Data Interface) Tests - 6 tests covering 4 endpoints
# ============================================================================

class TestRDI:
    """Reference Data Interface (T7 markets) - 2-3 tests per endpoint."""

    # Endpoint 1: GET /v2/rdi/ - get_markets()
    def test_get_markets_returns_list(self, client, show_responses):
        """Test 1.1: Verify get_markets returns a list of market IDs."""
        markets = client.rdi.get_markets()
        assert isinstance(markets, list)
        assert len(markets) > 0
        print(f"\n✅ Found {len(markets)} T7 markets: {markets}")
        print_response(markets, show_responses)

    def test_get_markets_contains_known_markets(self, client):
        """Test 1.2: Verify known markets (XEUR, XETR) are in results."""
        markets = client.rdi.get_markets()
        assert "XEUR" in markets or "XETR" in markets
        print(f"\n✅ Known markets found in list")

    # Endpoint 2: GET /v2/rdi/{marketId}/{refDate}/ - get_market_segments()
    @skip_if_not_found
    def test_get_market_segments_returns_list(self, client, show_responses):
        """Test 2.1: Verify get_market_segments returns segment list."""
        market_id = "XEEE"
        ref_date = 20240812
        
        segments = client.rdi.get_market_segments(
            market_id=market_id,
            ref_date=ref_date
        )
        assert isinstance(segments, list)
        assert len(segments) > 0
        print(f"\n✅ Found {len(segments)} market segments for {market_id} on {ref_date}")
        print_response(segments, show_responses, truncate=1000)

    @skip_if_not_found
    def test_get_market_segments_different_market(self, client):
        """Test 2.2: Verify get_market_segments works for XEUR."""
        segments = client.rdi.get_market_segments(
            market_id="XEUR",
            ref_date=20200227
        )
        assert isinstance(segments, list)
        print(f"\n✅ Found {len(segments)} segments for XEUR")

    # Endpoint 3: GET /v2/rdi/{marketId}/{refDate}/{segmentId}/{securityId}/ - get_security_details()
    @skip_if_not_found
    def test_get_security_details_returns_data(self, client, show_responses):
        """Test 3.1: Verify get_security_details returns security data."""
        details = client.rdi.get_security_details(
            market_id="XEEE",
            ref_date=20240812,
            segment_id=154574,
            security_id="11340477"
        )
        assert details is not None
        print(f"\n✅ Retrieved security details")
        print_response(details, show_responses)

    # Endpoint 4: GET /v2/rdi/{marketId}/{date}/{segmentId}/{securityId}/{msgSeqNum} - get_instrument_snapshot()
    @skip_if_not_found
    def test_get_instrument_snapshot_xetr_cash(self, client, show_responses):
        """Test 4.1: Verify get_instrument_snapshot for XETR cash instrument."""
        snapshot = client.rdi.get_instrument_snapshot(
            market_id="XETR",
            date=20190402,
            segment_id=52087,
            security_id=2504158,
            msg_seq_num=54
        )
        assert snapshot is not None
        assert isinstance(snapshot, list)
        if len(snapshot) > 0:
            assert isinstance(snapshot[0], dict)
            assert "Template" in snapshot[0]
            assert snapshot[0]["Template"] == "InstrumentSnapshot"
        print(f"\n✅ Retrieved XETR cash instrument snapshot")
        print_response(snapshot, show_responses, truncate=1500)

    @skip_if_not_found
    def test_get_instrument_snapshot_xetr_etf(self, client, show_responses):
        """Test 4.2: Verify get_instrument_snapshot for XETR ETF."""
        snapshot = client.rdi.get_instrument_snapshot(
            market_id="XETR",
            date=20250212,
            segment_id=52242,
            security_id=2504335,
            msg_seq_num=711
        )
        assert snapshot is not None
        assert isinstance(snapshot, list)
        if len(snapshot) > 0:
            assert isinstance(snapshot[0], dict)
            assert "Template" in snapshot[0]
            assert snapshot[0]["Template"] == "InstrumentSnapshot"
            if "SecurityType" in snapshot[0]:
                assert snapshot[0]["SecurityType"] == "ETF"
        print(f"\n✅ Retrieved XETR ETF instrument snapshot")
        print_response(snapshot, show_responses, truncate=2000)


class TestSD:
    """Security Details (CME markets) integration tests."""

    @skip_if_not_found
    def test_get_exchanges(self, client):
        """Test retrieving CME exchanges."""
        exchanges = client.sd.get_exchanges()
        assert isinstance(exchanges, list)
        print(f"\n✅ Found {len(exchanges)} CME exchanges")

    @skip_if_not_found
    def test_get_dates(self, client, test_data):
        """Test retrieving CME trading days."""
        dates = client.sd.get_dates(test_data["cme"]["exchange"])
        assert isinstance(dates, list)
        print(f"\n✅ Found {len(dates)} trading days")

    @skip_if_not_found
    def test_get_assets(self, client, test_data):
        """Test retrieving CME assets."""
        assets = client.sd.get_assets(
            test_data["cme"]["exchange"],
            test_data["cme"]["date"]
        )
        assert isinstance(assets, list)
        print(f"\n✅ Found {len(assets)} assets")

    @skip_if_not_found
    def test_get_securities(self, client, test_data, show_responses):
        """Test retrieving security IDs for an asset."""
        securities = client.sd.get_securities(
            test_data["cme_cbcm"]["exchange"],
            test_data["cme_cbcm"]["date"],
            test_data["cme_cbcm"]["asset"]
        )
        assert isinstance(securities, list)
        print(f"\n✅ Found {len(securities)} securities for {test_data['cme_cbcm']['asset']}")
        print_response(securities[:10], show_responses)  # Show first 10

    @skip_if_not_found
    def test_get_security_details_cbcm(self, client, test_data, show_responses):
        """Test retrieving security details for CBCM/ZQ spread (from examples)."""
        details = client.sd.get_security_details(
            exchange=test_data["cme_cbcm"]["exchange"],
            date=test_data["cme_cbcm"]["date"],
            asset=test_data["cme_cbcm"]["asset"],
            security_id=test_data["cme_cbcm"]["security_id"]
        )
        assert isinstance(details, list)
        assert len(details) > 0
        # Verify expected fields from example
        first = details[0]
        assert "Name" in first
        assert "SecurityID" in first
        assert "Symbol" in first
        print(f"\n✅ Retrieved CBCM/ZQ security details: {first.get('Symbol')}")
        print_response(details, show_responses, truncate=500)

    @skip_if_not_found
    def test_get_security_details_glbx_fx(self, client, test_data, show_responses):
        """Test retrieving security details for GLBX FX futures (from examples)."""
        details = client.sd.get_security_details(
            exchange=test_data["cme_glbx"]["exchange"],
            date=test_data["cme_glbx"]["date"],
            asset=test_data["cme_glbx"]["asset"],
            security_id=test_data["cme_glbx"]["security_id"]
        )
        assert isinstance(details, list)
        assert len(details) > 0
        first = details[0]
        assert "SecurityType" in first
        assert first.get("SecurityType") == "FXSPOT"
        print(f"\n✅ Retrieved GLBX FX security: {first.get('Symbol')}")
        print_response(details, show_responses, truncate=500)


class TestAlgo:
    """Algorithm execution and management integration tests."""

    def test_list_owners(self, client):
        """Test listing algorithm owners."""
        owners = client.algo.list_owners()
        assert isinstance(owners, list)
        print(f"\n✅ Found {len(owners)} algorithm owners")

    @skip_if_not_found
    def test_list_algorithms(self, client, test_data):
        """Test listing algorithms for an owner."""
        algos = client.algo.list_algorithms(test_data["algo"]["owner"])
        assert isinstance(algos, list)
        print(f"\n✅ Found {len(algos)} algorithms for {test_data['algo']['owner']}")

    @skip_if_not_found
    def test_get_metadata(self, client, test_data):
        """Test retrieving algorithm metadata."""
        metadata = client.algo.get_metadata(
            owner=test_data["algo"]["owner"],
            algorithm=test_data["algo"]["algorithm"],
            mode="compact"
        )
        assert isinstance(metadata, dict)
        print(f"\n✅ Retrieved metadata for {test_data['algo']['algorithm']}")

    @skip_if_not_found
    def test_run_algorithm(self, client, test_data):
        """Test running an algorithm (dbag/top_level)."""
        # top_level algo requires: marketId, date, marketSegmentId, securityId
        result = client.algo.run(
            owner=test_data["algo"]["owner"],
            algorithm=test_data["algo"]["algorithm"],
            params={
                "marketId": test_data["t7"]["market_id"],
                "date": test_data["t7"]["date"],
                "marketSegmentId": test_data["t7"]["market_segment_id"],
                "securityId": str(test_data["t7"]["security_id"])
            }
        )
        # Result can be dict or list depending on algorithm
        assert isinstance(result, (dict, list))
        print(f"\n✅ Algorithm {test_data['algo']['algorithm']} executed successfully")


class TestEOBI:
    """Enhanced Order Book Interface integration tests."""

    def test_get_markets(self, client):
        """Test retrieving EOBI markets."""
        markets = client.eobi.get_markets()
        assert isinstance(markets, list)
        print(f"\n✅ Found {len(markets)} EOBI markets")

    @skip_if_not_found
    def test_get_dates(self, client, test_data):
        """Test retrieving EOBI dates."""
        dates = client.eobi.get_dates(test_data["t7"]["market_id"])
        assert isinstance(dates, list)
        print(f"\n✅ Found {len(dates)} EOBI dates")

    @skip_if_not_found
    def test_get_market_segments(self, client, test_data):
        """Test retrieving EOBI market segments."""
        segments = client.eobi.get_market_segments(
            test_data["t7"]["market_id"],
            test_data["t7"]["date"]
        )
        assert isinstance(segments, list)
        print(f"\n✅ Found {len(segments)} EOBI segments")

    @skip_if_not_found
    def test_get_transact_times(self, client, test_data):
        """Test retrieving transaction times."""
        # Using known working params: XETR/20230804/52885/2504978?limit=15
        times = client.eobi.get_transact_times(
            market_id=test_data["t7"]["market_id"],
            date=test_data["t7"]["date"],
            market_segment_id=test_data["t7"]["market_segment_id"],
            security_id=test_data["t7"]["security_id"],
            limit=15
        )
        assert isinstance(times, list)
        assert len(times) > 0
        print(f"\n✅ Found {len(times)} transaction times")


class TestMDP:
    """Market Data Platform integration tests."""

    @skip_if_not_found
    def test_get_exchanges(self, client):
        """Test retrieving MDP exchanges."""
        exchanges = client.mdp.get_exchanges()
        assert isinstance(exchanges, list)
        print(f"\n✅ Found {len(exchanges)} MDP exchanges")

    @skip_if_not_found
    def test_get_dates(self, client, test_data):
        """Test retrieving MDP dates."""
        dates = client.mdp.get_dates(test_data["cme"]["exchange"])
        assert isinstance(dates, list)
        print(f"\n✅ Found {len(dates)} MDP dates")

    @skip_if_not_found
    def test_get_assets(self, client, test_data):
        """Test retrieving MDP assets."""
        assets = client.mdp.get_assets(
            test_data["cme"]["exchange"],
            test_data["cme"]["date"]
        )
        assert isinstance(assets, list)
        print(f"\n✅ Found {len(assets)} MDP assets")


class TestOrderBook:
    """Constructed order book integration tests."""

    @skip_if_not_found
    def test_get_t7_orderbook(self, client, test_data):
        """Test retrieving T7 order book with from_time."""
        # Using known working params from transact_times
        ob = client.orderbook.get_t7(
            market_id=test_data["t7"]["market_id"],
            date=test_data["t7"]["date"],
            market_segment_id=test_data["t7"]["market_segment_id"],
            security_id=test_data["t7"]["security_id"],
            from_time=test_data["t7"]["transact_time"],
            limit=1,
            levels=10,
            orderbook="aggregated",
            trades=True,
            indicatives=False
        )
        assert isinstance(ob, dict) or isinstance(ob, list)
        print(f"\n✅ Retrieved T7 order book")

    @skip_if_not_found
    def test_get_cme_orderbook(self, client, test_data):
        """Test retrieving CME order book (may 404 if data not available)."""
        ob = client.orderbook.get_cme(
            exchange=test_data["cme"]["exchange"],
            date=test_data["cme"]["date"],
            asset=test_data["cme"]["asset"],
            security_id=test_data["cme"]["security_id"],
            limit=1,
            levels=5
        )
        assert isinstance(ob, (dict, list))
        print(f"\n✅ Retrieved CME order book")


class TestDataset:
    """Customer dataset integration tests."""

    @skip_if_not_found
    def test_list_owners(self, client):
        """Test listing dataset owners."""
        owners = client.dataset.list_owners(mode="compact")
        assert isinstance(owners, list)
        print(f"\n✅ Found {len(owners)} dataset owners")

    @skip_if_not_found
    def test_get_datasets(self, client, test_data):
        """Test listing datasets for an owner."""
        datasets = client.dataset.get_datasets(test_data["dataset"]["owner"])
        assert isinstance(datasets, list)
        print(f"\n✅ Found {len(datasets)} datasets")

    @skip_if_not_found
    def test_get_metadata(self, client, test_data):
        """Test retrieving dataset metadata (if datasets exist)."""
        datasets = client.dataset.get_datasets(test_data["dataset"]["owner"])
        if datasets:
            metadata = client.dataset.get_metadata(
                test_data["dataset"]["owner"],
                datasets[0]
            )
            assert isinstance(metadata, dict)
            print(f"\n✅ Retrieved dataset metadata")
        else:
            pytest.skip("No datasets available for testing")


class TestInsights:
    """Market insights integration tests."""

    @skip_if_not_found
    def test_get_por_market_segments(self, client):
        """Test retrieving POR market segments."""
        segments = client.insights.get_por_market_segments()
        assert isinstance(segments, list)
        # Check for known segments from examples
        known_segments = ["FOAT", "FXXP", "FGBM", "FGBS"]
        found = [s for s in known_segments if s in segments]
        print(f"\n✅ Found {len(segments)} POR market segments (known: {found})")

    @skip_if_not_found
    def test_get_por_rolls(self, client, test_data):
        """Test retrieving POR rolls for FOAT."""
        # Using known working segment: FOAT
        rolls = client.insights.get_por_rolls(test_data["insights"]["market_segment"])
        assert isinstance(rolls, list)
        print(f"\n✅ Found {len(rolls)} POR rolls for {test_data['insights']['market_segment']}")

    @skip_if_not_found
    def test_get_por_data_foat(self, client, test_data, show_responses):
        """Test retrieving POR data for FOAT/202406 (from examples)."""
        data = client.insights.get_por_data(
            market_segment=test_data["insights"]["market_segment"],
            roll=test_data["insights"]["roll"],
            days=10,
            n=20,
            comp="c"
        )
        assert isinstance(data, dict)
        # Verify expected structure from examples
        assert "dte" in data  # Days to expiry
        assert "r_0" in data  # Current roll
        assert "q_0" in data  # Quantile min
        print(f"\n✅ Retrieved POR data for {test_data['insights']['market_segment']}/{test_data['insights']['roll']}")
        print_response(data, show_responses, truncate=500)

    @skip_if_not_found
    def test_get_por_data_fgbm(self, client, show_responses):
        """Test retrieving POR data for FGBM/202412 (from examples)."""
        data = client.insights.get_por_data(
            market_segment="FGBM",
            roll=202412,
            days=10,
            n=30,
            comp="c"
        )
        assert isinstance(data, dict)
        assert "dte" in data
        # FGBM should have many historical rolls (r_0 to r_30)
        assert "r_0" in data
        print(f"\n✅ Retrieved POR data for FGBM/202412")
        print_response(data, show_responses, truncate=500)

    @skip_if_not_found
    def test_get_por_data_historical(self, client, show_responses):
        """Test retrieving historical POR data for FGBS/200306 (from examples)."""
        data = client.insights.get_por_data(
            market_segment="FGBS",
            roll=200306,
            days=10,
            n=20,
            comp="c"
        )
        assert isinstance(data, dict)
        assert "dte" in data
        print(f"\n✅ Retrieved historical POR data for FGBS/200306")
        print_response(data, show_responses, truncate=500)


class TestPrecalc:
    """Precalculation management integration tests."""

    def test_list_owners(self, client):
        """Test listing precalc owners."""
        owners = client.precalc.list_owners()
        assert isinstance(owners, list)
        print(f"\n✅ Found {len(owners)} precalc owners")

    @skip_if_not_found
    def test_get_jobs(self, client, test_data):
        """Test listing precalc jobs."""
        jobs = client.precalc.get_jobs(test_data["dataset"]["owner"])
        assert isinstance(jobs, list)
        print(f"\n✅ Found {len(jobs)} precalc jobs")

    @skip_if_not_found
    def test_get_definition(self, client, test_data):
        """Test retrieving job definition (if jobs exist)."""
        jobs = client.precalc.get_jobs(test_data["dataset"]["owner"])
        if jobs:
            definition = client.precalc.get_definition(
                test_data["dataset"]["owner"],
                jobs[0]
            )
            assert isinstance(definition, dict)
            print(f"\n✅ Retrieved job definition")
        else:
            pytest.skip("No precalc jobs available")


class TestAuction:
    """Auction simulation integration tests."""

    @skip_if_not_found
    def test_get_exchanges(self, client):
        """Test retrieving auction exchanges."""
        exchanges = client.auction.get_exchanges()
        assert isinstance(exchanges, list)
        assert "XETR" in exchanges
        print(f"\n✅ Found {len(exchanges)} auction exchanges")

    @skip_if_not_found
    def test_get_dates(self, client, test_data):
        """Test retrieving auction dates."""
        dates = client.auction.get_dates(test_data["auction"]["exchange"])
        assert isinstance(dates, list)
        print(f"\n✅ Found {len(dates)} auction dates")

    @skip_if_not_found
    def test_get_market_segments(self, client, test_data):
        """Test retrieving auction market segments."""
        segments = client.auction.get_market_segments(
            test_data["auction"]["exchange"],
            test_data["auction"]["date"],
            mode="segment"
        )
        assert isinstance(segments, list)
        print(f"\n✅ Found {len(segments)} auction segments")

    @skip_if_not_found
    def test_get_securities(self, client, test_data, show_responses):
        """Test retrieving securities for a market segment."""
        securities = client.auction.get_securities(
            test_data["auction"]["exchange"],
            test_data["auction"]["date"],
            test_data["auction"]["market_segment_id"]
        )
        assert isinstance(securities, list)
        print(f"\n✅ Found {len(securities)} securities in segment {test_data['auction']['market_segment_id']}")
        print_response(securities[:10], show_responses)

    @skip_if_not_found
    def test_get_security_reference_data(self, client, test_data, show_responses):
        """Test retrieving security reference data (from examples - TPE)."""
        # Using TPE test case from examples
        case = test_data["auction_cases"][0]  # TPE
        security = client.auction.get_security(
            exchange=case["exchange"],
            date=case["date"],
            market_segment_id=case["market_segment_id"],
            security_id=case["security_id"]
        )
        assert isinstance(security, dict)
        # Verify expected fields from examples
        assert "Exchange" in security
        assert "Symbol" in security
        assert "SecurityID" in security
        assert "Ticks" in security  # Tick size table
        assert security["Symbol"] == case["symbol"]
        print(f"\n✅ Retrieved security reference for {case['symbol']} ({case['index']})")
        print_response(security, show_responses, truncate=500)

    @skip_if_not_found
    def test_get_security_dax_stock(self, client, test_data, show_responses):
        """Test retrieving DAX stock reference data (VOW3)."""
        # Using VOW3 test case from examples
        case = test_data["auction_cases"][2]  # VOW3
        security = client.auction.get_security(
            exchange=case["exchange"],
            date=case["date"],
            market_segment_id=case["market_segment_id"],
            security_id=case["security_id"]
        )
        assert isinstance(security, dict)
        assert security.get("Index") == "DAX"
        assert "ISIN" in security
        print(f"\n✅ Retrieved DAX stock {case['symbol']}: {security.get('ISIN')}")
        print_response(security, show_responses, truncate=500)

    @skip_if_not_found
    def test_get_auction_types(self, client, test_data):
        """Test retrieving auction types for a security."""
        auction_types = client.auction.get_auction_types(
            test_data["auction"]["exchange"],
            test_data["auction"]["date"],
            test_data["auction"]["market_segment_id"],
            test_data["auction"]["security_id"]
        )
        assert isinstance(auction_types, list)
        # Common auction types
        assert any(t in auction_types for t in ["opening", "closing", "intraday"])
        print(f"\n✅ Found auction types: {auction_types}")


class TestNegativeScenarios:
    """Negative test scenarios for error handling and edge cases."""

    def test_invalid_token_returns_401(self):
        """Test that invalid token raises HTTP error."""
        from a7 import A7Client
        import os
        import httpx

        # Create client with invalid token (with proxy bypass)
        base_url = os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/")
        verify_ssl = os.getenv("A7_VERIFY_SSL", "true").lower() == "true"
        
        # Temporarily disable proxy
        orig_http = os.environ.get("HTTP_PROXY")
        orig_https = os.environ.get("HTTPS_PROXY")
        for key in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
            if key in os.environ:
                del os.environ[key]
        
        try:
            client = A7Client(token="invalid_token_12345", base_url=base_url, verify_ssl=verify_ssl)
            
            try:
                with pytest.raises((AuthenticationError, httpx.HTTPStatusError)):
                    client.rdi.get_markets()
                print("\n✅ Invalid token correctly raises authentication error")
            finally:
                client.close()
        finally:
            # Restore proxy settings
            if orig_http:
                os.environ["HTTP_PROXY"] = orig_http
            if orig_https:
                os.environ["HTTPS_PROXY"] = orig_https

    @skip_if_not_found
    def test_nonexistent_market_returns_404(self, client):
        """Test that requesting non-existent market returns 404 error."""
        import httpx
        with pytest.raises((NotFoundError, httpx.HTTPStatusError)) as exc_info:
            client.rdi.get_market_segments("INVALID_MARKET", 20200101)
        if isinstance(exc_info.value, httpx.HTTPStatusError):
            assert exc_info.value.response.status_code == 404
        print("\n✅ Non-existent market correctly raises 404 error")

    @skip_if_not_found
    def test_invalid_date_format(self, client):
        """Test that invalid date format is handled properly."""
        # This might raise ValidationError or NotFoundError depending on API
        with pytest.raises((NotFoundError, Exception)):
            client.rdi.get_market_segments("XEUR", 99999999)
        print("\n✅ Invalid date correctly raises error")

    @skip_if_not_found
    def test_nonexistent_security(self, client):
        """Test that non-existent security returns 404 error."""
        import httpx
        with pytest.raises((NotFoundError, httpx.HTTPStatusError)) as exc_info:
            client.rdi.get_security_details(
                market_id="XEUR",
                ref_date=20200227,
                segment_id=999999,
                security_id="9999999"
            )
        if isinstance(exc_info.value, httpx.HTTPStatusError):
            assert exc_info.value.response.status_code == 404
        print("\n✅ Non-existent security correctly raises 404 error")


class TestAuthentication:
    """Authentication and error handling tests."""

    def test_invalid_token_handling(self):
        """Test that invalid token raises error when accessing API."""
        from a7 import A7Client
        import os
        import httpx

        # Get same base_url as the real client to test against same API
        base_url = os.getenv("A7_BASE_URL", "https://a7.deutsche-boerse.com/api/")
        verify_ssl = os.getenv("A7_VERIFY_SSL", "true").lower() == "true"
        
        # Temporarily disable proxy for clean connection
        orig_http = os.environ.get("HTTP_PROXY")
        orig_https = os.environ.get("HTTPS_PROXY")
        for key in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
            if key in os.environ:
                del os.environ[key]
        
        try:
            client = A7Client(token="invalid_token", base_url=base_url, verify_ssl=verify_ssl)
            try:
                with pytest.raises((AuthenticationError, httpx.HTTPStatusError)):
                    client.rdi.get_markets()
                print("\n✅ Invalid token correctly raises error")
            finally:
                client.close()
        finally:
            # Restore proxy settings
            if orig_http:
                os.environ["HTTP_PROXY"] = orig_http
            if orig_https:
                os.environ["HTTPS_PROXY"] = orig_https

    def test_client_context_manager(self, client):
        """Test client works as context manager."""
        with client:
            markets = client.rdi.get_markets()
            assert isinstance(markets, list)
        print("\n✅ Context manager works correctly")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
