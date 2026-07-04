# ASVS 4.2.3 - Solution & Remediation

## Overview

This document explains how to fix the vulnerable implementation to achieve ASVS 4.2.3 compliance.

## Problem Summary

The vulnerable implementation accepts HTTP/2 requests containing connection-specific headers that should be forbidden per RFC 7540. This enables:

- Header injection attacks
- Response splitting
- Request smuggling
- Cache poisoning
- Protocol confusion

## Solution Architecture

### Key Components

1. **Header Validation Decorator/Middleware**
   - Intercepts all requests early
   - Checks for forbidden headers
   - Rejects with HTTP 400

2. **Forbidden Headers Set**
   - Maintained as configuration
   - Case-insensitive comparison
   - Clear documentation of why each is forbidden

3. **Error Response**
   - HTTP 400 Bad Request
   - Lists forbidden headers found
   - Includes RFC 7540 reference
   - Educational explanation

## Implementation Steps

### Step 1: Define Forbidden Headers

```python
# At the top of app.py

FORBIDDEN_HTTP2_HEADERS = {
    'transfer-encoding',
    'connection',
    'keep-alive',
    'upgrade',
    'proxy-connection',
    'trailer'
}

HEADER_EXPLANATIONS = {
    'transfer-encoding': (
        'HTTP/2 uses frame-level length encoding, not chunked transfer encoding. '
        'This header should never appear in HTTP/2.'
    ),
    'connection': (
        'HTTP/2 connections are persistent and managed via GOAWAY frames. '
        'The Connection header is meaningless in HTTP/2.'
    ),
    'keep-alive': (
        'HTTP/2 maintains connections automatically. Keep-Alive negotiation is obsolete.'
    ),
    'upgrade': (
        'Protocol upgrade happens at connection setup, not per-stream. '
        'Cannot upgrade mid-HTTP/2 connection.'
    ),
    'proxy-connection': (
        'Non-standard header. Presence indicates HTTP/1.1 confusion in HTTP/2 context.'
    ),
    'trailer': (
        'Trailers are handled via HTTP/2 frame continuation, not headers.'
    )
}
```

### Step 2: Create Validation Decorator

```python
from functools import wraps
from flask import jsonify

def validate_http2_headers(f):
    """
    Decorator that validates HTTP/2 requests do not contain 
    connection-specific headers.
    
    This implements ASVS 4.2.3 requirement.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Determine if this is HTTP/2
        http_version = request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1')
        is_http2 = 'h2' in http_version.lower()
        
        # Check for protocol hint in query params (for testing)
        protocol_hint = request.args.get('protocol', '')
        if protocol_hint in ['http2', 'http3']:
            is_http2 = True
        
        if is_http2:
            # Check all request headers
            forbidden_found = []
            for header_name in request.headers.keys():
                if header_name.lower() in FORBIDDEN_HTTP2_HEADERS:
                    forbidden_found.append(header_name)
            
            # Reject if forbidden headers found
            if forbidden_found:
                logger.warning(
                    f"HTTP/2 request rejected: forbidden headers {forbidden_found}"
                )
                
                return jsonify({
                    'status': 'FAIL',
                    'message': 'HTTP/2 and HTTP/3 must not contain connection-specific headers',
                    'asvs_control': '4.2.3',
                    'protocol': 'HTTP/2 or HTTP/3',
                    'forbidden_headers_found': forbidden_found,
                    'reason': 'RFC 7540 Section 8.1.2 forbids these headers in HTTP/2'
                }), 400
        
        # Request passes validation
        return f(*args, **kwargs)
    
    return decorated_function
```

### Step 3: Apply Decorator to Endpoints

```python
@app.route('/api/test', methods=['POST', 'GET'])
@validate_http2_headers  # <-- Add this
def test_endpoint():
    """Test endpoint with header validation"""
    try:
        data = request.get_json() if request.method == 'POST' else {}
        
        return jsonify({
            'status': 'PASS',
            'message': 'Request accepted - compliant with ASVS 4.2.3',
            'asvs_control': '4.2.3',
            'protocol': request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1'),
            'request_data': data,
            'forbidden_headers_found': []
        }), 200
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500
```

### Step 4: Early Validation in Middleware

