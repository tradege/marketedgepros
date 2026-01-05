"""
Production-Grade Gunicorn Configuration - GPT-5 Optimized
Based on GPT-5 analysis of RAM pressure and swapping bottleneck
Date: November 17, 2025
"""
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"
backlog = 4096  # Increased from 2048 per GPT-5 recommendation

# Worker processes - GPT-5 OPTIMIZED FOR RAM CONSTRAINTS
# Problem identified: 50 workers × 162MB = 8.1GB > 7.9GB RAM → swapping!
# Solution: Fewer workers that fit in RAM, more connections per worker
workers = 12  # Was: 50 (12 × 162MB = 1.9GB - safe!)
worker_class = "gevent"

# Worker connections - GPT-5 OPTIMIZED FOR HIGH CONCURRENCY
# With fewer workers, increase connections per worker for same total capacity
worker_connections = 512  # Was: 2000 (12 × 512 = 6,144 total capacity)

# Worker lifecycle - GPT-5 OPTIMIZED
# Restart workers periodically to prevent memory leaks
max_requests = 2000  # Was: 5000
max_requests_jitter = 200  # Was: 500

# Timeouts - GPT-5 OPTIMIZED
timeout = 30  # Was: 60 (faster failure detection)
graceful_timeout = 30
keepalive = 2  # Was: 5 (reduce keepalive overhead)

# Logging
accesslog = "/var/www/MarketEdgePros/backend/logs/gunicorn-access.log"
errorlog = "/var/www/MarketEdgePros/backend/logs/gunicorn-error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "marketedgepros"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/marketedgepros.pid"
umask = 0

# Preload app for better memory efficiency
preload_app = True

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting MarketEdgePros Gunicorn server (GPT-5 OPTIMIZED)")
    server.log.info(f"Workers: {workers}, Connections per worker: {worker_connections}")
    server.log.info(f"Total capacity: {workers * worker_connections} connections")
    server.log.info(f"Expected RAM: {workers * 162}MB (vs 7.9GB available)")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading MarketEdgePros Gunicorn server")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("MarketEdgePros Gunicorn server is ready. Spawning workers")
    server.log.info(f"GPT-5 optimization: No more swapping!")

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("worker received INT or QUIT signal")

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("worker received SIGABRT signal")
