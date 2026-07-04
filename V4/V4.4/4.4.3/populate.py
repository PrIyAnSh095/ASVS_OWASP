import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V4\V4.4\4.4.3"

def write_file(rel_path, content):
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Written {rel_path}")

layout_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ASVS 4.4.3 - WebSocket Authentication</title>
</head>
<body>
    <h1>ASVS 4.4.3: WebSocket Authentication Tokens</h1>
    {% block content %}{% endblock %}
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</body>
</html>
"""

write_file(r"secure\templates\layout.html", layout_html)
write_file(r"vulnerable\templates\layout.html", layout_html)

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure WebSocket Server</h2>
    <p>Authentication requires a dedicated, expiring, cryptographically secure token.</p>
    
    <div style="border:1px solid #000; padding:10px; margin-bottom:10px;">
        <h3>1. Authentication</h3>
        <button id="loginBtn">Simulate Login (Get Token)</button>
        <p>Your Token: <input type="text" id="tokenInput" placeholder="Click login to get token" style="width: 300px;"></p>
    </div>

    <div style="border:1px solid #000; padding:10px;">
        <h3>2. WebSocket Connection</h3>
        <button id="connectBtn">Connect to WebSocket</button>
        <button id="disconnectBtn" disabled>Disconnect</button>
        <br><br>
        <input type="text" id="messageBox" placeholder="Type a message..." disabled>
        <button id="sendBtn" disabled>Send</button>
        <br><br>
        <strong>Connection Status:</strong> <span id="statusIndicator">Disconnected</span>
        | <strong>PASS / FAIL:</strong> <span id="passFailIndicator">N/A</span>
    </div>
    
    <h3>Message Log:</h3>
    <pre id="logViewer" style="border:1px solid #ccc; padding:10px; height:200px; overflow-y:scroll;"></pre>

    <script>
        let socket;
        const statusIndicator = document.getElementById('statusIndicator');
        const passFailIndicator = document.getElementById('passFailIndicator');
        const logViewer = document.getElementById('logViewer');
        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');
        const loginBtn = document.getElementById('loginBtn');
        const tokenInput = document.getElementById('tokenInput');

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        loginBtn.addEventListener('click', async () => {
            const res = await fetch('/login', { method: 'POST' });
            const data = await res.json();
            tokenInput.value = data.token;
            logMessage('Login successful. Received WS Token: ' + data.token);
        });

        connectBtn.addEventListener('click', () => {
            const token = tokenInput.value;
            logMessage('Attempting to connect with token: ' + token);
            
            // Connect to Socket.IO sending the token in the auth payload
            socket = io({
                auth: {
                    token: token
                }
            });

            socket.on('connect', () => {
                statusIndicator.textContent = 'Connected';
                statusIndicator.style.color = 'green';
                passFailIndicator.textContent = 'PASS';
                passFailIndicator.style.color = 'green';
                connectBtn.disabled = true;
                disconnectBtn.disabled = false;
                messageBox.disabled = false;
                sendBtn.disabled = false;
                logMessage('Socket.IO connection established.');
            });

            socket.on('message', (data) => {
                logMessage('Server: ' + data);
            });

            socket.on('disconnect', () => {
                statusIndicator.textContent = 'Disconnected';
                statusIndicator.style.color = 'black';
                connectBtn.disabled = false;
                disconnectBtn.disabled = true;
                messageBox.disabled = true;
                sendBtn.disabled = true;
                logMessage('Disconnected from server.');
            });

            socket.on('connect_error', (err) => {
                statusIndicator.textContent = 'Connection Error / Rejected';
                statusIndicator.style.color = 'red';
                passFailIndicator.textContent = 'FAIL / REJECTED';
                passFailIndicator.style.color = 'red';
                logMessage('Connection Error: ' + err.message);
            });
        });

        disconnectBtn.addEventListener('click', () => {
            if (socket) socket.disconnect();
        });

        sendBtn.addEventListener('click', () => {
            const msg = messageBox.value;
            if (msg && socket && socket.connected) {
                socket.send(msg);
                logMessage('You: ' + msg);
                messageBox.value = '';
            }
        });
    </script>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Vulnerable WebSocket Server</h2>
    <p>Authentication accepts any token, no token, or a hardcoded token.</p>
    
    <div style="border:1px solid #000; padding:10px; margin-bottom:10px;">
        <h3>1. Authentication</h3>
        <button id="loginBtn">Simulate Login (Get Token)</button>
        <p>Your Token: <input type="text" id="tokenInput" placeholder="Leave empty or enter anything" style="width: 300px;"></p>
    </div>

    <div style="border:1px solid #000; padding:10px;">
        <h3>2. WebSocket Connection</h3>
        <button id="connectBtn">Connect to WebSocket</button>
        <button id="disconnectBtn" disabled>Disconnect</button>
        <br><br>
        <input type="text" id="messageBox" placeholder="Type a message..." disabled>
        <button id="sendBtn" disabled>Send</button>
        <br><br>
        <strong>Connection Status:</strong> <span id="statusIndicator">Disconnected</span>
        | <strong>PASS / FAIL:</strong> <span id="passFailIndicator">N/A</span>
    </div>
    
    <h3>Message Log:</h3>
    <pre id="logViewer" style="border:1px solid #ccc; padding:10px; height:200px; overflow-y:scroll;"></pre>

    <script>
        let socket;
        const statusIndicator = document.getElementById('statusIndicator');
        const passFailIndicator = document.getElementById('passFailIndicator');
        const logViewer = document.getElementById('logViewer');
        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');
        const loginBtn = document.getElementById('loginBtn');
        const tokenInput = document.getElementById('tokenInput');

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        loginBtn.addEventListener('click', async () => {
            const res = await fetch('/login', { method: 'POST' });
            const data = await res.json();
            tokenInput.value = data.token;
            logMessage('Login successful. Received WS Token: ' + data.token);
        });

        connectBtn.addEventListener('click', () => {
            const token = tokenInput.value;
            logMessage('Attempting to connect with token: ' + token);
            
            // Connect to Socket.IO sending the token
            socket = io({
                auth: {
                    token: token
                }
            });

            socket.on('connect', () => {
                statusIndicator.textContent = 'Connected (Vulnerable)';
                statusIndicator.style.color = 'orange';
                passFailIndicator.textContent = 'FAIL (Allowed connection)';
                passFailIndicator.style.color = 'red';
                connectBtn.disabled = true;
                disconnectBtn.disabled = false;
                messageBox.disabled = false;
                sendBtn.disabled = false;
                logMessage('Socket.IO connection established.');
            });

            socket.on('message', (data) => {
                logMessage('Server: ' + data);
            });

            socket.on('disconnect', () => {
                statusIndicator.textContent = 'Disconnected';
                statusIndicator.style.color = 'black';
                connectBtn.disabled = false;
                disconnectBtn.disabled = true;
                messageBox.disabled = true;
                sendBtn.disabled = true;
                logMessage('Disconnected from server.');
            });

            socket.on('connect_error', (err) => {
                statusIndicator.textContent = 'Connection Error';
                statusIndicator.style.color = 'red';
                logMessage('Connection Error: ' + err.message);
            });
        });

        disconnectBtn.addEventListener('click', () => {
            if (socket) socket.disconnect();
        });

        sendBtn.addEventListener('click', () => {
            const msg = messageBox.value;
            if (msg && socket && socket.connected) {
                socket.send(msg);
                logMessage('You: ' + msg);
                messageBox.value = '';
            }
        });
    </script>
{% endblock %}
""")

