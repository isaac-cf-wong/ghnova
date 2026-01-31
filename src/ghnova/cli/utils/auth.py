"""Utilities for authentication in the CLI."""

from __future__ import annotations

import logging
from pathlib import Path

from ghnova.config.manager import ConfigManager

logger = logging.getLogger("ghnova")


def get_auth_params(
    config_path: Path | str,
    account_name: str | None,
    token: str | None,
    base_url: str | None,
) -> tuple[str, str]:
    """Get authentication parameters from CLI context.

    Args:
        config_path: Path to the configuration file.
        account_name: Name of the account to use for authentication.
        token: Token for authentication.
        base_url: Base URL of the GitHub platform.

    Returns:
        A tuple containing the token and base URL for authentication.

    """
    if account_name is not None:
        if token is not None or base_url is not None:
            logger.warning(
                "Both account name and token/base_url provided. The token and base_url from the account '%s' will be used.",
                account_name,
            )

        config_manager = ConfigManager(filename=config_path)
        config_manager.load_config()
        account_config = config_manager.get_config(name=account_name)
        token = account_config.token
        base_url = account_config.base_url
    elif token is None or base_url is None:
        logger.error("Either account name or both token and base_url must be provided for authentication.")
        raise ValueError("Insufficient authentication parameters provided.")
    return token, base_url
