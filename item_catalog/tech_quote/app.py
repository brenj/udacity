"""Flask application for tech_quote."""

import os

from flask import Flask, render_template

from tech_quote import public
from tech_quote.extensions import db, migrate
from tech_quote.assets import assets


def create_app():
    """Create a tech_quote application.

    Returns:
        Flask: The tech_quote application.
    """
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    return app


def register_extensions(app):
    """Register flask extensions."""
    db.init_app(app)
    assets.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register flask blueprints."""
    app.register_blueprint(public.views.blueprint)


def register_errors(app):
    """Register flask error handlers."""
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template(
            'errors/{0}.html'.format(error_code)), error_code

    for error in (401, 404, 500):
        app.errorhandler(error)(render_error)
