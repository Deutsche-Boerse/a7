"""Unit tests for RDI resource with mocked HTTP responses."""

import httpx
import pytest
import respx

from a7 import A7Client

# Base URL for mocking - matches DEFAULT_BASE_URL in config.py
BASE_URL = "https://a7.deutsche-boerse.com/api"


@respx.mock
def test_get_markets_success(mock_client: A7Client) -> None:
    """Test successful market retrieval."""
    mock_response = [
        {"marketId": "XEUR", "name": "Eurex"},
        {"marketId": "XETR", "name": "Xetra"},
    ]

    respx.get(f"{BASE_URL}/v2/rdi/").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    markets = mock_client.rdi.get_markets()

    assert len(markets) == 2
    assert markets[0]["marketId"] == "XEUR"
    assert markets[1]["marketId"] == "XETR"


@respx.mock
def test_get_market_segments_success(mock_client: A7Client) -> None:
    """Test successful market segments retrieval."""
    mock_response = [
        {"segmentId": 688, "name": "FGBL"},
        {"segmentId": 689, "name": "FDAX"},
    ]

    respx.get(f"{BASE_URL}/v2/rdi/XEUR/20250101/").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    segments = mock_client.rdi.get_market_segments("XEUR", 20250101)

    assert len(segments) == 2
    assert segments[0]["segmentId"] == 688


@respx.mock
def test_get_security_details_success(mock_client: A7Client) -> None:
    """Test successful security details retrieval."""
    mock_response = {
        "instrumentId": "204934",
        "name": "FGBL MAR25",
        "segmentId": 688,
    }

    respx.get(f"{BASE_URL}/v2/rdi/XEUR/20250101/688/204934").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    details = mock_client.rdi.get_security_details("XEUR", 20250101, 688, "204934")

    assert details["instrumentId"] == "204934"
    assert details["segmentId"] == 688


@respx.mock
def test_rdi_authorization_header(mock_client: A7Client) -> None:
    """Test that requests include proper Authorization header."""
    route = respx.get(f"{BASE_URL}/v2/rdi/").mock(
        return_value=httpx.Response(200, json=[])
    )

    mock_client.rdi.get_markets()

    # Verify Authorization header was included
    assert route.called
    request = route.calls.last.request
    assert "Authorization" in request.headers
    assert request.headers["Authorization"].startswith("Bearer")


@respx.mock
def test_get_instrument_snapshot_success(mock_client: A7Client) -> None:
    """Test successful instrument snapshot retrieval."""
    mock_response = [
        {
            "Template": "InstrumentSnapshot",
            "MsgType": "d",
            "MsgSeqNum": 106,
            "SecurityID": "2504233",
            "SecurityIDSource": "M",
            "SecurityType": "CS",
            "SecurityStatus": "1",
            "SecurityDesc": "TMC CONTENT GR.AG INH.SF1",
            "SecurityExchange": "XFRA",
            "ProductComplex": "1",
            "InstrumentPricePrecision": 4,
            "MinPriceIncrement": 0.0001,
        }
    ]

    respx.get(f"{BASE_URL}/v2/rdi/XETR/20201104/52162/2504233/106").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    snapshot = mock_client.rdi.get_instrument_snapshot("XETR", 20201104, 52162, 2504233, 106)

    assert len(snapshot) == 1
    assert snapshot[0]["Template"] == "InstrumentSnapshot"
    assert snapshot[0]["SecurityID"] == "2504233"
    assert snapshot[0]["MsgSeqNum"] == 106
    assert snapshot[0]["SecurityType"] == "CS"


@respx.mock
def test_get_instrument_snapshot_not_found(mock_client: A7Client) -> None:
    """Test instrument snapshot not found."""
    respx.get(f"{BASE_URL}/v2/rdi/XETR/20201104/52162/9999999/106").mock(
        return_value=httpx.Response(404, json={"error": "Snapshot not found"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.rdi.get_instrument_snapshot("XETR", 20201104, 52162, 9999999, 106)
