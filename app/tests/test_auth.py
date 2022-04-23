"""Test Belinsky authorization."""
from flask import Flask
from flask.testing import FlaskClient

from . import credentials, utils


def test_signup(app: Flask, client: FlaskClient) -> None:
    """Test signup method with filled form."""
    client.post("/logout")
    response = client.post(
        "/signup",
        data={"username": "unittester_1", "password": "test_password", "raw": True},
    )
    utils.delete_user(app, "unittester_1")

    assert response.status_code == 200


def test_signup_template(app: Flask, client: FlaskClient) -> None:
    """Test signup method."""
    client.post("/logout")

    with utils.captured_templates(app) as templates:
        response = client.get("/signup")
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == "signup.html"


def test_login(client: FlaskClient) -> None:
    """Test login method with filled form."""
    client.post("/logout")
    response = client.post("login", data=credentials | {"raw": True})

    assert response.status_code == 200


def test_login_template(app: Flask, client: FlaskClient) -> None:
    """Test login method."""
    client.post("/logout")
    with utils.captured_templates(app) as templates:
        response = client.get("/login")
        assert response.status_code == 200
        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == "login.html"


def test_delete(app: Flask, client: FlaskClient) -> None:
    """Test delete method."""
    utils.add_user(app, "unittester_1", "test_password")

    response = client.post(
        "delete-user",
        json={"username": "unittester_1", "password": "test_password"},
    )

    assert response.status_code == 200


def test_logout(client: FlaskClient) -> None:
    """Test logout method."""
    response = client.post("/logout", data={"raw": True})

    assert response.status_code == 200
