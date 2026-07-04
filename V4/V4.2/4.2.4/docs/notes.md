# ASVS 4.2.4 — Educator Notes & Discussion Points

## Overview for Educators

This lab teaches ASVS 4.2.4, which belongs to V4.2 HTTP Message Structure Validation at Level 3 (highest assurance). It specifically targets CRLF injection in HTTP headers — a classic vulnerability that remains relevant despite protocol evolution to HTTP/2 and HTTP/3.

---

## Key Teaching Points

### 1. The Protocol Evolution Point

**The most important conceptual point of this lab** is the tension between:

- HTTP/2/3 binary framing preventing CRLF injection at the transport layer
- The ASVS requirement for application-layer validation regardless

Many students will initially say "HTTP/2 makes this impossible." Use the lab to show them they're partially right, but that the application-level attack surface remains.

**Discussion Question**: "If HTTP/2 blocks CRLF at the wire level, why does ASVS 4.2.4 still require application validation?"

**Expected Answer Elements**:
- Downstream HTTP/1.1 backends in microservice architectures
- Log files are not HTTP/2 protocol-aware
- Database-stored header values
- Defence in depth (ASVS Level 3 principle)
- JSON/form body data is not subject to HTTP/2 header validation

---

### 2. The "Transport vs Application" Distinction

Draw this diagram on the whiteboard:

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP/2 Protection Zone                   │
│                                                             │
│  Client ←──────────── HTTP/2 Frame ──────────────────────── │
│  (binary HEADERS frame, no CRLF possible in frame fields)  │
└──────────────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
              ┌────────────────────────────────────┐
              │         Application Code Zone      │
              │                                    │
              │  request.headers → dict            │
              │  request.get_json() → {"value": "...│\r\n..."} │
              │                                    │
              │  CRLF CAN EXIST HERE               │
              │  in JSON bodies, form data, etc.   │
              └────────────────────────────────────┘
                                   │
                                   ▼
              ┌────────────────────────────────────┐
              │         Vulnerable Sinks           │
              │                                    │
              │  resp.headers["X-Val"] = value     │
              │  logger.info("val: %s", value)     │
              │  db.store(value)                   │
              │  http11_backend.forward(value)     │
              └────────────────────────────────────┘
