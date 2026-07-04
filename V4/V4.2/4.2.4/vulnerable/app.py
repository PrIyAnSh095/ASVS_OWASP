"""
ASVS 4.2.4 - VULNERABLE Implementation
========================================
Requirement: Verify that the application only accepts HTTP/2 and HTTP/3 requests
where the header fields and values do not contain any CR (\\r), LF (\\n), or
CRLF (\\r\\n) sequences, to prevent header injection attacks.

This vulnerable implementation INTENTIONALLY OMITS CRLF validation.

>>> WHY THIS IS EDUCATIONAL <<<

In HTTP/1.1, headers were plain text separated by CRLF sequences. An attacker
who can inject \\r\\n into a header value effectively controls the HTTP response
structure, enabling:
  - Header Injection     : Forging arbitrary response headers
  - Response Splitting   : Injecting a second HTTP response
  - Log Injection        : Polluting server logs with fake entries
  - Cache Poisoning      : Causing proxies to cache malicious responses

HTTP/2 (RFC 9113) and HTTP/3 (RFC 9114) moved to binary framing, which means
raw CRLF bytes in the wire format no longer have special meaning. HOWEVER:
  1. The application may still pass user data to downstream HTTP/1.1 systems.
  2. The application may log header values that contain injected newlines.
  3. Some reverse proxies downgrade to HTTP/1.1 internally.
  4. ASVS 4.2.4 requires the application to validate these characters
     regardless of the transport protocol.

>>> IMPORTANT DISCLAIMER <<<

Modern HTTP frameworks (Flask, Werkzeug, h2, Hypercorn) often strip or reject
control characters before they reach application code. This lab simulates the
vulnerability by accepting test inputs via a JSON API that bypasses the HTTP
transport layer sanitization. This accurately represents real-world scenarios
where user input containing \\r\\n reaches application code through:
  - Form fields echoed into response headers (X-Custom-Header: %0d%0a...)
  - URL-decoded query parameters used in Location: headers (Open Redirect + CRLF)
  - JSON body values set as response headers without sanitization
"""

import re
import logging
from flask import Flask, request, jsonify, render_template, make_response

# ---------------------------------------------------------------------------
# Logging — NOTE: This logger is intentionally vulnerable to log injection
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [VULNERABLE] %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "asvs-4.2.4-vulnerable-demo-key"

CRLF_PATTERN = re.compile(r"[\r\n]")


