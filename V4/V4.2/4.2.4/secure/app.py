"""
ASVS 4.2.4 - SECURE Implementation
====================================
Requirement: Verify that the application only accepts HTTP/2 and HTTP/3 requests
where the header fields and values do not contain any CR (\\r), LF (\\n), or
CRLF (\\r\\n) sequences, to prevent header injection attacks.

This secure implementation:
  1. Validates ALL incoming request header names and values.
  2. Rejects any header containing \\r, \\n, or \\r\\n sequences.
  3. Also validates user-supplied data before echoing it in response headers.
  4. Returns a 400 Bad Request for any offending header.

Why this matters:
  - HTTP/1.1 headers are terminated by CRLF sequences. Injecting \\r\\n into a
    header value allows an attacker to "split" the HTTP response and inject
    arbitrary headers or even a second HTTP response body (Response Splitting).
  - HTTP/2 uses binary framing and forbids CR/LF in header fields per RFC 9113
    §8.2.1. However, application-level validation ensures defence-in-depth.
  - HTTP/3 (QUIC-based) similarly forbids these sequences per RFC 9114 §4.2.
  - Even if the transport layer rejects malformed frames, the application MUST
    validate any user-controlled data it places into response headers.
"""

import re
import logging
# pyrefly: ignore [missing-import]
from Flask import Flask, request, jsonify, render_template, make_response # type: ignore

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [SECURE] %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "asvs-4.2.4-secure-demo-key"

# ---------------------------------------------------------------------------
# CRLF Validation Helpers
# ---------------------------------------------------------------------------

# Regex that matches any CR, LF or CRLF byte sequence.
CRLF_PATTERN = re.compile(r"[\r\n]")


def contains_crlf(value: str) -> bool:
    """Return True if the string contains any CR (\\r) or LF (\\n) character."""
    return bool(CRLF_PATTERN.search(value))


def validate_headers(headers: dict) -> list[str]:
    """
    Inspect every header name and value for CR/LF sequences.

    Returns a list of violation descriptions. An empty list means all headers
    are clean.

    HTTP/2 RFC 9113 §8.2.1 states:
      "A field value MUST NOT contain characters in the ranges 0x00-0x08,
       0x0a-0x1f, or 0x7f (i.e., all control characters other than HTAB)."
    This explicitly forbids LF (0x0a) and CR (0x0d).
    """
    violations = []
    for name, value in headers.items():
        if contains_crlf(name):
            violations.append(
                f"Header name '{repr(name)}' contains CR/LF sequence"
            )
        if contains_crlf(value):
            violations.append(
                f"Header '{name}' value '{repr(value[:80])}' contains CR/LF sequence"
            )
    return violations


# ---------------------------------------------------------------------------
# Before-request hook: validate ALL incoming headers
# ---------------------------------------------------------------------------

