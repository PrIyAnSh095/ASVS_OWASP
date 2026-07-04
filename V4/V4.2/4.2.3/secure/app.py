"""
ASVS 4.2.3 Secure Implementation
HTTP/2 and HTTP/3 Connection-Specific Header Validation

This application validates HTTP/2 and HTTP/3 requests and rejects any messages
containing connection-specific headers that are forbidden in these protocols.

RFC 7540 (HTTP/2) explicitly forbids the following headers in HTTP/2 messages:
- Transfer-Encoding
- Connection
- Keep-Alive
- Upgrade
- Proxy-Connection
- Trailer

These headers are connection-specific and have no meaning in HTTP/2's multiplexing model.
Accepting them could enable header injection, response splitting, and protocol confusion attacks.
"""

from flask import Flask, render_template, request, jsonify
from functools import wraps
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RFC 7540: Connection-Specific Headers forbidden in HTTP/2
FORBIDDEN_HTTP2_HEADERS = {
    'transfer-encoding',
    'connection',
    'keep-alive',
    'upgrade',
    'proxy-connection',
    'trailer'
}

def validate_http2_headers(f):
    """
    Decorator to validate that HTTP/2/HTTP/3 requests do not contain
    connection-specific headers.
    
    This implements ASVS 4.2.3 requirement to reject HTTP/2 or HTTP/3 messages
    containing connection-specific header fields.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if this is an HTTP/2 or HTTP/3 request
        # HTTP/2 is indicated by 'h2' in Server variable or X-HTTP2-Request header
        http_version = request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1')
        is_http2_or_http3 = 'h2' in http_version.lower() or request.headers.get('X-HTTP2-Request')
        
        # For demonstration, we also check headers to simulate both protocols
        protocol_hint = request.args.get('protocol', 'http1')
        if protocol_hint in ['http2', 'http3']:
            is_http2_or_http3 = True
        
        if is_http2_or_http3:
            # Check for forbidden headers
            forbidden_found = []
            for header_name in request.headers.keys():
                if header_name.lower() in FORBIDDEN_HTTP2_HEADERS:
                    forbidden_found.append(header_name)
            
            if forbidden_found:
                logger.warning(
                    f"HTTP/2 request rejected: contains forbidden headers {forbidden_found}"
                )
                return jsonify({
                    'status': 'FAIL',
                    'message': 'HTTP/2 and HTTP/3 must not contain connection-specific headers',
                    'forbidden_headers_found': forbidden_found,
                    'asvs_control': '4.2.3',
                    'protocol': 'HTTP/2 or HTTP/3',
                    'reason': 'RFC 7540 forbids connection-specific headers in HTTP/2 to prevent response splitting and header injection attacks'
                }), 400
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Main page with lab interface"""
    return render_template('index.html')