# ---------------------------------------------------------------------------
# NO before_request validation — this is the vulnerability
# ---------------------------------------------------------------------------
# The secure implementation has a before_request hook that rejects any request
# with CR/LF in headers. This implementation has NO such check.


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Landing page - renders the educational UI."""
    return render_template("index.html", mode="vulnerable")


@app.route("/api/validate-header", methods=["POST"])
def api_validate_header():
    """
    VULNERABLE API endpoint — NO CRLF validation.

    This endpoint accepts a header name/value and processes it WITHOUT checking
    for CR or LF characters. It then reflects the value in the response header.

    VULNERABILITY: If an attacker supplies a value like:
        "legitimate value\\r\\nSet-Cookie: session=attacker"
    the application would naively set this as a response header, potentially
    injecting additional headers into the HTTP/1.1 response if this data
    reaches a downstream HTTP/1.1 system.

    In HTTP/2, Werkzeug/Hypercorn would block the raw frame-level injection,
    but the application still:
      1. Logs the injected newlines (Log Injection)
      2. Stores them in databases/files without sanitization
      3. Would inject them if forwarded to HTTP/1.1 backends
    """
    data = request.get_json(force=True, silent=True) or {}
    header_name = str(data.get("header_name", "X-Test-Header"))
    header_value = str(data.get("header_value", ""))

    # -------------------------------------------------------------------------
    # VULNERABILITY: No validation of CR/LF sequences
    # A secure implementation would call validate_headers() here.
    # -------------------------------------------------------------------------

    # Simulate what happens when this unsanitized value is used:
    attack_detected = bool(CRLF_PATTERN.search(header_name) or
                           CRLF_PATTERN.search(header_value))

    if attack_detected:
        # Log the value as-is — LOG INJECTION vulnerability
        # An attacker supplying \n[VULNERABLE] ADMIN LOGIN SUCCESSFUL\n
        # would write fake log entries
        logger.info(
            "Processing header: name=%s value=%s",
            header_name,          # Unsanitized — could inject log lines
            header_value,         # Unsanitized — could inject log lines
        )

        # Demonstrate what would happen with HTTP/1.1 response construction
        # In real HTTP/1.1, setting this header directly would split the response
        simulated_http1_response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: application/json\r\n"
            f"{header_name}: {header_value}\r\n"   # INJECTION POINT
            f"\r\n"
            f'{"body": "ok"}'
        )

        result = {
            "verdict": "ACCEPTED",           # <-- WRONG: should be REJECTED
            "asvs_pass": False,              # This implementation FAILS 4.2.4
            "asvs_control": "4.2.4",
            "explanation": (
                "The vulnerable application accepted a header containing CR/LF "
                "sequences WITHOUT validation. ASVS 4.2.4 requires rejection of "
                "such headers. In HTTP/1.1 contexts, this would enable Header "
                "Injection and Response Splitting attacks."
            ),
            "attack_type_demonstrated": "CRLF Injection / Header Injection",
            "header_name": header_name,
            "header_value_repr": repr(header_value[:80]),
            "simulated_http1_injection": simulated_http1_response,
            "log_injection_note": (
                "The unsanitized value was passed to the logger. If the value "
                "contained \\n[VULNERABLE] ADMIN LOGIN SUCCESSFUL, a fake log "
                "entry would appear in the server log."
            ),
            "what_secure_does": (
                "The secure implementation rejects this request immediately with "
                "HTTP 400 and logs a warning about the injection attempt."
            ),
            "missing_control": "No CRLF validation on header name or value",
        }
        # Attempt to set the header in the response (will be caught by Werkzeug
        # at the HTTP/2 framing layer, but demonstrates the application intent)
        try:
            resp = make_response(jsonify(result), 200)
            # Werkzeug will raise ValueError for invalid header characters in
            # HTTP/2 mode, but we demonstrate the application-level mistake:
            sanitized_for_demo = CRLF_PATTERN.sub(
                " [INJECTED_NEWLINE] ", header_value
            )
            resp.headers["X-Vulnerable-Echo"] = sanitized_for_demo[:256]
            return resp
        except (ValueError, Exception):
            return jsonify(result), 200

    # Clean header — no CRLF but still no validation was performed
    logger.info("Processing header: name=%s value=%s", header_name, header_value)
    result = {
        "verdict": "ACCEPTED",
        "asvs_pass": False,   # Still fails: no validation code exists at all
        "asvs_control": "4.2.4",
        "explanation": (
            "This header happened to be clean, but the application performed "
            "NO CRLF validation. The code would accept malicious headers equally. "
            "ASVS 4.2.4 requires explicit validation logic to be present."
        ),
        "header_name": header_name,
        "header_value_repr": repr(header_value[:80]),
        "missing_control": "No CRLF validation on header name or value",
    }
    resp = make_response(jsonify(result), 200)
    try:
        resp.headers[header_name] = header_value
    except (ValueError, Exception):
        pass
    return resp


@app.route("/api/echo-header", methods=["GET"])
def api_echo_header():
    """
    VULNERABLE echo endpoint — reflects user input into response headers
    without any validation.

    Classic CRLF injection attack scenario:
      GET /api/echo-header?name=X-Foo&value=bar%0d%0aSet-Cookie:%20evil=1

    In HTTP/1.1 this would inject 'Set-Cookie: evil=1' into the response.
    In HTTP/2 the framing layer prevents it, but the application code is wrong.
    """
    header_name = request.args.get("name", "X-Echo")
    header_value = request.args.get("value", "")

    # VULNERABILITY: No validation — directly reflect in response
    logger.info(
        "Echo request: reflecting header name=%s value=%s into response",
        header_name,   # Unsanitized
        header_value,  # Unsanitized — log injection possible
    )

    # Decode URL-encoded CRLF sequences for demonstration
    decoded_value = header_value.replace("%0d", "\r").replace("%0a", "\n") \
                                .replace("%0D", "\r").replace("%0A", "\n") \
                                .replace("%0d%0a", "\r\n").replace("%0D%0A", "\r\n")

    attack_present = bool(CRLF_PATTERN.search(decoded_value) or
                          CRLF_PATTERN.search(header_name))

    resp = make_response(jsonify({
        "verdict": "ACCEPTED_WITHOUT_VALIDATION",
        "asvs_pass": False,
        "message": "Header reflected without CRLF check",
        "header_name": header_name,
        "header_value_raw": repr(decoded_value[:80]),
        "attack_present": attack_present,
        "injection_explanation": (
            "If this were HTTP/1.1, the \\r\\n in the value would terminate "
            "the current header line and begin a new header, enabling an "
            "attacker to inject arbitrary headers (e.g., Set-Cookie, Location)."
        ) if attack_present else None,
    }))

    # Try to set — Werkzeug may block at HTTP/2 level
    try:
        resp.headers[header_name] = decoded_value
    except (ValueError, Exception) as e:
        resp.headers["X-Injection-Blocked-By-Framework"] = (
            f"Framework rejected invalid header: {type(e).__name__}"
        )
        resp.headers["X-Educational-Note"] = (
            "Even though the framework blocked this at transport level, "
            "the application code contains NO validation logic. ASVS 4.2.4 "
            "requires the application to validate, not rely on the framework."
        )

    return resp


@app.route("/api/info")
def api_info():
    """Return information about this implementation."""
    return jsonify({
        "app": "ASVS 4.2.4 - Vulnerable Implementation",
        "asvs_chapter": "V4.2 HTTP Message Structure Validation",
        "control": "4.2.4",
        "level": 3,
        "requirement": (
            "Verify that the application only accepts HTTP/2 and HTTP/3 requests "
            "where the header fields and values do not contain any CR (\\r), LF (\\n), "
            "or CRLF (\\r\\n) sequences, to prevent header injection attacks."
        ),
        "implementation": "VULNERABLE",
        "crlf_validation": False,
        "vulnerability": "No CRLF validation on request header names or values",
        "asvs_4_2_4_status": "FAIL",
        "transport": "HTTP/2 via Hypercorn",
        "important_note": (
            "HTTP/2 binary framing prevents raw CRLF injection at the wire level. "
            "The vulnerability demonstrated here is at the APPLICATION layer: "
            "missing validation logic that would protect downstream systems, logs, "
            "and any HTTP/1.1 backends this application communicates with."
        ),
    })


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "detail": str(e)}), 400


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
