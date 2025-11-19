"""
Gunicorn configuration file for production deployment
Optimized for security and performance
"""

import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.environ.get('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'portfolio-webapp'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if using gunicorn for SSL termination)
# In production, typically SSL is handled by nginx/reverse proxy
keyfile = os.environ.get('SSL_KEYFILE')
certfile = os.environ.get('SSL_CERTFILE')
ssl_version = 'TLSv1_2'
cert_reqs = 0
ca_certs = None
suppress_ragged_eofs = True
do_handshake_on_connect = False
ciphers = 'TLSv1.2'

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized"""
    server.log.info("Starting Gunicorn server")


def on_reload(server):
    """Called to recycle workers during a reload"""
    server.log.info("Reloading Gunicorn server")


def when_ready(server):
    """Called just after the server is started"""
    server.log.info("Gunicorn server is ready. Spawning workers")


def pre_fork(server, worker):
    """Called just before a worker is forked"""
    pass


def post_fork(server, worker):
    """Called just after a worker has been forked"""
    server.log.info(f"Worker spawned (pid: {worker.pid})")


def pre_exec(server):
    """Called just before a new master process is forked"""
    server.log.info("Forking new master process")


def worker_exit(server, worker):
    """Called just after a worker has been exited"""
    server.log.info(f"Worker exited (pid: {worker.pid})")
