import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V4\V4.4\4.4.2"

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
    <title>ASVS 4.4.2 - CSWSH & Origin Validation</title>
</head>
<body>
    <h1>ASVS 4.4.2: WebSocket Origin Validation</h1>
    {% block content %}{% endblock %}
    <!-- Include Socket.IO client library -->
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
    <p>This server strictly validates the <code>Origin</code> header during the initial HTTP handshake.</p>
    <p>Only <code>http://localhost:5000</code> is allowed.</p>
    
    <div>
        <label for="serverUrl">Server URL:</label>
        <input type="text" id="serverUrl" value="http://localhost:5000" disabled>
    </div>
    <br>
    <div>
        <button id="connectBtn">Connect</button>
        <button id="disconnectBtn" disabled>Disconnect</button>
    </div>
    <br>
    <div>
        <input type="text" id="messageBox" placeholder="Type a message..." disabled>
        <button id="sendBtn" disabled>Send</button>
    </div>
    <br>
    <div>
        <strong>Connection Status:</strong> <span id="statusIndicator">Disconnected</span>
        | <strong>PASS / FAIL:</strong> <span id="passFailIndicator">N/A</span>
    </div>
    
    <h3>Message Log:</h3>
    <pre id="logViewer" style="border:1px solid #ccc; padding:10px; height:200px; overflow-y:scroll;"></pre>

    <p><em>Note: Browsers automatically set the Origin header. You cannot modify it via JavaScript. To test Cross-Site WebSocket Hijacking (CSWSH), use Burp Suite to intercept the handshake and modify the <code>Origin</code> header to <code>http://evil.com</code>.</em></p>

    <script>
        let socket;
        const statusIndicator = document.getElementById('statusIndicator');
        const passFailIndicator = document.getElementById('passFailIndicator');
        const logViewer = document.getElementById('logViewer');
        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');
        const serverUrl = document.getElementById('serverUrl').value;

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        connectBtn.addEventListener('click', () => {
            logMessage('Connecting to ' + serverUrl + '...');
            socket = io(serverUrl);

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
                statusIndicator.textContent = 'Connection Error (Handshake rejected?)';
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
    <p>This server does NOT validate the <code>Origin</code> header during the handshake. It accepts connections from anywhere (<code>*</code>).</p>
    
    <div>
        <label for="serverUrl">Server URL:</label>
        <input type="text" id="serverUrl" value="http://localhost:5000" disabled>
    </div>
    <br>
    <div>
        <button id="connectBtn">Connect</button>
        <button id="disconnectBtn" disabled>Disconnect</button>
    </div>
    <br>
    <div>
        <input type="text" id="messageBox" placeholder="Type a message..." disabled>
        <button id="sendBtn" disabled>Send</button>
    </div>
    <br>
    <div>
        <strong>Connection Status:</strong> <span id="statusIndicator">Disconnected</span>
        | <strong>PASS / FAIL:</strong> <span id="passFailIndicator">N/A</span>
    </div>
    
    <h3>Message Log:</h3>
    <pre id="logViewer" style="border:1px solid #ccc; padding:10px; height:200px; overflow-y:scroll;"></pre>

    <p><em>Note: Browsers automatically set the Origin header. To test this vulnerability, intercept the handshake in Burp Suite and change the <code>Origin</code> header to <code>http://evil.com</code>. The server will incorrectly allow the connection.</em></p>

    <script>
        let socket;
        const statusIndicator = document.getElementById('statusIndicator');
        const passFailIndicator = document.getElementById('passFailIndicator');
        const logViewer = document.getElementById('logViewer');
        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');
        const serverUrl = document.getElementById('serverUrl').value;

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        connectBtn.addEventListener('click', () => {
            logMessage('Connecting to ' + serverUrl + '...');
            socket = io(serverUrl);

            socket.on('connect', () => {
                statusIndicator.textContent = 'Connected (Vulnerable)';
                statusIndicator.style.color = 'orange';
                passFailIndicator.textContent = 'FAIL (Allowed any origin)';
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
  secure-origin-442:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 4.4.2

This application strictly validates the `Origin` header during the initial WebSocket HTTP handshake.

## Security Control
By defining `cors_allowed_origins`, the server will only accept WebSocket upgrades if the request comes from an explicitly trusted site (e.g., `http://localhost:5000`). If a malicious site (`http://evil.com`) attempts to open a WebSocket connection to this server using the victim's browser, the server will reject the handshake, preventing Cross-Site WebSocket Hijacking (CSWSH).
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
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
  vulnerable-origin-442:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 4.4.2

This application fails to validate the `Origin` header during the initial WebSocket HTTP handshake.

## Vulnerability
By setting `cors_allowed_origins="*"` (or neglecting to check the origin entirely in native WebSocket implementations), the server accepts connections from any website. If a victim visits `http://evil.com`, the malicious site can establish a WebSocket connection to `http://localhost:5000` using the victim's browser. Because cookies (like session tokens) are automatically sent with the WebSocket handshake, the malicious site can interact with the server in the context of the authenticated user.
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 4.4.2 (CSWSH)

Cross-Site WebSocket Hijacking (CSWSH) is the WebSocket equivalent of Cross-Site Request Forgery (CSRF).

## Mechanism
When a browser opens a WebSocket connection, it performs an initial HTTP GET request with an `Upgrade: websocket` header. Crucially, the browser automatically attaches any cookies associated with the target domain (e.g., session cookies) and automatically sets the `Origin` header to the site hosting the JavaScript that initiated the connection.

## Exploitation
1. A victim logs into the vulnerable application (e.g., a banking site with a live WebSocket feed).
2. The victim is lured to `http://evil.com`.
3. `evil.com` executes JavaScript: `new WebSocket('ws://bank.com/feed')`.
4. The victim's browser sends the request to `bank.com`, attaching the victim's banking session cookies. The browser also sets `Origin: http://evil.com`.
5. If `bank.com` does not validate the `Origin` header, it accepts the connection.
6. The attacker on `evil.com` now has a persistent, two-way communication channel with the bank server, authenticated as the victim, allowing them to read sensitive data or execute actions.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

Since modern browsers do not allow JavaScript to spoof or modify the `Origin` header, you must use an intercepting proxy like Burp Suite to test for CSWSH vulnerabilities.

## Testing Steps
1. Open your browser and navigate to the target WebSocket application.
2. In Burp Suite, ensure Intercept is turned ON.
3. Click the "Connect" button in the application to initiate the WebSocket handshake.
4. In Burp Suite, locate the intercepted `GET` request containing `Upgrade: websocket`.
5. Find the `Origin` header (e.g., `Origin: http://localhost:5000`).
6. Change it to a malicious origin: `Origin: http://evil.com`.
7. Forward the request.

## Evaluating Results
* **PASS (Secure App):** The server returns an HTTP 400 Bad Request (or similar error) and the WebSocket connection fails. The server successfully validated the Origin.
* **FAIL (Vulnerable App):** The server returns an HTTP 101 Switching Protocols. The connection succeeds despite the malicious Origin.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

You can use cURL to simulate the WebSocket handshake and observe the server's response to different `Origin` headers.

## Secure Implementation (Expected to Fail)
```bash
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \\
-H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \\
-H "Origin: http://evil.com" http://localhost:5000/socket.io/?EIO=4&transport=websocket
```
**Result:** HTTP 400 Bad Request. (The server rejects the untrusted origin).

## Vulnerable Implementation (Expected to Succeed)
```bash
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \\
-H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \\
-H "Origin: http://evil.com" http://localhost:5000/socket.io/?EIO=4&transport=websocket
```
**Result:** HTTP 101 Switching Protocols. (The server accepts the untrusted origin).
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* The server maintains an explicit list of trusted Origins (e.g., the domains where the frontend is hosted).
* During the HTTP handshake, the server compares the incoming `Origin` header against the allowlist.
* Untrusted origins receive an HTTP 400 (Bad Request) or 403 (Forbidden).
* The WebSocket connection is never established.

## Vulnerable Implementation
* The server ignores the `Origin` header.
* It blindly upgrades the connection to a WebSocket for any requester.
* A malicious domain can successfully bind a socket using the victim's session cookies.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* `Flask-SocketIO` manages CORS and Origin validation natively via the `cors_allowed_origins` parameter. Setting this to a specific list completely mitigates CSWSH.
* If you are writing a raw WebSocket server using `websockets` or `flask-sock`, you must manually extract the `Origin` header from the handshake request and validate it before accepting the socket.
* **Important:** CSWSH only affects WebSocket endpoints that rely on ambient credentials (like cookies or HTTP Basic Auth) for authentication. If the endpoint requires a token to be sent inside the WebSocket payload (e.g., a Bearer token in the first frame), the impact of CSWSH is neutralized because the attacker on `evil.com` cannot access the token to send it. However, ASVS still mandates Origin validation as a defense-in-depth measure.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To prevent Cross-Site WebSocket Hijacking (ASVS 4.4.2):

1. **Implement Origin Validation:** Always verify the `Origin` header during the HTTP Upgrade request.
2. **Use an Allowlist:** Never use wildcards (`*`) or regexes that can be bypassed (e.g., allowing `*example.com` which an attacker can bypass by registering `badexample.com`). Specify exact, trusted URLs.
3. **Framework Configuration:** Use built-in framework protections.
   * **Socket.IO (Python):** `SocketIO(app, cors_allowed_origins=["https://trusted.com"])`
   * **ws (Node.js):** Use the `verifyClient` callback to check `info.origin`.
4. **Token-Based Authentication:** As an additional defense, avoid relying solely on cookies. Require the client to send a unique session token or CSRF token over the WebSocket channel immediately after the connection is established.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 4.4.2

The Same-Origin Policy (SOP) is the fundamental security mechanism of the web, preventing one website from reading data from another. However, the WebSocket protocol (RFC 6455) was explicitly designed to allow cross-origin communication.

Because WebSockets bypass the SOP, the responsibility for securing them falls entirely on the server. When a browser initiates a WebSocket connection, it sends an HTTP request to upgrade the connection. It automatically includes:
1. The user's Cookies.
2. The `Origin` header (indicating where the script is hosted).

If a server does not check the `Origin` header, it assumes the request is legitimate. Because the cookies were sent, the connection is authenticated. This creates a severe vulnerability where an attacker can commandeer the user's session over a WebSocket, bypassing standard CSRF defenses.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
GET /socket.io/?EIO=4&transport=websocket HTTP/1.1
Host: localhost:5000
Connection: Upgrade
Upgrade: websocket
Origin: http://evil.com
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE ---
HTTP/1.1 400 BAD REQUEST
Content-Type: text/plain
Content-Length: 43

The client is using an unsupported protocol.

--- VULNERABLE APPLICATION RESPONSE ---
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
""")

write_file(r"tests\curl.txt", """
# Simulate CSWSH by spoofing the Origin header

# Secure server will reject the request:
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Origin: http://evil.com" http://localhost:5000/socket.io/?EIO=4&transport=websocket

# Vulnerable server will accept the request:
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Origin: http://evil.com" http://localhost:5000/socket.io/?EIO=4&transport=websocket
""")

write_file(r"tests\payloads.txt", """
# Header manipulation payload
Origin: http://evil.com
Origin: null
Origin: http://localhost.evil.com
""")
