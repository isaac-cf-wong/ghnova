"""Tests for CLI authentication utilities."""

from __future__ import annotations

import pytest

from ghnova.cli.utils.auth import get_auth_params


class TestGetAuthParams:
    """Tests for the get_auth_params function."""

    def test_get_auth_params_with_account_name(self, tmp_path) -> None:
        """Test getting auth params using account name from config file."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n  test:\n    name: test\n    token: test_token\n"
            "    base_url: https://github.com\ndefault_account: test\n"
        )

        token, base_url = get_auth_params(
            config_path=config_file,
            account_name="test",
            token=None,
            base_url=None,
        )

        assert token == "test_token"
        assert base_url == "https://github.com"

    def test_get_auth_params_with_token_and_base_url(self) -> None:
        """Test getting auth params using token and base_url directly."""
        token, base_url = get_auth_params(
            config_path="/dummy/path",
            account_name=None,
            token="direct_token",
            base_url="https://custom.github.com",
        )

        assert token == "direct_token"
        assert base_url == "https://custom.github.com"

    def test_get_auth_params_missing_token_and_base_url(self) -> None:
        """Test error when neither account_name nor token/base_url provided."""
        with pytest.raises(ValueError, match="Insufficient authentication parameters provided"):
            get_auth_params(
                config_path="/dummy/path",
                account_name=None,
                token=None,
                base_url=None,
            )

    def test_get_auth_params_missing_base_url(self) -> None:
        """Test error when token provided but base_url missing."""
        with pytest.raises(ValueError, match="Insufficient authentication parameters provided"):
            get_auth_params(
                config_path="/dummy/path",
                account_name=None,
                token="some_token",
                base_url=None,
            )

    def test_get_auth_params_missing_token(self) -> None:
        """Test error when base_url provided but token missing."""
        with pytest.raises(ValueError, match="Insufficient authentication parameters provided"):
            get_auth_params(
                config_path="/dummy/path",
                account_name=None,
                token=None,
                base_url="https://github.com",
            )

    def test_get_auth_params_with_account_name_and_token_warning(self, tmp_path, caplog) -> None:
        """Test warning when both account_name and token are provided."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n  test:\n    name: test\n    token: test_token\n"
            "    base_url: https://github.com\ndefault_account: test\n"
        )

        token, base_url = get_auth_params(
            config_path=config_file,
            account_name="test",
            token="custom_token",
            base_url=None,
        )

        # Should use account config, not provided token
        assert token == "test_token"
        assert base_url == "https://github.com"
        # Check for warning in logs
        assert "Both account name and token/base_url provided" in caplog.text

    def test_get_auth_params_with_account_name_and_base_url_warning(self, tmp_path, caplog) -> None:
        """Test warning when both account_name and base_url are provided."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n  test:\n    name: test\n    token: test_token\n"
            "    base_url: https://github.com\ndefault_account: test\n"
        )

        token, base_url = get_auth_params(
            config_path=config_file,
            account_name="test",
            token=None,
            base_url="https://custom.com",
        )

        # Should use account config, not provided base_url
        assert token == "test_token"
        assert base_url == "https://github.com"
        # Check for warning in logs
        assert "Both account name and token/base_url provided" in caplog.text

    def test_get_auth_params_account_not_found(self, tmp_path) -> None:
        """Test error when specified account is not found in config."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n  test:\n    name: test\n    token: test_token\n"
            "    base_url: https://github.com\ndefault_account: test\n"
        )

        with pytest.raises(
            ValueError, match=r"Account 'nonexistent' does not exist in the configuration."
        ):  # ConfigManager raises when account not found
            get_auth_params(
                config_path=config_file,
                account_name="nonexistent",
                token=None,
                base_url=None,
            )

    def test_get_auth_params_with_multiple_accounts(self, tmp_path) -> None:
        """Test getting auth params from multiple accounts in config."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "accounts:\n"
            "  test1:\n    name: test1\n    token: token1\n    base_url: https://github.com\n"
            "  test2:\n    name: test2\n    token: token2\n    base_url: https://enterprise.github.com\n"
            "default_account: test1\n"
        )

        # Get first account
        token1, base_url1 = get_auth_params(
            config_path=config_file,
            account_name="test1",
            token=None,
            base_url=None,
        )
        assert token1 == "token1"
        assert base_url1 == "https://github.com"

        # Get second account
        token2, base_url2 = get_auth_params(
            config_path=config_file,
            account_name="test2",
            token=None,
            base_url=None,
        )
        assert token2 == "token2"
        assert base_url2 == "https://enterprise.github.com"
