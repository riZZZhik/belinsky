FROM --platform=linux/amd64 python:3.8 as base
LABEL MAINTAINER="Dmitry Barsukoff <t.me/riZZZhik>"

# Install requirements
WORKDIR /word_finder
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download pymystem weights
RUN python -c "from pymystem3 import autoinstall; autoinstall()"

# Copy work files
COPY app app
COPY modules modules
COPY main.py .

# Create production target
FROM base as production

# Expose Flask port
EXPOSE 5000

# Default execute
CMD ["gunicorn", "main:\"create_app()\"", "-b 0.0.0.0:5000"]

# Create test target
FROM base as test

# Install unittest dependencies
RUN pip install flask-unittest==0.1.2
COPY test.py .

# Default execute
CMD ["python", "test.py"]