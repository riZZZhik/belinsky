# Setup machine
FROM --platform=linux/amd64 python:3.8
LABEL MAINTAINER="Dmitry Barsukoff <t.me/riZZZhik>"

# Setup Flask
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

# Install requirements
WORKDIR /word_finder
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Run code
COPY . .
ENTRYPOINT ["flask", "run"]
