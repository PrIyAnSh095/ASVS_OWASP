FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy app and shared templates/static
COPY vulnerable/ /app/vulnerable/
COPY templates/ /app/templates/
COPY static/ /app/static/
WORKDIR /app/vulnerable
EXPOSE 5000
CMD ["python", "app.py"]
