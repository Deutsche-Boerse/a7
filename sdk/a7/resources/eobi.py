"""Enhanced Order Book Interface (EOBI) resource."""

from typing import Any, Optional

import httpx


class EOBIResource:
    """
    Enhanced Order Book Interface API endpoints.

    Provides access to EOBI market data messages for T7 markets.
    EOBI provides the most granular un-normalized historical order book data.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize EOBI resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def get_markets(self) -> list[str]:
        """
        Get list of available markets.

        Returns:
            List of market IDs (e.g., ['XEUR', 'XETR'])

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred

        Example:
            >>> markets = client.eobi.get_markets()
            >>> print(markets)
            ['XEUR', 'XETR']
        """
        response = self._client.get("/v1/eobi")
        response.raise_for_status()
        result = response.json()
        return result.get("MarketIDs", [])

    def get_dates(self, market_id: str) -> list[int]:
        """
        Get list of available trading days for a market.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')

        Returns:
            List of dates in YYYYMMDD format

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Market not found
            ServerError: Server error occurred

        Example:
            >>> dates = client.eobi.get_dates('XEUR')
            >>> print(dates[:5])
            [20200629, 20200630, 20200701, ...]
        """
        response = self._client.get(f"/v1/eobi/{market_id}")
        response.raise_for_status()
        result = response.json()
        return result.get("Dates", [])

    def get_market_segments(self, market_id: str, date: int) -> list[int]:
        """
        Get list of market segments (products) for a market and date.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Trading day in YYYYMMDD format

        Returns:
            List of market segment IDs

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Market or date not found
            ServerError: Server error occurred

        Example:
            >>> segments = client.eobi.get_market_segments('XEUR', 20200227)
            >>> print(segments)
            [3, 5, 21, 688, ...]
        """
        response = self._client.get(f"/v1/eobi/{market_id}/{date}")
        response.raise_for_status()
        result = response.json()
        return result.get("MarketSegmentIDs", [])

    def get_securities(self, market_id: str, date: int, market_segment_id: int) -> list[int]:
        """
        Get list of securities for a market, date, and segment.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Trading day in YYYYMMDD format
            market_segment_id: Market segment ID

        Returns:
            List of security IDs

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Market, date, or segment not found
            ServerError: Server error occurred

        Example:
            >>> securities = client.eobi.get_securities('XETR', 20230804, 52885)
            >>> print(securities[:5])
            [2504978, 2346321, ...]
        """
        response = self._client.get(f"/v1/eobi/{market_id}/{date}/{market_segment_id}")
        response.raise_for_status()
        result = response.json()
        return result.get("SecurityIDs", [])

    def get_transact_times(
        self,
        market_id: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        mode: str = "reference",
        limit: Optional[int] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        applseq_filter: Optional[str] = None,
    ) -> list[str]:
        """
        Get list of transaction times for a security.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Trading day in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID
            mode: 'reference' or 'detailed' (default: 'reference')
            limit: Maximum number of results (optional)
            from_time: Starting timestamp filter (optional)
            to_time: Ending timestamp filter (optional)
            applseq_filter: Application sequence number filter (optional)

        Returns:
            List of transaction times (nanoseconds since 1970)

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> times = client.eobi.get_transact_times(
            ...     'XETR', 20230804, 52885, 2504978, limit=15
            ... )
            >>> print(times[:5])
            ['1691099685504424493', '1691127000575050335', ...]
        """
        url = f"/v1/eobi/{market_id}/{date}/{market_segment_id}/{security_id}"

        params: dict[str, Any] = {}
        if mode is not None:
            params["mode"] = mode
        if limit is not None:
            params["limit"] = limit
        if from_time is not None:
            params["from"] = from_time
        if to_time is not None:
            params["to"] = to_time
        if applseq_filter is not None:
            params["applSeqNumFilter"] = applseq_filter

        response = self._client.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        return result.get("TransactTimes", [])

    def get_applseq_nums(
        self,
        market_id: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        transact_time: str,
        mode: str = "reference",
        msgseq_filter: Optional[str] = None,
        template_id_filter: Optional[str] = None,
    ) -> list[int] | list[dict[str, Any]]:
        """
        Get list of application sequence numbers or detailed packets.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Trading day in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID
            transact_time: Transaction time (nanoseconds since 1970)
            mode: 'reference' returns list of numbers, 'detailed' returns packets
            msgseq_filter: Message sequence number filter (optional)
            template_id_filter: Template ID filter (optional)

        Returns:
            List of ApplSeqNum values if mode='reference',
            or list of packet details if mode='detailed'

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> nums = client.eobi.get_applseq_nums(
            ...     'XEUR', 20200227, 187421, 72862561103511553,
            ...     '1582821000143045889'
            ... )
        """
        url = f"/v1/eobi/{market_id}/{date}/{market_segment_id}/{security_id}/{transact_time}"

        params: dict[str, Any] = {"mode": mode}
        if msgseq_filter is not None:
            params["msgSeqNumFilter"] = msgseq_filter
        if template_id_filter is not None:
            params["templateIdFilter"] = template_id_filter

        response = self._client.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        if mode == "detailed":
            return result.get("Packets", [])
        return result.get("ApplSeqNums", [])

    def get_msg_seq_nums(
        self,
        market_id: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        transact_time: str,
        applseq_num: int,
        mode: str = "reference",
        template_id_filter: Optional[str] = None,
    ) -> list[int] | list[dict[str, Any]]:
        """
        Get list of message sequence numbers or detailed messages.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Trading day in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID
            transact_time: Transaction time (nanoseconds since 1970)
            applseq_num: Application sequence number
            mode: 'reference' returns list of numbers, 'detailed' returns messages
            template_id_filter: Template ID filter (optional)

        Returns:
            List of MsgSeqNum values if mode='reference',
            or list of message details if mode='detailed'

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> nums = client.eobi.get_msg_seq_nums(
            ...     'XEUR', 20200227, 187421, 72862561103511553,
            ...     '1582821000143045889', 14687296
            ... )
        """
        url = f"/v1/eobi/{market_id}/{date}/{market_segment_id}/{security_id}/{transact_time}/{applseq_num}"

        params: dict[str, Any] = {"mode": mode}
        if template_id_filter is not None:
            params["templateIdFilter"] = template_id_filter

        response = self._client.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        if mode == "detailed":
            return result.get("Messages", [])
        return result.get("MsgSeqNums", [])

    def get_message(
        self,
        market_id: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        transact_time: str,
        applseq_num: int,
        msg_seq_num: int,
    ) -> dict[str, Any]:
        """
        Get EOBI message details by full identifier.

        Args:
            market_id: Market identifier (e.g., 'XEUR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID (formerly partition_id)
            security_id: Security ID (formerly packet_seq_num)
            transact_time: Transaction timestamp (nanoseconds since 1970)
            applseq_num: Application sequence number
            msg_seq_num: Message sequence number

        Returns:
            EOBI message data with MessageHeader and message-specific fields

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Message not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> msg = client.eobi.get_message(
            ...     'XEUR', 20200227, 187421, 72862561103511553,
            ...     '1582821000143045889', 14687296, 23
            ... )
            >>> print(msg['MessageHeader']['TemplateID'])
            13300
        """
        url = f"/v1/eobi/{market_id}/{date}/{market_segment_id}/{security_id}/{transact_time}/{applseq_num}/{msg_seq_num}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()