write_file(r"secure\static\css\style.css", "")
write_file(r"secure\static\js\app.js", "")
write_file(r"vulnerable\static\css\style.css", "")
write_file(r"vulnerable\static\js\app.js", "")

# --- SECURE APP ---
write_file(r"secure\app.py", """
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
""")

write_file(r"secure\requirements.txt", """
Flask==2.3.2
Flask-SocketIO==5.3.6
eventlet==0.33.3
""")

write_file(r"secure\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
""")

write_file(r"secure\docker-compose.yml", """
version: '3.8'
services:
  secure-auth-443:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 4.4.3

This application securely authenticates WebSocket connections using dedicated authentication tokens.

## How it works
1. When a user authenticates via standard HTTP (the `/login` endpoint), the server issues a cryptographically secure, random 256-bit token.
2. This token is stored on the server with a short expiration time (e.g., 30 seconds).
3. The client establishes the WebSocket connection and passes the token in the initial `auth` payload.
4. The server validates the token on the `connect` event. If the token is missing, invalid, or expired, the connection is instantly rejected with `ConnectionRefusedError`.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
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
""")

write_file(r"vulnerable\requirements.txt", """
Flask==2.3.2
Flask-SocketIO==5.3.6
eventlet==0.33.3
""")

write_file(r"vulnerable\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
""")

