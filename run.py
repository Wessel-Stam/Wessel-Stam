#!/usr/bin/env python3
"""
Development server runner
For production, use gunicorn with the provided configuration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import app
from app import app, logger


def main():
    """Run the development server"""
    env = os.environ.get('FLASK_ENV', 'development')
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    if env == 'production':
        logger.error("DO NOT use run.py in production! Use gunicorn instead:")
        logger.error("  gunicorn -c gunicorn.conf.py app:app")
        sys.exit(1)
    
    logger.info(f"Starting development server on {host}:{port}")
    logger.info("Press Ctrl+C to stop")
    logger.warning("This is a development server. Do not use in production!")
    
    try:
        # Run with self-signed certificate for HTTPS in development
        # Debug mode is intentionally enabled for development only
        # This script exits with error if FLASK_ENV=production (checked above)
        app.run(
            host=host,
            port=port,
            debug=True,
            ssl_context='adhoc'
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
