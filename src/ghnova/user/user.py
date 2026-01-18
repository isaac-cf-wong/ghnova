"""GitHub User resource."""

from __future__ import annotations

from typing import Any

from requests import Response

from ghnova.resource.resource import Resource
from ghnova.user.base import BaseUser


class User(BaseUser, Resource):
    """GitHub User resource."""

    def _get_user(
        self,
        username: str | None = None,
        account_id: int | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> Response:
        """Get user information.

        Args:
            username: The username of the user to retrieve. If None, retrieves the authenticated user.
            user_id
            **kwargs: Additional arguments for the request.

        Returns:
            The response object.
        """
        endpoint, kwargs = self._get_user_helper(username=username, account_id=account_id, **kwargs)
        return self._get(endpoint=endpoint, etag=etag, last_modified=last_modified, **kwargs)

    def get_user(
        self,
        username: str | None = None,
        account_id: int | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> tuple[dict[str, Any], int, str | None, str | None]:
        """Get user information.

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
        response = self._get_user(
            username=username, account_id=account_id, etag=etag, last_modified=last_modified, **kwargs
        )
        status_code = response.status_code
        etag_value = response.headers.get("ETag")
        last_modified_value = response.headers.get("Last-Modified")
        data = response.json() if status_code == 200 else {}  # noqa: PLR2004

        return data, status_code, etag_value, last_modified_value
