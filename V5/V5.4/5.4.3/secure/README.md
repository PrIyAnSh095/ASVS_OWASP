# ASVS 5.4.3 Upload Antivirus Lab

This workspace contains code and materials demonstrating OWASP ASVS Control 5.4.3 (Level 2).

## Directory Layout
- **`secure/`**: Secure Flask app running on port `5000`. Features an upload pipeline implementing temporary Quarantine zones, simulated Antivirus Scanning (EICAR check), threat logging, and Clean Downloads promotion.
- **`vulnerable/`**: Vulnerable Flask app running on port `5001`. Saves uploads directly into clean download zones with no AV validation.
- **`docs/`**: Comprehensive guides detailing attack methodologies, theoretical context, pass/fail standards, and verification tutorials.
- **`tests/`**: Practical command scripts, curl recipes, and raw proxy formats.

## Quick Start
Run containers using:
```bash
docker compose -f secure/docker-compose.yml up --build -d
docker compose -f vulnerable/docker-compose.yml up --build -d
```

- **Secure Lab**: `http://localhost:5000`
- **Vulnerable Lab**: `http://localhost:5001`