@app.before_request
def enforce_no_crlf_in_headers():
    """
    Global guard: reject any request whose headers contain CR or LF bytes.

    Note on HTTP/2 and HTTP/3 in practice:
      Modern servers (Hypercorn, h2, etc.) will typically reject frames with
      invalid pseudo-headers or control characters before the application even
      sees them. This middleware provides defence-in-depth validation at the
      application layer, which is what ASVS 4.2.4 requires.
    """
    violations = validate_headers(dict(request.headers))
    if violations:
        logger.warning(
            "BLOCKED request from %s - CRLF injection detected in headers: %s",
            request.remote_addr,
            "; ".join(violations),
        )
        response_body = {
            "status": "REJECTED",
            "asvs_control": "4.2.4",
            "reason": "Request headers contain forbidden CR (\\r) or LF (\\n) sequences.",
            "violations": violations,
            "remediation": (
                "Remove all CR (\\r, 0x0d) and LF (\\n, 0x0a) characters from "
                "HTTP header names and values. RFC 9113 §8.2.1 (HTTP/2) and "
                "RFC 9114 §4.2 (HTTP/3) explicitly forbid these characters."
            ),
        }
        return jsonify(response_body), 400


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Landing page - renders the educational UI."""
    return render_template("index.html", mode="secure")


@app.route("/api/validate-header", methods=["POST"])
def api_validate_header():
    """
    API endpoint for the educational UI.

    Accepts JSON body:
      {
        "header_name": "X-Custom-Header",
        "header_value": "some value with \\r\\n maybe"
      }

    Validates the supplied header name/value pair against CRLF injection,
    simulating what the server would do when it receives the header.
    Returns a structured educational response.
    """
    data = request.get_json(force=True, silent=True) or {}
    header_name = str(data.get("header_name", "X-Test-Header"))
    header_value = str(data.get("header_value", ""))

    violations = validate_headers({header_name: header_value})

    if violations:
        logger.warning(
            "API: CRLF injection attempt detected - name=%r value=%r from %s",
            header_name,
            header_value[:80],
            request.remote_addr,
        )
        result = {
            "verdict": "REJECTED",
            "asvs_pass": True,
            "asvs_control": "4.2.4",
            "explanation": (
                "The secure application detected CR (\\r) or LF (\\n) characters "
                "in the submitted header. Under ASVS 4.2.4 this request must be "
                "rejected to prevent Header Injection and Response Splitting attacks."
            ),
            "violations": violations,
            "header_name": header_name,
            "header_value_repr": repr(header_value[:80]),
            "attack_prevented": [
                "Header Injection",
                "HTTP Response Splitting",
                "Log Injection via forged header values",
                "Cache Poisoning (via response splitting)",
            ],
            "relevant_rfcs": [
                "RFC 9113 §8.2.1 - HTTP/2 field value restrictions",
                "RFC 9114 §4.2  - HTTP/3 field value restrictions",
                "RFC 7230 §3.2  - HTTP/1.1 header field syntax",
            ],
        }
        return jsonify(result), 400

    # Header is clean - safe to echo back (would be safe to set in response)
    logger.info(
        "API: Clean header accepted - name=%r from %s",
        header_name,
        request.remote_addr,
    )
    result = {
        "verdict": "ACCEPTED",
        "asvs_pass": True,
        "asvs_control": "4.2.4",
        "explanation": (
            "The header name and value contain no CR or LF characters. "
            "This header passes ASVS 4.2.4 validation and may safely be "
            "processed or reflected in a response."
        ),
        "header_name": header_name,
        "header_value_repr": repr(header_value[:80]),
    }
    resp = make_response(jsonify(result), 200)
    # Safely set the custom header in the response (after validation)
    # We sanitize just in case (defence-in-depth)
    safe_name = CRLF_PATTERN.sub("", header_name)[:64]
    safe_value = CRLF_PATTERN.sub("", header_value)[:256]
    if safe_name:
        resp.headers[safe_name] = safe_value
    return resp


@app.route("/api/echo-header", methods=["GET"])
def api_echo_header():
    """
    Echoes back a header value supplied as a query parameter.
    The secure version sanitizes the value BEFORE setting it in the response.

    Usage: GET /api/echo-header?name=X-Foo&value=bar
    """
    header_name = request.args.get("name", "X-Echo")
    header_value = request.args.get("value", "")

    violations = validate_headers({header_name: header_value})
    if violations:
        return jsonify({
            "verdict": "REJECTED",
            "reason": "Header value contains forbidden CR/LF sequences",
            "violations": violations,
        }), 400

    resp = make_response(jsonify({
        "verdict": "ACCEPTED",
        "message": "Header safely reflected",
        "header_name": header_name,
        "header_value": header_value,
    }))
    # Only set validated header
    resp.headers[header_name] = header_value
    return resp


@app.route("/api/info")
def api_info():
    """Return information about this implementation."""
    return jsonify({
        "app": "ASVS 4.2.4 - Secure Implementation",
        "asvs_chapter": "V4.2 HTTP Message Structure Validation",
        "control": "4.2.4",
        "level": 3,
        "requirement": (
            "Verify that the application only accepts HTTP/2 and HTTP/3 requests "
            "where the header fields and values do not contain any CR (\\r), LF (\\n), "
            "or CRLF (\\r\\n) sequences, to prevent header injection attacks."
        ),
        "implementation": "SECURE",
        "crlf_validation": True,
        "transport": "HTTP/2 via Hypercorn",
        "relevant_rfcs": [
            "RFC 9113 §8.2.1",
            "RFC 9114 §4.2",
            "RFC 7230 §3.2.6",
        ],
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
    # For local dev only; in Docker we use Hypercorn
    app.run(host="0.0.0.0", port=5000, debug=False)
