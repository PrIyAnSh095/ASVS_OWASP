# ASVS 4.2.3 - Screenshots and Visual Assets Guide

## Screenshots to Capture

### Group 1: Browser Testing Interface

#### Screenshot 1: Lab Interface - Main View
**Location:** http://localhost:8000/
**What to capture:**
- Full page from top to bottom
- Header section with ASVS 4.2.3 title
- Navigation tabs (Info, Test, Manual, Comparison, Learning)
- At least Info tab content visible

**Purpose:** Shows students the starting interface and navigation options

**Filename:** 01-interface-main.png

---

#### Screenshot 2: Lab Interface - Info Section
**Location:** http://localhost:8000/ (Info tab selected)
**What to capture:**
- ASVS Control section with requirement text
- "Why This Matters" section
- Forbidden Headers list with descriptions
- RFC reference

**Purpose:** Shows the educational content about the control

**Filename:** 02-interface-info-section.png

---

#### Screenshot 3: Lab Interface - Test Section
**Location:** http://localhost:8000/ (Test tab selected)
**What to capture:**
- Protocol selector dropdown (HTTP/1.1, HTTP/2)
- Header input form with "Add Header" button
- Request body textarea
- "Send Request" button
- Blank response area

**Purpose:** Shows the interactive testing interface before running tests

**Filename:** 03-interface-test-form.png

---

#### Screenshot 4: Lab Interface - Valid Request Response
**Location:** http://localhost:8000/ (after sending valid request)
**What to capture:**
- Send request result showing HTTP 200
- Response in Pretty tab showing status: "PASS"
- JSON formatted response with forbidden_headers_found: []

**Purpose:** Demonstrates what a compliant (passing) response looks like

**Filename:** 04-test-valid-response.png

---

### Group 2: Secure Implementation Testing

#### Screenshot 5: Secure - Forbidden Header Rejection (Transfer-Encoding)
**Steps to capture:**
1. Port: 8000 (Secure)
2. Protocol: HTTP/2
3. Add Header: Transfer-Encoding: chunked
4. Send request

**What to capture:**
- HTTP 400 status code
- Response showing status: "FAIL"
- forbidden_headers_found: ["Transfer-Encoding"]
- Error message explaining RFC 7540 requirement

**Purpose:** Shows secure implementation correctly rejecting a forbidden header

**Filename:** 05-secure-reject-transfer-encoding.png

---

#### Screenshot 6: Secure - Forbidden Header Rejection (Connection)
**Steps to capture:**
1. Port: 8000 (Secure)
2. Protocol: HTTP/2
3. Add Header: Connection: close
4. Send request

**What to capture:**
- HTTP 400 status code
- forbidden_headers_found: ["Connection"]

**Purpose:** Shows rejection of Connection header

**Filename:** 06-secure-reject-connection.png

---

#### Screenshot 7: Secure - Multiple Forbidden Headers Rejection
**Steps to capture:**
1. Port: 8000 (Secure)
2. Protocol: HTTP/2
3. Add 3 headers:
   - Transfer-Encoding: chunked
   - Connection: close
   - Keep-Alive: timeout=5
4. Send request

**What to capture:**
- HTTP 400 status code
- forbidden_headers_found: ["Transfer-Encoding", "Connection", "Keep-Alive"]
- Response indicating all 3 headers were detected

**Purpose:** Shows secure implementation detects multiple violations at once

**Filename:** 07-secure-reject-multiple.png

---

#### Screenshot 8: Secure - All 6 Forbidden Headers Rejection
**Steps to capture:**
1. Port: 8000 (Secure)
2. Protocol: HTTP/2
3. Add all 6 headers:
   - Transfer-Encoding: chunked
   - Connection: close
   - Keep-Alive: timeout=5
   - Upgrade: h2c
   - Proxy-Connection: keep-alive
   - Trailer: X-Signature
4. Send request

**What to capture:**
- HTTP 400 status code
- forbidden_headers_found: [all 6 headers listed]

**Purpose:** Shows secure implementation catches all RFC-forbidden headers

**Filename:** 08-secure-reject-all-six.png

---

### Group 3: Vulnerable Implementation Testing

