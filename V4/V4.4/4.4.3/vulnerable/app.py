from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # VULNERABILITY 1: Predictable/Hardcoded Token
    # The server issues a generic, non-expiring, predictable token.
    token = "admin-token-123"
    return jsonify({"token": token})

@socketio.on('connect')
def handle_connect(auth):
    # VULNERABILITY 2: No strict validation
    token = auth.get('token') if auth else None
    
    # We allow the connection even if the token is completely missing!
    if token == None:
        print("Client connected with NO token. Allowing anyway...")
    else:
        print(f"Client connected with token: {token}")

@socketio.on('message')
def handle_message(msg):
    send(f"Insecure Auth Echo: {msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
