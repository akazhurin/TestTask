import os


class Config:
    """Application configuration class"""
    DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Setting up caching
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    # Setting up SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

