"""List command for issue CLI."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

import typer


def list_command(  # noqa: PLR0913
    ctx: typer.Context,
    account_name: Annotated[
        str | None,
        typer.Option(
            "--account-name",
            help="Name of the account to use for authentication.",
        ),
    ] = None,
    token: Annotated[
        str | None,
        typer.Option(
            "--token",
            help="Token for authentication. If not provided, the token from the specified account will be used.",
        ),
    ] = None,
    base_url: Annotated[
        str | None,
        typer.Option(
            "--base-url",
            help="Base URL of the GitHub platform. If not provided, the base URL from the specified account will be used.",
        ),
    ] = None,
    owner: Annotated[
        str | None,
        typer.Option(
            "--owner",
            help="The owner of the repository.",
        ),
    ] = None,
    organization: Annotated[
        str | None,
        typer.Option(
            "--organization",
            help="The organization name.",
        ),
    ] = None,
    repository: Annotated[
        str | None,
        typer.Option(
            "--repository",
            help="The name of the repository.",
        ),
    ] = None,
    filter_by: Annotated[
        Literal["assigned", "created", "mentioned", "subscribed", "all"] | None,
        typer.Option(
            "--filter-by",
            help="Filter issues by: assigned, created, mentioned, subscribed, or all.",
        ),
    ] = None,
    state: Annotated[
        Literal["open", "closed", "all"] | None,
        typer.Option(
            "--state",
            help="Filter by state: open, closed, or all.",
        ),
    ] = None,
    labels: Annotated[list[str] | None, typer.Option("--labels", help="Filter by labels.")] = None,
    sort: Annotated[
        Literal["created", "updated", "comments"] | None,
        typer.Option(
            "--sort",
            help="Sort by: created, updated, or comments.",
        ),
    ] = None,
    direction: Annotated[
        Literal["asc", "desc"] | None,
        typer.Option(
            "--direction",
            help="Sort direction: asc or desc.",
        ),
    ] = None,
    since: Annotated[
        datetime | None,
        typer.Option(
            "--since",
            help="Only issues updated at or after this time are returned (ISO 8601 format).",
        ),
    ] = None,
    collab: Annotated[
        bool | None,
        typer.Option(
            "--collab/--no-collab",
            help="Include issues the user is a collaborator on.",
        ),
    ] = None,
    orgs: Annotated[
        bool | None,
        typer.Option(
            "--orgs/--no-orgs",
            help="Include issues from organizations the user is a member of.",
        ),
    ] = None,
    owned: Annotated[
        bool | None,
        typer.Option(
            "--owned/--no-owned",
            help="Include issues owned by the authenticated user.",
        ),
    ] = None,
    pulls: Annotated[
        bool | None,
        typer.Option(
            "--pulls/--no-pulls",
            help="Include pull requests in the results.",
        ),
    ] = None,
    issue_type: Annotated[
        str | None,
        typer.Option(
            "--issue-type",
            help="Filter by issue type.",
        ),
    ] = None,
    milestone: Annotated[
        str | None,
        typer.Option(
            "--milestone",
            help="Filter by milestone.",
        ),
    ] = None,
    assignee: Annotated[
        str | None,
        typer.Option(
            "--assignee",
            help="Filter by assignee.",
        ),
    ] = None,
    creator: Annotated[
        str | None,
        typer.Option(
            "--creator",
            help="Filter by creator.",
        ),
    ] = None,
    mentioned: Annotated[
        str | None,
        typer.Option(
            "--mentioned",
            help="Filter by mentioned user.",
        ),
    ] = None,
    per_page: Annotated[
        int,
        typer.Option(
            "--per-page",
            help="Number of results per page.",
        ),
    ] = 30,
    page: Annotated[
        int,
        typer.Option(
            "--page",
            help="Page number for pagination.",
        ),
    ] = 1,
    etag: Annotated[
        str | None,
        typer.Option(
            "--etag",
            help="ETag from a previous request for caching purposes.",
        ),
    ] = None,
    last_modified: Annotated[
        str | None,
        typer.Option(
            "--last-modified",
            help="Last-Modified header from a previous request for caching purposes.",
        ),
    ] = None,
) -> None:
    """List issues from a repository or organization.

    Args:
        ctx: Typer context.
        account_name: Name of the account to use for authentication.
        token: Token for authentication.
        base_url: Base URL of the GitHub platform.
        owner: The owner of the repository.
        organization: The organization name.
        repository: The name of the repository.
        filter_by: Filter issues by: assigned, created, mentioned, subscribed, or all.
        state: Filter by state: open, closed, or all.
        labels: Filter by labels.
        sort: Sort by: created, updated, or comments.
        direction: Sort direction: asc or desc.
        since: Only issues updated at or after this time are returned.
        collab: Include issues the user is a collaborator on.
        orgs: Include issues from organizations the user is a member of.
        owned: Include issues owned by the authenticated user.
        pulls: Include pull requests in the results.
        issue_type: Filter by issue type.
        milestone: Filter by milestone.
        assignee: Filter by assignee.
        creator: Filter by creator.
        mentioned: Filter by mentioned user.
        per_page: Number of results per page.
        page: Page number for pagination.
        etag: ETag from a previous request for caching purposes.
        last_modified: Last-Modified header from a previous request for caching purposes.

    """
    from typing import Any  # noqa: PLC0415

    from ghnova.cli.utils.api import execute_api_command  # noqa: PLC0415
    from ghnova.cli.utils.auth import get_auth_params  # noqa: PLC0415
    from ghnova.client.github import GitHub  # noqa: PLC0415

    token, base_url = get_auth_params(
        config_path=ctx.obj["config_path"],
        account_name=account_name,
        token=token,
        base_url=base_url,
    )

    def api_call() -> tuple[dict[str, Any] | list[dict[str, Any]], dict[str, Any]]:
        with GitHub(token=token, base_url=base_url) as client:
            return client.issue.list_issues(
                owner=owner,
                organization=organization,
                repository=repository,
                filter_by=filter_by,
                state=state,
                labels=labels,
                sort=sort,
                direction=direction,
                since=since,
                collab=collab,
                orgs=orgs,
                owned=owned,
                pulls=pulls,
                issue_type=issue_type,
                milestone=milestone,
                assignee=assignee,
                creator=creator,
                mentioned=mentioned,
                per_page=per_page,
                page=page,
                etag=etag,
                last_modified=last_modified,
            )

    execute_api_command(api_call=api_call, command_name="ghnova issue list")
