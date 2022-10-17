# Create base target
FROM --platform=linux/amd64 python:3.11.0rc2 as base
LABEL MAINTAINER="Dmitry Barsukoff <t.me/riZZZhik>"

# Define default environments
ENV PROMETHEUS_MULTIPROC_DIR /tmp

# Install requirements
WORKDIR /belinsky
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy default work files
COPY belinsky belinsky

# Create production target
FROM base as production

# Copy production work files
COPY wsgi.py .
COPY gunicorn_config.py .

# Default execute
CMD ["gunicorn", "wsgi:app", "--config ${BELINSKY_GUNICORN_CONFIG-gunicorn_config.py}"]

# Create test target
FROM base as test

# Install test requirements
RUN pip install pytest==7.1.1 blinker==1.4

# Copy test work files
COPY tests tests

# Default execute
CMD ["pytest", "-W ignore::DeprecationWarning"]