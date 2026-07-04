import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V4\V4.2\4.2.5"

def write_file(rel_path, content):
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Written {rel_path}")

# --- HTML/CSS/JS ---
write_file(r"templates\layout.html", """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASVS 4.2.5 - HTTP Message Structure Validation</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1>ASVS 4.2.5 Lab: HTTP Message Structure Validation</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
""")

write_file(r"templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
<div class="container">
    <h2>Make an Outbound Request</h2>
    <p>This lab demonstrates the necessity of validating outbound request parameters to prevent downstream denial-of-service or errors.</p>
    
    <form id="requestForm" method="POST" action="/">
        <div class="form-group">
            <label for="uri">Target URI (Downstream path):</label>
            <input type="text" id="uri" name="uri" placeholder="/api/v1/resource" required value="/api/v1/resource">
        </div>
        <div class="form-group">
            <label for="cookie">Cookie Header:</label>
            <input type="text" id="cookie" name="cookie" placeholder="session=123456" value="session=123456">
        </div>
        <div class="form-group">
            <label for="auth">Authorization Header:</label>
            <input type="text" id="auth" name="auth" placeholder="Bearer token123" value="Bearer token123">
        </div>
        <div class="form-group">
            <label for="custom_header">Custom Header (X-Custom-Data):</label>
            <input type="text" id="custom_header" name="custom_header" placeholder="custom_data" value="custom_data">
        </div>
        <button type="submit">Send Request</button>
    </form>

    {% if result %}
    <div class="result {% if result.status == 'PASS' %}pass{% else %}fail{% endif %}">
        <h3>Result: {{ result.status }} (HTTP {{ result.http_status }})</h3>
        {% if result.errors %}
            <ul>
            {% for error in result.errors %}
                <li>{{ error }}</li>
            {% endfor %}
            </ul>
        {% endif %}
        {% if result.message %}
            <p>{{ result.message }}</p>
        {% endif %}
        {% if result.downstream_response %}
            <p><strong>Downstream response:</strong> {{ result.downstream_response }}</p>
        {% endif %}
    </div>
    {% endif %}
</div>
{% endblock %}
""")

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
<div class="container">
    <h2>Make an Outbound Request (Secure)</h2>
    <p>This secure application validates the size of URI and headers before transmitting them to a downstream service.</p>
    
    <form id="requestForm" method="POST" action="/">
        <div class="form-group">
            <label for="uri">Target URI (Downstream path):</label>
            <input type="text" id="uri" name="uri" placeholder="/api/v1/resource" required value="/api/v1/resource">
        </div>
        <div class="form-group">
            <label for="cookie">Cookie Header:</label>
            <input type="text" id="cookie" name="cookie" placeholder="session=123456" value="session=123456">
        </div>
        <div class="form-group">
            <label for="auth">Authorization Header:</label>
            <input type="text" id="auth" name="auth" placeholder="Bearer token123" value="Bearer token123">
        </div>
        <div class="form-group">
            <label for="custom_header">Custom Header (X-Custom-Data):</label>
            <input type="text" id="custom_header" name="custom_header" placeholder="custom_data" value="custom_data">
        </div>
        <button type="submit">Send Request</button>
    </form>

    {% if result %}
    <div class="result {% if result.status == 'PASS' %}pass{% else %}fail{% endif %}">
        <h3>Result: {{ result.status }} (HTTP {{ result.http_status }})</h3>
        {% if result.errors %}
            <ul>
            {% for error in result.errors %}
                <li>{{ error }}</li>
            {% endfor %}
            </ul>
        {% endif %}
        {% if result.message %}
            <p>{{ result.message }}</p>
        {% endif %}
        {% if result.downstream_response %}
            <p><strong>Downstream Response:</strong> {{ result.downstream_response }}</p>
        {% endif %}
    </div>
    {% endif %}
</div>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
<div class="container">
    <h2>Make an Outbound Request (Vulnerable)</h2>
    <p>This vulnerable application does not validate the size of URI and headers before transmitting them. It's susceptible to downstream failures.</p>
    
    <form id="requestForm" method="POST" action="/">
        <div class="form-group">
            <label for="uri">Target URI (Downstream path):</label>
            <input type="text" id="uri" name="uri" placeholder="/api/v1/resource" required value="/api/v1/resource">
        </div>
        <div class="form-group">
            <label for="cookie">Cookie Header:</label>
            <input type="text" id="cookie" name="cookie" placeholder="session=123456" value="session=123456">
        </div>
        <div class="form-group">
            <label for="auth">Authorization Header:</label>
            <input type="text" id="auth" name="auth" placeholder="Bearer token123" value="Bearer token123">
        </div>
        <div class="form-group">
            <label for="custom_header">Custom Header (X-Custom-Data):</label>
            <input type="text" id="custom_header" name="custom_header" placeholder="custom_data" value="custom_data">
        </div>
        <button type="submit">Send Request</button>
    </form>

    {% if result %}
    <div class="result {% if result.status == 'PASS' %}pass{% else %}fail{% endif %}">
        <h3>Result: {{ result.status }} (HTTP {{ result.http_status }})</h3>
        {% if result.message %}
            <p>{{ result.message }}</p>
        {% endif %}
        {% if result.downstream_response %}
            <p><strong>Downstream Response:</strong> {{ result.downstream_response }}</p>
        {% endif %}
    </div>
    {% endif %}
</div>
{% endblock %}
""")