**Better Approach: Middleware (Applied to All Requests)**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.before_request
def validate_headers_middleware():
    """
    Middleware that validates headers BEFORE any endpoint processing.
    
    This is more secure than per-endpoint decorators.
    """
    
    # Determine protocol
    http_version = request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1')
    is_http2 = 'h2' in http_version.lower()
    
    # Check for protocol query param (for testing)
    if request.args.get('protocol') in ['http2', 'http3']:
        is_http2 = True
    
    if is_http2:
        # Validate headers
        forbidden_found = []
        for header_name in request.headers.keys():
            if header_name.lower() in FORBIDDEN_HTTP2_HEADERS:
                forbidden_found.append(header_name)
        
        if forbidden_found:
            logger.warning(f"HTTP/2 violation: {forbidden_found} in {request.path}")
            
            return jsonify({
                'status': 'FAIL',
                'message': 'HTTP/2 and HTTP/3 must not contain connection-specific headers',
                'asvs_control': '4.2.3',
                'forbidden_headers_found': forbidden_found,
                'reason': 'RFC 7540 Section 8.1.2 forbids connection-specific headers'
            }), 400
```

## Testing the Fix

### Test 1: Verify Rejection

```bash
# Should return 400
curl -H "Transfer-Encoding: chunked" \
  http://localhost:8000/api/test

# Should return 400 with FAIL status
curl -H "Connection: close" \
  http://localhost:8000/api/test
```

### Test 2: Verify Valid Requests Still Work

```bash
# Should return 200
curl -H "Accept: application/json" \
  http://localhost:8000/api/test
```

### Test 3: Verify All Six Headers

```bash
for header in "Transfer-Encoding: chunked" \
              "Connection: close" \
              "Keep-Alive: timeout=5" \
              "Upgrade: h2c" \
              "Proxy-Connection: keep-alive" \
              "Trailer: X-Signature"
do
  echo "Testing: $header"
  curl -H "$header" http://localhost:8000/api/test | jq .status
done

# All should return "FAIL"
```

## Complete Fixed Implementation

### Minimal Working Example

```python
from flask import Flask, request, jsonify
from functools import wraps
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RFC 7540: Forbidden headers in HTTP/2
FORBIDDEN_HTTP2_HEADERS = {
    'transfer-encoding',
    'connection',
    'keep-alive',
    'upgrade',
    'proxy-connection',
    'trailer'
}

# Early validation via middleware
@app.before_request
def validate_http2_headers():
    """ASVS 4.2.3: Reject HTTP/2 with connection-specific headers"""
    
    # Check protocol
    http_version = request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1')
    is_http2 = ('h2' in http_version.lower() or 
                request.args.get('protocol') in ['http2', 'http3'])
    
    if is_http2:
        # Find forbidden headers
        forbidden = [h for h in request.headers.keys() 
                    if h.lower() in FORBIDDEN_HTTP2_HEADERS]
        
        if forbidden:
            return jsonify({
                'status': 'FAIL',
                'message': 'HTTP/2 must not contain connection-specific headers',
                'asvs_control': '4.2.3',
                'forbidden_headers_found': forbidden
            }), 400

@app.route('/api/test', methods=['GET', 'POST'])
def test():
    return jsonify({
        'status': 'PASS',
        'message': 'Request accepted - compliant with ASVS 4.2.3',
        'asvs_control': '4.2.3'
    }), 200

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

## Defense in Depth

### Additional Measures

#### 1. Header Normalization

```python
def normalize_headers(headers):
    """Normalize and validate header names"""
    normalized = {}
    
    for name, value in headers.items():
        # Remove whitespace
        name = name.strip()
        
        # Reject if contains CRLF
        if '\r' in value or '\n' in value:
            raise ValueError(f"Invalid characters in header: {name}")
        
        # Check length limits
        if len(name) > 8192 or len(value) > 8192:
            raise ValueError(f"Header exceeds size limit: {name}")
        
        # Store normalized
        normalized[name.lower()] = value
    
    return normalized
```

#### 2. Logging and Monitoring

```python
@app.before_request
def log_requests():
    """Log all requests for security monitoring"""
    protocol = request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1')
    method = request.method
    path = request.path
    
    logger.info(f"{protocol} {method} {path}")
    
    # Log forbidden header attempts
    for header in FORBIDDEN_HTTP2_HEADERS:
        if header in request.headers:
            logger.warning(f"Forbidden header attempt: {header}")
```

#### 3. Security Headers

