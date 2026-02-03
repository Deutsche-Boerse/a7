"""Reference Data Interface (RDI) v2 resource."""

from typing import Any

import httpx


class RDIResource:
    """
    Reference Data Interface v2 API endpoints.

    Provides access to market data, segments, and security details.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize RDI resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def get_markets(self) -> list[dict[str, Any]]:
        """
        Get list of available markets.

        Returns:
            List of market IDs (e.g., ['XEEE', 'XETR', 'XEUR', 'XFRA'])

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred
            ConnectionError: Connection failed

        Example:
            >>> markets = client.rdi.get_markets()
            >>> print(markets)
            ['XEUR', 'XETR', 'XFRA', 'XEEE']
        """
        response = self._client.get("/v2/rdi/")
        response.raise_for_status()
        return response.json()

    def get_market_segments(self, market_id: str, date: int) -> list[dict[str, Any]]:
        """
        Get market segments for a specific market and date.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Reference date in YYYYMMDD format

        Returns:
            List of market segment IDs

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Market not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> segments = client.rdi.get_market_segments('XEUR', 20250101)
            >>> print(len(segments))
            42
        """
        response = self._client.get(f"/v2/rdi/{market_id}/{date}/")
        response.raise_for_status()
        return response.json()

    def get_security_details(
        self,
        market_id: str,
        date: int,
        market_segment_id: int,
        security_id: int,
    ) -> dict[str, Any]:
        """
        Get detailed security information.

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Reference date in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID

        Returns:
            Security details dictionary with RDI messages

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Security not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> details = client.rdi.get_security_details('XEUR', 20250101, 688, 204934)
            >>> print(details)
        """
        response = self._client.get(f"/v2/rdi/{market_id}/{date}/{market_segment_id}/{security_id}")
        response.raise_for_status()
        return response.json()

    def get_instrument_snapshot(
        self,
        market_id: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        msg_seq_num: int,
    ) -> list[dict[str, Any]]:
        """
        Get RDI v2 instrument snapshot message.

        Args:
            market_id: Market identifier (e.g., 'XETR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID
            msg_seq_num: Message sequence number

        Returns:
            List of instrument snapshot messages

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Snapshot not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> snapshot = client.rdi.get_instrument_snapshot(
            ...     'XETR', 20201104, 52162, 2504233, 106
            ... )
            >>> print(snapshot[0]['Template'])
            'InstrumentSnapshot'
        """
        response = self._client.get(
            f"/v2/rdi/{market_id}/{date}/{market_segment_id}/{security_id}/{msg_seq_num}"
        )
        response.raise_for_status()
        return response.json()
