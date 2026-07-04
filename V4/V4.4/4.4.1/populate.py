import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V4\V4.4\4.4.1"

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
    <title>ASVS 4.4.1 - WSS over WS</title>
</head>
<body>
    <h1>ASVS 4.4.1: WebSocket over TLS (WSS)</h1>
    {% block content %}{% endblock %}
</body>
</html>
"""

# Write layout to both secure and vulnerable
write_file(r"secure\templates\layout.html", layout_html)
write_file(r"vulnerable\templates\layout.html", layout_html)

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure WebSocket Chat (WSS)</h2>
    <p>This application enforces TLS. It uses `wss://` for WebSocket communication.</p>
    
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

    <script>
        let ws;
        const statusIndicator = document.getElementById('statusIndicator');
        const passFailIndicator = document.getElementById('passFailIndicator');
        const logViewer = document.getElementById('logViewer');
        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        connectBtn.addEventListener('click', () => {
            const wsUrl = 'wss://' + window.location.host + '/chat';
            
            logMessage('Attempting to connect to: ' + wsUrl);
            ws = new WebSocket(wsUrl);

            ws.onopen = () => {
                statusIndicator.textContent = 'Connected (Secure)';
                statusIndicator.style.color = 'green';
                passFailIndicator.textContent = 'PASS';
                passFailIndicator.style.color = 'green';
                connectBtn.disabled = true;
                disconnectBtn.disabled = false;
                messageBox.disabled = false;
                sendBtn.disabled = false;
                logMessage('Connection established successfully over WSS.');
            };

            ws.onmessage = (event) => {
                logMessage('Server: ' + event.data);
            };

            ws.onclose = () => {
                statusIndicator.textContent = 'Disconnected';
                statusIndicator.style.color = 'black';
                connectBtn.disabled = false;
                disconnectBtn.disabled = true;
                messageBox.disabled = true;
                sendBtn.disabled = true;
                logMessage('Connection closed.');
            };

            ws.onerror = (error) => {
                logMessage('WebSocket Error. Ensure you are accessing the site via HTTPS.');
                statusIndicator.textContent = 'Error';
                statusIndicator.style.color = 'red';
                passFailIndicator.textContent = 'FAIL';
                passFailIndicator.style.color = 'red';
            };
        });

        disconnectBtn.addEventListener('click', () => {
            if (ws) ws.close();
        });

        sendBtn.addEventListener('click', () => {
            const msg = messageBox.value;
            if (msg && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(msg);
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
    <h2>Vulnerable WebSocket Chat (WS)</h2>
    <p>This application does not enforce TLS. It uses insecure `ws://` for WebSocket communication.</p>
    
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

    <script>
        let ws;
        const statusIndicator = document.getElementById('statusIndicator');
        const passFailIndicator = document.getElementById('passFailIndicator');
        const logViewer = document.getElementById('logViewer');
        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const messageBox = document.getElementById('messageBox');
        const sendBtn = document.getElementById('sendBtn');

        function logMessage(msg) {
            logViewer.textContent += msg + '\\n';
            logViewer.scrollTop = logViewer.scrollHeight;
        }

        connectBtn.addEventListener('click', () => {
            const wsUrl = 'ws://' + window.location.host + '/chat';
            
            logMessage('Attempting to connect to: ' + wsUrl);
            ws = new WebSocket(wsUrl);

            ws.onopen = () => {
                statusIndicator.textContent = 'Connected (Insecure)';
                statusIndicator.style.color = 'orange';
                passFailIndicator.textContent = 'FAIL (Using WS)';
                passFailIndicator.style.color = 'red';
                connectBtn.disabled = true;
                disconnectBtn.disabled = false;
                messageBox.disabled = false;
                sendBtn.disabled = false;
                logMessage('Connection established over plain WS. Traffic is unencrypted!');
            };

            ws.onmessage = (event) => {
                logMessage('Server: ' + event.data);
            };

            ws.onclose = () => {
                statusIndicator.textContent = 'Disconnected';
                statusIndicator.style.color = 'black';
                connectBtn.disabled = false;
                disconnectBtn.disabled = true;
                messageBox.disabled = true;
                sendBtn.disabled = true;
                logMessage('Connection closed.');
            };

            ws.onerror = (error) => {
                logMessage('WebSocket Error.');
            };
        });

        disconnectBtn.addEventListener('click', () => {
            if (ws) ws.close();
        });

        sendBtn.addEventListener('click', () => {
            const msg = messageBox.value;
            if (msg && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(msg);
                logMessage('You: ' + msg);
                messageBox.value = '';
            }
        });
    </script>
{% endblock %}
""")

# Static files if needed, per-app
write_file(r"secure\static\css\style.css", "")
write_file(r"secure\static\js\app.js", "")
write_file(r"vulnerable\static\css\style.css", "")
write_file(r"vulnerable\static\js\app.js", "")

# --- SECURE APP ---
write_file(r"secure\app.py", """
from flask import Flask, render_template, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/chat')
def chat(ws):
    if not request.is_secure:
        ws.send("ERROR: Connection rejected. WSS is required.")
        ws.close()
        return

    ws.send("Welcome to the Secure Chat! Your connection is encrypted (WSS).")
    while True:
        data = ws.receive()
        if data is None:
            break
        ws.send(f"Secure Echo: {data}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
""")

write_file(r"secure\requirements.txt", """
Flask==2.3.2
flask-sock==0.6.0
pyOpenSSL==23.2.0
cryptography==41.0.3
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
  secure-wss-441:
    build: .
    ports:
      - "5000:5000"
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/chat')
def chat(ws):
    ws.send("Welcome to the Vulnerable Chat! Your connection is NOT encrypted.")
    while True:
        data = ws.receive()
        if data is None:
            break
        ws.send(f"Insecure Echo: {data}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"vulnerable\requirements.txt", """
Flask==2.3.2
flask-sock==0.6.0
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
  vulnerable-ws-441:
    build: .
    ports:
      - "5000:5000"
""")
