"""Belinsky application tests configuration."""
import typing as t

import pytest
from flask import Flask

from belinsky import create_app
from . import credentials, utils


# Initialize pytest fixtures
@pytest.fixture()
def app() -> t.Generator:
    """Initialize Belinsky test application."""
    # Initialize app
    _app = create_app()

    # Create test user and remove old ones
    utils.add_user(_app, credentials["username"], credentials["password"])
    utils.delete_user(_app, "unittester_1")

    return _app


# pylint: disable=redefined-outer-name
@pytest.fixture()
def client(app: Flask):
    """Initialize Belinsky test client."""
    _client = app.test_client()
    _client.post("/login", data=credentials)

    return _client


# pylint: disable=redefined-outer-name
@pytest.fixture()
def runner(app: Flask):
    """Initialize Belinsky test cli runner."""
    return app.test_cli_runner()