```

---

### 3. Why Level 3?

ASVS Level 3 is the highest assurance level, typically required for high-security applications (banking, healthcare, government). It mandates defence-in-depth controls that go beyond what frameworks provide by default.

Level 1 and 2 applications might rely on framework/server protection. Level 3 requires the application itself to validate, independently of what layers below it do.

---

### 4. The Log Injection Demonstration

The most viscerally convincing demo is the log injection:

1. Start the vulnerable Docker container
2. Show the clean Docker logs
3. Send a request with `\n[ADMIN] LOGIN SUCCESSFUL user=administrator` in a header value
4. Show the `docker logs` output — the fake admin login appears as a real entry
5. Ask: "If you were an SOC analyst reviewing these logs during an incident, what would you think?"

This immediately makes students understand why sanitization in logging is critical.

---

### 5. The "Modern Framework Does It Automatically" Misconception

Students often believe: "Flask/Django/Rails protects me from injection attacks automatically."

Demonstrate:
1. The vulnerable app uses Flask (same as the secure app)
2. Flask does NOT automatically validate CRLF in request bodies
3. The developer must explicitly add validation
4. Werkzeug may protect HTTP/2 headers at the transport layer, but JSON body strings are just strings

---

## Suggested Lab Flow (90-minute session)

### Phase 1: Theory (20 min)
- Read `docs/theory.md` sections 1-4
- Whiteboard: HTTP/1.1 header structure and CRLF termination
- Show the attack demo from `docs/attack.md` (Header Injection)

### Phase 2: Exploration (30 min)
- Students start both Docker containers
- Open both UIs side-by-side
- Work through the browser interactive lab
- Use all presets: Clean, CR, LF, CRLF, Response Split, Log Injection

### Phase 3: Burp/curl Testing (20 min)
- Follow `docs/burp.md` steps 1-6
- Attempt raw CRLF injection via curl (observe the curl error)
- Compare JSON body injection results

### Phase 4: Fix Challenge (20 min)
- Students edit `vulnerable/app.py` to add validation
- Rebuild Docker container: `docker compose up --build`
- Verify the fix using the same payloads
- Discuss trade-offs: reject vs. sanitize

---

## Common Student Misconceptions

| Misconception | Correction |
|--------------|-----------|
| "HTTP/2 makes CRLF injection impossible" | Only at the transport wire level. Application-layer data is still vulnerable. |
| "curl prevents it so the attack isn't real" | curl prevents it in headers. JSON bodies carry \r\n freely. |
| "Just strip \r\n from the output" | ASVS 4.2.4 requires rejection, not sanitization. Silent stripping masks attacks. |
| "This only affects HTTP/1.1 apps" | Logs, databases, and HTTP/1.1 backends remain vulnerable even in HTTP/2 apps. |
| "The framework validates headers automatically" | Frameworks validate HTTP transport frames; they don't sanitize all user-supplied string data. |

---

## Assessment Rubric

### Understanding (40 points)

| Points | Criteria |
|--------|---------|
| 10 | Correctly explains what CR, LF, and CRLF are |
| 10 | Explains how CRLF injection enables header injection |
| 10 | Distinguishes transport-layer vs application-layer protection |
| 10 | References RFC 9113 §8.2.1 correctly |

### Practical Skills (40 points)

| Points | Criteria |
|--------|---------|
| 10 | Successfully demonstrates CR, LF, CRLF injection on vulnerable app |
| 10 | Correctly observes rejection on secure app |
| 10 | Demonstrates log injection with Docker logs |
| 10 | Writes working validation code to fix vulnerable app |

### Analysis (20 points)

| Points | Criteria |
|--------|---------|
| 10 | Explains why HTTP/2 alone does not satisfy ASVS 4.2.4 |
| 10 | Documents the attack scenario with clear impact and remediation |

---

## Screenshot Capture Guide

Students should capture the following screenshots during the lab:

### Screenshot 1: Clean Header — Secure App
**What to capture**: The browser UI showing a clean header accepted with a green "ACCEPTED" banner and `"asvs_pass": true`.  
**Filename**: `01_secure_clean_accepted.png`

### Screenshot 2: CR Injection — Secure App
**What to capture**: The UI showing a CR-injected header rejected with a red "REJECTED" banner, HTTP 400 status, and violations listed.  
**Filename**: `02_secure_cr_rejected.png`

### Screenshot 3: LF Injection — Secure App
**What to capture**: Same as above for LF injection.  
**Filename**: `03_secure_lf_rejected.png`

### Screenshot 4: CRLF Injection — Secure App
**What to capture**: CRLF injection with the violation detail showing the repr of the injected value.  
**Filename**: `04_secure_crlf_rejected.png`

### Screenshot 5: LF Injection — Vulnerable App
**What to capture**: The vulnerable app accepting the LF injection (orange warning banner), with the simulated HTTP/1.1 injection shown.  
**Filename**: `05_vulnerable_lf_accepted.png`

### Screenshot 6: CRLF Injection — Vulnerable App
**What to capture**: The vulnerable app accepting CRLF injection with the response splitting simulation visible.  
**Filename**: `06_vulnerable_crlf_accepted.png`

### Screenshot 7: Log Injection — Docker Logs
**What to capture**: Terminal showing `docker logs asvs-4.2.4-vulnerable` with the injected fake log entry visible as a separate line.  
**Filename**: `07_log_injection_docker_logs.png`

### Screenshot 8: Burp Suite — Comparison
**What to capture**: Burp Repeater showing the same CRLF payload sent to both apps (one tab per app), with responses side by side.  
**Filename**: `08_burp_comparison.png`

### Screenshot 9: Fixed Vulnerable App
**What to capture**: After fixing `vulnerable/app.py`, the previously-accepted CRLF payload now showing HTTP 400.  
**Filename**: `09_vulnerable_fixed_rejected.png`

---

## Discussion Questions

1. "If you were deploying this application in production, what additional controls beyond ASVS 4.2.4 would you implement?"

2. "How would you test this in a CI/CD pipeline? What automated tests would you write?"

3. "If the application must accept user-supplied header names (e.g., a header forwarding proxy), how would you design the validation?"

4. "Compare the trade-offs between rejecting requests vs. sanitizing input. When is each approach appropriate?"

5. "What would a WAF (Web Application Firewall) rule for CRLF injection look like? Would it catch all cases?"
