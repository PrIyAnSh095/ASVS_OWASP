FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy app and shared templates/static
COPY secure/ /app/secure/
COPY templates/ /app/templates/
COPY static/ /app/static/
WORKDIR /app/secure
EXPOSE 5000
CMD ["python", "app.py"]
