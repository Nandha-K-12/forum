"""
Gunicorn configuration for production deployment.
"""
import os
import multiprocessing

port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"
workers = 2
worker_class = "sync"
timeout = 120
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
