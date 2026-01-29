"""Configuration manager for ghnova."""

from __future__ import annotations

import logging
from pathlib import Path

import platformdirs
import yaml

from ghnova.config.model import AccountConfig, Config

logger = logging.getLogger("ghnova")


class ConfigManager:
    """Configuration manager for ghnova."""

    def __init__(self, filename: Path | str | None = None) -> None:
        """Initialize ConfigManager.

        Args:
            file_name: Name of the configuration file.
        """
        filename = filename or Path(platformdirs.user_config_dir(appname="ghnova")) / "config.yaml"
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)
        self.config_path = filename

    def get_config(self, name: str | None) -> AccountConfig:
        """Get the configuration for a specific account.

        Args:
            name: Name of the account. If None, the default account is used.

        Returns:
            AccountConfig: Configuration of the specified account.
        """
        if self._config is None:
            self.load_config()

        name = self._config.default_account if name is None else name

        if name not in self._config.accounts:
            raise ValueError(f"Account '{name}' does not exist in the configuration.")

        return self._config.accounts[name]

    def add_account(
        self, name: str, token: str, base_url: str = "https://github.com", is_default: bool = False
    ) -> None:
        """Add a new account to the configuration.

        Args:
            name: Name of the account.
            token: Authentication token for the account.
            base_url: Base URL of the GitHub platform.

        """
        if self._config is None:
            self.load_config()

        if name in self._config.accounts:
            raise ValueError(f"Account '{name}' already exists in the configuration.")

        self._config.accounts[name] = AccountConfig(name=name, token=token, base_url=base_url)

        if is_default or len(self._config.accounts) == 1:
            self._config.default_account = name

    def update_account(
        self,
        name: str,
        token: str | None = None,
        base_url: str | None = None,
        is_default: bool | None = None,
    ) -> None:
        """Update an existing account in the configuration.

        Args:
            name: Name of the account to update.
            token: New authentication token for the account (optional).
            base_url: New base URL of the account (optional).
        """
        if self._config is None:
            self.load_config()

        if name not in self._config.accounts:
            raise ValueError(f"Account '{name}' does not exist in the configuration.")

        account = self._config.accounts[name]

        if token is not None:
            account.token = token
        if base_url is not None:
            account.base_url = base_url

        if is_default is not None:
            if is_default:
                self._config.default_account = name
            elif self._config.default_account == name:
                self._config.default_account = None
            else:
                logger.warning("Account '%s' is not the default account. No changes made to default account.", name)

    def delete_account(self, name: str) -> None:
        """Delete an account from the configuration.

        Args:
            name: Name of the account to delete.
        """
        if self._config is None:
            self.load_config()

        if name not in self._config.accounts:
            raise ValueError(f"Account '{name}' does not exist in the configuration.")

        del self._config.accounts[name]

        if self._config.default_account == name:
            self._config.default_account = None

    def load_config(self, filename: Path | str | None = None) -> None:
        """Load configuration from the YAML file.

        Args:
            filename: Optional path to the configuration file.
        """
        filename = filename or self.config_path
        filename = Path(filename)
        if not filename.exists():
            self._config = Config()
            return

        with filename.open("r", encoding="utf-8") as file:
            raw_config = yaml.safe_load(file) or {}

        try:
            self._config = Config(**raw_config)
        except ValueError as e:
            raise ValueError(f"Invalid configuration format: {e}") from e

    def save_config(self, filename: Path | str | None = None) -> None:
        """Save configuration to the YAML file.

        Args:
            filename: Optional path to the configuration file.
        """
        filename = filename or self.config_path
        filename = Path(filename)
        with filename.open("w", encoding="utf-8") as file:
            yaml.safe_dump(self._config.model_dump(), file)
