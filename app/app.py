# System imports
import os

# Import Flask
from flask import Flask

# Import app modules blueprints
from modules import create_blueprint_phrase_finder


def create_app():
    # Create Flask app
    app = Flask("Belinsky")

    # Register blueprints
    app.register_blueprint(create_blueprint_phrase_finder())

    return app


if __name__ == "__main__":
    app_host = os.environ.get("FLASK_RUN_HOST", 'localhost')
    app_port = int(os.environ.get("FLASK_RUN_PORT", '4958'))

    app = create_app()
    app.run(host=app_host, port=app_port)
