import json
from flask import Flask, jsonify, render_template, request, Response

app = Flask(__name__, template_folder='../templates', static_folder='../static')

CONTROL = '4.2.2'

RESPONSE_TEMPLATES = {
    'normal': ('Plain text response body.', 'text/plain'),
    'json': (
        json.dumps({
            'status': 'success',
            'message': 'This is a JSON response.',
            'value': 42
        }, indent=2),
        'application/json'
    ),
    'html': ('<html><body><h1>HTML response</h1><p>This is an HTML response.</p></body></html>', 'text/html'),
    'truncated': ('Truncated body demonstration.', 'text/plain')
}


def build_body(response_type):
    body, content_type = RESPONSE_TEMPLATES.get(response_type, RESPONSE_TEMPLATES['normal'])
    return body, content_type


def build_response(response_type):
    body_text, content_type = build_body(response_type)
    body_bytes = body_text.encode('utf-8')
    declared_length = len(body_bytes)

    if response_type == 'json':
        declared_length += 15
    elif response_type == 'truncated':
        declared_length = max(len(body_bytes) - 5, 0)
    elif response_type == 'html':
        declared_length = max(len(body_bytes) - 10, 0)
    else:
        declared_length = max(len(body_bytes) - 3, 0)

    response = Response(body_bytes, status=200, mimetype=content_type)
    response.headers['Content-Length'] = str(declared_length)
    return response


def analyze_response(response_type):
    body_text, content_type = build_body(response_type)
    body_bytes = body_text.encode('utf-8')
    actual_length = len(body_bytes)
    declared_length = actual_length

    if response_type == 'json':
        declared_length += 15
    elif response_type == 'truncated':
        declared_length = max(actual_length - 5, 0)
    elif response_type == 'html':
        declared_length = max(actual_length - 10, 0)
    else:
        declared_length = max(actual_length - 3, 0)

    matches = declared_length == actual_length
    return {
        'response_type': response_type,
        'content_type': content_type,
        'declared_length': declared_length,
        'body_length': actual_length,
        'matches': matches,
        'status': 'PASS' if matches else 'FAIL',
        'body': body_text,
        'message': 'This vulnerable implementation intentionally misreports Content-Length to demonstrate protocol framing failures.'
    }


@app.route('/')
def index():
    return render_template(
        'index.html',
        title=f'ASVS V{CONTROL}',
        description='Vulnerable response generation with incorrect Content-Length.',
        badge='VULNERABLE',
        badge_class='vulnerable',
        control=CONTROL
    )


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(silent=True) or {}
    response_type = data.get('type', 'normal')
    return build_response(response_type)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(silent=True) or {}
    response_type = data.get('type', 'normal')
    return jsonify(analyze_response(response_type))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
