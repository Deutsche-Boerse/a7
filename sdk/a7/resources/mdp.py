"""Market Data Platform (MDP) resource."""

from typing import Any, Optional

import httpx


class MDPResource:
    """
    Market Data Platform API endpoints.

    Provides access to CME MDP market data messages.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize MDP resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def get_exchanges(self) -> list[str]:
        """
        Get list of available exchanges.

        Returns:
            List of exchange codes (e.g., ['XCME', 'NYUM', 'XCBT'])

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred

        Example:
            >>> exchanges = client.mdp.get_exchanges()
            >>> print(exchanges)
            ['XCME', 'NYUM', 'XCBT']
        """
        response = self._client.get("/v1/mdp")
        response.raise_for_status()
        result = response.json()
        return result.get("Exchanges", [])

    def get_dates(self, exchange: str) -> list[int]:
        """
        Get list of available trading days for an exchange.

        Args:
            exchange: Exchange code (e.g., 'XCME', 'NYUM')

        Returns:
            List of dates in YYYYMMDD format

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Exchange not found
            ServerError: Server error occurred

        Example:
            >>> dates = client.mdp.get_dates('NYUM')
            >>> print(dates[:5])
            [20220913, 20220914, 20220915, ...]
        """
        response = self._client.get(f"/v1/mdp/{exchange}")
        response.raise_for_status()
        result = response.json()
        return result.get("Dates", [])

    def get_assets(self, exchange: str, date: int) -> list[str]:
        """
        Get list of assets for an exchange and date.

        Args:
            exchange: Exchange code (e.g., 'XCME', 'NYUM')
            date: Trading day in YYYYMMDD format

        Returns:
            List of asset codes

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Exchange or date not found
            ServerError: Server error occurred

        Example:
            >>> assets = client.mdp.get_assets('NYUM', 20220915)
            >>> print(assets)
            ['BZ', 'GE', 'CL', ...]
        """
        response = self._client.get(f"/v1/mdp/{exchange}/{date}")
        response.raise_for_status()
        result = response.json()
        return result.get("Assets", [])

    def get_securities(self, exchange: str, date: int, asset: str) -> list[int]:
        """
        Get list of security IDs for an exchange, date, and asset.

        Args:
            exchange: Exchange code (e.g., 'XCME', 'NYUM')
            date: Trading day in YYYYMMDD format
            asset: Asset code (e.g., 'BZ', 'GE')

        Returns:
            List of security IDs

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> securities = client.mdp.get_securities('NYUM', 20220915, 'BZ')
            >>> print(securities[:5])
            [86054, 86055, ...]
        """
        response = self._client.get(f"/v1/mdp/{exchange}/{date}/{asset}")
        response.raise_for_status()
        result = response.json()
        return result.get("SecurityIDs", [])

    def get_sending_times(
        self,
        exchange: str,
        date: int,
        asset: str,
        security_id: int,
        mode: str = "reference",
        limit: Optional[int] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        msgseq_num: Optional[int] = None,
        template_id: Optional[int] = None,
    ) -> list[str] | list[dict[str, Any]]:
        """
        Get list of sending times or detailed packets for a security.

        Args:
            exchange: Exchange code (e.g., 'XCME', 'NYUM')
            date: Trading day in YYYYMMDD format
            asset: Asset code (e.g., 'BZ', 'GE')
            security_id: Security ID
            mode: 'reference' returns list of times, 'detailed' returns packets
            limit: Maximum number of results (optional)
            from_time: Starting timestamp filter (optional)
            to_time: Ending timestamp filter (optional)
            msgseq_num: Message sequence number filter (optional)
            template_id: Template ID filter (optional)

        Returns:
            List of sending times if mode='reference',
            or list of packet details if mode='detailed'

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> times = client.mdp.get_sending_times(
            ...     'NYUM', 20220915, 'BZ', 86054, limit=10
            ... )
        """
        url = f"/v1/mdp/{exchange}/{date}/{asset}/{security_id}"

        params: dict[str, Any] = {"mode": mode}
        if limit is not None:
            params["limit"] = limit
        if from_time is not None:
            params["from"] = from_time
        if to_time is not None:
            params["to"] = to_time
        if msgseq_num is not None:
            params["msgSeqNum"] = msgseq_num
        if template_id is not None:
            params["templateID"] = template_id

        response = self._client.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        if mode == "detailed":
            return result.get("Packets", [])
        return result.get("SendingTimes", [])

    def get_message(
        self,
        exchange: str,
        date: int,
        asset: str,
        security_id: int,
        sending_time: int,
    ) -> dict[str, Any]:
        """
        Get MDP packet/message details by identifier.

        Args:
            exchange: Exchange code (e.g., 'XCME', 'NYUM', 'XCBT')
            date: Date in YYYYMMDD format
            asset: Asset/security group code (e.g., 'BZ', 'GE')
            security_id: Security ID (formerly msg_seq_num parameter)
            sending_time: Sending timestamp

        Returns:
            MDP packet data with Messages array

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Message not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> msg = client.mdp.get_message(
            ...     'NYUM', 20220915, 'BZ', 86054, 1663191900206448987
            ... )
            >>> print(msg['Messages'][0]['MsgSeqNum'])
            271039433
        """
        url = f"/v1/mdp/{exchange}/{date}/{asset}/{security_id}/{sending_time}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()
