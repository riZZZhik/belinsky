#!/bin/bash

echo Starting Belinsky application.
exec gunicorn wsgi:app --config "${BELINSKY_GUNICORN_CONFIG-gunicorn_config.py}"