"""Order Book resource."""

from typing import Any, Optional

import httpx


class OrderBookResource:
    """
    Order Book API endpoints.

    Provides access to constructed order books from EOBI and MDP data.
    Supports both T7 markets (XEUR, XETR) and CME markets.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize Order Book resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def get_t7(
        self,
        market_id: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        limit: int = 1,
        levels: int = 10,
        orderbook: str = "aggregated",
        trades: bool = False,
        indicatives: bool = False,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get order book(s) for T7 markets (XEUR, XETR).

        Args:
            market_id: Market identifier (e.g., 'XEUR', 'XETR')
            date: Trading day in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID
            from_time: Starting timestamp (nanoseconds since 1970, optional)
                      If not provided, returns first order book of the day
            to_time: Ending timestamp (nanoseconds since 1970, optional)
            limit: Max number of order books to return (1-10000, default: 1)
                  If limit=1, returns single order book dict
                  If limit>1, returns list of order book dicts
            levels: Order book depth (default: 10)
            orderbook: 'aggregated' or 'complete' (default: 'aggregated')
            trades: Include trades (default: False)
            indicatives: Include indicative auction uncrossing (default: False)

        Returns:
            Single order book dict if limit=1, or list of order book dicts if limit>1

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Order book not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> # Get single order book at specific time
            >>> ob = client.orderbook.get_t7(
            ...     'XETR', 20230804, 52885, 2504978,
            ...     from_time='1691099685504424493',
            ...     limit=1
            ... )
            >>> print(ob['TransactTime'])

            >>> # Get multiple order books in time range
            >>> obs = client.orderbook.get_t7(
            ...     'XETR', 20230804, 52885, 2504978,
            ...     from_time='1691099685504424493',
            ...     to_time='1691127000575050335',
            ...     limit=10
            ... )
            >>> print(len(obs))
        """
        url = f"/v1/ob/{market_id}/{date}/{market_segment_id}/{security_id}"

        params: dict[str, Any] = {
            "limit": limit,
            "levels": levels,
            "orderbook": orderbook,
            "trades": trades,
            "indicatives": indicatives,
        }

        if from_time is not None:
            params["from"] = from_time
        if to_time is not None:
            params["to"] = to_time

        response = self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_cme(
        self,
        exchange: str,
        date: int,
        asset: str,
        security_id: int,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        limit: int = 1,
        levels: int = 10,
        orderbook: str = "aggregated",
        trades: bool = False,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get order book(s) for CME markets.

        Args:
            exchange: Exchange identifier (e.g., 'XCME')
            date: Trading day in YYYYMMDD format
            asset: Asset identifier (e.g., 'GE', 'BZ')
            security_id: Security ID
            from_time: Starting timestamp (nanoseconds since 1970, optional)
                      If not provided, returns first order book of the day
            to_time: Ending timestamp (nanoseconds since 1970, optional)
            limit: Max number of order books to return (1-10000, default: 1)
                  If limit=1, returns single order book dict
                  If limit>1, returns list of order book dicts
            levels: Order book depth (default: 10)
            orderbook: 'aggregated' or 'complete' (default: 'aggregated')
            trades: Include trades (default: False)

        Returns:
            Single order book dict if limit=1, or list of order book dicts if limit>1

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Order book not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> # Get single order book
            >>> ob = client.orderbook.get_cme(
            ...     'XCME', 20220915, 'BZ', 12345,
            ...     from_time='1663191900206448987',
            ...     limit=1
            ... )
        """
        url = f"/v1/ob/{exchange}/{date}/{asset}/{security_id}"

        params: dict[str, Any] = {
            "limit": limit,
            "levels": levels,
            "orderbook": orderbook,
            "trades": trades,
        }

        if from_time is not None:
            params["from"] = from_time
        if to_time is not None:
            params["to"] = to_time

        response = self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()
