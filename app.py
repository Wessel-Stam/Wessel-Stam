"""
Secure Flask Web Application
Portfolio website with comprehensive security features

Author: Wessel Stam
Security Features:
- HTTPS/TLS enforcement
- Security headers (CSP, HSTS, X-Frame-Options, etc.)
- CSRF protection
- Rate limiting
- Secure session management
- Input validation
- XSS protection
"""

from flask import Flask, render_template, send_from_directory, request, abort
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import logging
from datetime import timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            static_folder='.',
            template_folder='.')

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Trust proxy headers (for deployment behind reverse proxy)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# CSRF Protection
csrf = CSRFProtect(app)

# Content Security Policy
csp = {
    'default-src': ["'self'"],
    'script-src': [
        "'self'",
        "'unsafe-inline'",  # Needed for inline scripts in current implementation
        'cdnjs.cloudflare.com'
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",  # Needed for inline styles
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

# Security Headers with Flask-Talisman
talisman = Talisman(
    app,
    force_https=os.environ.get('FLASK_ENV') == 'production',
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,  # 1 year
    strict_transport_security_include_subdomains=True,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src'],
    referrer_policy='strict-origin-when-cross-origin',
    feature_policy={
        'geolocation': "'none'",
        'microphone': "'none'",
        'camera': "'none'"
    }
)

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


@app.after_request
def set_security_headers(response):
    """Add additional security headers to all responses"""
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # XSS Protection (for older browsers)
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Remove server header
    response.headers.pop('Server', None)
    
    # Permissions Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    return response


@app.errorhandler(404)
def not_found(e):
    """Custom 404 error handler"""
    logger.warning(f"404 error: {request.url}")
    return "Page not found", 404


@app.errorhandler(403)
def forbidden(e):
    """Custom 403 error handler"""
    logger.warning(f"403 error: {request.url}")
    return "Forbidden", 403


@app.errorhandler(500)
def internal_error(e):
    """Custom 500 error handler"""
    logger.error(f"500 error: {str(e)}")
    return "Internal server error", 500


@app.route('/')
@limiter.limit("30 per minute")
def index():
    """Serve the main portfolio page"""
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        logger.error(f"Error serving index: {str(e)}")
        abort(500)


@app.route('/<path:filename>')
@limiter.limit("100 per minute")
def serve_static(filename):
    """Serve static files with security checks"""
    # Prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        logger.warning(f"Directory traversal attempt: {filename}")
        abort(403)
    
    # Whitelist allowed file extensions
    allowed_extensions = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp'}
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        logger.warning(f"Unauthorized file type requested: {filename}")
        abort(403)
    
    try:
        return send_from_directory('.', filename)
    except FileNotFoundError:
        abort(404)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        abort(500)


@app.route('/health')
@csrf.exempt  # Health check endpoint doesn't need CSRF
@limiter.limit("10 per minute")
def health_check():
    """Health check endpoint for monitoring"""
    return {'status': 'healthy', 'service': 'portfolio-webapp'}, 200


if __name__ == '__main__':
    # Development server (use Gunicorn for production)
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    if debug_mode:
        logger.warning("Running in development mode. DO NOT use in production!")
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=True,
            ssl_context='adhoc'  # Self-signed cert for development
        )
    else:
        logger.info("Starting production server")
        # In production, this should be run through Gunicorn/uWSGI
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=False
        )
