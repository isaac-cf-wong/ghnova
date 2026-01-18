"""GitHub API client implementation."""

from __future__ import annotations

from typing import Any

import requests
from requests import Response

from ghnova.client.base import Client


class GitHub(Client):
    """Synchronous GitHub API client."""

    def __init__(self, token: str | None = None, base_url: str = "https://github.com") -> None:
        """Initialize the GitHub client.

        Args:
            token: The API token for authentication.
            base_url: The base URL of the GitHub instance.
        """
        super().__init__(token=token, base_url=base_url)
        self.session: requests.Session | None = None

    def __str__(self) -> str:
        """Return a string representation of the GitHub client.

        Returns:
            str: String representation.
        """
        return f"<GitHub base_url={self.base_url}>"

    def __enter__(self) -> GitHub:
        """Enter the context manager.

        Returns:
            The GitHub client instance.
        """
        if self.session is not None:
            raise RuntimeError("GitHub session already open; do not re-enter context manager.")
        self.session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager.

        Args:
            exc_type: The exception type.
            exc_val: The exception value.
            exc_tb: The traceback.
        """
        if self.session:
            self.session.close()
            self.session = None

    def _request(
        self, method: str, endpoint: str, headers: dict | None = None, timeout: int = 30, **kwargs: Any
    ) -> Response:
        """Make an HTTP request to the GitHub API.

        Args:
            method: The HTTP method (GET, POST, etc.).
            endpoint: The API endpoint.
            headers: Additional headers for the request.
            timeout: Timeout for the request in seconds.
            **kwargs: Additional arguments for the request.

        Returns:
            The HTTP response.
        """
        if self.session is None:
            raise RuntimeError(
                "GitHub must be used as a context manager. "
                + "Use 'with GitHub(...) as client:' to ensure proper resource cleanup."
            )
        url = self._build_url(endpoint=endpoint)
        response = self.session.request(
            method, url, headers={**self.headers, **(headers or {})}, timeout=timeout, **kwargs
        )
        response.raise_for_status()

        return response
