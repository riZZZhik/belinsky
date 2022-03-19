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

# Copy work files
COPY modules modules
COPY app.py .
COPY gunicorn_config.py .

# Create production target
FROM base as production

# Default execute
CMD ["gunicorn", "app:\"create_app()\"", "-b 0.0.0.0:5000"]

# Create test target
FROM base as test

# Install unittest dependencies
RUN pip install flask-unittest==0.1.2
COPY app_test.py .

# Default execute
CMD ["python", "test.py"]