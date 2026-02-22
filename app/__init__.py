"""Flask application factory for Energy Tracker."""
import os

from flask import Flask

from .models import init_db


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(
        __name__, template_folder="../templates", static_folder="../static"
    )

    # Default configuration
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    app.config["DATABASE"] = os.environ.get("DATABASE", "energy_tracker.db")
    app.config["DEBUG"] = os.environ.get("FLASK_ENV") == "development"

    # Override with custom config if provided
    if config:
        app.config.update(config)

    # Initialize database
    with app.app_context():
        init_db(app.config["DATABASE"])

    # Register routes
    from . import routes

    app.register_blueprint(routes.bp)

    return app
