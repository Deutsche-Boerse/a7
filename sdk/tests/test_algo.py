"""Unit tests for Algorithm resource with mocked HTTP responses."""

import httpx
import pytest
import respx

from a7 import A7Client

# Base URL for mocking - matches DEFAULT_BASE_URL in config.py
BASE_URL = "https://a7.deutsche-boerse.com/api"


@respx.mock
def test_run_algorithm_success(mock_client: A7Client) -> None:
    """Test successful algorithm execution."""
    mock_response = {
        "status": "success",
        "data": [{"timestamp": 1234567890, "bid": 131.5, "ask": 131.52}],
    }

    respx.get(f"{BASE_URL}/v1/algo/a7/top_level/run").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = mock_client.algo.run(
        owner="a7",
        algorithm="top_level",
        params={"marketId": "XEUR", "date": 20250101, "marketSegmentId": 688, "securityId": 204934},
    )

    assert result["status"] == "success"
    assert len(result["data"]) == 1


@respx.mock
def test_run_top_level_helper(mock_client: A7Client) -> None:
    """Test top_level helper method."""
    mock_response = {"status": "success", "data": []}

    respx.get(f"{BASE_URL}/v1/algo/a7/top_level/run").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = mock_client.algo.run_top_level("XEUR", 20250101, 688, 204934)

    assert result["status"] == "success"


@respx.mock
def test_run_price_level_v2_helper(mock_client: A7Client) -> None:
    """Test PriceLevelv2 helper method."""
    mock_response = {"status": "success", "data": []}

    route = respx.get(f"{BASE_URL}/v1/algo/a7/PriceLevelv2/run").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = mock_client.algo.run_price_level_v2("XEUR", 20250101, 688, 204934, level=10)

    assert result["status"] == "success"
    assert route.called


@respx.mock
def test_run_algorithm_invalid_algorithm(mock_client: A7Client) -> None:
    """Test algorithm execution with invalid algorithm name."""
    respx.get(f"{BASE_URL}/v1/algo/a7/invalid_algo/run").mock(
        return_value=httpx.Response(404, json={"error": "Algorithm not found"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.algo.run("a7", "invalid_algo", {})


@respx.mock
def test_run_algorithm_auth_error(mock_client: A7Client) -> None:
    """Test algorithm execution with authentication error."""
    respx.get(f"{BASE_URL}/v1/algo/a7/top_level/run").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.algo.run_top_level("XEUR", 20250101, 688, 204934)


@respx.mock
def test_get_algorithm_metadata_success(mock_client: A7Client) -> None:
    """Test successful algorithm metadata retrieval."""
    mock_response = {
        "algo": "DBAG",
        "desc": "DBAG Logo",
        "params": [],
        "results": [
            {
                "name": "logo",
                "desc": "logo",
                "type": "Series",
                "fields": [
                    {"name": "x", "desc": "x", "type": "Timestamp"},
                    {"name": "DBAG", "desc": "DBAG", "type": "Int64"},
                ],
            }
        ],
        "owner": "dbag",
        "signed": True,
    }

    respx.get(f"{BASE_URL}/v1/algo/dbag/DBAG").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = mock_client.algo.get_metadata("dbag", "DBAG", mode="compact")

    assert result["algo"] == "DBAG"
    assert result["desc"] == "DBAG Logo"
    assert result["owner"] == "dbag"
    assert result["signed"] is True
    assert len(result["results"]) == 1
    assert result["results"][0]["name"] == "logo"


@respx.mock
def test_list_user_algorithms_success(mock_client: A7Client) -> None:
    """Test listing user's algorithms."""
    mock_response = {"Algos": ["ComprehensiveMarket", "VwapSummarization", "smiling_face"]}

    respx.get(f"{BASE_URL}/v1/algo/lp124").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = mock_client.algo.get_metadata("lp124", "", mode="compact")

    assert "Algos" in result
    assert isinstance(result["Algos"], list)
    assert len(result["Algos"]) > 0


@respx.mock
def test_list_algorithms_convenience_method(mock_client: A7Client) -> None:
    """Test convenience method for listing algorithms."""
    mock_response = {"Algos": ["ComprehensiveMarket", "VwapSummarization", "smiling_face"]}

    respx.get(f"{BASE_URL}/v1/algo/lp124").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    algos = mock_client.algo.list_algorithms("lp124")

    assert isinstance(algos, list)
    assert len(algos) == 3
    assert "ComprehensiveMarket" in algos
    assert "VwapSummarization" in algos
    assert "smiling_face" in algos


@respx.mock
def test_get_algorithm_metadata_not_found(mock_client: A7Client) -> None:
    """Test algorithm metadata not found."""
    respx.get(f"{BASE_URL}/v1/algo/dbag/INVALID").mock(
        return_value=httpx.Response(404, json={"error": "Algorithm not found"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.algo.get_metadata("dbag", "INVALID")
