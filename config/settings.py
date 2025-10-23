"""
Configuration settings for the Tornado application.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""
    
    # Server settings
    PORT: int = int(os.getenv('PORT', 8888))
    HOST: str = os.getenv('HOST', 'localhost')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Logging settings
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/app.log')
    
    # CORS settings
    ALLOWED_ORIGINS: str = os.getenv('ALLOWED_ORIGINS', '*')
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return {
            'port': cls.PORT,
            'host': cls.HOST,
            'debug': cls.DEBUG,
            'log_level': cls.LOG_LEVEL,
            'log_file': cls.LOG_FILE,
            'allowed_origins': cls.ALLOWED_ORIGINS
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'


class TestConfig(Config):
    """Test configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    PORT = 9999


def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'test':
        return TestConfig()
    else:
        return DevelopmentConfig()