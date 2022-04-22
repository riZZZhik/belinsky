"""Initialize belinsky Flask application."""
# Import Flask
from flask import Flask, url_for, redirect, render_template
from flask_login import current_user

# Module imports
from . import config
from .database import db
from .models import User
from .routes import login_manager


def home():
    """Redirect to home page."""
    if current_user.is_authenticated:
        available_modules = {
            "phrase_finder": ("Phrase Finder", url_for("phrase_finder.phrase_finder")),
            "text_analyzer": ("Text Analyzer", url_for("text_analyzer.text_analyzer"))
        }

        return render_template("home.html", available_modules=available_modules)

    return redirect(url_for("auth.login"))


# pylint: disable=import-outside-toplevel
def create_app() -> Flask:
    """Initialize belinsky Flask application."""
    app = Flask("Belinsky")
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # Initialize app modules and routes
    with app.app_context():
        # Import routes
        from . import routes

        # Initialize database
        app.config["SQLALCHEMY_DATABASE_URI"] = config.BELINSKY_POSTGRES_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        db.create_all()

        # Initialize plugins
        login_manager.init_app(app)

        # Register blueprints
        app.add_url_rule("/", view_func=home)
        app.register_blueprint(routes.create_blueprint_auth())
        app.register_blueprint(routes.create_blueprint_observability())
        for module in config.MODULES:
            app.register_blueprint(getattr(routes, "create_blueprint_" + module)())

    return app


__all__ = ["create_app", "db", "login_manager"]