#### Screenshot 9: Vulnerable - Accepts Forbidden Header (Transfer-Encoding)
**Steps to capture:**
1. Port: 8001 (Vulnerable)
2. Protocol: HTTP/2
3. Add Header: Transfer-Encoding: chunked
4. Send request

**What to capture:**
- HTTP 200 status code (DIFFERENT from secure!)
- Response showing status: "ACCEPTED"
- all_received_headers showing Transfer-Encoding was received
- Message indicating "VULNERABLE"

**Purpose:** Demonstrates contrast - vulnerable accepts what secure rejects

**Filename:** 09-vulnerable-accept-transfer-encoding.png

---

#### Screenshot 10: Vulnerable - Accepts Connection Header
**Steps to capture:**
1. Port: 8001 (Vulnerable)
2. Protocol: HTTP/2
3. Add Header: Connection: close
4. Send request

**What to capture:**
- HTTP 200 status code
- status: "ACCEPTED"
- Connection header shown in all_received_headers

**Purpose:** Shows vulnerability accepting Connection header

**Filename:** 10-vulnerable-accept-connection.png

---

#### Screenshot 11: Vulnerable - Accepts All 6 Headers
**Steps to capture:**
1. Port: 8001 (Vulnerable)
2. Add all 6 forbidden headers (same as Screenshot 8)
4. Send request

**What to capture:**
- HTTP 200 status code (not 400!)
- all_received_headers showing all 6 headers
- dangerous_headers_found: 6

**Purpose:** Shows how different behavior is compared to secure (direct comparison)

**Filename:** 11-vulnerable-accept-all-six.png

---

### Group 4: Comparison View

#### Screenshot 12: Comparison Table
**Location:** http://localhost:8000/ (Comparison tab)
**What to capture:**
- Full comparison table showing:
  - Row 1: Header Validation (Secure: Yes vs Vulnerable: No)
  - Row 2: Forbidden Headers (Secure: Rejected vs Vulnerable: Accepted)
  - Individual rows for each forbidden header
  - Row: Protocol Compliance (Secure: PASS vs Vulnerable: FAIL)
  - Row: ASVS 4.2.3 Compliance (Secure: PASS vs Vulnerable: FAIL)

**Purpose:** Shows direct side-by-side comparison

**Filename:** 12-comparison-table.png

---

### Group 5: Burp Suite Testing

#### Screenshot 13: Burp Repeater - Valid Request
**Setup:**
1. Open Burp Suite
2. Set proxy to localhost:8081 (or system proxy)
3. Navigate to http://localhost:8000/api/test
4. Capture request
5. Send to Repeater

**What to capture:**
- Burp Repeater window showing:
  - Request pane: GET /api/test HTTP/2
  - Response pane: HTTP 200 with valid response

**Purpose:** Shows baseline working request in Burp

**Filename:** 13-burp-repeater-valid.png

---

#### Screenshot 14: Burp Repeater - Forbidden Header (Secure)
**Setup:**
1. In Burp Repeater, modify request
2. Add header: Transfer-Encoding: chunked
3. Send to http://localhost:8000/api/test

**What to capture:**
- Request pane: Shows Transfer-Encoding header added
- Response pane: HTTP 400 Bad Request with FAIL message

**Purpose:** Shows Burp detection of rejection

**Filename:** 14-burp-repeater-secure-reject.png

---

#### Screenshot 15: Burp Repeater - Same Request to Vulnerable
**Setup:**
1. Keep same request with Transfer-Encoding header
2. Change host to localhost:8001

**What to capture:**
- Request pane: Same Transfer-Encoding header
- Response pane: HTTP 200 OK with ACCEPTED message (NOT 400!)

**Purpose:** Dramatic visual difference showing vulnerability

**Filename:** 15-burp-repeater-vulnerable-accept.png

---

#### Screenshot 16: Burp Comparer - Side-by-Side Comparison
**Setup:**
1. In Burp, open Comparer
2. Load response from Screenshot 14 (Secure 400)
3. Load response from Screenshot 15 (Vulnerable 200)
4. Click "Words" or "Lines" comparison

**What to capture:**
- Left side: Secure response (red highlighting on 400)
- Right side: Vulnerable response (red highlighting on 200)
- Differences highlighted

**Purpose:** Shows exact response differences in Burp's comparison tool

