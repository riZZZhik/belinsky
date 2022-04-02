# Create base target
FROM --platform=linux/amd64 python:3.10.4 as base
LABEL MAINTAINER="Dmitry Barsukoff <t.me/riZZZhik>"

# Define default environments
ENV PROMETHEUS_MULTIPROC_DIR /tmp

# Install requirements
WORKDIR /belinsky
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download spacy weights
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm

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
CMD ["python", "app_test.py"]