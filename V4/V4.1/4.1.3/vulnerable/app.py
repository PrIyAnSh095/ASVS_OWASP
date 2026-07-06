from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

TRUSTED_HEADERS = [
    'X-Forwarded-For',
    'X-Forwarded-Host',
    'X-Forwarded-Proto',
    'X-Real-IP',
    'X-User-ID'
]


def get_display_values():
    return {
        'client_ip': request.headers.get('X-Forwarded-For', request.remote_addr),
        'user_id': request.headers.get('X-User-ID', 'anonymous'),
        'host': request.headers.get('X-Forwarded-Host', request.host),
        'proto': request.headers.get('X-Forwarded-Proto', request.scheme),
        'real_ip': request.headers.get('X-Real-IP', request.remote_addr)
    }


def get_request_headers():
    return {name: request.headers.get(name, '') for name in TRUSTED_HEADERS}


def evaluate_result(headers):
    return 'FAIL' if any(value.strip() for value in headers.values()) else 'PASS'


@app.route('/')
def index():
    values = get_display_values()
    return render_template(
        'index.html',
        title='ASVS V4.1.3',
        description='Trusted Proxy Header Protection',
        badge='VULNERABLE',
        badge_class='vulnerable',
        control='4.1.3',
        result='PASS',
        client_ip=values['client_ip'],
        user_id=values['user_id'],
        host=values['host'],
        proto=values['proto'],
        real_ip=values['real_ip'],
        headers=get_request_headers()
    )


@app.route('/api/headers')
def api_headers():
    response = get_display_values()
    response['headers'] = get_request_headers()
    response['result'] = evaluate_result(response['headers'])
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
