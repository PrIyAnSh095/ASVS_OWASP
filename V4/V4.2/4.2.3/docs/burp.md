# ASVS 4.2.3 - Burp Suite Testing Guide

## Overview

Burp Suite Community Edition provides excellent tools for testing HTTP/2 header validation. This guide walks through comprehensive Burp-based testing for ASVS 4.2.3.

## Prerequisites

1. Burp Suite Community Edition installed
2. Lab applications running (secure on 8000, vulnerable on 8001)
3. Browser proxy configured to Burp (127.0.0.1:8080)
4. SSL certificate installed in browser (if using HTTPS)

## Initial Setup

### 1. Configure Burp Proxy

**Proxy Settings:**
1. Open Burp Suite
2. Go to **Proxy** → **Options**
3. Verify **Proxy Listeners** includes `127.0.0.1:8080`
4. Check "Support invisible proxy"

### 2. Configure Browser Proxy

**Chrome/Edge:**
- Proxy: http://127.0.0.1:8080
- Bypass: localhost

**Firefox:**
- Settings → Network Settings
- Manual proxy configuration: 127.0.0.1:8080

### 3. Test Basic Connectivity

```
Open browser to: http://localhost:8000
Should see request in Burp Proxy → History
```

## Testing Workflow

### Step 1: Capture Baseline Request

1. Open Burp → **Proxy** → **Intercept** tab
2. Navigate to: http://localhost:8000/api/test
3. Burp intercepts the request
4. Click **Forward**
5. Request appears in **Proxy** → **History**

**Example Captured Request:**
```http
GET /api/test HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0
Accept: */*
Connection: close

```

### Step 2: Send to Repeater

1. Right-click request in **Proxy** → **History**
2. Select **Send to Repeater**
3. Go to **Repeater** tab
4. Request is ready for modification

### Step 3: Modify Headers (Secure - Port 8000)

#### Test 1: Add Transfer-Encoding Header

**Original Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Content-Type: application/json

{"data": "test"}
```

**Modified Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Content-Type: application/json
Transfer-Encoding: chunked

{"data": "test"}
```

**Expected Result (Secure):**
```
HTTP/2 400 Bad Request
Content-Type: application/json

{
  "status": "FAIL",
  "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
  "forbidden_headers_found": ["Transfer-Encoding"],
  "asvs_control": "4.2.3"
}
```

#### Test 2: Add Connection Header

**Modified Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Connection: close

{"data": "test"}
```

**Expected Result (Secure):**
```
HTTP/2 400 Bad Request
{
  "status": "FAIL",
  "message": "HTTP/2 and HTTP/3 must not contain connection-specific headers",
  "forbidden_headers_found": ["Connection"]
}
```

#### Test 3: Add Multiple Forbidden Headers

**Modified Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Transfer-Encoding: chunked
Connection: close
Keep-Alive: timeout=5
Upgrade: h2c

{"data": "test"}
```

**Expected Result (Secure):**
```
HTTP/2 400 Bad Request
{
  "status": "FAIL",
  "forbidden_headers_found": ["Transfer-Encoding", "Connection", "Keep-Alive", "Upgrade"]
}
```

#### Test 4: Add Proxy-Connection Header

**Modified Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Proxy-Connection: keep-alive

{"data": "test"}
```

**Expected Result (Secure):**
```
HTTP/2 400 Bad Request
{
  "forbidden_headers_found": ["Proxy-Connection"]
}
```

#### Test 5: Add Trailer Header

**Modified Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Trailer: X-Custom-Trailer

{"data": "test"}
```

**Expected Result (Secure):**
```
HTTP/2 400 Bad Request
{
  "forbidden_headers_found": ["Trailer"]
}
```

#### Test 6: Valid Request (Should Pass)

**Valid Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Accept: application/json
User-Agent: Burp-Test

{"data": "test"}
```

**Expected Result (Secure):**
```
HTTP/2 200 OK
{
  "status": "PASS",
  "message": "Request accepted - compliant with ASVS 4.2.3",
  "forbidden_headers_found": []
}
```

### Step 4: Compare with Vulnerable (Port 8001)

Repeat all tests against `localhost:8001`:

1. Change all requests to use `Host: localhost:8001`
2. Keep all forbidden headers
3. All should return **HTTP 200 OK** with "ACCEPTED"
4. Observe headers are processed without rejection

**Example Vulnerable Response:**
```
HTTP/2 200 OK
{
  "status": "ACCEPTED",
  "message": "Request accepted without validation - VULNERABLE",
  "asvs_control": "4.2.3",
  "compliance": "FAIL",
  "all_received_headers": {
    "Host": "localhost:8001",
    "Transfer-Encoding": "chunked",
    "Connection": "close"
  }
}
```

## Advanced Testing

### Using Burp Intruder for Batch Testing

#### Setup Intruder Attack

1. Send request to **Intruder**
2. Clear automatic payload markers
3. Set payload positions:

```http
POST /api/test HTTP/2
Host: localhost:8000
§HeaderName§: §HeaderValue§

{"data": "test"}
```

#### Configure Payloads

1. Go to **Intruder** → **Payloads**
2. Select Payload Set 1 (HeaderName):
   - **Payload type:** Simple list
   - **Payload list:**
     ```
     Transfer-Encoding
     Connection
     Keep-Alive
     Upgrade
     Proxy-Connection
     Trailer
     ```

3. Select Payload Set 2 (HeaderValue):
   - **Payload type:** Simple list
   - **Payload list:**
     ```
     chunked
     close
     timeout=5
     h2c
     keep-alive
     X-Custom-Trailer
     ```

#### Run Attack

1. Click **Start attack**
2. Burp sends all combinations
3. **Secure (8000):** All should return 400
4. **Vulnerable (8001):** All should return 200

#### Analyze Results

- Filter by Status Code
- Look for unexpected 200s on secure
- Look for unexpected 400s on vulnerable

### Header Injection Testing

#### Technique 1: CRLF Injection

**Payload with CRLF:**
```
Header-Name: value%0d%0aX-Injected: malicious

