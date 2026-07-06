# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='../static')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        uri = request.form.get('uri', '')
        cookie = request.form.get('cookie', '')
        auth = request.form.get('auth', '')
        custom_header = request.form.get('custom_header', '')

        # VULNERABILITY: No length validation on URI or headers
        try:
            headers = {}
            if cookie: headers['Cookie'] = cookie
            if auth: headers['Authorization'] = auth
            if custom_header: headers['X-Custom-Data'] = custom_header
            
            # The vulnerable app directly proxies whatever the user provided
            downstream_url = f"http://localhost:5000/mock_downstream{uri}"
            
            # In a real scenario, this could hit internal components causing memory exhaustion or timeouts
            resp = requests.get(downstream_url, headers=headers, timeout=2)
            
            result = {
                'status': 'PASS', 
                'message': 'Request sent downstream successfully.', 
                'http_status': 200,
                'downstream_response': resp.text
            }
        except requests.exceptions.RequestException as e:
            # We catch it here to show that the downstream component threw an error or timed out
            # when dealing with oversized requests.
            result = {
                'status': 'FAIL', 
                'message': f"Downstream request failed: {str(e)}", 
                'http_status': 500
            }

    return render_template('index.html', result=result)

@app.route('/mock_downstream/<path:subpath>')
def mock_downstream(subpath):
    # Werkzeug built-in server will likely drop or error out natively if URI/headers are too huge,
    # mimicking a downstream DoS or rejection (e.g. 431 Request Header Fields Too Large or 414 URI Too Long).
    return jsonify({"success": True, "received_path": subpath})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
