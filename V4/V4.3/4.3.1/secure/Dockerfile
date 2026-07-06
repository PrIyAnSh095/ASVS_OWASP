FROM python:3.9-slim
WORKDIR /app
COPY secure/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY secure/ /app/secure/
COPY static/ /app/static/

WORKDIR /app/secure
EXPOSE 5000
CMD ["python", "app.py"]
