"""Pull request CLI commands for ghnova."""

from __future__ import annotations

import typer

pull_request_app = typer.Typer(
    name="pull-request",
    help="Manage pull requests.",
    rich_markup_mode="rich",
)


def register_commands() -> None:
    """Register pull request subcommands."""
    from ghnova.cli.pull_request.list import list_command  # noqa: PLC0415

    pull_request_app.command(name="list", help="List pull requests.")(list_command)


register_commands()