write_file(r"vulnerable\docker-compose.yml", """
version: '3.8'
services:
  vulnerable-auth-443:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 4.4.3

This application fails to implement secure dedicated tokens for WebSocket authentication.

## Vulnerability
The server does not enforce token presence or validity. An attacker can connect to the WebSocket endpoint without providing a token at all. Furthermore, the token generated by the server is a hardcoded, predictable string (`admin-token-123`) that never expires, meaning even if it were checked, an attacker could easily guess or reuse it indefinitely.
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 4.4.3 (WebSocket Authentication)

WebSockets present a unique challenge for authentication because they do not always easily inherit the standard HTTP session management controls (like `HttpOnly` cookies, depending on the client library or CORS configurations).

## Authentication Bypasses
If an application fails to securely authenticate a WebSocket connection:
1. **Missing Authentication:** An attacker can directly connect to `wss://api.example.com/stream` and start sending/receiving sensitive data without proving their identity.
2. **Weak Tokens:** If the WebSocket expects a token via a query parameter (e.g., `?token=123`) or initial payload, and the token is predictable, weak, or non-expiring, an attacker can guess it or steal it and use it forever.

## Impact
Unauthorized access to real-time data feeds, unauthorized execution of privileged commands via the WebSocket channel, and full session hijacking of the WebSocket context.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

You can use Burp Suite to manipulate the WebSocket connection parameters and test authentication controls.

## Testing Steps
1. Intercept the WebSocket connection request (the `GET` request upgrading the connection).
2. For Socket.IO v4, the authentication token is usually passed in the first WebSocket payload immediately after the HTTP upgrade, or as a query parameter in the handshake (e.g., `EIO=4&token=...`).
3. Attempt the following tests:
   * **Missing Token:** Delete the token parameter entirely and forward the request.
   * **Invalid Token:** Modify the token to random characters.
   * **Expired Token:** Wait 60 seconds and attempt to reconnect using the same token.

## Evaluating Results
* **PASS (Secure App):** The server refuses the connection or immediately closes the socket when invalid/expired/missing tokens are used.
* **FAIL (Vulnerable App):** The server establishes the connection and allows data exchange regardless of the token's state.
""")

