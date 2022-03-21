from flask import Blueprint
from healthcheck import HealthCheck, EnvironmentDump
from prometheus_client import multiprocess, generate_latest, CollectorRegistry

from .database import get_all
from .models import User

main_bp = Blueprint('main', __name__)


# Register healthcheck routes
def check_database():
    get_all(User)
    return True, 'Belinsky database is ok'


health = HealthCheck()
health.add_check(check_database)
main_bp.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())

env_dump = EnvironmentDump()
main_bp.add_url_rule("/environment", "environment", view_func=lambda: env_dump.run())


# Register prometheus route
@main_bp.route("/metrics/prometheus")
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return data, 200
