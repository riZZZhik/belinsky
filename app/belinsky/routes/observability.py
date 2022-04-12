"""Belinsky observability blueprint."""
from flask import Blueprint
from healthcheck import HealthCheck, EnvironmentDump
from prometheus_client import multiprocess, generate_latest, CollectorRegistry

from ..database import get_all
from ..models import User


# Create healthcheck function
def check_database():
    """Check database is available."""
    get_all(User)
    return True, 'Belinsky database is ok'


# Create observability function
def metrics_prometheus():
    """Generate prometheus metrics response."""
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return data, 200


def create_blueprint_observability():
    """Create observability blueprint."""
    # Create blueprint
    observability_bp = Blueprint('observability', __name__)

    # Register healthcheck route
    health = HealthCheck()
    health.add_check(check_database)
    observability_bp.add_url_rule("/healthcheck", "healthcheck", view_func=health.run)

    env_dump = EnvironmentDump()
    observability_bp.add_url_rule("/environment", "environment", view_func=env_dump.run)

    # Register prometheus route
    observability_bp.add_url_rule("/metrics/prometheus", "prometheus", view_func=metrics_prometheus)

    return observability_bp
