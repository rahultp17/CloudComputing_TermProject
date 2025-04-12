# config.py
# This file contains configuration classes for the Weather Application.
# Sensitive information such as secret keys and API keys are loaded from environment variables.
# This configuration supports both development and production environments.

import os

class Config:
    """
    Base configuration class with default settings used by both
    DevelopmentConfig and ProductionConfig.
    """
    # Secret key for Flask sessions and CSRF protection.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    
    # Google Cloud SQL PostgreSQL connection string format:
    # postgresql://username:password@host:port/dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://weather_user:Shaligram%401001@34.58.156.251/weatherapp'  # Replace with your actual public IP
    )
    
    # Disable SQLAlchemy modification tracking to reduce overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache settings: Using simple in-memory caching.
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds (5 minutes)
    
    # API key for the OpenWeatherMap service used to fetch weather data.
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')
    
    # Secret key for generating JSON Web Tokens (JWT).
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Google Client ID used for verifying Google Sign-In tokens.
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

class DevelopmentConfig(Config):
    """
    Development configuration:
    Enables debugging and verbose error messages.
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configuration:
    Disables debugging and sets production-level settings.
    """
    DEBUG = False

# Dictionary to map configuration names to their respective classes.
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
