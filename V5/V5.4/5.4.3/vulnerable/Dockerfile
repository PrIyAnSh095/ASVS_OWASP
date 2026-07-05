# Dockerfile for ASVS 5.4.3 Vulnerable Lab
FROM python:3.12-slim

WORKDIR /app

COPY vulnerable/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY vulnerable/ /app/vulnerable/
COPY templates/ /app/templates/
COPY static/ /app/static/

WORKDIR /app/vulnerable

# Create the downloads/uploads directories
RUN mkdir -p downloads static/files

EXPOSE 5001

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

CMD ["flask", "run"]
