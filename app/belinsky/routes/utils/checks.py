"""Belinsky checks."""
from flask import request


def check_request_keys(required_keys):
    """Check request input body."""
    if not request.json:
        response = {
            'error': "Json body not found in request.",
            'status': 400
        }
        return response, 400

    if not all(key in request.json.keys() for key in required_keys):
        response = {
            'error': f"Not enough keys in request. Required keys: {', '.join(required_keys)}.",
            'status': 400
        }
        return response, 400

    return False
