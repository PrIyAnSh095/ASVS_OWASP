from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

# SECURE IMPLEMENTATION:
# We maintain a strict allowlist of trusted origins.
# SocketIO will inspect the 'Origin' HTTP header during the initial WebSocket handshake.
# If the origin is not in this list, the handshake is rejected with a 400 Bad Request.
# This prevents Cross-Site WebSocket Hijacking (CSWSH).
ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5000"
]

socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGINS)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    # Simple echo
    send(f"Secure Echo: {msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
