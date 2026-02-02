"""Tests for the pull request CLI main module."""

from __future__ import annotations

from typer.testing import CliRunner

from ghnova.cli.main import app

runner = CliRunner()


class TestPullRequestMain:
    """Tests for the pull request CLI main module."""

    def test_pull_request_command_help(self) -> None:
        """Test pull-request command help."""
        result = runner.invoke(app, ["pull-request", "--help"])
        assert result.exit_code == 0
        assert "pull-request" in result.stdout.lower()
        assert "list" in result.stdout.lower()
