# ASVS 4.2.3 - HTTP/2 Message Structure Validation

## Overview

This lab demonstrates ASVS Control 4.2.3, which requires that applications do not accept HTTP/2 or HTTP/3 messages containing connection-specific header fields such as `Transfer-Encoding`, `Connection`, `Keep-Alive`, `Upgrade`, `Proxy-Connection`, and `Trailer`.

These headers are forbidden in HTTP/2 (RFC 7540) because:
1. HTTP/2 uses multiplexing - multiple logical streams share one TCP connection
2. Connection-scoped concepts are meaningless in this architecture
3. Accepting them enables header injection, response splitting, and request smuggling attacks

## Learning Objectives

After completing this lab, you will understand:

- Why HTTP/2 forbids connection-specific headers
- The architectural differences between HTTP/1.1 and HTTP/2
- How header injection attacks work
- Response splitting vulnerabilities
- Request smuggling via protocol confusion
- How to implement proper HTTP/2 header validation
- How to test for this vulnerability using multiple tools

## Project Structure

```
V4/V4.2/4.2.3/
├── docker-compose.yml           # Run both apps together
├── secure/                       # ASVS 4.2.3 COMPLIANT
│   ├── app.py                    # Flask app with header validation
│   ├── Dockerfile                # Container configuration
│   ├── docker-compose.yml        # Standalone compose file
│   ├── requirements.txt           # Python dependencies
│   ├── README.md                  # Secure implementation guide
│   ├── templates/
│   │   ├── layout.html            # Base template
│   │   └── index.html             # Main page
│   └── static/
│       ├── css/style.css          # Styling
│       └── js/app.js              # Frontend logic
├── vulnerable/                   # ASVS 4.2.3 NON-COMPLIANT
│   ├── app.py                    # Flask app without validation
│   ├── Dockerfile                # Container configuration
│   ├── docker-compose.yml        # Standalone compose file
│   ├── requirements.txt           # Python dependencies
│   ├── README.md                  # Vulnerable implementation guide
│   ├── templates/
│   │   ├── layout.html            # Base template
│   │   └── index.html             # Main page
│   └── static/
│       ├── css/style.css          # Styling
│       └── js/app.js              # Frontend logic
├── docs/
│   ├── README.md                 # Documentation index
│   ├── theory.md                 # Detailed technical explanation
│   ├── attack.md                 # Attack vectors and techniques
│   ├── burp.md                   # Burp Suite testing guide
│   ├── curl.md                   # curl command reference
│   ├── expected.md               # Expected test results
│   ├── solution.md               # How to fix the vulnerable app
│   └── notes.md                  # Additional notes and references
├── tests/
│   ├── curl.txt                  # curl command examples
│   ├── burp_requests.txt         # Burp request payloads
│   ├── burp_responses.txt        # Expected Burp responses
│   └── payloads.txt              # Header injection payloads
└── assets/
    ├── diagrams/                 # Architecture diagrams
    ├── screenshots/              # Screenshot placeholders
    ├── gifs/                     # Animation placeholders
    └── sample-files/             # Example files
```

## Docker Setup

### Prerequisites

- Docker and Docker Compose installed
- curl (for testing)
- Optional: Burp Suite Community Edition

### Quick Start - Run Both

```bash
cd V4/V4.2/4.2.3/
docker-compose up --build
```

This starts:
- **Secure version:** http://localhost:8000
- **Vulnerable version:** http://localhost:8001

### Run Secure Implementation Only

```bash
cd V4/V4.2/4.2.3/secure/
docker-compose up --build
```

Runs on: http://localhost:8000

### Run Vulnerable Implementation Only

```bash
cd V4/V4.2/4.2.3/vulnerable/
docker-compose up --build
```

Runs on: http://localhost:8001

## Browser Testing

### 1. Access the Lab Interface

- **Secure:** http://localhost:8000
- **Vulnerable:** http://localhost:8001

Both provide an interactive testing interface.

### 2. Understanding the Interface

- **Info Section:** Learn about the control, standards, and why it matters
- **Test Section:** Send custom HTTP requests with different headers
- **Manual Section:** Guides for Burp Suite and curl
- **Comparison Section:** See differences between implementations
- **Learning Outcomes:** Challenge tasks and exercises

### 3. Interactive Testing

