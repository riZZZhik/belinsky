FROM --platform=linux/amd64 python:3.8 as base
LABEL MAINTAINER="Dmitry Barsukoff <t.me/riZZZhik>"

# Define default environments
ENV PROMETHEUS_MULTIPROC_DIR /tmp

# Install requirements
WORKDIR /belinsky
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download pymystem weights
RUN python -c "from pymystem3 import autoinstall; autoinstall()"

# Copy default work files
COPY belinsky belinsky

# Create production target
FROM base as production

# Copy production work files
COPY wsgi.py .
COPY gunicorn_config.py .
COPY start_gunicorn.sh .

# Default execute
CMD ["sh", "start_gunicorn.sh"]

# Create test target
FROM base as test

# Install unittest dependencies
RUN pip install flask-unittest==0.1.2

# Copy test work files
COPY app_test.py .

# Default execute
CMD ["python", "test.py"]