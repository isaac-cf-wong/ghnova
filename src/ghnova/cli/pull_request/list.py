"""List command for pull request CLI."""

from __future__ import annotations

from typing import Annotated, Literal

import typer


def list_command(  # noqa: PLR0913
    ctx: typer.Context,
    owner: Annotated[
        str,
        typer.Option(
            "--owner",
            help="The owner of the repository.",
        ),
    ],
    repository: Annotated[
        str,
        typer.Option(
            "--repository",
            help="The name of the repository.",
        ),
    ],
    state: Annotated[
        Literal["open", "closed", "all"] | None,
        typer.Option(
            "--state",
            help="Filter pull requests by state: open, closed, or all.",
        ),
    ] = None,
    head: Annotated[
        str | None,
        typer.Option(
            "--head",
            help="Filter pull requests by head branch name.",
        ),
    ] = None,
    base: Annotated[
        str | None,
        typer.Option(
            "--base",
            help="Filter pull requests by base branch name.",
        ),
    ] = None,
    sort: Annotated[
        Literal["created", "updated", "popularity", "long-running"] | None,
        typer.Option(
            "--sort",
            help="Sort pull requests by: created, updated, popularity, or long-running.",
        ),
    ] = None,
    direction: Annotated[
        Literal["asc", "desc"] | None,
        typer.Option(
            "--direction",
            help="Sort direction: asc or desc.",
        ),
    ] = None,
    per_page: Annotated[
        int | None,
        typer.Option(
            "--per-page",
            help="Number of results per page.",
        ),
    ] = None,
    page: Annotated[
        int | None,
        typer.Option(
            "--page",
            help="Page number of the results to fetch.",
        ),
    ] = None,
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
) -> None:
    """List pull requests from a repository.

    Args:
        ctx: Typer context.
        owner: The owner of the repository.
        repository: The name of the repository.
        state: Filter pull requests by state: open, closed, or all.
        head: Filter pull requests by head branch name.
        base: Filter pull requests by base branch name.
        sort: Sort pull requests by: created, updated, popularity, or long-running.
        direction: Sort direction: asc or desc.
        per_page: Number of results per page.
        page: Page number of the results to fetch.
        etag: ETag from a previous request for caching purposes.
        last_modified: Last-Modified header from a previous request for caching purposes.
        account_name: Name of the account to use for authentication.
        token: Token for authentication.
        base_url: Base URL of the GitHub platform.

    """
    import json  # noqa: PLC0415
    import logging  # noqa: PLC0415

    from ghnova.cli.utils.auth import get_auth_params  # noqa: PLC0415
    from ghnova.client.github import GitHub  # noqa: PLC0415

    logger = logging.getLogger("ghnova")

    token, base_url = get_auth_params(
        config_path=ctx.obj["config_path"],
        account_name=account_name,
        token=token,
        base_url=base_url,
    )

    try:
        with GitHub(token=token, base_url=base_url) as client:
            response_data, status_code, etag_value, last_modified_value = client.pull_request.list_pull_requests(
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
            )
            result = {
                "data": response_data,
                "status_code": status_code,
                "etag": etag_value,
                "last_modified": last_modified_value,
            }
            print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.exception("Error listing pull requests: %s", e)
        raise typer.Exit(code=1) from e
