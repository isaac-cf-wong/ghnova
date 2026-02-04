"""Create command for issue CLI."""

from __future__ import annotations

from typing import Annotated

import typer


def create_command(  # noqa: PLR0913
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
    title: Annotated[
        str,
        typer.Option(
            "--title",
            help="The title of the issue.",
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
    body: Annotated[
        str | None,
        typer.Option(
            "--body",
            help="The body of the issue.",
        ),
    ] = None,
    assignee: Annotated[
        str | None,
        typer.Option(
            "--assignee",
            help="The assignee of the issue.",
        ),
    ] = None,
    milestone: Annotated[
        str | None,
        typer.Option(
            "--milestone",
            help="The milestone for the issue.",
        ),
    ] = None,
    labels: Annotated[
        list[str] | None,
        typer.Option(
            "--labels",
            help="A list of labels to assign to the issue.",
        ),
    ] = None,
    assignees: Annotated[
        list[str] | None,
        typer.Option(
            "--assignees",
            help="A list of assignees to assign to the issue.",
        ),
    ] = None,
    issue_type: Annotated[
        str | None,
        typer.Option(
            "--issue-type",
            help="The type of the issue (e.g., 'bug', 'feature').",
        ),
    ] = None,
) -> None:
    """Create a new issue in a repository.

    Args:
        ctx: Typer context.
        owner: The owner of the repository.
        repository: The name of the repository.
        title: The title of the issue.
        account_name: Name of the account to use for authentication.
        token: Token for authentication.
        base_url: Base URL of the GitHub platform.
        body: The body of the issue.
        assignee: The assignee of the issue.
        milestone: The milestone for the issue.
        labels: A list of labels to assign to the issue.
        assignees: A list of assignees to assign to the issue.
        issue_type: The type of the issue.

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
            return client.issue.create_issue(
                owner=owner,
                repository=repository,
                title=title,
                body=body,
                assignee=assignee,
                milestone=milestone,
                labels=labels,
                assignees=assignees,
                issue_type=issue_type,
            )

    execute_api_command(api_call=api_call, command_name="ghnova issue create")
