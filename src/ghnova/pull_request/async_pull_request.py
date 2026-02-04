"""Asynchronous Pull Request operations for GitHub."""

from __future__ import annotations

from typing import Any, Literal, cast

from aiohttp import ClientResponse

from ghnova.pull_request.base import BasePullRequest
from ghnova.resource.async_resource import AsyncResource
from ghnova.utils.response import process_async_response_with_last_modified


class AsyncPullRequest(AsyncResource, BasePullRequest):
    """Asynchronous Pull Request operations for GitHub."""

    async def _list_pull_requests(  # noqa: PLR0913
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
    ) -> ClientResponse:
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
            ClientResponse object containing the list of pull requests.

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
        return await self._get(
            endpoint=endpoint, params=params, etag=etag, last_modified=last_modified, **updated_kwargs
        )

    async def list_pull_requests(  # noqa: PLR0913
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
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
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
            A tuple containing the list of pull requests and a dictionary with metadata including status_code, etag, and last_modified.

        """
        response = await self._list_pull_requests(
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
        data, status_code, etag_value, last_modified_value = await process_async_response_with_last_modified(response)
        return cast(list[dict[str, Any]], data), {
            "status_code": status_code,
            "etag": etag_value,
            "last_modified": last_modified_value,
        }