write_file(r"static\css\style.css", """
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f9;
}
header {
    background-color: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
}
.container {
    max-width: 600px;
    margin: 2rem auto;
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.form-group {
    margin-bottom: 1rem;
}
label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
}
input[type="text"] {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}
button {
    background-color: #007bff;
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
button:hover {
    background-color: #0056b3;
}
.result {
    margin-top: 1.5rem;
    padding: 1rem;
    border-radius: 4px;
}
.pass {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
.fail {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}
""")

write_file(r"static\js\app.js", """
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('requestForm');
    if (form) {
        form.addEventListener('submit', () => {
            console.log('Form submitted');
        });
    }
});
""")

# --- SECURE APP ---
write_file(r"secure\app.py", """
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='../static')

MAX_URI_LENGTH = 128
MAX_COOKIE_LENGTH = 256
MAX_AUTH_LENGTH = 256
MAX_CUSTOM_HEADER_LENGTH = 128

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        uri = request.form.get('uri', '')
        cookie = request.form.get('cookie', '')
        auth = request.form.get('auth', '')
        custom_header = request.form.get('custom_header', '')

        errors = []
        if len(uri.encode('utf-8')) > MAX_URI_LENGTH:
            errors.append(f'URI length exceeds maximum allowed ({MAX_URI_LENGTH} bytes).')
        if len(cookie.encode('utf-8')) > MAX_COOKIE_LENGTH:
            errors.append(f'Cookie header length exceeds maximum allowed ({MAX_COOKIE_LENGTH} bytes).')
        if len(auth.encode('utf-8')) > MAX_AUTH_LENGTH:
            errors.append(f'Authorization header length exceeds maximum allowed ({MAX_AUTH_LENGTH} bytes).')
        if len(custom_header.encode('utf-8')) > MAX_CUSTOM_HEADER_LENGTH:
            errors.append(f'Custom header length exceeds maximum allowed ({MAX_CUSTOM_HEADER_LENGTH} bytes).')

        if errors:
            result = {'status': 'FAIL', 'errors': errors, 'http_status': 400}
        else:
            try:
                headers = {}
                if cookie: headers['Cookie'] = cookie
                if auth: headers['Authorization'] = auth
                if custom_header: headers['X-Custom-Data'] = custom_header
                
                # Mock downstream endpoint call
                downstream_url = f"http://localhost:5000/mock_downstream{uri}"
                resp = requests.get(downstream_url, headers=headers, timeout=2)
                result = {
                    'status': 'PASS', 
                    'message': 'Request validated and sent successfully.', 
                    'http_status': 200,
                    'downstream_response': resp.text
                }
            except requests.exceptions.RequestException as e:
                result = {'status': 'FAIL', 'errors': [f"Downstream request failed: {str(e)}"], 'http_status': 500}

    return render_template('index.html', result=result)

@app.route('/mock_downstream/<path:subpath>')
def mock_downstream(subpath):
    # This endpoint simulates a downstream service that would crash on huge headers or URIs
    # In reality, a web server (like nginx/apache or gunicorn) has built-in limits and returns 414 or 431.
    return jsonify({"success": True, "received_path": subpath})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"secure\requirements.txt", """
Flask==2.3.2
Werkzeug==2.3.6
requests==2.31.0
""")

write_file(r"secure\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Copy static files appropriately
COPY ../static /static
COPY ../templates /templates
CMD ["python", "app.py"]
""")

