"""Insights resource."""

from typing import Any

import httpx


class InsightsResource:
    """
    Market Data Insights API endpoints.

    Provides access to pre-defined market data benchmarks including:
    - Pace of the Roll (POR): Open interest metrics for roll timing
    - Latency Histograms: Market participants' reaction time analysis
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize Insights resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def get_por_market_segments(self) -> list[str]:
        """
        Get list of market segments available for Pace of the Roll analysis.

        Returns:
            List of market segment names (e.g., ['FDAX', 'FGBL', ...])

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred

        Example:
            >>> segments = client.insights.get_por_market_segments()
            >>> print(segments)
            ['FDAX', 'FGBL', 'OGBL', ...]
        """
        response = self._client.get("/v1/insights/por")
        response.raise_for_status()
        result = response.json()
        return result.get("MarketSegments", [])

    def get_por_rolls(self, market_segment: str) -> list[int]:
        """
        Get list of available rolls for a market segment.

        Args:
            market_segment: Market segment name (e.g., 'FDAX', 'FGBL')

        Returns:
            List of rolls in YYYYMM format

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Market segment not found
            ServerError: Server error occurred

        Example:
            >>> rolls = client.insights.get_por_rolls('FDAX')
            >>> print(rolls)
            [202101, 202102, 202103, ...]
        """
        response = self._client.get(f"/v1/insights/por/{market_segment}")
        response.raise_for_status()
        result = response.json()
        return result.get("Rolls", [])

    def get_por_data(
        self,
        market_segment: str,
        roll: int,
        days: int = 10,
        n: int = 20,
        comp: str = "c",
    ) -> dict[str, Any]:
        """
        Get Pace of the Roll details for a specific roll.

        Provides open interest ratios and quantiles for roll timing analysis.
        The roll ratio is calculated as: back-month OI / (front-month OI + back-month OI)

        Args:
            market_segment: Market segment name (e.g., 'FDAX', 'FGBL')
            roll: Roll identifier in YYYYMM format (e.g., 202103)
            days: Number of days till expiry including expiry day (1-31, default: 10)
            n: Maximum number of previous rolls for quantile calculation (default: 20)
            comp: Comparison method:
                  'c' = consecutive (Jun-2012, Mar-2012, Dec-2011, ...)
                  's' = same month (Sep-2011, Sep-2010, Sep-2009, ...)
                  (default: 'c')

        Returns:
            Roll details with current (r_0), previous (r_1, r_2, ..., r_n) rolls
            and quantiles (q_0=min, q_1=10%, q_2=25%, q_3=75%, q_4=90%, q_5=max)

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Market segment or roll not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> data = client.insights.get_por_data('FDAX', 202103, days=15, n=30)
            >>> print(data['r_0'])  # Current roll data
            >>> print(data['quantiles'])  # Historical quantiles
        """
        url = f"/v1/insights/por/{market_segment}/{roll}"
        params = {"days": days, "n": n, "comp": comp}

        response = self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_latency_histogram(
        self,
        date: int,
        trigger: str,
        target: str,
        regime: str,
        target_action: str,
        format: str = "json",
    ) -> dict[str, Any] | str:
        """
        Get latency histogram for market participants' reaction times.

        Visualizes the distribution of reaction times based on HPT timestamps.
        Measures from when a market data update for trigger product leaves
        Deutsche Börse's network (t_9d) to when requests for target product
        reach the outer layer of the network (t_3a).

        Args:
            date: Trading day in YYYYMMDD format
            trigger: Trigger product identifier (e.g., 'FDAX')
            target: Target product identifier (e.g., 'FGBL')
            regime: Latency interval regime:
                    'fast' = up to 500 ns wire-to-wire latency, 1 ns resolution
                    'slow' = up to 50 μs wire-to-wire latency, 100 ns resolution
            target_action: Type of target action:
                          'new' = new order
                          'modify' = order modification
                          'delete' = order deletion
            format: 'json' or 'csv' (default: 'json')

        Returns:
            Latency histogram data as dict (JSON) or CSV string

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Data not found for specified parameters
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> histogram = client.insights.get_latency_histogram(
            ...     date=20210315,
            ...     trigger='FDAX',
            ...     target='FGBL',
            ...     regime='fast',
            ...     target_action='new'
            ... )
            >>> print(histogram['latencies'])
        """
        url = f"/v1/insights/latencies/{date}/{trigger}/{target}/{regime}/{target_action}"
        params = {"format": format}

        response = self._client.get(url, params=params)
        response.raise_for_status()

        if format == "csv":
            return response.text
        return response.json()
