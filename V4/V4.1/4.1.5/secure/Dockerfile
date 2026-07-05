FROM python:3.11-slim
WORKDIR /app
COPY secure/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY secure/ /app/secure/
COPY templates/ /app/templates/
COPY static/ /app/static/

WORKDIR /app/secure
EXPOSE 5000
CMD ["python", "app.py"]
