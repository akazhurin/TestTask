import os

import dotenv
from flask import Flask

from . import cache, db, migrate
from . import endpoints_views, scripts_views


def create_app():
    """Создание Flask приложения"""
    app = Flask(__name__)

    # Загрузка переменных окружения
    dotenv.load_dotenv('.env')
    app.config.from_object(os.getenv('CONFIG'))

    # Регистрация blueprint`ov
    app.register_blueprint(endpoints_views.bp)
    app.register_blueprint(scripts_views.bp)

    # Создание расширений для работы с БД
    db.init_app(app)
    migrate.init_app(app, db)

    # Создание расширения для работы с кешированием
    cache.init_app(app)

    return app
