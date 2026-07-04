from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

# VULNERABLE IMPLEMENTATION:
# The server is configured to accept WebSocket connections from ANY origin ('*').
# It does not validate the Origin header during the HTTP handshake.
# This makes the application vulnerable to Cross-Site WebSocket Hijacking (CSWSH).
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    send(f"Insecure Echo: {msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