The web interface allows you to:
- Select HTTP protocol version (HTTP/1.1, HTTP/2, HTTP/3)
- Add custom headers
- Send request bodies
- View formatted and raw responses
- Identify forbidden headers

## curl Testing

### Important Note

`curl` requires HTTP/2 support (usually with `--http2` flag). Basic curl may not properly demonstrate HTTP/2 behavior.

### Test with Transfer-Encoding Header

```bash
# Secure (should reject)
curl -v --http2 \
  -H "Transfer-Encoding: chunked" \
  http://localhost:8000/api/test

# Expected: HTTP 400 Bad Request
# Message: "HTTP/2 must not contain connection-specific headers"

# Vulnerable (should accept)
curl -v --http2 \
  -H "Transfer-Encoding: chunked" \
  http://localhost:8001/api/test

# Expected: HTTP 200 OK
# Shows what headers were received
```

### Test with Connection Header

```bash
# Secure (should reject)
curl -v --http2 \
  -H "Connection: close" \
  http://localhost:8000/api/test

# Expected: HTTP 400 Bad Request

# Vulnerable (should accept)
curl -v --http2 \
  -H "Connection: close" \
  http://localhost:8001/api/test

# Expected: HTTP 200 OK
```

### Test with Multiple Forbidden Headers

```bash
# Secure (should reject)
curl -v --http2 \
  -H "Transfer-Encoding: chunked" \
  -H "Connection: close" \
  -H "Keep-Alive: timeout=5" \
  http://localhost:8000/api/test

# Expected: HTTP 400 Bad Request
# Lists all forbidden headers found

# Vulnerable (should accept)
curl -v --http2 \
  -H "Transfer-Encoding: chunked" \
  -H "Connection: close" \
  -H "Keep-Alive: timeout=5" \
  http://localhost:8001/api/test

# Expected: HTTP 200 OK
# Shows all headers were accepted
```

### Test with Valid Headers

```bash
# Both should accept valid headers
curl -v --http2 \
  -H "Accept: application/json" \
  -H "User-Agent: curl-test" \
  http://localhost:8000/api/test

# Expected: HTTP 200 OK with PASS status
```

### All Forbidden Headers

Test each individually:

```bash
# Transfer-Encoding
curl -H "Transfer-Encoding: chunked" http://localhost:8000/api/test

# Connection
curl -H "Connection: keep-alive" http://localhost:8000/api/test

# Keep-Alive
curl -H "Keep-Alive: timeout=5, max=100" http://localhost:8000/api/test

# Upgrade
curl -H "Upgrade: h2c" http://localhost:8000/api/test

# Proxy-Connection
curl -H "Proxy-Connection: keep-alive" http://localhost:8000/api/test

# Trailer
curl -H "Trailer: X-Custom-Trailer" http://localhost:8000/api/test
```

## Burp Suite Testing

### Setup

1. Start Burp Suite Community Edition
2. Configure browser to use Burp as proxy (typically 127.0.0.1:8080)
3. Visit http://localhost:8000 or http://localhost:8001

### Testing Workflow

#### 1. Capture a Request

1. In Burp, go to **Proxy** → **Intercept** tab
2. Visit http://localhost:8000/api/test in browser
3. A GET request will be captured
4. Click **Forward** (or send without intercepting)

#### 2. Send to Repeater

1. Right-click the request in **Proxy** → **History**
2. Select **Send to Repeater**
3. Go to **Repeater** tab
4. Modify the request

#### 3. Add Forbidden Headers

Change the request from:

```
GET /api/test HTTP/2
Host: localhost:8000
```

To:

```
GET /api/test HTTP/2
Host: localhost:8000
Transfer-Encoding: chunked
```

4. Click **Send**
5. Observe response: **HTTP 400 Bad Request**

#### 4. Compare Implementations

Repeat with http://localhost:8001:

```
GET /api/test HTTP/2
Host: localhost:8001
Transfer-Encoding: chunked
```

5. Click **Send**
6. Observe response: **HTTP 200 OK** (vulnerable!)

#### 5. Header Injection Testing

Try injecting CRLF sequences in headers:

```
GET /api/test HTTP/2
Host: localhost:8000
User-Agent: test
X-Injection: value%0d%0aX-Injected-Header: malicious

```

**Secure:** Rejected
**Vulnerable:** May accept and reflect

