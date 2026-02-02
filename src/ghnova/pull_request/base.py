"""Base class for pull request operations."""

from __future__ import annotations

from typing import Any, Literal


class BasePullRequest:
    """Base class for pull request operations."""

    def _list_pull_requests_endpoint(self, owner: str, repository: str) -> str:
        """Get the endpoint for listing pull requests.

        Args:
            owner: Owner of the repository.
            repository: Name of the repository.

        Returns:
            Endpoint URL for listing pull requests.

        """
        return f"/repos/{owner}/{repository}/pulls"

    def _list_pull_requests_helper(  # noqa: PLR0913
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
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        """Prepare parameters for listing pull requests.

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
            **kwargs: Additional keyword arguments.

        Returns:
            A tuple containing the endpoint URL, parameters dictionary, and updated kwargs.

        """
        endpoint = self._list_pull_requests_endpoint(owner=owner, repository=repository)
        default_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        headers = kwargs.get("headers", {})
        headers = {**default_headers, **headers}
        kwargs["headers"] = headers

        params: dict[str, Any] = {}
        if state is not None:
            params["state"] = state
        if head is not None:
            params["head"] = head
        if base is not None:
            params["base"] = base
        if sort is not None:
            params["sort"] = sort
        if direction is not None:
            params["direction"] = direction
        if per_page is not None:
            params["per_page"] = per_page
        if page is not None:
            params["page"] = page

        return endpoint, params, kwargs
