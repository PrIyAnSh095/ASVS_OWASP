import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V4\V4.4\4.4.4"

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
    <title>ASVS 4.4.4 - Transitioning HTTPS Session to WebSocket</title>
</head>
<body>
    <h1>ASVS 4.4.4: WebSocket Session Transition</h1>
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
    <h2>Secure WebSocket Implementation</h2>
    <p>This implementation requires you to establish an authenticated HTTP session first, which is then used to securely obtain a dedicated WebSocket token.</p>
    
    <div style="border:1px solid #000; padding:10px; margin-bottom:10px;">
        <h3>1. HTTPS Authentication (Session Establishment)</h3>
        <input type="text" id="username" placeholder="Username" value="admin">
        <input type="password" id="password" placeholder="Password" value="password">
        <button id="loginBtn">Login (Set HTTP Cookie)</button>
        <br>
        <span id="loginStatus" style="font-weight:bold;">Not Logged In</span>
    </div>

    <div style="border:1px solid #000; padding:10px; margin-bottom:10px;">
        <h3>2. Get WebSocket Token (Uses HTTP Session)</h3>
        <button id="getTokenBtn" disabled>Get WS Token</button>
        <br>
        Issued Token: <input type="text" id="tokenInput" placeholder="Requires successful login" disabled style="width: 300px;">
    </div>

    <div style="border:1px solid #000; padding:10px;">
        <h3>3. WebSocket Connection (Transition)</h3>
        <button id="connectBtn" disabled>Connect to WebSocket</button>
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
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        
        const loginBtn = document.getElementById('loginBtn');
        const loginStatus = document.getElementById('loginStatus');
        
        const getTokenBtn = document.getElementById('getTokenBtn');
        const tokenInput = document.getElementById('tokenInput');

        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        loginBtn.addEventListener('click', async () => {
            const formData = new FormData();
            formData.append('username', usernameInput.value);
            formData.append('password', passwordInput.value);

            const res = await fetch('/login', { method: 'POST', body: formData });
            const data = await res.json();
            
            if (res.ok) {
                loginStatus.textContent = "Logged In as " + data.user;
                loginStatus.style.color = "green";
                getTokenBtn.disabled = false;
                logMessage('Login successful via HTTP POST. Session Cookie is now set.');
            } else {
                loginStatus.textContent = "Login Failed";
                loginStatus.style.color = "red";
                logMessage('Login Failed.');
            }
        });

        getTokenBtn.addEventListener('click', async () => {
            const res = await fetch('/api/ws-token');
            const data = await res.json();
            if (res.ok) {
                tokenInput.value = data.token;
                connectBtn.disabled = false;
                logMessage('Obtained WS Token securely using HTTP Session: ' + data.token);
            } else {
                logMessage('Failed to obtain token (Not authenticated?): ' + data.error);
            }
        });

        connectBtn.addEventListener('click', () => {
            const token = tokenInput.value;
            logMessage('Attempting to connect with token: ' + token);
            
            socket = io({
                auth: { token: token }
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
                logMessage('Socket.IO connection established. Token verified.');
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
    <h2>Vulnerable WebSocket Implementation</h2>
    <p>This implementation allows obtaining a token without an HTTP session, or completely ignores the token requirement to establish the WS connection.</p>
    
    <div style="border:1px solid #000; padding:10px; margin-bottom:10px;">
        <h3>1. HTTPS Authentication (Bypassed)</h3>
        <input type="text" id="username" placeholder="Username" value="admin">
        <input type="password" id="password" placeholder="Password" value="password">
        <button id="loginBtn">Login (Set HTTP Cookie)</button>
        <br>
        <span id="loginStatus" style="font-weight:bold;">Not Logged In</span>
    </div>

    <div style="border:1px solid #000; padding:10px; margin-bottom:10px;">
        <h3>2. Get WebSocket Token (No Session Checked!)</h3>
        <button id="getTokenBtn">Get WS Token (Unauthenticated)</button>
        <br>
        Issued Token: <input type="text" id="tokenInput" placeholder="Will be issued anyway" disabled style="width: 300px;">
    </div>

    <div style="border:1px solid #000; padding:10px;">
        <h3>3. WebSocket Connection (Direct Connect Possible)</h3>
        <button id="connectBtn">Connect to WebSocket Directly</button>
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
        
        const loginBtn = document.getElementById('loginBtn');
        const loginStatus = document.getElementById('loginStatus');
        
        const getTokenBtn = document.getElementById('getTokenBtn');
        const tokenInput = document.getElementById('tokenInput');

        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        loginBtn.addEventListener('click', async () => {
            const formData = new FormData();
            formData.append('username', usernameInput.value);
            formData.append('password', passwordInput.value);

            const res = await fetch('/login', { method: 'POST', body: formData });
            const data = await res.json();
            
            if (res.ok) {
                loginStatus.textContent = "Logged In as " + data.user;
                loginStatus.style.color = "green";
                logMessage('Login successful via HTTP POST. Session Cookie is now set.');
            } else {
                loginStatus.textContent = "Login Failed";
                loginStatus.style.color = "red";
                logMessage('Login Failed.');
            }
        });

        getTokenBtn.addEventListener('click', async () => {
            // VULNERABLE: Getting token without needing an HTTP session
            const res = await fetch('/api/ws-token');
            const data = await res.json();
            if (res.ok) {
                tokenInput.value = data.token;
                logMessage('Obtained WS Token WITHOUT requiring HTTP Session: ' + data.token);
            } else {
                logMessage('Failed: ' + data.error);
            }
        });

        connectBtn.addEventListener('click', () => {
            const token = tokenInput.value || "missing-token";
            logMessage('Attempting to connect with token: ' + token);
            
            socket = io({
                auth: { token: token }
            });

            socket.on('connect', () => {
                statusIndicator.textContent = 'Connected (Vulnerable)';
                statusIndicator.style.color = 'orange';
                passFailIndicator.textContent = 'FAIL (Bypassed Flow)';
                passFailIndicator.style.color = 'red';
                connectBtn.disabled = true;
                disconnectBtn.disabled = false;
                messageBox.disabled = false;
                sendBtn.disabled = false;
                logMessage('Socket.IO connection established without requiring authenticated HTTPS flow.');
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
  secure-transition-444:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 4.4.4

This application enforces a secure transition from an authenticated HTTPS session to a WebSocket channel.

## How it works
1. The user logs in via a standard `POST /login` request. The server issues a standard HTTP session cookie (e.g., `session`).
2. To open a WebSocket, the user makes an authenticated `GET /api/ws-token` request. The server verifies the HTTP session cookie and generates a single-use, short-lived cryptographic token (a "Connection Ticket").
3. The frontend initiates the WebSocket handshake, passing this specific token.
4. The WebSocket server validates the token, associates the socket with the authenticated user, and invalidates the token so it cannot be reused.
""")


# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
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
  vulnerable-transition-444:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 4.4.4

This application fails to correctly transition an authenticated HTTPS session into a WebSocket session.

## Vulnerability
The application exposes a `/api/ws-token` endpoint that issues tokens without verifying the requester's HTTP session cookies. Furthermore, the WebSocket server itself does not rigorously validate the tokens upon connection. Consequently, an attacker can completely bypass the standard HTTPS authentication flow and immediately bind a WebSocket to interact with the backend API.
""")


# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 4.4.4 (Session Transition Bypass)

When applications use WebSockets for authenticated data feeds, attackers will look for ways to connect to the WebSocket directly, bypassing the traditional HTTP login flow.

## The Disconnect Between HTTP and WebSockets
Because WebSockets operate on a different protocol layer and often sit on different infrastructure (like a separate microservice), they frequently lack access to the primary HTTP session state (e.g., memory-backed sessions or Redis session stores). 

## Exploitation
If the WebSocket endpoint fails to mandate a cryptographically secure token *that was issued exclusively to a verified HTTP session*, an attacker can:
1. Connect directly to the WebSocket URL using `wscat` or a script.
2. If tokens are required but issued indiscriminately via an unauthenticated REST endpoint (e.g., `/api/get-token`), the attacker requests a token and connects.
3. Access real-time data or dispatch commands that should have required a valid user session.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

Burp Suite can be used to test the enforcement of the session transition logic.

## Testing Steps
1. **Unauthenticated Token Generation:** Send a `GET /api/ws-token` request in Burp Suite Repeater *without* any `Cookie` headers.
   * **FAIL:** The server issues a valid token.
   * **PASS:** The server returns a `401 Unauthorized`.
2. **Unauthenticated WS Connection:** Initiate a WebSocket connection (`GET /socket.io/?...`) without an auth payload or with a forged payload.
   * **FAIL:** The server returns `101 Switching Protocols` and allows interaction.
   * **PASS:** The server returns `400 Bad Request` or immediately closes the socket with an error frame.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

You can use cURL to quickly verify if the token issuance endpoint requires an established HTTP session.

## Testing the Transition Endpoint

**Attempt without authentication:**
```bash
curl -i http://localhost:5000/api/ws-token
```
* **Secure App:** Returns `401 Unauthorized` (Must login first).
* **Vulnerable App:** Returns `200 OK` and a `{"token": "..."}`.

**Attempt with authentication (Secure App):**
```bash
# 1. Login and save the session cookie
curl -i -c cookies.txt -X POST -d "username=admin&password=password" http://localhost:5000/login

# 2. Use the cookie to get the WS token
curl -i -b cookies.txt http://localhost:5000/api/ws-token
```
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* The user cannot obtain a WebSocket token without first possessing a valid HTTP session cookie.
* The WebSocket token is linked to the user's identity.
* The WebSocket connection is refused if the token is missing, expired, or previously used.
* Only the authenticated user can successfully upgrade to a WebSocket.

## Vulnerable Implementation
* The WebSocket endpoint can be accessed directly.
* Token endpoints (if they exist) issue valid tokens to unauthenticated users.
* The application fails to tie the WebSocket connection back to a securely authenticated HTTP session.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* The pattern implemented in the Secure application is known as the **"Ticket-based Authentication"** or **"Connection Ticket"** pattern.
* It bridges the gap between REST (HTTP) authentication and WebSocket (TCP) persistence securely.
* A crucial part of this pattern is ensuring that tickets are **single-use** (deleted upon successful connection) and **short-lived** (e.g., 30 seconds), preventing attackers from stealing a ticket and reusing it later.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To satisfy ASVS 4.4.4, strictly link WebSocket access to the standard HTTP authentication flow:

1. **Protect Token Endpoints:** Ensure any endpoint issuing WebSocket tokens (like `/api/ws-token`) requires the standard HTTP session (e.g., `@login_required` or JWT validation).
2. **Issue Secure Tickets:** The token must be cryptographically random and explicitly mapped to the authenticated user on the backend.
3. **Validate on Connect:** When the WebSocket handshake occurs, intercept the token, validate it, and immediately invalidate the token so it cannot be reused.
4. **Link Identity:** Map the newly established WebSocket to the user identity found during ticket validation, so all subsequent WebSocket messages are processed in the context of that user.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 4.4.4

Modern applications often use dual architectures: an HTTP REST API for standard CRUD operations and a WebSocket server for real-time pub/sub functionality. 

Because standard HTTP session management relies heavily on cookies, transitioning that authenticated state to a separate protocol (WebSockets) requires careful engineering. Browsers often handle cross-domain cookies poorly during WebSocket upgrades, and non-browser clients (like mobile apps) don't use cookies natively.

Therefore, the most secure mechanism is to use the proven HTTP session to request a dedicated WebSocket token. This proves the client was authenticated in the HTTP realm before allowing them to transition into the WebSocket realm, maintaining a continuous chain of trust.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
# 1. Unauthenticated Token Request (Should Fail in Secure App)
GET /api/ws-token HTTP/1.1
Host: localhost:5000

# 2. Authenticated Token Request (Should Pass in Secure App)
GET /api/ws-token HTTP/1.1
Host: localhost:5000
Cookie: session=eyJ1c2VyIjoiYWRtaW4ifQ.Yxz...
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE (Unauthenticated /api/ws-token) ---
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json

{"error":"Unauthorized. Please login over HTTP first."}

--- VULNERABLE APPLICATION RESPONSE (Unauthenticated /api/ws-token) ---
HTTP/1.1 200 OK
Content-Type: application/json

{"token":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}
""")

write_file(r"tests\curl.txt", """
# Step 1: Ensure unauthenticated users are blocked
curl -s http://localhost:5000/api/ws-token

# Step 2: Login and get session cookie
curl -s -c cookies.txt -X POST -d "username=admin&password=password" http://localhost:5000/login

# Step 3: Use session cookie to get a valid, short-lived WS token
curl -s -b cookies.txt http://localhost:5000/api/ws-token
""")

write_file(r"tests\payloads.txt", """
# The payloads involve standard web authentication, focusing on the absence of the Cookie header when requesting the WS token.
""")
