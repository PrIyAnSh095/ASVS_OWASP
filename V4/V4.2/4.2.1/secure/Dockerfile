FROM python:3.11-slim

WORKDIR /app

# No external packages needed - uses stdlib only (socket, threading)
COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