#### 6. Use Intruder for Batch Testing

1. Send request to **Intruder**
2. Payload positions: Add markers around header values
3. Payload list: Add all forbidden headers
4. Launch attack
5. Compare successful/failed requests

## Expected Results

### Secure Implementation (Port 8000)

| Test Case | HTTP Status | Response | ASVS Compliance |
|-----------|------------|----------|-----------------|
| No forbidden headers | 200 OK | PASS | ✓ PASS |
| Transfer-Encoding header | 400 Bad Request | FAIL with reason | ✓ PASS |
| Connection header | 400 Bad Request | FAIL with reason | ✓ PASS |
| Keep-Alive header | 400 Bad Request | FAIL with reason | ✓ PASS |
| Multiple forbidden headers | 400 Bad Request | FAIL, lists all | ✓ PASS |

### Vulnerable Implementation (Port 8001)

| Test Case | HTTP Status | Response | ASVS Compliance |
|-----------|------------|----------|-----------------|
| No forbidden headers | 200 OK | ACCEPTED | ✗ FAIL |
| Transfer-Encoding header | 200 OK | ACCEPTED (wrong!) | ✗ FAIL |
| Connection header | 200 OK | ACCEPTED (wrong!) | ✗ FAIL |
| Keep-Alive header | 200 OK | ACCEPTED (wrong!) | ✗ FAIL |
| Multiple forbidden headers | 200 OK | ACCEPTED (wrong!) | ✗ FAIL |

## Demonstration Script

For educational presentations, run this sequence:

```bash
# 1. Check both apps are running
curl http://localhost:8000/health
curl http://localhost:8001/health

# 2. Show valid request to secure
echo "=== Secure with valid request ==="
curl -H "Accept: application/json" http://localhost:8000/api/test | jq .

# 3. Show valid request to vulnerable
echo "=== Vulnerable with valid request ==="
curl -H "Accept: application/json" http://localhost:8001/api/test | jq .

# 4. Show forbidden header rejection in secure
echo "=== Secure with Transfer-Encoding (should reject) ==="
curl -H "Transfer-Encoding: chunked" http://localhost:8000/api/test | jq .

# 5. Show forbidden header acceptance in vulnerable
echo "=== Vulnerable with Transfer-Encoding (should reject but doesn't) ==="
curl -H "Transfer-Encoding: chunked" http://localhost:8001/api/test | jq .

# 6. Show multiple violations
echo "=== Secure with multiple violations ==="
curl -H "Transfer-Encoding: chunked" -H "Connection: close" http://localhost:8000/api/test | jq .

echo "=== Vulnerable accepts all violations ==="
curl -H "Transfer-Encoding: chunked" -H "Connection: close" http://localhost:8001/api/test | jq .
```

## API Endpoints

### GET /

Main lab interface with interactive testing.

### GET /api/test (POST also supported)

Test endpoint that processes requests and returns validation results.

**Secure Response (Valid Request):**
```json
{
  "status": "PASS",
  "message": "Request accepted - compliant with ASVS 4.2.3",
  "asvs_control": "4.2.3",
  "protocol": "HTTP/2",
  "forbidden_headers_found": []
}
```

**Secure Response (Forbidden Header):**
```json
{
  "status": "FAIL",
  "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
  "asvs_control": "4.2.3",
  "forbidden_headers_found": ["Transfer-Encoding"],
  "reason": "RFC 7540 forbids connection-specific headers..."
}
```

### GET /api/validate

Validate headers and return detailed analysis.

### GET /api/info

Get detailed information about the control, including forbidden headers, why they're dangerous, and attack scenarios.

### GET /health

Health check endpoint.

## Common Issues and Solutions

### Issue: HTTP/1.1 Instead of HTTP/2

**Problem:** curl or browser shows HTTP/1.1 instead of HTTP/2

**Solution:**
- Use `curl --http2` flag explicitly
- Check if your curl supports HTTP/2: `curl --version | grep h2`
- Consider using Burp Suite which has better HTTP/2 support
- Verify docker logs: `docker logs asvs-4-2-3-secure`

### Issue: HTTPS/TLS Errors

**Problem:** SSL certificate errors when testing HTTPS

**Solution:**
- The lab uses HTTP by default, not HTTPS
- If testing HTTPS, use: `curl -k --http2 https://localhost:8000`
- Or disable certificate verification in Burp Suite settings

