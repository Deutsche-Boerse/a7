"""Precalculation Management resource."""

from typing import Any

import httpx


class PrecalcResource:
    """
    Precalculation Management API endpoints.

    Provides access to precalc job management and results.
    Precalc jobs generate datasets that can be accessed via the Dataset API.
    """

    def __init__(self, client: httpx.Client) -> None:
        """
        Initialize Precalc resource.

        Args:
            client: Configured httpx client
        """
        self._client = client

    def list_owners(self) -> list[str]:
        """
        List precalc owners accessible to current user.

        Returns:
            List of owner names

        Raises:
            AuthenticationError: Invalid token
            ServerError: Server error occurred

        Example:
            >>> owners = client.precalc.list_owners()
            >>> print(owners)
            ['owner1', 'owner2', ...]
        """
        response = self._client.get("/v1/precalc")
        response.raise_for_status()
        result = response.json()
        return result.get("Owners", [])

    def get_jobs(self, owner: str) -> list[str]:
        """
        Get list of precalc jobs for an owner.

        Args:
            owner: Owner identifier

        Returns:
            List of precalc job names

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to access this owner
            NotFoundError: Owner not found
            ServerError: Server error occurred

        Example:
            >>> jobs = client.precalc.get_jobs('owner1')
            >>> print(jobs)
            ['job1', 'job2', ...]
        """
        response = self._client.get(f"/v1/precalc/{owner}")
        response.raise_for_status()
        result = response.json()
        return result.get("Jobs", [])

    def get_definition(self, owner: str, precalc: str) -> dict[str, Any]:
        """
        Get precalc job definition.

        Args:
            owner: Owner identifier
            precalc: Precalc job name

        Returns:
            Job definition including configuration and parameters

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to access this job
            NotFoundError: Job not found
            ServerError: Server error occurred

        Example:
            >>> definition = client.precalc.get_definition('owner1', 'job1')
            >>> print(definition['active'])
        """
        response = self._client.get(f"/v1/precalc/{owner}/{precalc}")
        response.raise_for_status()
        return response.json()

    def create(
        self,
        owner: str,
        precalc: str,
        definition: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create a new precalc job.

        Note: Updating existing jobs is not supported. To update, delete the
        existing job first and then create it again.

        Args:
            owner: Owner identifier
            precalc: Precalc job name
            definition: Job definition as dictionary (will be sent as JSON)

        Returns:
            Success message

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to create jobs for this owner
            ValidationError: Invalid job definition
            ServerError: Server error occurred

        Example:
            >>> result = client.precalc.create(
            ...     'owner1', 'new_job',
            ...     {'algo': 'my_algo', 'params': {...}}
            ... )
            >>> print(result['success'])
        """
        response = self._client.put(
            f"/v1/precalc/{owner}/{precalc}",
            json=definition,
        )
        response.raise_for_status()
        return response.json()

    def delete(self, owner: str, precalc: str) -> dict[str, Any]:
        """
        Delete a precalc job.

        Note: Associated datasets are not deleted automatically.
        Use the Dataset API to delete them separately.

        Args:
            owner: Owner identifier
            precalc: Precalc job name

        Returns:
            Success message

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to delete this job
            NotFoundError: Job not found
            ServerError: Server error occurred

        Example:
            >>> result = client.precalc.delete('owner1', 'old_job')
            >>> print(result['success'])
        """
        response = self._client.delete(f"/v1/precalc/{owner}/{precalc}")
        response.raise_for_status()
        return response.json()

    def activate(self, owner: str, precalc: str) -> dict[str, Any]:
        """
        Activate a precalc job.

        Args:
            owner: Owner identifier
            precalc: Precalc job name

        Returns:
            Success message

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to activate this job
            NotFoundError: Job not found
            ServerError: Server error occurred

        Example:
            >>> result = client.precalc.activate('owner1', 'job1')
            >>> print(result['success'])
        """
        response = self._client.patch(f"/v1/precalc/{owner}/{precalc}/activate")
        response.raise_for_status()
        return response.json()

    def deactivate(self, owner: str, precalc: str) -> dict[str, Any]:
        """
        Deactivate a precalc job.

        Args:
            owner: Owner identifier
            precalc: Precalc job name

        Returns:
            Success message

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to deactivate this job
            NotFoundError: Job not found
            ServerError: Server error occurred

        Example:
            >>> result = client.precalc.deactivate('owner1', 'job1')
            >>> print(result['success'])
        """
        response = self._client.patch(f"/v1/precalc/{owner}/{precalc}/deactivate")
        response.raise_for_status()
        return response.json()

    def get_dates(self, owner: str, precalc: str) -> list[int]:
        """
        Get available dates where tasks exist for a precalc job.

        Args:
            owner: Owner identifier
            precalc: Precalc job name

        Returns:
            List of dates in YYYYMMDD format

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to access this job
            NotFoundError: Job not found
            ServerError: Server error occurred

        Example:
            >>> dates = client.precalc.get_dates('owner1', 'job1')
            >>> print(dates)
            [20210301, 20210302, ...]
        """
        # Note: OpenAPI shows trailing slash for this endpoint
        response = self._client.get(f"/v1/precalc/{owner}/{precalc}/")
        response.raise_for_status()
        result = response.json()
        return result.get("Dates", [])

    def get_tasks(self, owner: str, precalc: str, date: int) -> list[str]:
        """
        Get available tasks for a precalc job on a specific date.

        Args:
            owner: Owner identifier
            precalc: Precalc job name
            date: Date in YYYYMMDD format

        Returns:
            List of task names

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to access this job
            NotFoundError: Job or date not found
            ServerError: Server error occurred

        Example:
            >>> tasks = client.precalc.get_tasks('owner1', 'job1', 20210301)
            >>> print(tasks)
            ['task1', 'task2', ...]
        """
        response = self._client.get(f"/v1/precalc/{owner}/{precalc}/{date}")
        response.raise_for_status()
        result = response.json()
        return result.get("Tasks", [])

    def get_results(self, owner: str, precalc: str, date: int, task: str) -> list[str]:
        """
        Get available result sets for a specific task.

        Args:
            owner: Owner identifier
            precalc: Precalc job name
            date: Date in YYYYMMDD format
            task: Task name

        Returns:
            List of result set names

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to access this job
            NotFoundError: Job, date, or task not found
            ServerError: Server error occurred

        Example:
            >>> results = client.precalc.get_results('owner1', 'job1', 20210301, 'task1')
            >>> print(results)
            ['result1', 'result2', ...]
        """
        response = self._client.get(f"/v1/precalc/{owner}/{precalc}/{date}/{task}")
        response.raise_for_status()
        result = response.json()
        return result.get("Results", [])

    def get_data(
        self,
        owner: str,
        precalc: str,
        date: int,
        task: str,
        result: str,
        mode: str = "json",
    ) -> dict[str, Any]:
        """
        Get generated data for a specific result set.

        Args:
            owner: Owner identifier
            precalc: Precalc job name
            date: Date in YYYYMMDD format
            task: Task name
            result: Result set name
            mode: 'json' or 'raw' (default: 'json')

        Returns:
            Generated data for the result set

        Raises:
            AuthenticationError: Invalid token
            ForbiddenError: Not authorized to access this job
            NotFoundError: Resource not found
            ServerError: Server error occurred

        Example:
            >>> data = client.precalc.get_data(
            ...     'owner1', 'job1', 20210301, 'task1', 'result1'
            ... )
            >>> print(data)
        """
        url = f"/v1/precalc/{owner}/{precalc}/{date}/{task}/{result}"
        params = {"mode": mode}

        response = self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()