write_file(r"docs\curl.md", """
# Testing with cURL / CLI

Because authentication happens during the Socket.IO protocol handshake or the initial WS payload, standard cURL is difficult to use for full validation. However, you can use CLI scripts or Postman's WebSocket interface.

To test manually:
1. Connect to the WebSocket endpoint.
2. Send an initial frame without the token payload.
3. Observe if the server closes the connection (Secure) or responds normally (Vulnerable).
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* The server issues a long, cryptographically random string (e.g., a 256-bit hex token or a signed JWT) upon a successful HTTP login.
* The server records the expiration time of the token.
* The client passes the token securely (via the WS `auth` payload).
* The server strictly validates the token before allowing any business logic. Invalid tokens result in connection refusal.

## Vulnerable Implementation
* The server allows connections without checking for a token.
* Or, the server uses a static, hardcoded token (like `admin-token-123`) that never expires.
* An attacker can easily bypass authentication and access the WebSocket channel.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* **Why Dedicated Tokens?** If your WebSocket server is hosted on a different domain than your frontend (e.g., `api.example.com` vs `www.example.com`), `HttpOnly` session cookies might not be sent automatically during the WebSocket handshake due to CORS/SameSite restrictions. In these cases, dedicated connection tokens (like Connection Tickets) are strictly required.
* **One-Time Use:** Ideally, a dedicated WebSocket token should be a one-time use "ticket". The client requests a ticket via an authenticated HTTP REST call, receives a ticket valid for 30 seconds, uses it to open the WebSocket, and the server immediately burns the ticket.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To securely implement ASVS 4.4.3:

1. **Do Not Rely Exclusively on Query Parameters:** Avoid passing long-lived API keys or session tokens in the WebSocket URI (e.g., `ws://...?token=abc`), as URIs are logged in server access logs and proxy logs.
2. **Use Initial Payload Authentication:** Send the token inside the very first WebSocket frame after the connection is established (or via the `auth` payload supported by Socket.IO).
3. **Use Connection Tickets:**
   * Create an HTTP endpoint `/api/ws-ticket` protected by standard session cookies.
   * Generate a short-lived (e.g., 60 seconds), single-use cryptographic token.
   * Send the ticket to the client.
   * The client connects to the WebSocket and sends the ticket.
   * The server validates the ticket, links the WebSocket to the user's session, and invalidates the ticket.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 4.4.3

Authentication over WebSockets differs from REST APIs because WebSockets are stateful, persistent connections. 

Standard web applications use cookies for session management. However, WebSockets often reside on subdomains or cross-origin environments where standard cookies are not available or are blocked by browser security policies. Furthermore, non-browser clients (like mobile apps) don't manage cookies natively.

When an application falls back to alternative session management for WebSockets, developers often make fatal errors, such as using predictable tokens, non-expiring tokens, or skipping authentication entirely. ASVS 4.4.3 requires that any dedicated WebSocket token must possess the same security guarantees as a standard HTTP session identifier (entropy, uniqueness, unpredictability, and expiration).
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
# 1. HTTP Request to get the token (Simulated Login)
POST /login HTTP/1.1
Host: localhost:5000
Content-Length: 0

# 2. Socket.IO connection payload (First WebSocket Frame containing the auth token)
40{"token":"bf0a7...[snipped]..."}
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE (Invalid Token) ---
44{"message":"Authentication required. Missing token."}
# Followed immediately by connection close.

--- VULNERABLE APPLICATION RESPONSE (No Token) ---
40{"sid":"ab123x...","upgrades":[],"pingInterval":25000,"pingTimeout":5000}
# Connection successfully established without authentication.
""")

write_file(r"tests\curl.txt", """
# Step 1: Obtain a token from the Secure server
curl -X POST http://localhost:5000/login

# Example Response:
# {"token": "a1b2c3d4e5f6g7h8i9j0..."}

# Note: Standard cURL cannot easily send the Socket.IO v4 auth payload. 
# You must use a tool like Postman or wscat, establishing the WS and manually sending:
# 40{"token":"a1b2c3d4e5f6g7h8i9j0..."}
""")

write_file(r"tests\payloads.txt", """
# Valid Socket.IO Auth Payload (Sent as the first WS frame)
40{"token":"YOUR_TOKEN_HERE"}

# Missing Token Payload
40{}

# Invalid Token Payload
40{"token":"invalid-token-12345"}
""")
