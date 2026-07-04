from flask import Flask, jsonify, make_response, render_template, request

# This secure implementation intentionally limits the accepted HTTP methods.
# Unnecessary HTTP methods increase attack surface and should be rejected.
app = Flask(__name__, template_folder='../templates', static_folder='../static')

ALLOWED_METHODS = {
    '/': ['GET'],
    '/login': ['GET', 'POST'],
    '/profile': ['GET'],
    '/api/users': ['GET', 'POST', 'OPTIONS'],
    '/api/products': ['GET', 'OPTIONS']
}


def format_allow(methods):
    return ', '.join(methods)


def cors_options(allowed):
    headers = {
        'Allow': format_allow(allowed),
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': format_allow(allowed),
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return make_response('', 204, headers)


@app.before_request
def enforce_allowed_methods():
    allowed = ALLOWED_METHODS.get(request.path)
    if allowed is None:
        return None

    if request.method == 'OPTIONS':
        if 'OPTIONS' in allowed:
            return cors_options(allowed)
        return make_response(jsonify({'error': 'Method Not Allowed', 'allowed': allowed}), 405, {'Allow': format_allow(allowed)})

    if request.method not in allowed:
        return make_response(jsonify({'error': 'Method Not Allowed', 'allowed': allowed}), 405, {'Allow': format_allow(allowed)})


@app.route('/', methods=['GET'], provide_automatic_options=False)
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.4',
        description='Strict HTTP method enforcement for ASVS 4.1.4',
        badge='SECURE',
        badge_class='secure',
        control='4.1.4',
        endpoints=list(ALLOWED_METHODS.keys()),
        allowed_methods=ALLOWED_METHODS
    )


@app.route('/login', methods=['GET', 'POST'], provide_automatic_options=False)
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {'username': 'anonymous'}
        return jsonify({
            'status': 'success',
            'endpoint': '/login',
            'method': 'POST',
            'message': 'Login request accepted',
            'payload': data
        })

    return jsonify({
        'status': 'success',
        'endpoint': '/login',
        'method': 'GET',
        'message': 'Login page is available'
    })


@app.route('/profile', methods=['GET'], provide_automatic_options=False)
def profile():
    return jsonify({
        'status': 'success',
        'endpoint': '/profile',
        'method': 'GET',
        'profile': {
            'username': 'student',
            'role': 'tester'
        }
    })


@app.route('/api/users', methods=['GET', 'POST', 'OPTIONS'], provide_automatic_options=False)
def api_users():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {'username': 'anonymous'}
        return jsonify({
            'status': 'success',
            'endpoint': '/api/users',
            'method': 'POST',
            'created': data
        })

    return jsonify({
        'status': 'success',
        'endpoint': '/api/users',
        'method': 'GET',
        'users': [
            {'id': 1, 'username': 'alice'},
            {'id': 2, 'username': 'bob'}
        ]
    })


@app.route('/api/products', methods=['GET', 'OPTIONS'], provide_automatic_options=False)
def api_products():
    return jsonify({
        'status': 'success',
        'endpoint': '/api/products',
        'method': 'GET',
        'products': [
            {'id': 1, 'name': 'Widget'},
            {'id': 2, 'name': 'Gadget'}
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
