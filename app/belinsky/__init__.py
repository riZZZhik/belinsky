"""Initialize belinsky Flask application."""
# Import Flask
from flask import Flask

# Module imports
from . import config
from .database import db
from .models import User
from .routes import login_manager


def create_app():
    """Initialize belinsky Flask application."""
    app = Flask("Belinsky")
    app.config['SECRET_KEY'] = config.SECRET_KEY

    # pylint: disable=import-outside-toplevel
    with app.app_context():
        # Import routes
        from . import routes

        # Initialize database
        app.config['SQLALCHEMY_DATABASE_URI'] = config.BELINSKY_POSTGRES_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        db.create_all()

        # Initialize plugins
        login_manager.init_app(app)

        # Register blueprints
        app.register_blueprint(routes.create_blueprint_auth())
        app.register_blueprint(routes.create_blueprint_observability())
        app.register_blueprint(routes.create_blueprint_phrase_finder())

    return app


__all__ = ['create_app', 'db', 'login_manager']
