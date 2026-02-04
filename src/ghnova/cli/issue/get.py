"""Get command for issue CLI."""

from __future__ import annotations

from typing import Annotated

import typer


def get_command(  # noqa: PLR0913
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
    issue_number: Annotated[
        int,
        typer.Option(
            "--issue-number",
            help="The issue number.",
        ),
    ],
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
    """Get a specific issue by owner, repository, and issue number.

    Args:
        ctx: Typer context.
        owner: The owner of the repository.
        repository: The name of the repository.
        issue_number: The issue number.
        account_name: Name of the account to use for authentication.
        token: Token for authentication.
        base_url: Base URL of the GitHub platform.
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

    def api_call() -> tuple[dict[str, Any], dict[str, Any]]:
        with GitHub(token=token, base_url=base_url) as client:
            return client.issue.get_issue(
                owner=owner,
                repository=repository,
                issue_number=issue_number,
                etag=etag,
                last_modified=last_modified,
            )

    execute_api_command(api_call=api_call, command_name="ghnova issue get")
