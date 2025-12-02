"""CME Security Details (SD v2) resource."""

from typing import Any

import httpx


class SDResource:
    """
    CME Reference Data API (Security Details v2) endpoints.

    Provides access to reference data for CME Group markets.
    Similar to RDI but specifically for CME exchanges.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize SD resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def get_exchanges(self) -> list[str]:
        """
        Get available CME exchanges.

        Returns:
            List of exchange identifiers (e.g., ['XCME', 'XCBT', ...])

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred

        Example:
            >>> exchanges = client.sd.get_exchanges()
            >>> print(exchanges)
            ['XCME', 'XCBT', 'XNYM', ...]
        """
        response = self._client.get("/v2/sd/")
        response.raise_for_status()
        result = response.json()
        # API returns a list directly, not wrapped in a dict
        if isinstance(result, list):
            return result
        return result.get("Exchanges", [])

    def get_dates(self, exchange: str) -> list[int]:
        """
        Get available trading days for a CME exchange.

        Args:
            exchange: Exchange identifier (e.g., 'XCME')

        Returns:
            List of dates in YYYYMMDD format

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Exchange not found
            ServerError: Server error occurred

        Example:
            >>> dates = client.sd.get_dates('XCME')
            >>> print(dates)
            [20200106, 20200107, ...]
        """
        response = self._client.get(f"/v2/sd/{exchange}/")
        response.raise_for_status()
        result = response.json()
        # API returns a list directly, not wrapped in a dict
        if isinstance(result, list):
            return result
        return result.get("Dates", [])

    def get_assets(self, exchange: str, date: int) -> list[str]:
        """
        Get available assets for a CME exchange on a trading day.

        Args:
            exchange: Exchange identifier (e.g., 'XCME')
            date: Date in YYYYMMDD format

        Returns:
            List of asset identifiers (product IDs)

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Exchange or date not found
            ServerError: Server error occurred

        Example:
            >>> assets = client.sd.get_assets('XCME', 20200106)
            >>> print(assets)
            ['GE', 'ES', 'NQ', ...]
        """
        response = self._client.get(f"/v2/sd/{exchange}/{date}/")
        response.raise_for_status()
        result = response.json()
        # API returns a list directly, not wrapped in a dict
        if isinstance(result, list):
            return result
        return result.get("Assets", [])

    def get_securities(self, exchange: str, date: int, asset: str) -> list[str]:
        """
        Get security IDs for an asset.

        Args:
            exchange: Exchange identifier (e.g., 'XCME')
            date: Date in YYYYMMDD format
            asset: Asset identifier (e.g., 'GE')

        Returns:
            List of security IDs (as strings due to Int64 compatibility)

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> securities = client.sd.get_securities('XCME', 20200106, 'GE')
            >>> print(securities)
            ['12345678', '23456789', ...]
        """
        response = self._client.get(f"/v2/sd/{exchange}/{date}/{asset}/")
        response.raise_for_status()
        result = response.json()
        # API returns a list directly, not wrapped in a dict
        if isinstance(result, list):
            return result
        return result.get("SecurityIDs", [])

    def get_all_security_details(
        self, exchange: str, date: int, asset: str
    ) -> list[dict[str, Any]]:
        """
        Get security details for all securities in an asset.

        Args:
            exchange: Exchange identifier (e.g., 'XCME')
            date: Date in YYYYMMDD format
            asset: Asset identifier (e.g., 'GE')

        Returns:
            List of security detail dictionaries for all securities

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> details = client.sd.get_all_security_details('XCME', 20200106, 'GE')
            >>> for security in details:
            ...     print(f"{security['SecurityID']}: {security['Symbol']}")
        """
        response = self._client.get(f"/v2/sd/{exchange}/{date}/{asset}")
        response.raise_for_status()
        return response.json()

    def get_security_details(
        self, exchange: str, date: int, asset: str, security_id: str
    ) -> dict[str, Any]:
        """
        Get security details for a specific security.

        Args:
            exchange: Exchange identifier (e.g., 'XCME')
            date: Date in YYYYMMDD format
            asset: Asset identifier (e.g., 'GE')
            security_id: Security ID (as string)

        Returns:
            Security details dictionary including all CME reference fields

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Resource not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> details = client.sd.get_security_details(
            ...     'XCME', 20200106, 'GE', '12345678'
            ... )
            >>> print(details['Symbol'])
            >>> print(details['MaturityDate'])
        """
        response = self._client.get(f"/v2/sd/{exchange}/{date}/{asset}/{security_id}")
        response.raise_for_status()
        return response.json()
