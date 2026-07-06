from flask import Flask, jsonify, make_response, render_template, request

# This vulnerable implementation accepts too many HTTP methods.
# It intentionally exposes additional methods that should be blocked.
app = Flask(__name__, template_folder='../templates', static_folder='../static')
ALL_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']
SECURE_POLICY = {
    '/': ['GET'],
    '/login': ['GET', 'POST'],
    '/profile': ['GET'],
    '/api/users': ['GET', 'POST', 'OPTIONS'],
    '/api/products': ['GET', 'OPTIONS']
}


def format_allow(methods):
    return ', '.join(methods)


@app.route('/', methods=ALL_METHODS, provide_automatic_options=False)
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.4',
        description='Insecure HTTP method handling for ASVS 4.1.4',
        badge='VULNERABLE',
        badge_class='vulnerable',
        control='4.1.4',
        endpoints=list(SECURE_POLICY.keys()),
        allowed_methods=SECURE_POLICY
    )


@app.route('/login', methods=ALL_METHODS, provide_automatic_options=False)
def login():
    if request.method == 'TRACE':
        return make_response(request.get_data(as_text=True), 200, {'Content-Type': 'message/http', 'Allow': format_allow(ALL_METHODS)})
    if request.method == 'OPTIONS':
        return make_response('', 204, {
            'Allow': format_allow(ALL_METHODS),
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': format_allow(ALL_METHODS),
            'Access-Control-Allow-Headers': 'Content-Type'
        })
    if request.method in ['POST', 'PUT', 'PATCH']:
        data = request.get_json(silent=True) or {'username': 'anonymous'}
        return jsonify({'status': 'insecure', 'method': request.method, 'endpoint': '/login', 'payload': data})
    return jsonify({'status': 'insecure', 'method': request.method, 'endpoint': '/login', 'message': 'Login endpoint accepted the request'})


@app.route('/profile', methods=ALL_METHODS, provide_automatic_options=False)
def profile():
    if request.method == 'TRACE':
        return make_response(request.get_data(as_text=True), 200, {'Content-Type': 'message/http', 'Allow': format_allow(ALL_METHODS)})
    if request.method == 'OPTIONS':
        return make_response('', 204, {
            'Allow': format_allow(ALL_METHODS),
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': format_allow(ALL_METHODS),
            'Access-Control-Allow-Headers': 'Content-Type'
        })
    return jsonify({'status': 'insecure', 'method': request.method, 'endpoint': '/profile', 'profile': {'username': 'attacker', 'role': 'admin'}})


@app.route('/api/users', methods=ALL_METHODS, provide_automatic_options=False)
def api_users():
    if request.method == 'TRACE':
        return make_response(request.get_data(as_text=True), 200, {'Content-Type': 'message/http', 'Allow': format_allow(ALL_METHODS)})
    if request.method == 'OPTIONS':
        return make_response('', 204, {
            'Allow': format_allow(ALL_METHODS),
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': format_allow(ALL_METHODS),
            'Access-Control-Allow-Headers': 'Content-Type'
        })
    if request.method == 'POST':
        return jsonify({'status': 'insecure', 'method': 'POST', 'endpoint': '/api/users', 'created': request.get_json(silent=True) or {}})
    if request.method == 'DELETE':
        return jsonify({'status': 'insecure', 'method': 'DELETE', 'endpoint': '/api/users', 'message': 'All users deleted (simulated)'}), 200
    return jsonify({'status': 'insecure', 'method': request.method, 'endpoint': '/api/users', 'message': 'Request accepted'})


@app.route('/api/products', methods=ALL_METHODS, provide_automatic_options=False)
def api_products():
    if request.method == 'TRACE':
        return make_response(request.get_data(as_text=True), 200, {'Content-Type': 'message/http', 'Allow': format_allow(ALL_METHODS)})
    if request.method == 'OPTIONS':
        return make_response('', 204, {
            'Allow': format_allow(ALL_METHODS),
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': format_allow(ALL_METHODS),
            'Access-Control-Allow-Headers': 'Content-Type'
        })
    return jsonify({'status': 'insecure', 'method': request.method, 'endpoint': '/api/products', 'message': 'Request accepted'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
