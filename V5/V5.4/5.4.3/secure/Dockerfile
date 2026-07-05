# Dockerfile for ASVS 5.4.3 Secure Lab
FROM python:3.12-slim

WORKDIR /app

COPY secure/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY secure/ /app/secure/
COPY templates/ /app/templates/
COPY static/ /app/static/

WORKDIR /app/secure

# Create the uploads/quarantine/downloads directories
RUN mkdir -p uploads quarantine downloads static/files

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["flask", "run"]