write_file(r"secure\docker-compose.yml", """
version: '3.8'
services:
  secure-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
""")

write_file(r"secure\.env", """
FLASK_APP=app.py
FLASK_ENV=development
""")

write_file(r"secure\README.md", """
# Secure Implementation - ASVS 4.2.5

This application demonstrates the secure way to handle outbound HTTP requests.

## How it works

The application validates the length of the URI and various HTTP headers (Cookie, Authorization, Custom Headers) before constructing and sending the request to the downstream component. If any part of the request exceeds the predefined limits, it rejects the request early and returns an error message to the user. This prevents potential denial of service (DoS) attacks on downstream microservices or internal components that might allocate significant resources to parse giant requests or crash entirely.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='../static')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        uri = request.form.get('uri', '')
        cookie = request.form.get('cookie', '')
        auth = request.form.get('auth', '')
        custom_header = request.form.get('custom_header', '')

        # VULNERABILITY: No length validation on URI or headers
        try:
            headers = {}
            if cookie: headers['Cookie'] = cookie
            if auth: headers['Authorization'] = auth
            if custom_header: headers['X-Custom-Data'] = custom_header
            
            # The vulnerable app directly proxies whatever the user provided
            downstream_url = f"http://localhost:5000/mock_downstream{uri}"
            
            # In a real scenario, this could hit internal components causing memory exhaustion or timeouts
            resp = requests.get(downstream_url, headers=headers, timeout=2)
            
            result = {
                'status': 'PASS', 
                'message': 'Request sent downstream successfully.', 
                'http_status': 200,
                'downstream_response': resp.text
            }
        except requests.exceptions.RequestException as e:
            # We catch it here to show that the downstream component threw an error or timed out
            # when dealing with oversized requests.
            result = {
                'status': 'FAIL', 
                'message': f"Downstream request failed: {str(e)}", 
                'http_status': 500
            }

    return render_template('index.html', result=result)

@app.route('/mock_downstream/<path:subpath>')
def mock_downstream(subpath):
    # Werkzeug built-in server will likely drop or error out natively if URI/headers are too huge,
    # mimicking a downstream DoS or rejection (e.g. 431 Request Header Fields Too Large or 414 URI Too Long).
    return jsonify({"success": True, "received_path": subpath})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"vulnerable\requirements.txt", """
Flask==2.3.2
Werkzeug==2.3.6
requests==2.31.0
""")

write_file(r"vulnerable\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Copy static files appropriately
COPY ../static /static
COPY ../templates /templates
CMD ["python", "app.py"]
""")

write_file(r"vulnerable\docker-compose.yml", """
version: '3.8'
services:
  vulnerable-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
""")

write_file(r"vulnerable\.env", """
FLASK_APP=app.py
FLASK_ENV=development
""")

write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 4.2.5

This application demonstrates the vulnerable way to handle outbound HTTP requests.

## How it works

The application takes user input for the URI and various HTTP headers and directly embeds them into an outbound HTTP request using the `requests` library. It performs no length validation on these parameters. 

This is a security risk because an attacker can provide massive inputs (e.g., a 10MB authorization header), which the vulnerable server will happily allocate memory for, serialize, and transmit to the downstream service. This can lead to exhaustion of resources on the current server, the network link, or the downstream server, causing a denial of service.
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 4.2.5

When applications dynamically construct outbound requests (such as server-side requests to internal APIs or microservices) based on user input, attackers can exploit this behavior if no length validation is enforced.

## Mechanism

