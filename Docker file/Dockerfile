FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python logic
COPY ./Pythoncode/functions.py ./functions.py

# Flask app
COPY ./Website/app.py ./app.py

# Templates and static files (включая Bootstrap локально)
COPY ./Website/templates ./templates
COPY ./Website/static ./static

RUN pip3 install --no-cache-dir flask gunicorn

EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
