from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, send, ConnectionRefusedError
import secrets
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure-super-secret'
# Note: For production, cookies should be HttpOnly and Secure.

socketio = SocketIO(app, cors_allowed_origins="*")

# Valid WS tokens mapped to the user who requested them and an expiry.
# Format: { "token": {"user": "admin", "expires": 1600000000} }
ws_tokens = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # 1. Establish HTTP Session via authentication
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'admin' and password == 'password':
        session['user'] = username # Sets HTTP Cookie
        return jsonify({"success": True, "user": username})
    return jsonify({"success": False}), 401

@app.route('/api/ws-token', methods=['GET'])
def get_ws_token():
    # 2. Issue a WS Token ONLY to authenticated HTTP sessions
    if 'user' not in session:
        return jsonify({"error": "Unauthorized. Please login over HTTP first."}), 401
    
    token = secrets.token_hex(32)
    # Token valid for 30 seconds for the transition
    ws_tokens[token] = {
        "user": session['user'],
        "expires": time.time() + 30
    }
    return jsonify({"token": token})

@socketio.on('connect')
def handle_connect(auth):
    # 3. WebSocket validates the transitioned token
    token = auth.get('token') if auth else None
    
    if not token:
        raise ConnectionRefusedError('Missing WebSocket token.')
    
    if token not in ws_tokens:
        raise ConnectionRefusedError('Invalid or reused token.')
    
    token_data = ws_tokens[token]
    
    if time.time() > token_data['expires']:
        del ws_tokens[token]
        raise ConnectionRefusedError('Token expired.')
    
    # Burn the token after successful transition (single-use ticket)
    user = token_data['user']
    del ws_tokens[token]
    
    print(f"WebSocket connected securely for user: {user}")

@socketio.on('message')
def handle_message(msg):
    send(f"Secure Transition Echo: {msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
