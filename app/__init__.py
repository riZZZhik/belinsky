# Import Flask
from flask import Flask

# Import app modules blueprints
from modules import create_blueprint_word_finder


def create_app():
    # Create Flask app
    app = Flask("WordFinder")

    # Register blueprints
    app.register_blueprint(create_blueprint_word_finder())

    return app


__all__ = ["create_app"]
