FROM python:3.9-slim
WORKDIR /app
COPY vulnerable/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY vulnerable/ /app/vulnerable/
COPY static/ /app/static/

WORKDIR /app/vulnerable
EXPOSE 5000
CMD ["python", "app.py"]
