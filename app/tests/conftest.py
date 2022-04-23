"""Belinsky application tests configuration."""
import typing as t

import pytest
from flask import Flask

from . import credentials, utils
from belinsky import create_app


# Initialize pytest fixtures
@pytest.fixture()
def app() -> t.Generator:
    """Initialize Belinsky test application."""
    # Initialize app
    app = create_app()

    # Create test user and remove old ones
    utils.add_user(app, credentials["username"], credentials["password"])
    utils.delete_user(app, "unittester_1")

    return app


@pytest.fixture()
def client(app: Flask):
    """Initialize Belinsky test client."""
    _client = app.test_client()
    _client.post("/login", data=credentials)

    return _client


@pytest.fixture()
def runner(app: Flask):
    """Initialize Belinsky test cli runner."""
    return app.test_cli_runner()
