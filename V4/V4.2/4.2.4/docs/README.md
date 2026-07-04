# ASVS 4.2.4 — Lab Overview & README

## Lab Overview

| Property | Value |
|----------|-------|
| **ASVS Chapter** | V4.2 HTTP Message Structure Validation |
| **Control** | 4.2.4 |
| **Level** | 3 (highest) |
| **Topic** | CRLF Header Injection Prevention |
| **Protocol Focus** | HTTP/2 and HTTP/3 |

## Learning Objectives

By completing this lab, students will:

1. Understand the structure of HTTP headers and the role of CRLF in HTTP/1.1
2. Explain why CR (`\r`), LF (`\n`), and CRLF (`\r\n`) sequences are forbidden in HTTP/2 and HTTP/3 header fields
3. Demonstrate CRLF injection and its consequences: Header Injection, Response Splitting, Log Injection
4. Distinguish between transport-layer protection (binary framing) and application-layer validation
5. Implement ASVS 4.2.4 compliant validation in Python/Flask
6. Reference the relevant RFCs: 9113, 9114, and 7230
7. Use Burp Suite and curl to probe CRLF handling

## ASVS Requirement

> **4.2.4 (L3)**: Verify that the application only accepts HTTP/2 and HTTP/3 requests where the header fields and values do not contain any CR (`\r`), LF (`\n`), or CRLF (`\r\n`) sequences, to prevent header injection attacks.

## Project Structure

```
V4/V4.2/4.2.4/
├── secure/                    # ASVS-compliant implementation (port 5000)
│   ├── app.py                 # Flask app with CRLF validation
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── README.md
│   ├── templates/
│   │   ├── layout.html
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
│
├── vulnerable/                # Intentionally insecure (port 5001)
│   ├── app.py                 # Flask app — NO CRLF validation
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── README.md
│   ├── templates/
│   │   ├── layout.html
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
│
├── docs/                      # Educational documentation
│   ├── README.md              # This file
│   ├── theory.md              # HTTP header structure, CRLF, RFC references
│   ├── attack.md              # Attack vectors and techniques
│   ├── burp.md                # Burp Suite walkthrough
│   ├── curl.md                # curl testing guide
│   ├── expected.md            # Expected PASS/FAIL outcomes
│   ├── solution.md            # Complete solution for student challenges
│   └── notes.md               # Educator notes and discussion points
│
├── tests/                     # Test artifacts
│   ├── curl.txt               # curl commands and expected outputs
│   ├── burp_requests.txt      # Sample Burp requests
│   ├── burp_responses.txt     # Expected Burp responses
│   └── payloads.txt           # CRLF payload library
│
└── assets/                    # Screenshots and diagrams
    ├── screenshots/           # (Capture during lab — see notes.md)
    ├── diagrams/
    ├── gifs/
    └── sample-files/
```

## Docker Setup

### Running Both Apps Simultaneously

Open two terminal windows:

**Terminal 1 — Secure App**
```bash
cd V4/V4.2/4.2.4/secure
docker compose up --build
# Access: http://localhost:5000
```

**Terminal 2 — Vulnerable App**
```bash
cd V4/V4.2/4.2.4/vulnerable
docker compose up --build
# Access: http://localhost:5001
```

### Stopping

```bash
# In each terminal:
docker compose down

# Or to remove everything:
docker compose down --volumes --rmi local
```

## Browser Testing

### Secure App (http://localhost:5000)
1. Open the interactive lab
2. Click **CR Injection** preset → observe HTTP 400 rejection
3. Click **LF Injection** preset → observe HTTP 400 rejection
4. Click **CRLF Injection** preset → observe HTTP 400 rejection
5. Submit a clean header → observe HTTP 200 acceptance

### Vulnerable App (http://localhost:5001)
1. Open the attack demonstrator
2. Click **CR Injection** preset → observe the app ACCEPTS it
3. Click **LF Injection** preset → examine the simulated HTTP/1.1 response
4. Click **Log Injection** preset → check Docker logs afterward
5. Click **Response Split** preset → examine the injected second response

## Burp Testing

See `docs/burp.md` for complete walkthrough.

## curl Testing

See `docs/curl.md` for all curl commands.

## PASS Behaviour (Secure App)

| Input | Expected HTTP Status | ASVS 4.2.4 |
|-------|---------------------|------------|
| `X-Foo: legitimate` | 200 OK | ✅ PASS |
| `X-Foo: value\r` | 400 Bad Request | ✅ PASS |
| `X-Foo: value\n` | 400 Bad Request | ✅ PASS |
| `X-Foo: value\r\n` | 400 Bad Request | ✅ PASS |
| `X-Foo\r: value` | 400 Bad Request | ✅ PASS |

## FAIL Behaviour (Vulnerable App)

| Input | Expected HTTP Status | ASVS 4.2.4 |
|-------|---------------------|------------|
| `X-Foo: legitimate` | 200 OK (no validation) | ❌ FAIL |
| `X-Foo: value\r` | 200 OK (accepted) | ❌ FAIL |
| `X-Foo: value\n` | 200 OK + log injection | ❌ FAIL |
| `X-Foo: value\r\n` | 200 OK + header injection | ❌ FAIL |