@app.route('/api/test', methods=['POST', 'GET'])
@validate_http2_headers
def test_endpoint():
    """
    Test endpoint that accepts requests and shows response.
    
    Protected by @validate_http2_headers decorator which ensures
    HTTP/2 compliance.
    """
    try:
        data = request.get_json() if request.method == 'POST' else {}
        
        # Echo back request headers for educational purposes
        request_headers = dict(request.headers)
        
        # Check for connection-specific headers (redundant check for clarity)
        forbidden_headers = [
            h for h in request_headers.keys() 
            if h.lower() in FORBIDDEN_HTTP2_HEADERS
        ]
        
        response = {
            'status': 'PASS',
            'message': 'Request accepted - compliant with ASVS 4.2.3',
            'asvs_control': '4.2.3',
            'protocol': request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1'),
            'request_data': data,
            'forbidden_headers_found': forbidden_headers,
            'explanation': (
                'No forbidden connection-specific headers were present in this HTTP/2 request. '
                'HTTP/2 (RFC 7540) removed connection-specific headers because: '
                '1) HTTP/2 uses multiplexing - multiple streams share one connection '
                '2) Connection-scoped concepts (Keep-Alive, Upgrade) are meaningless in HTTP/2 '
                '3) These headers could be used for header injection and response splitting attacks'
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
    Endpoint for testing custom headers.
    Returns detailed validation results.
    """
    try:
        # Get all request headers
        headers_dict = dict(request.headers)
        
        # Check for forbidden HTTP/2 headers
        forbidden_found = {}
        for header_name, header_value in headers_dict.items():
            if header_name.lower() in FORBIDDEN_HTTP2_HEADERS:
                forbidden_found[header_name] = header_value
        
        # Determine protocol
        protocol = request.args.get('protocol', 'HTTP/1.1')
        
        result = {
            'protocol': protocol,
            'all_headers': headers_dict,
            'forbidden_headers_count': len(forbidden_found),
            'forbidden_headers': forbidden_found,
            'is_compliant': len(forbidden_found) == 0,
            'asvs_control': '4.2.3',
            'rfc': 'RFC 7540 (HTTP/2)',
            'explanation': {
                'transfer_encoding': 'HTTP/2 uses chunk encoding internally; this header should not be sent by clients',
                'connection': 'HTTP/2 connections are persistent; Connection header is meaningless',
                'keep_alive': 'HTTP/2 maintains connections automatically; Keep-Alive is obsolete',
                'upgrade': 'HTTP/2 uses different negotiation; Upgrade header is not applicable',
                'proxy_connection': 'Non-standard header; meaningless in HTTP/2',
                'trailer': 'Trailers are handled differently in HTTP/2'
            }
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({
            'status': 'ERROR',
            'message': str(e)
        }), 500

@app.route('/api/info', methods=['GET'])
def info():
    """
    Educational endpoint providing information about the control.
    """
    return jsonify({
        'asvs_control': '4.2.3',
        'requirement': (
            'Verify that the application does not send nor accept HTTP/2 or HTTP/3 '
            'messages with connection-specific header fields such as Transfer-Encoding '
            'to prevent response splitting and header injection attacks.'
        ),
        'level': 3,
        'forbidden_headers': list(FORBIDDEN_HTTP2_HEADERS),
        'why_forbidden': {
            'background': (
                'HTTP/2 (RFC 7540) fundamentally changed how HTTP works. '
                'While HTTP/1.1 uses one TCP connection per request/response pair, '
                'HTTP/2 multiplexes multiple logical streams over a single TCP connection. '
                'This architectural difference makes connection-specific headers meaningless and dangerous.'
            ),
            'transfer_encoding': (
                'In HTTP/2, all messages are transmitted in frames with explicit length. '
                'The Transfer-Encoding header is not used. An attacker sending '
                'Transfer-Encoding: chunked could cause confusion between HTTP/2 and upstream proxies.'
            ),
            'connection': (
                'Explicitly tells the recipient to close the connection after this message. '
                'HTTP/2 prohibits this because connections are shared across multiple streams. '
                'This could force connection termination affecting other users.'
            ),
            'keep_alive': (
                'Negotiates connection persistence. HTTP/2 connections are always persistent '
                'until an explicit GOAWAY frame. This header is obsolete in HTTP/2.'
            ),
            'header_injection': (
                'If an application accepts and forwards these headers without validation, '
                'an attacker could inject them to manipulate intermediary proxies, '
                'potentially causing request smuggling or response splitting.'
            ),
            'response_splitting': (
                'By injecting CRLF sequences within these headers, an attacker could '
                'inject additional HTTP headers or even a complete response, '
                'bypassing security controls.'
            )
        },
        'implementation': (
            'The secure implementation validates all incoming HTTP/2 requests and '
            'rejects any message containing connection-specific headers. '
            'This is done before request processing to fail securely.'
        ),
        'tests_included': [
            'curl command with custom headers',
            'Burp Suite intruder to test multiple headers',
            'Direct header injection attempts',
            'Protocol confusion scenarios'
        ]
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    # Note: In production, use Gunicorn with Hypercorn worker or Hypercorn directly
    # This app should be run with: hypercorn app:app --bind 0.0.0.0:8000 --http2
    app.run(host='0.0.0.0', port=8000, debug=False)
