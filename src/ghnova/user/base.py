"""Base class for GitHub User resource."""

from __future__ import annotations

from typing import Any


class BaseUser:
    """Base class for GitHub User resource."""

    def _get_user_endpoint(self, username: str | None, account_id: int | None) -> str:
        """Determine the user endpoint based on username or account ID.

        Args:
            username: The username of the user.
            account_id: The account ID of the user.

        Returns:
            The API endpoint for the user.
        """
        if username is None and account_id is None:
            return "/user"
        elif username is not None and account_id is None:
            return f"/users/{username}"
        elif username is None and account_id is not None:
            return f"/user/{account_id}"
        else:
            raise ValueError("Specify either username or account_id, not both.")

    def _get_user_helper(
        self, username: str | None = None, account_id: int | None = None, **kwargs: Any
    ) -> tuple[str, dict[str, Any]]:
        """Get user information.

        Args:
            username: The username of the user to retrieve. If None, retrieves the authenticated user.
            account_id: The account ID of the user to retrieve. If None, retrieves by username.
            **kwargs: Additional arguments for the request.

        Returns:
            A tuple containing the endpoint and the request arguments.
        """
        endpoint = self._get_user_endpoint(username=username, account_id=account_id)
        default_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        headers = kwargs.get("headers", {})
        headers = {**default_headers, **headers}
        kwargs["headers"] = headers

        return endpoint, kwargs

    def _update_user_endpoint(self) -> str:
        """Get the endpoint for updating the authenticated user.

        Returns:
            The API endpoint for updating the authenticated user.
        """
        return "/user"
