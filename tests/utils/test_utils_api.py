"""Unit tests for CLI API utilities."""

from __future__ import annotations

import json
import logging

import pytest

from ghnova.cli.utils.api import execute_api_command


def test_execute_api_command_success(capsys):
    """Should print JSON with data and metadata on success."""

    def api_call():
        return [{"id": 1}], {"page": 1}

    execute_api_command(api_call=api_call, command_name="test cmd")

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert output["data"] == [{"id": 1}]
    assert output["metadata"] == {"page": 1}


def test_execute_api_command_exception(caplog):
    """Should log exception and raise typer.Exit on error."""

    def bad_call():
        raise RuntimeError("boom")

    caplog.set_level(logging.ERROR, logger="ghnova")

    with pytest.raises(Exception, match="1") as excinfo:
        execute_api_command(api_call=bad_call, command_name="failing cmd")

    # As typer.Exit is raised with code 1
    # ensure the original exception was wrapped
    assert excinfo.type.__name__ in ("Exit", "TyperExit")
    assert "Error executing failing cmd" in caplog.text
