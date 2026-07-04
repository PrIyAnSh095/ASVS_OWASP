# ASVS 4.2.4 — Vulnerable Implementation

> **ASVS Chapter**: V4.2 HTTP Message Structure Validation  
> **Control**: 4.2.4 | **Level**: 3  
> **Status**: ❌ FAIL

## Overview

This is the **vulnerable** implementation for ASVS control 4.2.4. The application **intentionally omits** CRLF header validation, demonstrating what happens when an application fails to check for CR (`\r`), LF (`\n`), and CRLF (`\r\n`) sequences in header names and values.

> ⚠️ **Educational Notice**: This application is intentionally insecure for teaching purposes. Do not deploy in production.

## Why This Fails ASVS 4.2.4

The application has:
- ❌ **No** `before_request` hook to validate incoming headers
- ❌ **No** `validate_headers()` function
- ❌ **No** regex check for `[\r\n]` in any endpoint
- ❌ **No** rejection logic for malformed headers
- ❌ **No** sanitization before logging header values

## An Important Note About HTTP/2 and CRLF

Modern HTTP/2 servers (Hypercorn, h2, Nginx, etc.) prevent raw CRLF bytes from being injected at the **wire/framing level**. This is by design — HTTP/2 uses binary framing, not text-based headers.

**However, this does NOT mean applications are safe by default.** The vulnerability demonstrated here is at the **application layer**:

1. User-supplied data containing `\r\n` reaches application code via JSON, form fields, or URL parameters
2. The application uses this data in response headers, log statements, or forwards it to HTTP/1.1 backends
3. Without application-level validation, these downstream systems become vulnerable

ASVS 4.2.4 explicitly requires application validation, not reliance on the transport layer.

## ASVS Requirement (NOT MET)

> Verify that the application only accepts HTTP/2 and HTTP/3 requests where the header fields and values do not contain any CR (`\r`), LF (`\n`), or CRLF (`\r\n`) sequences, to prevent header injection attacks.

## Project Structure

```
vulnerable/
├── app.py                  # Flask application — NO CRLF validation
├── Dockerfile              # Container definition (Hypercorn HTTP/2)
├── docker-compose.yml      # Compose configuration (port 5001)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/
│   ├── layout.html         # Base HTML template
│   └── index.html          # Educational attack demonstrator UI
└── static/
    ├── css/style.css       # Design system styles
    └── js/app.js           # Interactive lab JavaScript
```

## Docker Setup

### Running the Vulnerable App

```bash
cd V4/V4.2/4.2.4/vulnerable
docker compose up --build
```

The app will be available at: **http://localhost:5001**

### Stopping

```bash
docker compose down
```

## Browser Testing

1. Navigate to **http://localhost:5001**
2. Use the attack payload preset buttons (CR, LF, CRLF, Log Injection, Response Split)
3. Observe that the app **accepts** these payloads without rejection
4. Examine the simulated HTTP/1.1 injection output
5. Compare with the secure app at **http://localhost:5000**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Educational attack demonstrator UI |
| `POST` | `/api/validate-header` | Processes header without validation (VULNERABLE) |
| `GET`  | `/api/echo-header?name=X&value=Y` | Echoes header without validation (VULNERABLE) |
| `GET`  | `/api/info` | Implementation metadata |

### Example: CRLF Injection — Accepted (FAIL)

```bash
curl -s -X POST http://localhost:5001/api/validate-header \
  -H "Content-Type: application/json" \
  -d "{\"header_name\":\"X-Attack\",\"header_value\":\"value\r\nSet-Cookie: evil=1\"}"
```

**Expected**: HTTP 200, `"verdict": "ACCEPTED"`, `"asvs_pass": false`  
This demonstrates the vulnerability — the app accepted a header with CRLF sequences.

### Log Injection Demo

```bash
curl -s -X POST http://localhost:5001/api/validate-header \
  -H "Content-Type: application/json" \
  -d "{\"header_name\":\"X-User-Agent\",\"header_value\":\"Mozilla/5.0\n[ADMIN] LOGIN SUCCESSFUL\"}"
```

Then check Docker logs:
```bash
docker logs asvs-4.2.4-vulnerable
```

You will see the injected log line appear as a separate entry.

## FAIL Behaviour

| Scenario | Response | ASVS 4.2.4 |
|----------|----------|------------|
| Clean header `X-Foo: bar` | HTTP 200, ACCEPTED (no validation done) | ❌ FAIL |
| Header with `\r` | HTTP 200, ACCEPTED | ❌ FAIL |
| Header with `\n` | HTTP 200, ACCEPTED + Log Injection | ❌ FAIL |
| Header with `\r\n` | HTTP 200, ACCEPTED + Header Injection | ❌ FAIL |

## Remediation

To make this application compliant with ASVS 4.2.4, add the following to `app.py`:

```python
import re

CRLF_PATTERN = re.compile(r"[\r\n]")

def validate_headers(headers):
    violations = []
    for name, value in headers.items():
        if CRLF_PATTERN.search(name):
            violations.append(f"Header name '{name}' contains CR/LF")
        if CRLF_PATTERN.search(value):
            violations.append(f"Header '{name}' value contains CR/LF")
    return violations

@app.before_request
def enforce_no_crlf():
    violations = validate_headers(dict(request.headers))
    if violations:
        return jsonify({"status": "REJECTED", "violations": violations}), 400
```

See `secure/app.py` for the complete reference implementation.

## Learning Outcomes

After completing this lab, students will be able to:

1. Identify the missing CRLF validation in vulnerable application code
2. Demonstrate CRLF injection via the interactive API
3. Explain the difference between transport-layer and application-layer protection
4. Understand log injection and its impact on security monitoring
5. Write the remediation code to make the application ASVS 4.2.4 compliant
6. Articulate why HTTP/2 binary framing alone does not satisfy ASVS 4.2.4
