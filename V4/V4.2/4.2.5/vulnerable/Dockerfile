FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Copy static files appropriately
COPY ../static /static
COPY ../templates /templates
CMD ["python", "app.py"]
