"""Tests for the pull request list CLI command."""

from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from ghnova.cli.main import app

runner = CliRunner()


class TestListCommand:
    """Tests for the list pull requests command."""

    def test_list_command_help(self) -> None:
        """Test list command help."""
        result = runner.invoke(app, ["pull-request", "list", "--help"])
        assert result.exit_code == 0

    def test_list_pull_requests(self, tmp_path) -> None:
        """Test listing pull requests from a repository."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n  test:\n    name: test\n    token: test_token\n"
            "    base_url: https://github.com\ndefault_account: test\n"
        )

        with patch("ghnova.client.github.GitHub") as mock_github:
            mock_client = mock_github.return_value.__enter__.return_value
            mock_pr_client = mock_client.pull_request
            mock_pr_client.list_pull_requests.return_value = (
                [
                    {"id": 1, "number": 1, "title": "First PR", "state": "open"},
                    {"id": 2, "number": 2, "title": "Second PR", "state": "closed"},
                ],
                200,
                None,
                None,
            )

            result = runner.invoke(
                app,
                [
                    "--config-path",
                    str(config_file),
                    "pull-request",
                    "list",
                    "--account-name",
                    "test",
                    "--owner",
                    "test-owner",
                    "--repository",
                    "test-repo",
                ],
            )

            assert result.exit_code == 0
            assert "First PR" in result.stdout
            assert "Second PR" in result.stdout
            mock_pr_client.list_pull_requests.assert_called_once_with(
                owner="test-owner",
                repository="test-repo",
                state=None,
                head=None,
                base=None,
                sort=None,
                direction=None,
                per_page=None,
                page=None,
                etag=None,
                last_modified=None,
            )

    def test_list_pull_requests_with_params(self, tmp_path) -> None:
        """Test listing pull requests with parameters."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n  test:\n    name: test\n    token: test_token\n"
            "    base_url: https://github.com\ndefault_account: test\n"
        )

        with patch("ghnova.client.github.GitHub") as mock_github:
            mock_client = mock_github.return_value.__enter__.return_value
            mock_pr_client = mock_client.pull_request
            mock_pr_client.list_pull_requests.return_value = (
                [{"id": 1, "number": 1, "title": "Open PR", "state": "open"}],
                200,
                '"etag-value"',
                "Wed, 21 Oct 2015 07:28:00 GMT",
            )

            result = runner.invoke(
                app,
                [
                    "--config-path",
                    str(config_file),
                    "pull-request",
                    "list",
                    "--account-name",
                    "test",
                    "--owner",
                    "test-owner",
                    "--repository",
                    "test-repo",
                    "--state",
                    "open",
                    "--per-page",
                    "10",
                    "--page",
                    "1",
                ],
            )

            assert result.exit_code == 0
            assert "Open PR" in result.stdout
            mock_pr_client.list_pull_requests.assert_called_once_with(
                owner="test-owner",
                repository="test-repo",
                state="open",
                head=None,
                base=None,
                sort=None,
                direction=None,
                per_page=10,
                page=1,
                etag=None,
                last_modified=None,
            )

    def test_list_pull_requests_exception(self, tmp_path) -> None:
        """Test listing pull requests with exception."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n  test:\n    name: test\n    token: test_token\n"
            "    base_url: https://github.com\ndefault_account: test\n"
        )

        with patch("ghnova.client.github.GitHub") as mock_github:
            mock_client = mock_github.return_value.__enter__.return_value
            mock_pr_client = mock_client.pull_request
            mock_pr_client.list_pull_requests.side_effect = Exception("API Error")

            result = runner.invoke(
                app,
                [
                    "--config-path",
                    str(config_file),
                    "pull-request",
                    "list",
                    "--account-name",
                    "test",
                    "--owner",
                    "test-owner",
                    "--repository",
                    "test-repo",
                ],
            )

            assert result.exit_code == 1
            assert "API Error" in result.stderr
