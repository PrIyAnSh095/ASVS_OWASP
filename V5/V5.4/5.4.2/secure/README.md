# ASVS 5.4.2 Lab Documentation

This directory contains the files and implementations demonstrating OWASP ASVS Control 5.4.2 (Level 2).

## Lab Directories

- **`secure/`**: Secure Flask app running on port `5000` which safely sanitizes/encodes filenames inside `Content-Disposition` headers using RFC 6266 rules.
- **`vulnerable/`**: Vulnerable Flask app running on port `5001` which naively interpolates user input into `Content-Disposition` headers, allowing CRLF and response header injections.
- **`docs/`**: Complete theory, attack models, testing guides, and verification credentials.
- **`tests/`**: Automated script samples and HTTP payloads for curl and Burp Suite verification.

## Getting Started

Start both labs using Docker Compose from the root directory of this control:

```bash
docker compose -f secure/docker-compose.yml up --build -d
docker compose -f vulnerable/docker-compose.yml up --build -d
```

Access:
- **Secure Lab**: `http://localhost:5000`
- **Vulnerable Lab**: `http://localhost:5001`
