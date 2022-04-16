"""Belinsky checks."""
import typing as t

from flask import request


def check_request_keys(
    required_keys: t.Iterable[str],
) -> tuple[dict[str, str | int], int] or bool:
    """Check request input body.

    Args:
        required_keys (t.Iterable[str]): Required keys.

    Returns:
        tuple[dict[str, str | int], int] or bool
    """

    if not isinstance(required_keys, t.Iterable):
        raise TypeError(f"Unknown required_keys type: {type(required_keys)}. Required: Iterable")

    if not request.json:
        response = {"error": "Json body not found in request.", "status": 400}
        return response, 400

    if not all(key in request.json.keys() for key in required_keys):
        response = {
            "error": f"Not enough keys in request. Required keys: {', '.join(required_keys)}.",
            "status": 400,
        }
        return response, 400

    return False
