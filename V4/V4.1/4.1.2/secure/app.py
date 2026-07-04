from flask import Flask, jsonify, redirect, request, render_template

app = Flask(__name__)


def get_request_scheme():
    forwarded_proto = request.headers.get('X-Forwarded-Proto', '').split(',')[0].strip().lower()
    if forwarded_proto:
        return forwarded_proto
    return request.scheme


def redirect_browser_to_https():
    if get_request_scheme() == 'http':
        https_url = request.url.replace('http://', 'https://', 1)
        return redirect(https_url, code=302)
    return None


def require_https_for_api():
    if get_request_scheme() == 'http':
        return jsonify({
            'error': 'HTTPS required for API endpoints',
            'message': 'Do not redirect API requests automatically. Retry using HTTPS.'
        }), 403
    return None


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.2',
        description='Redirect and API Security',
        badge='SECURE',
        badge_class='secure',
        control='4.1.2'
    )


@app.route('/page')
def page():
    redirect_response = redirect_browser_to_https()
    if redirect_response:
        return redirect_response
    return render_template('page.html')


@app.route('/login')
def login():
    redirect_response = redirect_browser_to_https()
    if redirect_response:
        return redirect_response
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    reject = require_https_for_api()
    if reject:
        return reject
    data = request.get_json(silent=True) or {}
    username = data.get('username', 'anonymous')
    return jsonify({
        'status': 'secure',
        'message': 'Login accepted over HTTPS',
        'user': username
    })


@app.route('/api/profile')
def api_profile():
    reject = require_https_for_api()
    if reject:
        return reject
    return jsonify({
        'status': 'secure',
        'profile': {
            'username': 'student',
            'role': 'tester'
        }
    })


@app.route('/api/data')
def api_data():
    reject = require_https_for_api()
    if reject:
        return reject
    return jsonify({
        'status': 'secure',
        'data': [
            {'id': 1, 'value': 'alpha'},
            {'id': 2, 'value': 'beta'}
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
