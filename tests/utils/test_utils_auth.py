"""Unit tests for CLI auth utilities."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from ghnova.cli.utils.auth import get_auth_params


def test_get_auth_params_with_account_name_and_token_base_url_warns(caplog):
    """Providing account_name should use account values and log a warning if token/base_url were also passed."""
    caplog.set_level("WARNING", logger="ghnova")

    with patch("ghnova.cli.utils.auth.ConfigManager") as mock_cm:
        mock_inst = mock_cm.return_value
        mock_inst.load_config.return_value = None
        mock_inst.get_config.return_value = SimpleNamespace(token="acct-token", base_url="https://acct.example")

        token, base_url = get_auth_params(config_path="/tmp/config", account_name="acct", token="t", base_url="u")

        assert token == "acct-token"
        assert base_url == "https://acct.example"
        assert any("Both account name and token/base_url provided" in r.message for r in caplog.records)


def test_get_auth_params_use_default_account():
    """When neither token nor account_name provided, use default account from config."""
    with patch("ghnova.cli.utils.auth.ConfigManager") as mock_cm:
        mock_inst = mock_cm.return_value
        mock_inst.load_config.return_value = None
        mock_inst.has_default_account.return_value = True
        mock_inst.get_config.return_value = SimpleNamespace(token="def-token", base_url="https://def.example")

        token, base_url = get_auth_params(config_path="/tmp/config", account_name=None, token=None, base_url=None)

        assert token == "def-token"
        assert base_url == "https://def.example"


def test_get_auth_params_no_default_raises():
    """If no default account and no credentials provided, raise ValueError."""
    with patch("ghnova.cli.utils.auth.ConfigManager") as mock_cm:
        mock_inst = mock_cm.return_value
        mock_inst.load_config.return_value = None
        mock_inst.has_default_account.return_value = False

        with pytest.raises(ValueError, match=r"No default account available for authentication"):
            get_auth_params(config_path="/tmp/config", account_name=None, token=None, base_url=None)


@pytest.mark.parametrize(("token_val", "base_url_val", "missing_msg"), [(None, "x", "token"), ("x", None, "base_url")])
def test_get_auth_params_missing_fields_raises(token_val, base_url_val, missing_msg):
    """If only one of token/base_url is provided, raise informative ValueError."""
    with pytest.raises(ValueError, match="Insufficient authentication parameters") as excinfo:
        get_auth_params(config_path="/tmp/config", account_name=None, token=token_val, base_url=base_url_val)

    assert missing_msg in str(excinfo.value)
