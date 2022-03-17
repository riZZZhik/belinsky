from flask import Flask

from .modules import register_word_finder_handlers


def create_app():
    # Create Flask app
    app = Flask("WordFinder")

    # Register handlers
    register_word_finder_handlers(app)

    return app


__all__ = ["create_app"]