# %0d = \r (carriage return)
# %0a = \n (line feed)
```

**Test Steps:**
1. Modify request header:
   ```http
   User-Agent: Mozilla%0d%0aX-Injected-Header: malicious
   ```

2. Send request
3. Check if additional header appears in response
4. **Secure:** Should reject due to forbidden header detection
5. **Vulnerable:** May reflect injected header

#### Technique 2: Response Splitting

**Payload:**
```
Header-Name: value%0d%0a%0d%0a<HTML><BODY>Injected</BODY></HTML>

# %0d%0a%0d%0a = \r\n\r\n (double CRLF - marks end of headers)
```

**Test Steps:**
1. Modify request:
   ```http
   User-Agent: test%0d%0a%0d%0a<HTML><BODY>Response Injected</BODY></HTML>
   ```

2. Send to **Repeater**
3. Observe if injected HTML appears in response
4. **Secure:** Rejects early, no split
5. **Vulnerable:** May show injected content

### Testing with Content-Length Manipulation

#### Technique: Content-Length Mismatch

**Request:**
```http
POST /api/test HTTP/2
Host: localhost:8000
Content-Length: 10
Transfer-Encoding: chunked

{"data": "longer than 10 bytes actually"}
```

**Expected:**
- **Secure:** Rejects due to Transfer-Encoding header
- **Vulnerable:** Processes, confusion about message boundary

## Comparison Report Template

Create a comparison table in Burp's reporting:

| Test Case | Secure (8000) | Vulnerable (8001) | Observation |
|-----------|---------------|------------------|-------------|
| Transfer-Encoding | 400 | 200 | ✓ Secure correct |
| Connection | 400 | 200 | ✓ Secure correct |
| Keep-Alive | 400 | 200 | ✓ Secure correct |
| Upgrade | 400 | 200 | ✓ Secure correct |
| Proxy-Connection | 400 | 200 | ✓ Secure correct |
| Trailer | 400 | 200 | ✓ Secure correct |
| Multiple | 400 | 200 | ✓ Secure correct |
| Valid Headers | 200 | 200 | ✓ Both accept valid |

## Using Burp Macros for Automated Testing

### Create Macro: Test All Forbidden Headers

1. **Proxy** → **Options** → **Macros**
2. Click **Add**
3. Record requests testing each forbidden header
4. Configure macro to run in sequence

### Create Macro: Generate Report

1. **Extender** → **Add** (if using Python module)
2. Create script to:
   - Send requests with forbidden headers
   - Collect responses
   - Generate HTML report
   - Compare secure vs vulnerable

## Logging and Analysis

### Monitor Requests in Real-Time

1. **Proxy** → **History** tab
2. Filter by URL: `localhost:8000` and `localhost:8001`
3. Right-click → **Search** for headers:
   ```
   Transfer-Encoding
   Connection
   Keep-Alive
   Upgrade
   ```

### Generate Test Report

1. **Reporter** (Enterprise) or manual export
2. Document all test cases
3. Include screenshots of:
   - Rejected requests (secure)
   - Accepted requests (vulnerable)
   - Response differences
4. Create compliance statement

## Troubleshooting

### Issue: No HTTP/2 Visible in Burp

**Solution:**
- Check browser support for HTTP/2
- Try Firefox (better HTTP/2 support)
- Verify endpoint supports HTTP/2
- Check Burp version (updated version recommended)

### Issue: Headers Not Appearing in Burp

**Solution:**
- Ensure Proxy Intercept is working
- Check request in Repeater instead of Intercept
- Verify browser proxy settings
- Try direct curl with Burp proxy

### Issue: Response Not Showing

**Solution:**
- Click **Forward** in Intercept tab
- Check **Response** tab in Repeater
- Verify application is running
- Check application logs

## Best Practices

1. **Always test both:** Secure and vulnerable versions
2. **Document findings:** Screenshot all tests
3. **Create baseline:** Save requests for comparison
4. **Use repeater:** For precise header manipulation
5. **Monitor logs:** Check backend logs for attempts
6. **Test combinations:** Try multiple headers together
7. **Verify responses:** Ensure expected HTTP status codes
8. **Automate:** Use macros/extensions for large test suites

## Evidence Collection

For your security assessment report, collect:

1. Screenshots of:
   - Secure implementation rejecting forbidden headers (HTTP 400)
   - Vulnerable implementation accepting them (HTTP 200)
   - Response differences
   - Burp Intruder results

2. Request/Response pairs:
   - Forbidden header request
   - Rejection response (secure)
   - Acceptance response (vulnerable)

3. Compliance statement:
   - Secure version: ✓ PASS ASVS 4.2.3
   - Vulnerable version: ✗ FAIL ASVS 4.2.3
   - Remediation proof (if applicable)

## Summary

Burp Suite Testing Checklist:

- [ ] Configure Burp proxy
- [ ] Configure browser proxy
- [ ] Capture baseline requests
- [ ] Test each forbidden header individually
- [ ] Test multiple forbidden headers
- [ ] Test valid headers (should pass)
- [ ] Repeat all tests on vulnerable version
- [ ] Document all results
- [ ] Create comparison table
- [ ] Run Intruder for batch testing
- [ ] Test injection techniques
- [ ] Collect evidence
- [ ] Generate report

After completing all tests, both versions should show clear differences in header validation behavior, demonstrating the ASVS 4.2.3 requirement.
