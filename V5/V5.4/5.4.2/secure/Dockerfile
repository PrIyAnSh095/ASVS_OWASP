# Dockerfile for ASVS 5.4.2 Secure Lab
FROM python:3.12-slim

WORKDIR /app

COPY secure/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY secure/ /app/secure/
COPY templates/ /app/templates/
COPY static/ /app/static/

WORKDIR /app/secure

# Create the sample-files directory with test files
RUN mkdir -p static/files && \
    echo "This is a sample PDF document for testing." > static/files/sample.pdf && \
    echo "This is a sample document with spaces in the filename." > "static/files/sample with spaces.pdf" && \
    echo "This is a sample document with unicode character checkmark." > "static/files/sample_checkmark.pdf"

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["flask", "run"]
