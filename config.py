"""
Security Configuration for Flask Application
Centralized security settings with environment-based configuration
"""

import os
from datetime import timedelta


class Config:
    """Base configuration with security defaults"""
    
    # Secret key for session signing (MUST be set in production)
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    
    # Session Configuration
    SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Security Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    
    # CORS Settings (if needed)
    CORS_ORIGINS = []
    
    # Content Security Policy
    CSP_POLICY = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            'cdnjs.cloudflare.com'
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            'cdnjs.cloudflare.com'
        ],
        'font-src': [
            "'self'",
            'cdnjs.cloudflare.com'
        ],
        'img-src': [
            "'self'",
            'data:',
            'https://github-readme-stats.vercel.app',
            'https://img.shields.io'
        ],
        'connect-src': ["'self'"],
        'frame-ancestors': ["'none'"],
        'base-uri': ["'self'"],
        'form-action': ["'self'"]
    }


class DevelopmentConfig(Config):
    """Development configuration with relaxed security for local testing"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    FORCE_HTTPS = False


class ProductionConfig(Config):
    """Production configuration with maximum security"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    FORCE_HTTPS = True
    
    # Ensure SECRET_KEY is set
    if not os.environ.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
