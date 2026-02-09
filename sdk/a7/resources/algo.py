"""Algorithm execution resource."""

from typing import Any
from urllib.parse import quote_plus

import httpx


class AlgoResource:
    """
    Algorithm execution API endpoints.

    Provides access to run algorithms for data extraction and management.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize Algorithm resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def run(
        self,
        owner: str,
        algorithm: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute an algorithm with parameters.

        Args:
            owner: Algorithm owner (e.g., 'a7', 'dbag', 'lp124')
            algorithm: Algorithm name (e.g., 'top_level', 'PriceLevelv2', 'DBAG')
            params: Algorithm parameters as query parameters
                   Common params: marketId, exchange, date, marketSegmentId,
                   asset, securityId, plus any algorithm-specific params

        Returns:
            Algorithm execution result

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Algorithm not found
            ValidationError: Invalid parameters
            ServerError: Server error occurred

        Example:
            >>> result = client.algo.run(
            ...     owner='a7',
            ...     algorithm='top_level',
            ...     params={'marketId': 'XEUR', 'date': 20250101, 'securityId': '204934'}
            ... )
        """
        # URL encode algorithm name to handle special characters
        encoded_algorithm = quote_plus(algorithm)
        response = self._client.get(
            f"/v1/algo/{owner}/{encoded_algorithm}/run",
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def get_metadata(
        self,
        owner: str,
        algorithm: str = "",
        mode: str = "compact",
    ) -> dict[str, Any]:
        """
        Get algorithm metadata and configuration.

        Args:
            owner: Algorithm owner (e.g., 'a7', 'dbag', 'lp124')
            algorithm: Algorithm name (e.g., 'DBAG', 'top_level')
                      Leave empty to list all algorithms for owner
            mode: Response mode ('compact' or 'full', default: 'compact')

        Returns:
            Algorithm metadata including params, results, and code
            Or list of algorithms if algorithm name is empty: {"Algos": ["algo1", "algo2"]}

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Algorithm not found
            ServerError: Server error occurred

        Example:
            >>> # Get specific algorithm metadata
            >>> metadata = client.algo.get_metadata('dbag', 'DBAG')
            >>> print(metadata['desc'])
            'DBAG Logo'

            >>> # List all algorithms for user
            >>> algos = client.algo.get_metadata('lp124')
            >>> print(algos['Algos'])
            ['ComprehensiveMarket', 'VwapSummarization', 'smiling_face']
        """
        if algorithm:
            encoded_algorithm = quote_plus(algorithm)
            url = f"/v1/algo/{owner}/{encoded_algorithm}"
        else:
            url = f"/v1/algo/{owner}"
        response = self._client.get(url, params={"mode": mode})
        response.raise_for_status()
        return response.json()

    def list_owners(self) -> list[str]:
        """
        List all algorithm owners accessible to current user.

        Returns:
            List of owner names

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred

        Example:
            >>> owners = client.algo.list_owners()
            >>> print(owners)
            ['dbag', 'lp124', 'a7', ...]
        """
        response = self._client.get("/v1/algo")
        response.raise_for_status()
        result = response.json()
        return result.get("Owners", [])

    def list_algorithms(self, owner: str, mode: str = "compact") -> list[str]:
        """
        List all algorithms for a specific owner.

        Convenience method that calls get_metadata without algorithm name
        and extracts the algorithm list.

        Args:
            owner: Algorithm owner (e.g., 'lp124', 'dbag')
            mode: Response mode ('compact' or 'full', default: 'compact')

        Returns:
            List of algorithm names

        Raises:
            AuthenticationError: Invalid token
            NotFoundError: Owner not found
            ServerError: Server error occurred

        Example:
            >>> algos = client.algo.list_algorithms('lp124')
            >>> print(algos)
            ['ComprehensiveMarket', 'VwapSummarization', 'smiling_face']
        """
        result = self.get_metadata(owner, "", mode)
        return result.get("Algos", [])

    def run_top_level(
        self,
        market: str,
        date: int,
        market_segment_id: int,
        security_id: int,
    ) -> dict[str, Any]:
        """
        Run top_level algorithm (convenience method).

        Args:
            market: Market identifier (e.g., 'XEUR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID

        Returns:
            Top level order book data

        Example:
            >>> data = client.algo.run_top_level('XEUR', 20250101, 688, 204934)
        """
        return self.run(
            owner="a7",
            algorithm="top_level",
            params={
                "marketId": market,
                "date": date,
                "marketSegmentId": market_segment_id,
                "securityId": security_id,
            },
        )

    def run_price_level_v2(
        self,
        market: str,
        date: int,
        market_segment_id: int,
        security_id: int,
        level: int = 5,
    ) -> dict[str, Any]:
        """
        Run PriceLevelv2 algorithm for order book depth (convenience method).

        Args:
            market: Market identifier (e.g., 'XEUR')
            date: Date in YYYYMMDD format
            market_segment_id: Market segment ID
            security_id: Security ID
            level: Order book depth level (default: 5)

        Returns:
            Multi-level order book data

        Example:
            >>> data = client.algo.run_price_level_v2('XEUR', 20250101, 688, 204934, level=10)
        """
        return self.run(
            owner="a7",
            algorithm="PriceLevelv2",
            params={
                "marketId": market,
                "date": date,
                "marketSegmentId": market_segment_id,
                "securityId": security_id,
                "Level": level,
            },
        )

    def upload(
        self,
        owner: str,
        algorithm: str,
        yaml_content: str,
    ) -> dict[str, Any]:
        """
        Upload/create an algorithm with YAML source code.

        Args:
            owner: Algorithm owner
            algorithm: Algorithm name
            yaml_content: Algorithm source code in YAML format

        Returns:
            Upload response with success, saved, compiled, runnable status

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to upload for this owner
            ValidationError: Invalid YAML or algorithm configuration
            ServerError: Server error occurred

        Example:
            >>> with open('my_algo.yml', 'r') as f:
            ...     yaml_content = f.read()
            >>> result = client.algo.upload('lp124', 'my_algo', yaml_content)
            >>> print(result['success'])
            True
        """
        encoded_algorithm = quote_plus(algorithm)
        response = self._client.put(
            f"/v1/algo/{owner}/{encoded_algorithm}",
            content=yaml_content,
            headers={"Content-Type": "application/yaml"},
        )
        response.raise_for_status()
        return response.json()

    def download(
        self,
        owner: str,
        algorithm: str,
    ) -> str:
        """
        Download algorithm source code.

        Args:
            owner: Algorithm owner
            algorithm: Algorithm name

        Returns:
            Algorithm source code in YAML format

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to download this algorithm
            NotFoundError: Algorithm not found
            ServerError: Server error occurred

        Example:
            >>> yaml_code = client.algo.download('lp124', 'my_algo')
            >>> with open('downloaded_algo.yml', 'w') as f:
            ...     f.write(yaml_code)
        """
        encoded_algorithm = quote_plus(algorithm)
        response = self._client.get(f"/v1/algo/{owner}/{encoded_algorithm}/download")
        response.raise_for_status()
        return response.text

    def delete(
        self,
        owner: str,
        algorithm: str,
    ) -> dict[str, Any]:
        """
        Delete an algorithm.

        Args:
            owner: Algorithm owner
            algorithm: Algorithm name

        Returns:
            Deletion response with success status

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to delete this algorithm
            NotFoundError: Algorithm not found
            ServerError: Server error occurred

        Example:
            >>> result = client.algo.delete('lp124', 'old_algo')
            >>> print(result['success'])
            'true'
        """
        encoded_algorithm = quote_plus(algorithm)
        response = self._client.delete(f"/v1/algo/{owner}/{encoded_algorithm}")
        response.raise_for_status()
        return response.json()