**Filename:** 16-burp-comparer-diff.png

---

#### Screenshot 17: Burp Intruder Setup
**Setup:**
1. Create request with forbidden headers
2. Send to Intruder
3. Set payload positions on header names
4. Configure with 6 forbidden headers as payload set

**What to capture:**
- Intruder attack editor
- Payload sets configuration
- Positions marked on headers

**Purpose:** Shows automated testing setup

**Filename:** 17-burp-intruder-setup.png

---

#### Screenshot 18: Burp Intruder Results
**Setup:**
1. Run attack on port 8000 (Secure)
2. Save results showing all 400s

**What to capture:**
- Results table showing:
  - All requests to port 8000 return 400
  - Sorted by status code column showing uniform 400s

**Purpose:** Shows systematic rejection of all variants

**Filename:** 18-burp-intruder-results-secure.png

---

#### Screenshot 19: Burp Intruder Results - Vulnerable
**Setup:**
1. Change target to port 8001
2. Run same attack

**What to capture:**
- Results table showing:
  - All requests to port 8001 return 200
  - Sorted by status code showing all 200s

**Purpose:** Contrast with secure - all accepted

**Filename:** 19-burp-intruder-results-vulnerable.png

---

### Group 6: Command Line Testing (curl/Terminal)

#### Screenshot 20: Terminal - curl Version Check
**Command:**
curl --version

**What to capture:**
- Terminal output showing:
  - curl version
  - HTTP2 support indication

**Purpose:** Shows how to verify HTTP/2 support

**Filename:** 20-terminal-curl-version.png

---

#### Screenshot 21: Terminal - Valid curl Request
**Command:**
curl -v http://localhost:8000/api/test

**What to capture:**
- Terminal output showing:
  - Request headers
  - HTTP 200 response
  - Response body

**Purpose:** Shows baseline curl request

**Filename:** 21-terminal-curl-valid.png

---

#### Screenshot 22: Terminal - curl Forbidden Header Secure
**Command:**
curl -v --http2 -H "Transfer-Encoding: chunked" http://localhost:8000/api/test

**What to capture:**
- Terminal output showing:
  - Request with Transfer-Encoding header
  - HTTP 400 response
  - Error message

**Purpose:** Shows curl rejection by secure app

**Filename:** 22-terminal-curl-secure-reject.png

---

#### Screenshot 23: Terminal - curl Forbidden Header Vulnerable
**Command:**
curl -v --http2 -H "Transfer-Encoding: chunked" http://localhost:8001/api/test

**What to capture:**
- Terminal output showing:
  - Same request to vulnerable
  - HTTP 200 response (not 400!)
  - Acceptance message

**Purpose:** Shows vulnerability in terminal

**Filename:** 23-terminal-curl-vulnerable-accept.png

---

#### Screenshot 24: Terminal - Batch Testing Script Output
**Command:**
Run batch testing script from docs/curl.md

**What to capture:**
- Terminal output showing:
  - Multiple curl commands running
  - Color-coded status (Green for secure 400s, Red for vulnerable acceptance)
  - Summary table

**Purpose:** Shows automated testing results

**Filename:** 24-terminal-batch-test.png

---

### Group 7: Docker and Infrastructure

#### Screenshot 25: Docker Desktop - Both Containers Running
**Setup:**
1. Build images: docker-compose build
2. Start containers: docker-compose up
3. Open Docker Desktop

**What to capture:**
- Docker Desktop showing:
  - asvs-4-2-3-secure container running on port 8000
  - asvs-4-2-3-vulnerable container running on port 8001
  - Both showing "running" status

**Purpose:** Shows infrastructure working

**Filename:** 25-docker-both-containers.png

---

#### Screenshot 26: Docker Logs - Secure Container
**Command:**
docker logs -f asvs-4-2-3-secure

**What to capture:**
- Terminal showing container logs:
  - Hypercorn startup messages
  - HTTP/2 server ready
  - Port 8000 listening
  - Recent request logs showing 400 rejections

**Purpose:** Shows secure container logging

**Filename:** 26-docker-logs-secure.png

---

#### Screenshot 27: Docker Logs - Vulnerable Container
**Command:**
docker logs -f asvs-4-2-3-vulnerable

