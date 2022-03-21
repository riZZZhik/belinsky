# Import Flask
from flask import Flask

# Module imports
from . import config
from .auth import login_manager
from .database import db
from .models import User


def create_app():
    # Create Flask belinsky
    app = Flask("Belinsky")
    app.config['SECRET_KEY'] = config.SECRET_KEY

    with app.app_context():
        # Import modules
        from .auth import auth_bp
        from .route import main_bp
        from .modules import create_blueprint_phrase_finder

        # Initialize database
        app.config['SQLALCHEMY_DATABASE_URI'] = config.BELINSKY_POSTGRES_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        db.create_all()

        # Initialize authentication
        login_manager.init_app(app)

        # Register blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(create_blueprint_phrase_finder())

    return app