### Issue: Connection Refused

**Problem:** Cannot connect to localhost:8000 or 8001

**Solution:**
```bash
# Check if containers are running
docker ps | grep asvs-4-2-3

# Check logs
docker logs asvs-4-2-3-secure
docker logs asvs-4-2-3-vulnerable

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Issue: Port Already in Use

**Problem:** Port 8000 or 8001 already in use

**Solution:**
```bash
# Find what's using the port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# Edit docker-compose.yml to use different ports
# Change "8000:8000" to "8010:8000" etc.
```

## Challenge Tasks

Try these exercises to deepen your understanding:

### Task 1: Manual Header Injection

Send a custom header with CRLF injection to the vulnerable app:
```
Header-Name: value%0d%0aX-Injected: malicious
```

Observe the vulnerable app echoing the injected header.

### Task 2: Protocol Confusion

Send HTTP/1.1-specific headers in an HTTP/2 request. Observe:
- Secure: Rejection
- Vulnerable: Acceptance leading to potential confusion

### Task 3: Fix the Vulnerable App

Modify `vulnerable/app.py` to add the same validation as `secure/app.py`:

1. Add the `FORBIDDEN_HTTP2_HEADERS` set
2. Add the `@validate_http2_headers` decorator
3. Apply it to endpoints that process requests
4. Test that it now rejects forbidden headers

### Task 4: Create Custom Payloads

Design header injection payloads that:
- Inject additional headers
- Attempt to split the HTTP response
- Try to trigger cache poisoning

Test against both implementations.

### Task 5: Burp Suite Automation

Use Burp Suite to:
1. Create a macro that sends forbidden headers
2. Use Intruder to test all 6 forbidden headers simultaneously
3. Generate a scan report comparing both implementations

## Real-World Examples

### 2019: HTTP/2 Header Overflow (CVE-2019-9193)

Nginx incorrectly processed certain headers in HTTP/2 connections, allowing header injection.

### 2015: HTTP/2 Dependency Chains (CVE-2015-3193)

OpenSSL HTTP/2 implementation didn't properly validate header field names, allowing injection.

### Request Smuggling via Protocol Confusion

Modern attack: Send HTTP/1.1-style headers in HTTP/2 to confuse proxies and backends about message boundaries.

## Files and Documentation

- [theory.md](docs/theory.md) - Deep technical explanation
- [attack.md](docs/attack.md) - Attack vectors and exploitation techniques
- [burp.md](docs/burp.md) - Detailed Burp Suite testing guide
- [curl.md](docs/curl.md) - curl command reference
- [expected.md](docs/expected.md) - Detailed expected outputs
- [solution.md](docs/solution.md) - How to implement the fix
- [notes.md](docs/notes.md) - Additional references and resources

## References

- [RFC 7540 - HTTP/2 Specification](https://tools.ietf.org/html/rfc7540)
- [RFC 7540 Section 8.1.2 - Connection-Specific Header Fields](https://tools.ietf.org/html/rfc7540#section-8.1.2)
- [OWASP - HTTP Request Smuggling](https://owasp.org/www-community/attacks/HTTP_Request_Smuggling)
- [OWASP - HTTP Response Splitting](https://owasp.org/www-community/attacks/HTTP_Response_Splitting)
- [CWE-444: Inconsistent Interpretation of HTTP Requests](https://cwe.mitre.org/data/definitions/444.html)
- [CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers](https://cwe.mitre.org/data/definitions/113.html)
- [ASVS Standard](https://owasp.org/www-project-application-security-verification-standard/)

## Learning Outcomes

Upon completion, you will:

✓ Understand HTTP/2 multiplexing and why it forbids certain headers
✓ Identify connection-specific headers and their dangers
✓ Recognize header injection and response splitting attacks
✓ Implement proper HTTP/2 header validation
✓ Test for HTTP/2 compliance vulnerabilities
✓ Use multiple tools for security testing
✓ Apply ASVS 4.2.3 in real applications

## Contributing

Found an issue or have a suggestion?

1. Test the lab thoroughly
2. Document the issue with steps to reproduce
3. Submit feedback with improvements

## License

This educational material is provided as-is for learning purposes.

## Disclaimer

This lab is for **authorized security testing only**. Only test systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal.
