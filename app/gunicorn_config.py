"""Belinsky configuration for gunicorn."""
from prometheus_client import multiprocess


def child_exit(server, worker):
    """Mark process dead for correct prometheus metrics."""
    multiprocess.mark_process_dead(worker.pid)
