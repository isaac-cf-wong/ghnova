"""Repository CLI commands for ghnova."""

from __future__ import annotations

import typer

repository_app = typer.Typer(
    name="repository",
    help="Manage git repositories.",
    rich_markup_mode="rich",
)


def register_commands() -> None:
    """Register repository subcommands."""


register_commands()
