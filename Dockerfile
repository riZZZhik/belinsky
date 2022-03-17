FROM --platform=linux/amd64 python:3.8 as base
LABEL MAINTAINER="Dmitry Barsukoff <t.me/riZZZhik>"

# Setup Flask
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

# Install requirements
WORKDIR /word_finder
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy work files
COPY word_finder word_finder
COPY app.py .

# Create production entrypoint
FROM base as production
EXPOSE $FLASK_RUN_PORT
ENTRYPOINT ["flask", "run"]

# Create test entrypoint
FROM base as test

RUN pip install flask-unittest
COPY test_app.py .

ENV FLASK_ENV=development
ENTRYPOINT ["python3", "test_app.py"]