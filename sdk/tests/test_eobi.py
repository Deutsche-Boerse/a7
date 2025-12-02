"""Unit tests for EOBI resource with mocked HTTP responses."""

import httpx
import pytest
import respx

from a7 import A7Client

# Base URL for mocking - matches DEFAULT_BASE_URL in config.py
BASE_URL = "https://a7.deutsche-boerse.com/api"


@respx.mock
def test_get_eobi_message_success(mock_client: A7Client) -> None:
    """Test successful EOBI message retrieval."""
    mock_response = {
        "MessageHeader": {
            "BodyLen": 24,
            "TemplateID": 13300,
            "MsgSeqNum": 23,
        },
        "TransactTime": "1582821000143010121",
        "TradingSessionID": 5,
        "TradingSessionSubID": 5,
        "TradSesStatus": 2,
        "MarketCondition": 0,
        "FastMarketIndicator": 0,
    }

    respx.get(
        f"{BASE_URL}/v1/eobi/XEUR/20200227/187421/72862561103511553/1582821000143045889/14687296/23"
    ).mock(return_value=httpx.Response(200, json=mock_response))

    result = mock_client.eobi.get_message(
        market_id="XEUR",
        date=20200227,
        market_segment_id=187421,
        security_id=72862561103511553,
        transact_time="1582821000143045889",
        applseq_num=14687296,
        msg_seq_num=23,
    )

    assert result["MessageHeader"]["TemplateID"] == 13300
    assert result["MessageHeader"]["MsgSeqNum"] == 23
    assert result["TradingSessionID"] == 5


@respx.mock
def test_get_eobi_message_not_found(mock_client: A7Client) -> None:
    """Test EOBI message not found."""
    respx.get(
        f"{BASE_URL}/v1/eobi/XEUR/20200227/187421/72862561103511553/1582821000143045889/14687296/999"
    ).mock(return_value=httpx.Response(404, json={"error": "Message not found"}))

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.eobi.get_message(
            market_id="XEUR",
            date=20200227,
            market_segment_id=187421,
            security_id=72862561103511553,
            transact_time="1582821000143045889",
            applseq_num=14687296,
            msg_seq_num=999,
        )


@respx.mock
def test_get_eobi_message_auth_error(mock_client: A7Client) -> None:
    """Test EOBI message with authentication error."""
    respx.get(
        f"{BASE_URL}/v1/eobi/XEUR/20200227/187421/72862561103511553/1582821000143045889/14687296/23"
    ).mock(return_value=httpx.Response(401, json={"error": "Unauthorized"}))

    with pytest.raises(httpx.HTTPStatusError):
        mock_client.eobi.get_message(
            market_id="XEUR",
            date=20200227,
            market_segment_id=187421,
            security_id=72862561103511553,
            transact_time="1582821000143045889",
            applseq_num=14687296,
            msg_seq_num=23,
        )
