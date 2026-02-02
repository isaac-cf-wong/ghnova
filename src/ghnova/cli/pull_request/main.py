"""Pull request CLI commands for ghnova."""

from __future__ import annotations

import typer

pull_request_app = typer.Typer(
    name="pull-request",
    help="Manage GitHub pull requests.",
    rich_markup_mode="rich",
)


def register_commands() -> None:
    """Register pull request subcommands."""


register_commands()
