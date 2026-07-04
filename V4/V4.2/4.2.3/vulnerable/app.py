"""
ASVS 4.2.3 Vulnerable Implementation
Accepting HTTP/2 Connection-Specific Headers

This application DOES NOT validate HTTP/2 requests and accepts
connection-specific headers that should be forbidden by RFC 7540.

This demonstrates why ASVS 4.2.3 is critical:
- Connection-specific headers could be used for header injection
- Could enable response splitting attacks
- Allows protocol confusion attacks
- Enables request smuggling scenarios

VULNERABILITIES DEMONSTRATED:
1. No validation of connection-specific headers
2. Headers are processed and potentially forwarded upstream
3. No protocol version enforcement
4. Headers are echoed back to client (info disclosure)
"""

from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_request_headers(headers_dict):
    """
    VULNERABLE: Processes headers without validating them.
    
    In a real application, these headers might be:
    1. Forwarded to upstream services (request smuggling)
    2. Used in response headers (header injection)
    3. Passed to cache layers (cache poisoning)
    4. Processed by WAF/proxies (protocol confusion)
    """
    processed = {}
    for key, value in headers_dict.items():
        # VULNERABLE: No filtering of dangerous headers
        processed[key] = value
    return processed

@app.route('/')
def index():
    """Main page with lab interface"""
    return render_template('index.html')

@app.route('/api/test', methods=['POST', 'GET'])
def test_endpoint():
    """
    Test endpoint that accepts ALL headers without validation.
    
    VULNERABLE: No @validate_http2_headers decorator.
    Connection-specific headers are processed normally.
    """
    try:
        data = request.get_json() if request.method == 'POST' else {}
        
        # VULNERABLE: All headers are processed without validation
        request_headers = dict(request.headers)
        processed_headers = process_request_headers(request_headers)
        
        # Simulate forwarding to upstream service
        # In a real app, these headers would be sent to backend/cache/proxy
        forwarded_headers = {}
        for k, v in processed_headers.items():
            # VULNERABLE: Connection-specific headers are included
            forwarded_headers[k] = v
        
        response = {
            'status': 'ACCEPTED',
            'message': 'Request accepted without validation - VULNERABLE',
            'asvs_control': '4.2.3',
            'compliance': 'FAIL',
            'protocol': request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1'),
            'request_data': data,
            'all_received_headers': request_headers,
            'forwarded_headers': forwarded_headers,
            'vulnerability_explanation': (
                'This application accepts connection-specific headers without validation. '
                'These headers should be forbidden in HTTP/2 per RFC 7540. '
                'An attacker could inject headers to cause: '
                '1) Protocol confusion between HTTP/2 and upstream systems '
                '2) Request smuggling if forwarded to multiple backends '
                '3) Response splitting if headers are reflected in response '
                '4) Cache poisoning if processed by intermediate proxies'
            )
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'status': 'ERROR',
            'message': str(e)
        }), 500

