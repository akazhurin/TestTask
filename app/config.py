import os


class Config:
    """Клас конфигурации приложения"""
    DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Настройка кеширования
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    # Настройка SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

