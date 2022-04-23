"""Belinsky routes blueprints."""
from .auth import create_blueprint_auth, login_manager
from .observability import create_blueprint_observability
from .phrase_finder import create_blueprint_phrase_finder
from .text_analyzer import create_blueprint_text_analyzer

__all__ = [
    "login_manager",
    "create_blueprint_auth",
    "create_blueprint_observability",
    "create_blueprint_phrase_finder",
    "create_blueprint_text_analyzer",
]
