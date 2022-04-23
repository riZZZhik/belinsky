"""Test Belinsky application."""
from flask.testing import FlaskClient


def test_healthcheck(client: FlaskClient) -> None:
    """Test application healthcheck."""
    response = client.get("/healthcheck")
    assert response.json["status"] == "success"