@app.route('/api/validate', methods=['POST'])
def validate_headers():
    """
    Endpoint that reports on received headers.
    VULNERABLE: Shows all headers including forbidden ones.
    """
    try:
        headers_dict = dict(request.headers)
        
        # List of headers that SHOULD be forbidden but aren't checked
        should_be_forbidden = {
            'transfer-encoding',
            'connection',
            'keep-alive',
            'upgrade',
            'proxy-connection',
            'trailer'
        }
        
        # VULNERABLE: Find dangerous headers but don't reject them
        suspicious_headers = {}
        for header_name, header_value in headers_dict.items():
            if header_name.lower() in should_be_forbidden:
                suspicious_headers[header_name] = header_value
        
        protocol = request.args.get('protocol', 'HTTP/1.1')
        
        # VULNERABLE: Still accepts the request and reports what was received
        result = {
            'protocol': protocol,
            'all_headers': headers_dict,
            'dangerous_headers_found': len(suspicious_headers),
            'dangerous_headers_list': suspicious_headers,
            'asvs_control': '4.2.3',
            'compliance': 'FAIL - Headers that should be forbidden are accepted',
            'vulnerability': (
                'This implementation identifies dangerous headers but does NOT reject them. '
                'This is a critical vulnerability. HTTP/2 forbids these headers for good reasons:'
            ),
            'why_dangerous': {
                'transfer_encoding': 'Could trigger different chunking behavior in proxies',
                'connection': 'Could cause connection termination affecting multiplexed streams',
                'keep_alive': 'Could affect connection pooling and cause desynchronization',
                'header_injection': 'Any of these could be crafted with CRLF to inject additional headers',
                'response_splitting': 'Specially crafted values could split HTTP response'
            },
            'attack_scenario': (
                'An attacker sends: Transfer-Encoding: chunked\\r\\nContent-Length: 100\\r\\n\\r\\n... '
                'If forwarded to an HTTP/1.1 backend, this could cause request smuggling. '
                'The backend would interpret this differently than the HTTP/2 layer, '
                'leading to request desynchronization.'
            )
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({
            'status': 'ERROR',
            'message': str(e)
        }), 500

@app.route('/api/echo', methods=['POST', 'GET'])
def echo_headers():
    """
    VULNERABLE: Echo all received headers directly in response.
    
    Demonstrates header injection if client controls headers.
    Shows what happens when headers are reflected without sanitization.
    """
    try:
        all_headers = {}
        for header in request.headers:
            all_headers[header[0]] = header[1]
        
        # VULNERABLE: Headers echoed directly in response
        # Could demonstrate response splitting if headers contain CRLF
        return jsonify({
            'received_headers': all_headers,
            'vulnerability': 'Headers are echoed back without sanitization'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/info', methods=['GET'])
def info():
    """
    Information endpoint explaining the vulnerability.
    """
    return jsonify({
        'asvs_control': '4.2.3',
        'requirement': (
            'Verify that the application does not send nor accept HTTP/2 or HTTP/3 '
            'messages with connection-specific header fields such as Transfer-Encoding '
            'to prevent response splitting and header injection attacks.'
        ),
        'level': 3,
        'implementation_status': 'VULNERABLE',
        'what_is_wrong': (
            'This implementation does NOT validate or reject connection-specific headers. '
            'All headers are accepted and processed, creating multiple attack vectors.'
        ),
        'forbidden_headers': [
            'Transfer-Encoding',
            'Connection',
            'Keep-Alive',
            'Upgrade',
            'Proxy-Connection',
            'Trailer'
        ],
        'attack_vectors': {
            'header_injection': {
                'description': 'Attacker injects CRLF to create new headers',
                'example': 'Transfer-Encoding: chunked\\r\\nX-Injected: malicious\\r\\n',
                'impact': 'Inject arbitrary headers into response or upstream request'
            },
            'response_splitting': {
                'description': 'Craft headers to split HTTP response',
                'example': 'Connection: close\\r\\n\\r\\n<injected response>',
                'impact': 'Inject entire response, potentially phishing or XSS'
            },
            'request_smuggling': {
                'description': 'Use Transfer-Encoding with Content-Length',
                'example': 'Transfer-Encoding: chunked\\r\\nContent-Length: 100',
                'impact': 'Confuse different layers about request boundaries'
            },
            'cache_poisoning': {
                'description': 'Inject headers that poison cache key',
                'example': 'Host: attacker.com (if headers are used in cache key)',
                'impact': 'Serve attacker content to other users'
            },
            'protocol_confusion': {
                'description': 'Send HTTP/1.1-style headers in HTTP/2 request',
                'example': 'Send Connection: Upgrade to trigger protocol fallback',
                'impact': 'Downgrade to HTTP/1.1 or cause parsing errors'
            }
        },
        'why_http2_forbids_these': {
            'architecture': (
                'HTTP/2 uses multiplexing - multiple logical streams over one TCP connection. '
                'Connection-level concepts do not apply.'
            ),
            'transfer_encoding': (
                'HTTP/2 frames have explicit length field. Chunking is internal. '
                'This header should never appear in HTTP/2.'
            ),
            'connection': (
                'HTTP/2 manages connection state with GOAWAY frames. '
                'Connection: close could terminate connection affecting other streams.'
            ),
            'rfc': 'RFC 7540 Section 8.1.2 explicitly forbids these headers'
        },
        'how_to_fix': (
            'Validate all HTTP/2 requests before processing. '
            'Reject any request containing connection-specific headers with HTTP 400. '
            'See secure/app.py for correct implementation.'
        ),
        'related_vulnerabilities': [
            'CWE-444: Inconsistent Interpretation of HTTP Requests',
            'CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers',
            'CWE-441: Unintended Proxy or Intermediary (HTTP Request Smuggling)'
        ]
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    # VULNERABLE: No protocol enforcement
    # Should validate and reject HTTP/2 requests with forbidden headers
    app.run(host='0.0.0.0', port=8001, debug=False)
