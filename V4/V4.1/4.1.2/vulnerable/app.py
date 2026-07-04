from flask import Flask, jsonify, redirect, request, render_template

app = Flask(__name__)


def get_request_scheme():
    forwarded_proto = request.headers.get('X-Forwarded-Proto', '').split(',')[0].strip().lower()
    if forwarded_proto:
        return forwarded_proto
    return request.scheme


def redirect_all_http_requests():
    if get_request_scheme() == 'http':
        https_url = request.url.replace('http://', 'https://', 1)
        return redirect(https_url, code=307)
    return None


@app.before_request
def before_request():
    redirect_response = redirect_all_http_requests()
    if redirect_response:
        return redirect_response


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.2',
        description='Redirect and API Security',
        badge='VULNERABLE',
        badge_class='vulnerable',
        control='4.1.2'
    )


@app.route('/page')
def page():
    return render_template('page.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or {}
    return jsonify({
        'status': 'vulnerable',
        'message': 'HTTP login requests are redirected to HTTPS',
        'received': data
    })


@app.route('/api/profile')
def api_profile():
    return jsonify({
        'status': 'vulnerable',
        'profile': {
            'username': 'insecure',
            'role': 'user'
        }
    })


@app.route('/api/data')
def api_data():
    return jsonify({
        'status': 'vulnerable',
        'data': ['one', 'two', 'three']
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