If an attacker supplies excessively large inputs (e.g., hundreds of megabytes) into fields that are subsequently used as URI paths or HTTP headers (Cookie, Authorization, etc.), the application may:
1. Allocate excessive memory to hold the string.
2. Send the bloated request over the network, consuming bandwidth.
3. Overwhelm the downstream service, which might crash, hang, or return errors when trying to parse an unusually large HTTP header or URI.

This chain of events can cause Denial of Service (DoS) across multiple layers of the application infrastructure.

## Impact

* **Memory Exhaustion:** Both the frontend/backend creating the request and the downstream component receiving it might run out of memory.
* **Network Congestion:** Massive requests can tie up network connections.
* **Component Failures:** Web servers like NGINX or Apache have default limits for headers and URIs (e.g., `large_client_header_buffers`). Exceeding these causes HTTP 414 (URI Too Long) or 431 (Request Header Fields Too Large) errors, effectively breaking the downstream process.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

You can use Burp Suite's Repeater or Intruder tools to test whether an application correctly limits the size of generated URIs and HTTP headers.

## Steps

1. **Capture the Request:** Intercept the form submission where you provide the target URI, Cookie, or Authorization header using Burp Suite Proxy.
2. **Send to Repeater:** Right-click the intercepted request and select "Send to Repeater".
3. **Generate a Payload:**
   * In the Repeater tab, find the parameter (e.g., `auth=Bearer+token123`).
   * Modify the value to an excessively long string (e.g., 50,000 characters of `A`). You can use Burp Suite's payload generator or simply paste a large block of text.
4. **Send the Request:**
   * In the **Secure Application**, you should receive a clean HTTP 400 Bad Request or an application-level failure message indicating the input exceeded maximum length limits. The request is never forwarded downstream.
   * In the **Vulnerable Application**, the server will attempt to process the request. It might take a long time, and you might receive an HTTP 500 error because the downstream component crashed, timed out, or returned a 414/431 error.

By generating oversized inputs, you can verify if the intermediate application is properly guarding its outbound requests.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

You can use `curl` to quickly test the application's handling of oversized inputs from the command line.

## Procedure

You can use Python or `printf` to generate a massively long string and pass it to `curl` as form data.

### Testing the Secure Application

```bash
# Generate a 10,000 character 'A' payload for the Authorization header
PAYLOAD=$(python3 -c "print('A' * 10000)")

curl -X POST http://localhost:5000/ \\
     -d "uri=/api/data" \\
     -d "cookie=session=123" \\
     -d "auth=$PAYLOAD" \\
     -d "custom_header=test"
```
**Expected Result:** The application should respond immediately with a validation error (e.g., "Authorization header length exceeds maximum allowed").

### Testing the Vulnerable Application

Using the same payload against the vulnerable endpoint:
```bash
curl -X POST http://localhost:5000/ \\
     -d "uri=/api/data" \\
     -d "cookie=session=123" \\
     -d "auth=$PAYLOAD" \\
     -d "custom_header=test"
```
**Expected Result:** The vulnerable application will attempt to send this 10,000-character header to the downstream service. The downstream service will likely reject it, causing a 500 Internal Server Error in the vulnerable app due to the downstream failure (e.g., connection reset or HTTP 431).
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* **Validation:** Before constructing the outbound HTTP request, the length of the URI, Cookie, Authorization, and custom headers must be checked against strict maximum length limits.
* **Rejection:** If any limit is exceeded, the application must immediately return a descriptive error to the client (e.g., HTTP 400) without ever attempting to contact the downstream service.
* **Safe Forwarding:** Only requests within acceptable bounds are transmitted.

## Vulnerable Implementation
* **No Validation:** The application blindly takes user-provided strings and embeds them into outbound requests.
* **Downstream Errors:** Oversized payloads will reach the downstream target, triggering timeouts, 414 URI Too Long, or 431 Request Header Fields Too Large errors.
* **Resource Waste:** The vulnerable server wastes CPU, memory, and network resources dealing with arbitrarily large payloads.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* The secure application enforces limits using Python's `len(string.encode('utf-8'))` to accurately measure byte length, not just character length. This prevents bypasses using multi-byte characters.
* Real-world applications should define these limits based on the actual capacities of downstream components (e.g., AWS API Gateway limits, NGINX `large_client_header_buffers`, etc.).
* It is highly recommended to combine size limits with proper character sanitization (e.g., rejecting newline characters in headers to prevent HTTP Request Smuggling or Header Injection). While this lab focuses on length (4.2.5), sanitization is equally critical.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To fix the vulnerable application and adhere to ASVS 4.2.5, follow these steps:

