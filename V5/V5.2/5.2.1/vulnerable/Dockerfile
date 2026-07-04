FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# We limit memory inside the docker container to easily demonstrate OOM DoS
CMD ["python", "app.py"]
