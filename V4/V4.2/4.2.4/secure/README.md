# ASVS 4.2.4 — Secure Implementation

> **ASVS Chapter**: V4.2 HTTP Message Structure Validation  
> **Control**: 4.2.4 | **Level**: 3  
> **Status**: ✅ PASS

## Overview

This is the **secure** implementation for ASVS control 4.2.4. The application validates every incoming HTTP header name and value, rejecting any request that contains CR (`\r`), LF (`\n`), or CRLF (`\r\n`) sequences.

CRLF injection in HTTP headers is the root cause of:
- **Header Injection** — Attacker-controlled headers in responses
- **HTTP Response Splitting** — Two responses from one request
- **Log Injection** — Forged server log entries
- **Cache Poisoning** — Malicious content served from shared caches

## ASVS Requirement

> Verify that the application only accepts HTTP/2 and HTTP/3 requests where the header fields and values do not contain any CR (`\r`), LF (`\n`), or CRLF (`\r\n`) sequences, to prevent header injection attacks.

## How This App Satisfies 4.2.4

1. A Flask `before_request` hook inspects **every header name and value** using a regex `[\r\n]`
2. Any match triggers an immediate **HTTP 400 Bad Request** with violation details
3. User-supplied data is also validated before being set in response headers
4. The application never reflects unsanitized user input in HTTP headers

## Project Structure

```
secure/
├── app.py                  # Flask application with CRLF validation
├── Dockerfile              # Container definition (uses Hypercorn for HTTP/2)
├── docker-compose.yml      # Compose configuration (port 5000)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/
│   ├── layout.html         # Base HTML template
│   └── index.html          # Educational interactive UI
└── static/
    ├── css/style.css       # Design system styles
    └── js/app.js           # Interactive lab JavaScript
```

## Docker Setup

### Prerequisites

- Docker Engine 24+
- Docker Compose v2+

### Running the Secure App

```bash
cd V4/V4.2/4.2.4/secure
docker compose up --build
```

The app will be available at: **http://localhost:5000**

### Stopping

```bash
docker compose down
```

## Browser Testing

1. Navigate to **http://localhost:5000**
2. Use the preset payload buttons to inject CR, LF, or CRLF
3. Observe the **HTTP 400** rejection and violation details
4. Compare with the vulnerable app at **http://localhost:5001**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Educational UI |
| `POST` | `/api/validate-header` | Validate a header name/value pair |
| `GET`  | `/api/echo-header?name=X&value=Y` | Echo a header (validates first) |
| `GET`  | `/api/info` | Implementation metadata |

### Example: Valid Header

```bash
curl -s -X POST http://localhost:5000/api/validate-header \
  -H "Content-Type: application/json" \
  -d '{"header_name":"X-Custom","header_value":"safe-value"}'
```

**Expected**: HTTP 200, `"verdict": "ACCEPTED"`, `"asvs_pass": true`

### Example: CRLF Injection Attempt

```bash
curl -s -X POST http://localhost:5000/api/validate-header \
  -H "Content-Type: application/json" \
  -d "{\"header_name\":\"X-Attack\",\"header_value\":\"value\r\nSet-Cookie: evil=1\"}"
```

**Expected**: HTTP 400, `"verdict": "REJECTED"`, violations listed

## PASS Behaviour

| Scenario | Response | ASVS 4.2.4 |
|----------|----------|------------|
| Clean header `X-Foo: bar` | HTTP 200, ACCEPTED | ✅ PASS |
| Header with `\r` | HTTP 400, REJECTED | ✅ PASS |
| Header with `\n` | HTTP 400, REJECTED | ✅ PASS |
| Header with `\r\n` | HTTP 400, REJECTED | ✅ PASS |

## Burp Suite Testing

1. Set Burp as your proxy
2. Browse to http://localhost:5000
3. Send the POST to `/api/validate-header` to Repeater
4. Modify the `header_value` JSON field to include `\r\n`
5. Observe the 400 rejection

> **Note**: Burp Repeater with JSON body is the recommended method. Injecting literal CRLF into actual HTTP headers via Burp is blocked at the HTTP/2 framing layer by Hypercorn. The API approach accurately demonstrates the application-layer validation ASVS 4.2.4 requires.

## Learning Outcomes

After completing this lab, students will be able to:

1. Explain what CR, LF, and CRLF are and their significance in HTTP/1.1
2. Describe how CRLF injection enables Header Injection and Response Splitting
3. Understand why HTTP/2 binary framing alone is not sufficient
4. Implement application-level CRLF validation using `before_request` hooks
5. Articulate the defence-in-depth principle for HTTP header security
6. Reference RFC 9113 §8.2.1 and RFC 9114 §4.2 for protocol requirements
