# ASVS 5.4.2 Vulnerable Lab Documentation

This directory contains the vulnerable implementation of the file download server.

## Vulnerability

The application takes a user-supplied filename and interpolates it directly into the `Content-Disposition` header:

```python
response.headers['Content-Disposition'] = f"attachment; filename={filename_param}"
```

## Running the Lab

Start the container using:

```bash
docker compose up --build -d
```

Access the app on `http://localhost:5001`. Use the test suite or curl commands in the parent `tests/` directory to demonstrate Header and CRLF Injection.
