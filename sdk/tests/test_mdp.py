"""Unit tests for MDP resource with mocked HTTP responses."""

import httpx
import pytest
import respx

from a7 import A7Client

# Base URL for mocking - matches DEFAULT_BASE_URL in config.py
BASE_URL = "https://a7.deutsche-boerse.com/api"


@respx.mock
def test_get_mdp_message_nyum_success(mock_client: A7Client) -> None:
    """Test successful MDP message retrieval for NYUM."""
    mock_response = {
        "Messages": [
            {"MsgSeqNum": 271039433, "SendingTime": "1663191900206448987"},
            {"blockLength": 11, "templateId": 46, "schemaId": 1, "version": 9},
            {
                "Name": "MDIncrementalRefreshBook46",
                "TemplateId": 46,
                "TransactTime": 1663191900000000000,
                "MatchEventIndicator": ["EndOfEvent"],
                "MDEntry": [],
                "OrderIDEntry": [],
            },
        ]
    }

    respx.get(f"{BASE_URL}/v1/mdp/NYUM/20220915/BZ/86054/1663191900206448987").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = mock_client.mdp.get_message(
        exchange="NYUM",
        date=20220915,
        asset="BZ",
        security_id=86054,
        sending_time="1663191900206448987",
    )

    assert "Messages" in result
    assert result["Messages"][0]["MsgSeqNum"] == 271039433
    assert result["Messages"][2]["Name"] == "MDIncrementalRefreshBook46"


@respx.mock
def test_get_mdp_message_xcbt_success(mock_client: A7Client) -> None:
    """Test successful MDP message retrieval for XCBT."""
    mock_response = {
        "Messages": [
            {"MsgSeqNum": 45778650, "SendingTime": "1749159840081860246"},
            {"blockLength": 30, "templateId": 30, "schemaId": 1, "version": 13},
            {
                "Name": "SecurityStatus30",
                "TemplateId": 30,
                "TransactTime": 1749159840000000000,
                "SecurityGroup": "#E",
                "Asset": "",
                "SecurityID": None,
                "TradeDate": 20245,
                "MatchEventIndicator": [],
                "SecurityTradingStatus": "NotAvailableForTrading",
                "HaltReason": "GroupSchedule",
                "SecurityTradingEvent": "NoEvent",
            },
        ]
    }

    respx.get(f"{BASE_URL}/v1/mdp/XCBT/20250606/00C/42037732/1749159840081860246").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = mock_client.mdp.get_message(
        exchange="XCBT",
        date=20250606,
        asset="00C",
        security_id=42037732,
        sending_time="1749159840081860246",
    )

    assert "Messages" in result
    assert result["Messages"][0]["MsgSeqNum"] == 45778650
    assert result["Messages"][2]["Name"] == "SecurityStatus30"
    assert result["Messages"][2]["SecurityTradingStatus"] == "NotAvailableForTrading"


@respx.mock
def test_get_mdp_message_not_found(mock_client: A7Client) -> None:
    """Test MDP message not found."""
    respx.get(f"{BASE_URL}/v1/mdp/NYUM/20220915/BZ/99999/1663191900206448987").mock(
        return_value=httpx.Response(404, json={"error": "Message not found"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.mdp.get_message(
            exchange="NYUM",
            date=20220915,
            asset="BZ",
            security_id=99999,
            sending_time="1663191900206448987",
        )


@respx.mock
def test_get_mdp_message_auth_error(mock_client: A7Client) -> None:
    """Test MDP message with authentication error."""
    respx.get(f"{BASE_URL}/v1/mdp/NYUM/20220915/BZ/86054/1663191900206448987").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.mdp.get_message(
            exchange="NYUM",
            date=20220915,
            asset="BZ",
            security_id=86054,
            sending_time="1663191900206448987",
        )
