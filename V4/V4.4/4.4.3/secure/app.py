# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, ConnectionRefusedError
import secrets
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

# SECURE IMPLEMENTATION:
# We require a dedicated, cryptographically secure token to connect to the WebSocket.
# This prevents attacks where standard session cookies cannot be attached properly,
# or where WebSockets cross domains. Tokens expire after 30 seconds.
socketio = SocketIO(app, cors_allowed_origins="*") # Origin checked handled in previous lab, focusing on auth here

# Store valid tokens in memory: { "token_string": expiry_timestamp }
valid_tokens = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Simulate a successful login returning a unique, secure, expiring token
    token = secrets.token_hex(32)
    # Token expires in 30 seconds for demonstration purposes
    valid_tokens[token] = time.time() + 30
    return jsonify({"token": token})

@socketio.on('connect')
def handle_connect(auth):
    # Retrieve the token from the auth payload
    token = auth.get('token') if auth else None
    
    if not token:
        raise ConnectionRefusedError('Authentication required. Missing token.')
    
    if token not in valid_tokens:
        raise ConnectionRefusedError('Invalid token.')
    
    if time.time() > valid_tokens[token]:
        del valid_tokens[token]
        raise ConnectionRefusedError('Token expired.')
    
    # Optional: Delete token after use if it's a one-time connection ticket
    # del valid_tokens[token]
    
    print(f"Client connected successfully with token: {token}")

@socketio.on('message')
def handle_message(msg):
    send(f"Secure Auth Echo: {msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
