"""Synchronous Pull Request operations for GitHub."""

from __future__ import annotations

from typing import Any, Literal, cast

from requests import Response

from ghnova.pull_request.base import BasePullRequest
from ghnova.resource.resource import Resource
from ghnova.utils.response import process_response_with_last_modified


class PullRequest(Resource, BasePullRequest):
    """Synchronous Pull Request operations for GitHub."""

    def _list_pull_requests(  # noqa: PLR0913
        self,
        owner: str,
        repository: str,
        state: Literal["open", "closed", "all"] | None = None,
        head: str | None = None,
        base: str | None = None,
        sort: Literal["created", "updated", "popularity", "long-running"] | None = None,
        direction: Literal["asc", "desc"] | None = None,
        per_page: int | None = None,
        page: int | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> Response:
        """List pull requests from a repository.

        Args:
            owner: Owner of the repository.
            repository: Name of the repository.
            state: Filter by state: open, closed, or all.
            head: Filter by head branch name.
            base: Filter by base branch name.
            sort: Sort by: created, updated, popularity, or long-running.
            direction: Sort direction: asc or desc.
            per_page: Number of results per page.
            page: Page number of the results to fetch.
            etag: ETag from a previous request for caching purposes.
            last_modified: Last-Modified header from a previous request for caching purposes.
            **kwargs: Additional keyword arguments.

        Returns:
            Response object containing the list of pull requests.

        """
        endpoint, params, updated_kwargs = self._list_pull_requests_helper(
            owner=owner,
            repository=repository,
            state=state,
            head=head,
            base=base,
            sort=sort,
            direction=direction,
            per_page=per_page,
            page=page,
            **kwargs,
        )
        return self._get(endpoint=endpoint, params=params, etag=etag, last_modified=last_modified, **updated_kwargs)

    def list_pull_requests(  # noqa: PLR0913
        self,
        owner: str,
        repository: str,
        state: Literal["open", "closed", "all"] | None = None,
        head: str | None = None,
        base: str | None = None,
        sort: Literal["created", "updated", "popularity", "long-running"] | None = None,
        direction: Literal["asc", "desc"] | None = None,
        per_page: int | None = None,
        page: int | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        **kwargs: Any,
    ) -> tuple[list[dict[str, Any]], int, str | None, str | None]:
        """List pull requests from a repository.

        Args:
            owner: Owner of the repository.
            repository: Name of the repository.
            state: Filter by state: open, closed, or all.
            head: Filter by head branch name.
            base: Filter by base branch name.
            sort: Sort by: created, updated, popularity, or long-running.
            direction: Sort direction: asc or desc.
            per_page: Number of results per page.
            page: Page number of the results to fetch.
            etag: ETag from a previous request for caching purposes.
            last_modified: Last-Modified header from a previous request for caching purposes.
            **kwargs: Additional keyword arguments.

        Returns:
            A tuple containing the list of pull requests, status code, ETag, and Last-Modified value.

        """
        response = self._list_pull_requests(
            owner=owner,
            repository=repository,
            state=state,
            head=head,
            base=base,
            sort=sort,
            direction=direction,
            per_page=per_page,
            page=page,
            etag=etag,
            last_modified=last_modified,
            **kwargs,
        )
        data, status_code, etag_value, last_modified_value = process_response_with_last_modified(response)
        return cast(list[dict[str, Any]], data), status_code, etag_value, last_modified_value
