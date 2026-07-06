from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Trusted infrastructure values simulated internally.
# These values represent what the backend would actually use when
# a trusted proxy or load balancer injects the headers.
TRUSTED_CLIENT_IP = '10.0.0.10'
TRUSTED_USER_ID = 'proxy-user-42'
TRUSTED_HOST = 'secure.example.com'
TRUSTED_PROTO = 'https'
TRUSTED_REAL_IP = '10.0.0.10'
TRUSTED_HEADERS = [
    'X-Forwarded-For',
    'X-Forwarded-Host',
    'X-Forwarded-Proto',
    'X-Real-IP',
    'X-User-ID'
]


def get_trusted_values():
    return {
        'client_ip': TRUSTED_CLIENT_IP,
        'user_id': TRUSTED_USER_ID,
        'host': TRUSTED_HOST,
        'proto': TRUSTED_PROTO,
        'real_ip': TRUSTED_REAL_IP
    }


def get_request_headers():
    return {name: request.headers.get(name, '') for name in TRUSTED_HEADERS}


def evaluate_result(headers):
    # The secure implementation ignores any client-supplied proxy headers.
    # A trusted proxy header must come from infrastructure, not the end user.
    return 'PASS'


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.3',
        description='Trusted Proxy Header Protection',
        badge='SECURE',
        badge_class='secure',
        control='4.1.3',
        result='PASS',
        client_ip=TRUSTED_CLIENT_IP,
        user_id=TRUSTED_USER_ID,
        host=TRUSTED_HOST,
        proto=TRUSTED_PROTO,
        real_ip=TRUSTED_REAL_IP,
        headers=get_request_headers()
    )


@app.route('/api/headers')
def api_headers():
    response = get_trusted_values()
    response['headers'] = get_request_headers()
    response['result'] = evaluate_result(response['headers'])
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
