from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='../static')

MAX_URI_LENGTH = 128
MAX_COOKIE_LENGTH = 256
MAX_AUTH_LENGTH = 256
MAX_CUSTOM_HEADER_LENGTH = 128

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        uri = request.form.get('uri', '')
        cookie = request.form.get('cookie', '')
        auth = request.form.get('auth', '')
        custom_header = request.form.get('custom_header', '')

        errors = []
        if len(uri.encode('utf-8')) > MAX_URI_LENGTH:
            errors.append(f'URI length exceeds maximum allowed ({MAX_URI_LENGTH} bytes).')
        if len(cookie.encode('utf-8')) > MAX_COOKIE_LENGTH:
            errors.append(f'Cookie header length exceeds maximum allowed ({MAX_COOKIE_LENGTH} bytes).')
        if len(auth.encode('utf-8')) > MAX_AUTH_LENGTH:
            errors.append(f'Authorization header length exceeds maximum allowed ({MAX_AUTH_LENGTH} bytes).')
        if len(custom_header.encode('utf-8')) > MAX_CUSTOM_HEADER_LENGTH:
            errors.append(f'Custom header length exceeds maximum allowed ({MAX_CUSTOM_HEADER_LENGTH} bytes).')

        if errors:
            result = {'status': 'FAIL', 'errors': errors, 'http_status': 400}
        else:
            try:
                headers = {}
                if cookie: headers['Cookie'] = cookie
                if auth: headers['Authorization'] = auth
                if custom_header: headers['X-Custom-Data'] = custom_header
                
                # Mock downstream endpoint call
                downstream_url = f"http://localhost:5000/mock_downstream{uri}"
                resp = requests.get(downstream_url, headers=headers, timeout=2)
                result = {
                    'status': 'PASS', 
                    'message': 'Request validated and sent successfully.', 
                    'http_status': 200,
                    'downstream_response': resp.text
                }
            except requests.exceptions.RequestException as e:
                result = {'status': 'FAIL', 'errors': [f"Downstream request failed: {str(e)}"], 'http_status': 500}

    return render_template('index.html', result=result)

@app.route('/mock_downstream/<path:subpath>')
def mock_downstream(subpath):
    # This endpoint simulates a downstream service that would crash on huge headers or URIs
    # In reality, a web server (like nginx/apache or gunicorn) has built-in limits and returns 414 or 431.
    return jsonify({"success": True, "received_path": subpath})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