**What to capture:**
- Terminal showing:
  - Hypercorn startup
  - Port 8001 listening
  - Request logs showing 200 acceptances

**Purpose:** Shows vulnerable container in action

**Filename:** 27-docker-logs-vulnerable.png

---

### Group 8: Development and Code

#### Screenshot 28: VS Code - Secure App Code
**File:** V4/V4.2/4.2.3/secure/app.py

**What to capture:**
- Code showing:
  - FORBIDDEN_HTTP2_HEADERS set definition
  - @validate_http2_headers decorator
  - HTTP/2 protocol detection
  - Early rejection logic

**Purpose:** Shows secure implementation code

**Filename:** 28-vscode-secure-code.png

---

#### Screenshot 29: VS Code - Vulnerable App Code
**File:** V4/V4.2/4.2.3/vulnerable/app.py

**What to capture:**
- Code showing:
  - Same endpoints but WITHOUT validation decorator
  - Direct acceptance of all headers
  - No protocol checking
  - Forwarding headers as-is

**Purpose:** Shows what insecure code looks like

**Filename:** 29-vscode-vulnerable-code.png

---

#### Screenshot 30: VS Code - File Structure
**Location:** Explorer sidebar in VS Code

**What to capture:**
- Expanded V4/V4.2/4.2.3 directory showing:
  - secure/ folder (with app.py, templates/, static/, etc.)
  - vulnerable/ folder (same structure)
  - docs/ folder (all markdown files)
  - tests/ folder (all test files)
  - assets/ folder (for screenshots, diagrams)

**Purpose:** Shows complete project structure

**Filename:** 30-vscode-file-structure.png

---

### Group 9: Learning Outcomes

#### Screenshot 31: Lab Interface - Learning Outcomes Section
**Location:** http://localhost:8000/ (Learning tab)

**What to capture:**
- List of learning outcomes
- Challenge tasks for students
- Progress indicators if available

**Purpose:** Shows educational goals

**Filename:** 31-interface-learning-outcomes.png

---

#### Screenshot 32: Documentation - theory.md in Browser
**Location:** Open docs/theory.md in markdown viewer or GitHub

**What to capture:**
- Header explaining HTTP/2 architecture
- Diagram or explanation of forbidden headers
- RFC references

**Purpose:** Shows theory documentation

**Filename:** 32-docs-theory.png

---

#### Screenshot 33: Documentation - attack.md in Browser

**What to capture:**
- Header injection section
- Response splitting attack example
- Code example showing vulnerability

**Purpose:** Shows attack vector documentation

**Filename:** 33-docs-attack.png

---

## Summary of Visual Assets

**Total Screenshots Needed:** 33

**By Category:**
- Interface/Browser (4 screenshots)
- Secure Testing (4 screenshots)
- Vulnerable Testing (3 screenshots)
- Comparison (1 screenshot)
- Burp Suite (7 screenshots)
- Command Line (5 screenshots)
- Docker (3 screenshots)
- Development (3 screenshots)
- Documentation (3 screenshots)

**Filename Pattern:** NN-category-description.png

## Instructions for Capturing Screenshots

### Browser Screenshots
1. Open browser to http://localhost:8000 or :8001
2. Maximize window for full visibility
3. Use Print Screen or Snipping Tool
4. Save as PNG in assets/screenshots/
5. Crop to show relevant section if needed

### Terminal Screenshots
1. Use screenshot tool to capture terminal window
2. Ensure command and full output visible
3. Background should show command prompt
4. Save as PNG with high contrast

### Code Screenshots
1. Open file in VS Code
2. Select relevant code section
3. Use VS Code's "Select All" if showing full file
4. Or manually select key lines
5. Screenshot should show line numbers and syntax highlighting

### Burp Suite Screenshots
1. Arrange Repeater or Intruder windows for clarity
2. Show both request and response panes
3. Highlight key differences (status codes, headers)
4. Ensure readable font size in screenshot

## Using Screenshots in Documentation

Each screenshot can be referenced in documents:

**In markdown:**
![Lab Interface](assets/screenshots/01-interface-main.png)

**In HTML:**
<img src="assets/screenshots/01-interface-main.png" alt="Lab Interface">

**In PowerPoint/Google Slides:**
Insert → Image → Select from file

---
