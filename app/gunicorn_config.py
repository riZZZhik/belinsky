"""Belinsky configuration for gunicorn."""
# pylint: disable=invalid-name,unused-argument
import os
import multiprocessing

from loguru import logger
from prometheus_client import multiprocess

# Gunicorn config variables
# Host configuration
bind = "0.0.0.0:5000"

# Resources configuration
preload_app = True
worker_class = os.getenv("BELINSKY_WORKER_CLASS", "sync")
worker_connections = int(os.getenv("BELINSKY_NUM_WORKER_CONNECTIONS", "1000"))
if "BELINSKY_NUM_WORKERS" in os.environ and "BELINSKY_NUM_THREADS" in os.environ:
    workers = int(os.environ["BELINSKY_NUM_WORKERS"])
    threads = int(os.environ["BELINSKY_NUM_THREADS"])
else:
    workers = multiprocessing.cpu_count() * 2 + 1
    threads = 1

# Logs configuration
accesslog = os.getenv("BELINSKY_ACCESS_LOGFILE", "-")
errorlog = os.getenv("BELINSKY_ERROR_LOGFILE", "-")


# Print configuration
def __repr__():
    config = {
        "bind": bind,
        "workers": workers,
        "threads": threads,
        "worker_class": worker_class,
        "worker_connections": worker_connections,
        "preload_app": preload_app,
        "accesslog": accesslog,
        "errorlog": errorlog,
    }
    return ", ".join(f"{key}: {value}" for key, value in config.items())


logger.info("Gunicorn configuration: " + __repr__())


# noinspection PyUnusedLocal
def child_exit(server, worker):
    """Mark process dead for correct prometheus metrics."""
    multiprocess.mark_process_dead(worker.pid)
