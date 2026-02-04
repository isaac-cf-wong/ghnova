"""Update command for issue CLI."""

from __future__ import annotations

from typing import Annotated, Literal

import typer


def update_command(  # noqa: PLR0913
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
    title: Annotated[
        str | None,
        typer.Option(
            "--title",
            help="The new title of the issue.",
        ),
    ] = None,
    body: Annotated[
        str | None,
        typer.Option(
            "--body",
            help="The new body of the issue.",
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
            help="A new list of labels to assign to the issue.",
        ),
    ] = None,
    assignees: Annotated[
        list[str] | None,
        typer.Option(
            "--assignees",
            help="A new list of assignees for the issue.",
        ),
    ] = None,
    state: Annotated[
        Literal["open", "closed"] | None,
        typer.Option(
            "--state",
            help="The state of the issue (open or closed).",
        ),
    ] = None,
) -> None:
    """Update an existing issue.

    Args:
        ctx: Typer context.
        owner: The owner of the repository.
        repository: The name of the repository.
        issue_number: The issue number.
        account_name: Name of the account to use for authentication.
        token: Token for authentication.
        base_url: Base URL of the GitHub platform.
        title: The new title of the issue.
        body: The new body of the issue.
        assignee: The assignee of the issue.
        milestone: The milestone for the issue.
        labels: A new list of labels to assign to the issue.
        assignees: A new list of assignees for the issue.
        state: The state of the issue (open or closed).

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
            return client.issue.update_issue(
                owner=owner,
                repository=repository,
                issue_number=issue_number,
                title=title,
                body=body,
                assignee=assignee,
                milestone=milestone,
                labels=labels,
                assignees=assignees,
                state=state,
            )

    execute_api_command(api_call=api_call, command_name="ghnova issue update")
