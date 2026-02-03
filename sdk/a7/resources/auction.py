"""Xetra Auction Simulations resource."""

from typing import Any, Optional

import httpx


class AuctionResource:
    """
    Xetra Auction Simulations API endpoints.

    Provides access to auction data and simulation capabilities for T7 exchanges.
    Simulates outcomes of opening/intraday/closing auctions with additional orders.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize Auction resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def get_exchanges(self) -> list[str]:
        """
        Get available exchanges for auction simulations.

        Returns:
            List of exchange MICs (e.g., ['XETR', 'XEUR', 'XEEE'])

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred

        Example:
            >>> exchanges = client.auction.get_exchanges()
            >>> print(exchanges)
            ['XETR', 'XEUR', 'XEEE']
        """
        response = self._client.get("/v1/simulation/auction/")
        response.raise_for_status()
        return response.json()

    def get_dates(self, exchange: str) -> list[int]:
        """
        Get available trading days for an exchange.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')

        Returns:
            List of dates in YYYYMMDD format

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Exchange not found
            ServerError: Server error occurred

        Example:
            >>> dates = client.auction.get_dates('XETR')
            >>> print(dates)
            [20230111, 20230112, 20230113, ...]
        """
        response = self._client.get(f"/v1/simulation/auction/{exchange}/")
        response.raise_for_status()
        return response.json()

    def get_market_segments(self, exchange: str, date: int, mode: str = "segment") -> list[str]:
        """
        Get market segments or symbols for a trading day.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            mode: 'segment' returns market segment IDs (default),
                  'symbol' returns trading symbols

        Returns:
            List of market segment IDs or symbols

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Exchange or date not found
            ValidationError: Invalid mode parameter
            ServerError: Server error occurred

        Example:
            >>> segments = client.auction.get_market_segments('XETR', 20230111)
            >>> print(segments)
            ['52915', '52378', '54105', ...]

            >>> symbols = client.auction.get_market_segments(
            ...     'XETR', 20230111, mode='symbol'
            ... )
            >>> print(symbols)
            ['DAX', 'SAP', 'BAYN', ...]
        """
        params = {"mode": mode}
        response = self._client.get(f"/v1/simulation/auction/{exchange}/{date}/", params=params)
        response.raise_for_status()
        return response.json()

    def get_securities(self, exchange: str, date: int, market_segment_id: int) -> list[int]:
        """
        Get security IDs for a market segment.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID

        Returns:
            List of security IDs

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> securities = client.auction.get_securities('XETR', 20230111, 52915)
            >>> print(securities)
            [2506257, 2506258, ...]
        """
        response = self._client.get(
            f"/v1/simulation/auction/{exchange}/{date}/{market_segment_id}/"
        )
        response.raise_for_status()
        return response.json()

    def get_security(
        self, exchange: str, date: int, market_segment_id: int, security_id: int
    ) -> dict[str, Any]:
        """
        Get security reference data by segment ID and security ID.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID

        Returns:
            Security reference data

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> security = client.auction.get_security(
            ...     'XETR', 20230111, 52915, 2506257
            ... )
            >>> print(security['symbol'])
        """
        response = self._client.get(
            f"/v1/simulation/auction/{exchange}/{date}/{market_segment_id}/{security_id}"
        )
        response.raise_for_status()
        return response.json()

    def get_security_by_symbol(self, exchange: str, date: int, symbol: str) -> dict[str, Any]:
        """
        Get security reference data by trading symbol.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            symbol: Trading symbol (e.g., 'DB1', 'SAP')

        Returns:
            Security reference data

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> security = client.auction.get_security_by_symbol(
            ...     'XETR', 20230111, 'DB1'
            ... )
            >>> print(security['securityID'])
        """
        response = self._client.get(f"/v1/simulation/auction/{exchange}/{date}/{symbol}")
        response.raise_for_status()
        return response.json()

    def get_auction_types(
        self,
        exchange: str,
        date: int,
        market_segment_id: int,
        security_id: int
    ) -> list[str]:
        """
        Get available auction types for a security.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID

        Returns:
            List of auction types (e.g., ['opening', 'intraday', 'closing'])

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> types = client.auction.get_auction_types(
            ...     'XETR', 20230111, 52915, 2506257
            ... )
            >>> print(types)
            ['opening', 'intraday', 'closing']
        """
        response = self._client.get(
            f"/v1/simulation/auction/{exchange}/{date}/{market_segment_id}/{security_id}/"
        )
        response.raise_for_status()
        return response.json()

    def get_auction_types_by_symbol(self, exchange: str, date: int, symbol: str) -> list[str]:
        """
        Get available auction types for a security by symbol.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            symbol: Trading symbol (e.g., 'DB1', 'SAP')

        Returns:
            List of auction types (e.g., ['opening', 'intraday', 'closing'])

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> types = client.auction.get_auction_types_by_symbol(
            ...     'XETR', 20230111, 'DB1'
            ... )
            >>> print(types)
            ['opening', 'closing']
        """
        response = self._client.get(f"/v1/simulation/auction/{exchange}/{date}/{symbol}/")
        response.raise_for_status()
        return response.json()

    def get_auction(
        self,
        exchange: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        auction_type: str,
        side: Optional[str] = None,
        px: Optional[float] = None,
        qty: Optional[int] = None,
        prio: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Get auction historical data and optionally simulate outcome.

        Retrieves historical auction data. If simulation parameters (side, px, qty)
        are provided, also simulates the auction outcome with an additional order.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID
            auction_type: Auction type ('opening', 'intraday', 'closing')
            side: Optional order side ('buy' or 'sell') for simulation
            px: Optional limit price for simulation
            qty: Optional quantity for simulation
            prio: Optional order priority for simulation

        Returns:
            Auction data including historical state and simulation results if requested

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ValidationError: Invalid simulation parameters
            ServerError: Server error occurred

        Example:
            >>> # Get historical data only
            >>> auction = client.auction.get_auction(
            ...     'XETR', 20230111, 52915, 2506257, 'opening'
            ... )

            >>> # Simulate with additional order
            >>> simulated = client.auction.get_auction(
            ...     'XETR', 20230111, 52915, 2506257, 'opening',
            ...     side='buy', px=100.50, qty=1000, prio=1
            ... )
            >>> print(simulated['simulation']['executionPrice'])
        """
        params = {}
        if side is not None:
            params["side"] = side
        if px is not None:
            params["px"] = px
        if qty is not None:
            params["qty"] = qty
        if prio is not None:
            params["prio"] = prio

        response = self._client.get(
            f"/v1/simulation/auction/{exchange}/{date}/{market_segment_id}/{security_id}/{auction_type}",
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def get_auction_by_symbol(
        self,
        exchange: str,
        date: int,
        symbol: str,
        auction_type: str,
        side: Optional[str] = None,
        px: Optional[float] = None,
        qty: Optional[int] = None,
        prio: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Get auction historical data and optionally simulate outcome by symbol.

        Retrieves historical auction data. If simulation parameters (side, px, qty)
        are provided, also simulates the auction outcome with an additional order.

        Args:
            exchange: Exchange MIC (e.g., 'XETR')
            date: Date in YYYYMMDD format
            symbol: Trading symbol (e.g., 'DB1', 'SAP')
            auction_type: Auction type ('opening', 'intraday', 'closing')
            side: Optional order side ('buy' or 'sell') for simulation
            px: Optional limit price for simulation
            qty: Optional quantity for simulation
            prio: Optional order priority for simulation

        Returns:
            Auction data including historical state and simulation results if requested

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ValidationError: Invalid simulation parameters
            ServerError: Server error occurred

        Example:
            >>> # Get historical data only
            >>> auction = client.auction.get_auction_by_symbol(
            ...     'XETR', 20230111, 'DB1', 'opening'
            ... )

            >>> # Simulate with additional order
            >>> simulated = client.auction.get_auction_by_symbol(
            ...     'XETR', 20230111, 'DB1', 'opening',
            ...     side='buy', px=15000.0, qty=10
            ... )
            >>> print(simulated['simulation']['executionPrice'])
        """
        params = {}
        if side is not None:
            params["side"] = side
        if px is not None:
            params["px"] = px
        if qty is not None:
            params["qty"] = qty
        if prio is not None:
            params["prio"] = prio

        response = self._client.get(
            f"/v1/simulation/auction/{exchange}/{date}/{symbol}/{auction_type}",
            params=params,
        )
        response.raise_for_status()
        return response.json()
