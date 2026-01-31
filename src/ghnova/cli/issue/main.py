"""Issue CLI commands for ghnova."""

from __future__ import annotations

import typer

issue_app = typer.Typer(
    name="issue",
    help="Manage git issues.",
    rich_markup_mode="rich",
)


def register_commands() -> None:
    """Register issue subcommands."""


register_commands()