1. **Identify Outbound Requests:** Locate where your application acts as an HTTP client (e.g., using `requests.get()`, `urllib`, `axios`, etc.).
2. **Define Limits:** Establish safe maximum lengths for variables that will be inserted into the URI or headers. 
   * URIs: Typically < 2048 bytes.
   * Standard Headers (Cookie/Auth): Typically < 4096 or 8192 bytes.
   * Custom Headers: Should be as small as possible based on business requirements.
3. **Implement Validation:** Before invoking the HTTP client, assert that the byte length of the user-supplied strings does not exceed the defined limits.
4. **Reject Early:** Return an error (like HTTP 400) if validation fails. Do not proceed to allocate the HTTP request objects.

Example in Python:
```python
MAX_URI_LEN = 2048
if len(user_uri.encode('utf-8')) > MAX_URI_LEN:
    raise ValidationError("URI too long")
```
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 4.2.5

The Open Worldwide Application Security Project (OWASP) Application Security Verification Standard (ASVS) Control 4.2.5 requires that applications restrict the size of generated URIs and HTTP headers when acting as an HTTP client.

## Why is this important?

When a web application interfaces with internal APIs or microservices, it acts as a client. If an attacker can control parts of the outgoing request—such as the path, query parameters, or specific headers (like Authorization tokens or custom correlation IDs)—they can inject massively oversized strings.

Web servers, proxies, and application frameworks have finite buffers for processing incoming HTTP requests. Common errors include:
* **HTTP 414 URI Too Long**
* **HTTP 431 Request Header Fields Too Large**

If the intermediate application does not enforce its own limits, an attacker can force the application to repeatedly generate enormous requests. This ties up thread pools, consumes memory, saturates network links, and causes denial of service in both the source application and the downstream infrastructure. Proper input validation and length restriction at the boundaries prevent these attacks.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
POST / HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded
Content-Length: 10078

uri=/api/v1/resource&cookie=session=123456&auth=Bearer+<INSERT_10000_A_CHARACTERS_HERE>&custom_header=custom_data
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE ---
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

...
<div class="result fail">
    <h3>Result: FAIL (HTTP 400)</h3>
    <ul>
        <li>Authorization header length exceeds maximum allowed (256 bytes).</li>
    </ul>
</div>
...

--- VULNERABLE APPLICATION RESPONSE ---
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

...
<div class="result fail">
    <h3>Result: FAIL (HTTP 500)</h3>
    <p>Downstream request failed: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))</p>
</div>
...
""")

write_file(r"tests\curl.txt", """
# Test 1: Secure App - Normal Request
curl -X POST http://localhost:5000/ \\
  -d "uri=/valid" \\
  -d "cookie=session=123" \\
  -d "auth=Bearer valid"

# Test 2: Secure App - Oversized Header
PAYLOAD=$(python3 -c "print('A' * 5000)")
curl -X POST http://localhost:5000/ \\
  -d "uri=/valid" \\
  -d "cookie=session=123" \\
  -d "auth=$PAYLOAD"

# Test 3: Vulnerable App - Normal Request
curl -X POST http://localhost:5000/ \\
  -d "uri=/valid" \\
  -d "cookie=session=123" \\
  -d "auth=Bearer valid"

# Test 4: Vulnerable App - Oversized URI
PAYLOAD_URI=$(python3 -c "print('/api/' + 'A' * 10000)")
curl -X POST http://localhost:5000/ \\
  -d "uri=$PAYLOAD_URI"
""")

write_file(r"tests\payloads.txt", """
# Payload for excessive URI length (10,000 bytes)
/api/v1/resource?data=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA... (repeat 10,000 times)

# Payload for excessive Authorization header
Bearer AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA... (repeat 10,000 times)

# Payload for excessive Cookie header
session=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA... (repeat 10,000 times)

# Payload for excessive custom header
X-Custom-Data: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA... (repeat 10,000 times)
""")

