FROM python:3.9-slim
WORKDIR /app
COPY vulnerable/requirements.txt .
RUN pip install -r requirements.txt
COPY vulnerable/ /app/vulnerable/
COPY templates/ /app/templates/
COPY static/ /app/static/
WORKDIR /app/vulnerable
EXPOSE 5000
CMD ["python", "app.py"]
