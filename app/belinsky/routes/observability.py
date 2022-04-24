"""Belinsky observability blueprint."""
import os

from flask import Blueprint
from healthcheck import HealthCheck
from healthcheck.security import safe_dict
from prometheus_client import CollectorRegistry, generate_latest, multiprocess

from ..database import get_all
from ..models import User


# Create healthcheck function
def check_database() -> tuple[bool, str]:
    """Check database is available."""
    get_all(User)
    return True, "Belinsky database is ok"


# Create observability function
def metrics_prometheus() -> tuple[bytes, int]:
    """Generate prometheus metrics response."""
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return data, 200


# Create environment function
def environment() -> tuple[dict, int]:
    """Generate application environment response."""
    return safe_dict(os.environ, ["key", "token", "pass", "credentials"]), 200


def create_blueprint_observability() -> Blueprint:
    """Create observability blueprint."""
    # Create blueprint
    observability_bp = Blueprint("observability", __name__)

    # Register healthcheck route
    health = HealthCheck()
    health.add_check(check_database)
    observability_bp.add_url_rule("/healthcheck", "healthcheck", view_func=health.run)

    # Register environment route
    observability_bp.add_url_rule("/environment", "environment", view_func=environment)

    # Register prometheus route
    observability_bp.add_url_rule(
        "/metrics/prometheus", "prometheus", view_func=metrics_prometheus
    )

    return observability_bp
