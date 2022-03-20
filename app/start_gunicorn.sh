#!/bin/bash

echo Starting Belinsky application.

params="${BELINSKY_WSGI_MODULE-wsgi:app} \
--config ${BELINSKY_GUNICORN_CONFIG-gunicorn_config.py} \
--bind 0.0.0.0:5000 \
--workers ${BELINSKY_NUM_WORKERS-4} \
--threads ${BELINSKY_NUM_THREADS-1} \
--worker-class ${BELINSKY_WORKER_CLASS-sync} \
--worker-connections ${BELINSKY_NUM_WORKER_CONNECTIONS-1000} \
--access-logfile ${BELINSKY_ACCESS_LOGFILE-"-"} \
--error-logfile ${BELINSKY_ERROR_LOGFILE-"-"}"
echo "gunicorn parameters: $params"

exec gunicorn $params