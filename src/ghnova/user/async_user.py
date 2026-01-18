"""Asynchronous User Resource for GitHub API."""

from __future__ import annotations

from typing import Any

from aiohttp import ClientResponse

from ghnova.resource.async_resource import AsyncResource
from ghnova.user.base import BaseUser


class AsyncUser(BaseUser, AsyncResource):
    """GitHub Asynchronous User resource."""

    async def _get_user(
        self,
        username: str | None = None,
        account_id: int | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> ClientResponse:
        """Asynchronously get user information.

        Args:
            username: The username of the user to retrieve. If None, retrieves the authenticated user.
            account_id: The account ID of the user to retrieve. If None, retrieves by username.
            etag: The ETag value for conditional requests.
            last_modified: The Last-Modified timestamp for conditional requests.
            **kwargs: Additional arguments for the request.

        Returns:
            The ClientResponse object.
        """
        endpoint, kwargs = self._get_user_helper(username=username, account_id=account_id, **kwargs)
        return await self._get(endpoint=endpoint, etag=etag, last_modified=last_modified, **kwargs)

    async def get_user(
        self,
        username: str | None = None,
        account_id: int | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> tuple[dict[str, Any], int, str | None, str | None]:
        """Asynchronously get user information.

        Args:
            username: The username of the user to retrieve. If None, retrieves the authenticated user.
            account_id: The account ID of the user to retrieve. If None, retrieves by username.
            etag: The ETag value for conditional requests.
            last_modified: The Last-Modified timestamp for conditional requests.
            **kwargs: Additional arguments for the request.

        Returns:
            A tuple containing:
                - A dictionary with user information (empty if 304 Not Modified).
                - The HTTP status code.
                - The ETag value from the response headers (if present).
                - The Last-Modified timestamp from the response headers (if present).
        """
        response = await self._get_user(
            username=username, account_id=account_id, etag=etag, last_modified=last_modified, **kwargs
        )
        status_code = response.status
        etag_value = response.headers.get("ETag")
        last_modified_value = response.headers.get("Last-Modified")

        data = await response.json() if status_code == 200 else {}  # noqa: PLR2004

        return data, status_code, etag_value, last_modified_value
