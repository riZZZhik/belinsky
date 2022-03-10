FROM --platform=linux/amd64 python:3.8 as base
LABEL MAINTAINER="Dmitry Barsukoff <t.me/riZZZhik>"

# Setup Flask
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0

# Install requirements
WORKDIR /word_finder
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy work files
COPY word_finder .
COPY app.py .

# Create test entrypoint
FROM base as test
COPY test_app.py .
ENTRYPOINT ["python", "test_app.py"]

# Create production entrypoint
FROM base as production
EXPOSE 5000
ENTRYPOINT ["flask", "run"]