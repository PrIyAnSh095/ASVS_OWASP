# Dockerfile for ASVS 5.4.2 Vulnerable Lab
FROM python:3.12-slim

WORKDIR /app

COPY vulnerable/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY vulnerable/ /app/vulnerable/
COPY templates/ /app/templates/
COPY static/ /app/static/

WORKDIR /app/vulnerable

# Create the uploads/sample-files directory and a sample file
RUN mkdir -p static/files && \
    echo "This is a sample PDF document for testing." > static/files/sample.pdf && \
    echo "This is a sample document with spaces in the filename." > "static/files/sample with spaces.pdf" && \
    echo "This is a sample document with Unicode character checkmark." > "static/files/sample_✓.pdf"

EXPOSE 5001

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

CMD ["flask", "run"]
