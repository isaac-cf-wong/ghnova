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

    def _update_user_helper(  # noqa: PLR0913
        self,
        name: str | None,
        email: str | None,
        blog: str | None,
        twitter_username: str | None,
        company: str | None,
        location: str | None,
        hirable: str | None,
        bio: str | None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, str], dict[str, Any]]:
        """Get the endpoint and arguments for updating the authenticated user.

        Args:
            name: The name of the user.
            email: The email of the user.
            blog: The blog URL of the user.
            twitter_username: The Twitter username of the user.
            company: The company of the user.
            location: The location of the user.
            hirable: The hirable status of the user.
            bio: The bio of the user.
            **kwargs: Additional arguments for the request.

        Returns:
            A tuple containing the endpoint and the request arguments.
        """
        endpoint = self._update_user_endpoint()
        default_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        headers = kwargs.get("headers", {})
        headers = {**default_headers, **headers}
        kwargs["headers"] = headers

        payload = {}
        if name is not None:
            payload["name"] = name
        if email is not None:
            payload["email"] = email
        if blog is not None:
            payload["blog"] = blog
        if twitter_username is not None:
            payload["twitter_username"] = twitter_username
        if company is not None:
            payload["company"] = company
        if location is not None:
            payload["location"] = location

        if hirable is not None:
            payload["hireable"] = hirable
        if bio is not None:
            payload["bio"] = bio

        return endpoint, payload, kwargs
