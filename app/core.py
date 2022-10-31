import os

import dotenv
from flask import Flask

from . import cache, db, migrate
from . import endpoints_views, scripts_views


def create_app():
    """Creating a Flask Application"""
    app = Flask(__name__)

    # Loading environment variables
    dotenv.load_dotenv('.env')
    app.config.from_object(os.getenv('CONFIG'))

    # Registration blueprint`ov
    app.register_blueprint(endpoints_views.bp)
    app.register_blueprint(scripts_views.bp)

    # Creating extensions for working with the database
    db.init_app(app)
    migrate.init_app(app, db)

    # Creating an extension for working with caching
    cache.init_app(app)

    return app
