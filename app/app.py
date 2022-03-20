# System imports
import os

# Import Flask
from flask import Flask

# Prometheus imports
from prometheus_client import multiprocess, generate_latest, CollectorRegistry

# Import app modules blueprints
from modules import create_blueprint_phrase_finder


def create_app():
    # Create Flask app
    app = Flask("Belinsky")

    # Register prometheus route
    @app.route("/metrics/prometheus")
    def metrics():
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)
        return data, 200

    # Register blueprints
    app.register_blueprint(create_blueprint_phrase_finder())

    return app


if __name__ == "__main__":
    app_host = os.environ.get("FLASK_RUN_HOST", 'localhost')
    app_port = int(os.environ.get("FLASK_RUN_PORT", '4958'))

    app = create_app()
    app.run(host=app_host, port=app_port)
