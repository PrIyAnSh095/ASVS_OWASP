from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, send
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vulnerable-super-secret'

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'password':
        session['user'] = username
        return jsonify({"success": True, "user": username})
    return jsonify({"success": False}), 401

@app.route('/api/ws-token', methods=['GET'])
def get_ws_token():
    # VULNERABILITY 1: The token endpoint does NOT check if the HTTP request is authenticated!
    # Anyone can request a WS token.
    token = secrets.token_hex(32)
    return jsonify({"token": token})

@socketio.on('connect')
def handle_connect(auth):
    # VULNERABILITY 2: The WebSocket connection doesn't even validate the token.
    # It allows connections completely bypassing the HTTPS authentication flow.
    print("WebSocket connected (Bypassing HTTPS Auth flow)")

@socketio.on('message')
def handle_message(msg):
    send(f"Insecure Transition Echo: {msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