```python
@app.after_request
def add_security_headers(response):
    """Add security headers to responses"""
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## Configuration Recommendations

### Reverse Proxy (Nginx)

```nginx
server {
    listen 80 http2;
    server_name localhost;
    
    # Reject forbidden headers
    if ($http_transfer_encoding) { return 400; }
    if ($http_connection) { return 400; }
    if ($http_keep_alive) { return 400; }
    if ($http_upgrade) { return 400; }
    if ($http_proxy_connection) { return 400; }
    
    location / {
        proxy_pass http://app:8000;
        proxy_http_version 1.1;
        
        # Forward necessary headers only
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker

Dockerfile with validation:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY templates templates/
COPY static static/

# Run with hypercorn HTTP/2
CMD ["hypercorn", "--bind", "0.0.0.0:8000", "--http2", "app:app"]
```

## Verification Checklist

After implementation, verify:

- [ ] Rejection of Transfer-Encoding header
- [ ] Rejection of Connection header
- [ ] Rejection of Keep-Alive header
- [ ] Rejection of Upgrade header
- [ ] Rejection of Proxy-Connection header
- [ ] Rejection of Trailer header
- [ ] Multiple forbidden headers detected
- [ ] Valid headers still accepted
- [ ] HTTP 400 response on violation
- [ ] Appropriate error message in response
- [ ] Includes asvs_control: "4.2.3" in response
- [ ] Lists all forbidden headers found
- [ ] Early validation (before endpoint processing)
- [ ] Case-insensitive header name matching
- [ ] Logging of violation attempts
- [ ] Performance impact is minimal
- [ ] Works with HTTP/1.1 (doesn't interfere)
- [ ] Works with actual HTTP/2 clients

## Testing Automation

### Python Unit Tests

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_reject_transfer_encoding(client):
    response = client.post(
        '/api/test',
        headers={'Transfer-Encoding': 'chunked'},
        environ_base={'SERVER_PROTOCOL': 'HTTP/2'}
    )
    assert response.status_code == 400
    assert response.json['status'] == 'FAIL'
    assert 'Transfer-Encoding' in response.json['forbidden_headers_found']

def test_reject_connection(client):
    response = client.post(
        '/api/test',
        headers={'Connection': 'close'},
        environ_base={'SERVER_PROTOCOL': 'HTTP/2'}
    )
    assert response.status_code == 400

def test_accept_valid_headers(client):
    response = client.post(
        '/api/test',
        headers={'Accept': 'application/json'},
        environ_base={'SERVER_PROTOCOL': 'HTTP/2'}
    )
    assert response.status_code == 200
    assert response.json['status'] == 'PASS'

# Run tests: pytest test_app.py
```

## Performance Impact

Expected performance characteristics:

| Aspect | Impact | Notes |
|--------|--------|-------|
| Validation overhead | ~1-5ms | Minimal header checking |
| Memory impact | Negligible | Small set of forbidden headers |
| Network latency | None | No network calls added |
| Request throughput | <1% impact | Efficient set membership test |

## Migration Strategy

For existing applications:

1. **Phase 1:** Add validation in middleware (non-breaking)
2. **Phase 2:** Monitor for real-world violations
3. **Phase 3:** Document in API (communicate breaking change)
4. **Phase 4:** Enforce rejection (breaking change)
5. **Phase 5:** Remove legacy HTTP/1.1 support (if applicable)

## Documentation Updates

Update API documentation:

```markdown
## HTTP/2 Request Requirements

HTTP/2 requests must NOT contain the following headers:
- Transfer-Encoding
- Connection
- Keep-Alive
- Upgrade
- Proxy-Connection
- Trailer

These headers are forbidden per RFC 7540 Section 8.1.2.
Requests containing these headers will receive HTTP 400 Bad Request.

Reason: HTTP/2 uses multiplexing with frame-level semantics.
Connection-specific concepts are not applicable.
```

## Troubleshooting

### Issue: Tests fail on HTTP/1.1

**Solution:** Validation should only apply to HTTP/2:

```python
# Only validate for HTTP/2
if 'h2' in http_version.lower():
    # validate...
# HTTP/1.1 continues normally
```

### Issue: Legitimate proxies are blocked

**Solution:** Evaluate if proxy can be updated or if conditional logic is needed:

```python
# Allow proxy bypass if configured
if app.config.get('ALLOW_PROXY_HEADERS'):
    return  # Skip validation

# Or validate based on source IP
if is_internal_proxy(request.remote_addr):
    return  # Skip validation
```

### Issue: Headers being forwarded that shouldn't

**Solution:** Clean headers before forwarding:

```python
def clean_headers_for_forwarding(headers):
    """Remove connection-specific headers before forwarding"""
    cleaned = {}
    for name, value in headers.items():
        if name.lower() not in FORBIDDEN_HTTP2_HEADERS:
            cleaned[name] = value
    return cleaned
```

## Summary

ASVS 4.2.3 Remediation:

1. **Identify:** Recognize the 6 forbidden headers
2. **Validate:** Add early header validation
3. **Reject:** Return HTTP 400 for violations
4. **Test:** Comprehensive testing of all cases
5. **Monitor:** Log and alert on attempts
6. **Document:** Update API documentation
7. **Migrate:** Phased rollout of enforcement

Secure implementation example in [secure/app.py](../secure/app.py) shows the complete working solution.
