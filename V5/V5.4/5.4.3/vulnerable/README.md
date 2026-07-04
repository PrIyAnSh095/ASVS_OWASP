# ASVS 5.4.3 Vulnerable Lab

This directory contains the vulnerable implementation of the upload processing server.

## Running the Lab

Build and launch the application:
```bash
docker compose up --build -d
```

Visit the frontend at `http://localhost:5001`. Test how uploading an EICAR threat payload makes it immediately available to anyone for downloading.
