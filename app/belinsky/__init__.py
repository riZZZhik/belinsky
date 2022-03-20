# System imports
import os
import secrets

# Import Flask
from flask import Flask

# Prometheus imports
from prometheus_client import multiprocess, generate_latest, CollectorRegistry

# Import belinsky modules blueprints
from .modules import create_blueprint_phrase_finder


def create_app():
    # Create Flask belinsky
    app = Flask("Belinsky")
    app.config['SECRET_KEY'] = os.environ.get("BELINSKY_SECRET_KEY", secrets.token_hex(16))

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
