FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# We limit disk space write logic or memory to observe crashes, but standard docker is fine.
CMD ["python", "app.py"]
