"""GitHub User resource."""

from __future__ import annotations

from typing import Any

from requests import Response

from ghnova.resource.resource import Resource
from ghnova.user.base import BaseUser
from ghnova.utils.response import process_response_with_last_modified


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
        data, status_code, etag_value, last_modified_value = process_response_with_last_modified(response)
        return data, status_code, etag_value, last_modified_value

    def _update_user(  # noqa: PLR0913
        self,
        name: str | None = None,
        email: str | None = None,
        blog: str | None = None,
        twitter_username: str | None = None,
        company: str | None = None,
        location: str | None = None,
        hirable: str | None = None,
        bio: str | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> Response:
        """Update the authenticated user's information.

        Args:
            name: The name of the user.
            email: The email of the user.
            blog: The blog URL of the user.
            twitter_username: The Twitter username of the user.
            company: The company of the user.
            location: The location of the user.
            hirable: The hirable status of the user.
            bio: The bio of the user.
            etag: The ETag value for conditional requests.
            last_modified: The Last-Modified timestamp for conditional requests.
            **kwargs: Additional arguments for the request.

        Returns:
            The response object.
        """
        endpoint, payload, kwargs = self._update_user_helper(
            name=name,
            email=email,
            blog=blog,
            twitter_username=twitter_username,
            company=company,
            location=location,
            hirable=hirable,
            bio=bio,
            **kwargs,
        )
        return self._patch(endpoint=endpoint, data=payload, etag=etag, last_modified=last_modified, **kwargs)

    def update_user(  # noqa: PLR0913
        self,
        name: str | None = None,
        email: str | None = None,
        blog: str | None = None,
        twitter_username: str | None = None,
        company: str | None = None,
        location: str | None = None,
        hirable: str | None = None,
        bio: str | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> tuple[dict[str, Any], int, str | None, str | None]:
        """Update the authenticated user's information.

        Args:
            name: The name of the user.
            email: The email of the user.
            blog: The blog URL of the user.
            twitter_username: The Twitter username of the user.
            company: The company of the user.
            location: The location of the user.
            hirable: The hirable status of the user.
            bio: The bio of the user.
            etag: The ETag value for conditional requests.
            last_modified: The Last-Modified timestamp for conditional requests.
            **kwargs: Additional arguments for the request.

        Returns:
            A tuple containing:
                - A dictionary with updated user information (empty if 304 Not Modified).
                - The HTTP status code.
                - The ETag value from the response headers (if present).
                - The Last-Modified timestamp from the response headers (if present).
        """
        response = self._update_user(
            name=name,
            email=email,
            blog=blog,
            twitter_username=twitter_username,
            company=company,
            location=location,
            hirable=hirable,
            bio=bio,
            etag=etag,
            last_modified=last_modified,
            **kwargs,
        )
        data, status_code, etag_value, last_modified_value = process_response_with_last_modified(response)

        return data, status_code, etag_value, last_modified_value
