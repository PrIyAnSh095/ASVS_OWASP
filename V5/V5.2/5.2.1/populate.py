import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V5\V5.2\5.2.1"

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
    <title>ASVS 5.2.1 - File Size Validation</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
        .status { padding: 5px; border: 1px solid #000; display: inline-block; }
    </style>
</head>
<body>
    <h1>ASVS 5.2.1: File Upload Size Limits</h1>
    {% block content %}{% endblock %}
</body>
</html>
"""

write_file(r"secure\templates\layout.html", layout_html)
write_file(r"vulnerable\templates\layout.html", layout_html)

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure Implementation: Strict File Size Limit</h2>
    
    <div class="box">
        <p><strong>Maximum Allowed File Size:</strong> 1 MB</p>
        <p>This server explicitly enforces a maximum content length at the transport layer. It will abort the connection immediately if the file exceeds the limit, preventing memory exhaustion.</p>
        
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload File</button>
        </form>
        
        <br>
        {% if message %}
            <div class="{% if success %}success{% else %}error{% endif %}">
                Result: {{ message }}
            </div>
            <br>
            <div class="status">
                <strong>PASS / FAIL:</strong>
                {% if success %}
                    <span style="color: green;">N/A (Normal file)</span>
                {% else %}
                    <span style="color: green;">PASS (File successfully blocked before processing)</span>
                {% endif %}
            </div>
        {% endif %}
    </div>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Vulnerable Implementation: Unbounded File Uploads</h2>
    
    <div class="box">
        <p><strong>Maximum Allowed File Size:</strong> <em>None (Unlimited)</em></p>
        <p>This server does not enforce a maximum content length. It will attempt to read any uploaded file entirely into memory, allowing an attacker to cause a Denial of Service (DoS).</p>
        
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload File</button>
        </form>
        
        <br>
        {% if message %}
            <div class="{% if success %}success{% else %}error{% endif %}">
                Result: {{ message }}
            </div>
            <br>
            <div class="status">
                <strong>PASS / FAIL:</strong>
                {% if success %}
                    <span style="color: red;">FAIL (File accepted regardless of size!)</span>
                {% else %}
                    <span style="color: red;">Error processing file</span>
                {% endif %}
            </div>
        {% endif %}
    </div>
{% endblock %}
""")

write_file(r"secure\static\css\style.css", "")
write_file(r"secure\static\js\app.js", "")
write_file(r"vulnerable\static\css\style.css", "")
write_file(r"vulnerable\static\js\app.js", "")

# --- SECURE APP ---
write_file(r"secure\app.py", """
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# SECURE IMPLEMENTATION
# We strictly enforce a maximum upload size.
# Flask/Werkzeug intercepts the Content-Length header and the data stream.
# If the stream exceeds this limit, it aborts the upload and raises a 413 error
# before the application logic ever touches the file, protecting the server from DoS.
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1 MB Limit

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', message="No file part", success=False)
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message="No selected file", success=False)
        
    if file and allowed_file(file.filename):
        # We process the file safely here, knowing it is <= 1MB
        file_bytes = file.read()
        return render_template('index.html', message=f"File {file.filename} ({len(file_bytes)} bytes) successfully processed.", success=True)
    else:
        return render_template('index.html', message="Invalid file type.", success=False)

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', message="Validation Error: File exceeds the maximum allowed size of 1 MB.", success=False), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"secure\requirements.txt", """
Flask==2.3.2
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
  secure-size-521:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 5.2.1

This application securely handles file uploads by enforcing a strict maximum file size before processing the file.

## Security Control
By configuring `MAX_CONTENT_LENGTH = 1MB` in Flask, the underlying WSGI server (Werkzeug) actively monitors the incoming HTTP stream. If a client attempts to upload a file larger than 1MB, the server immediately drops the connection and returns a `413 Request Entity Too Large` error. This guarantees that large files never consume disk space or RAM, effectively preventing Denial of Service (DoS) attacks via oversized payloads.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# VULNERABLE IMPLEMENTATION
# There is NO MAX_CONTENT_LENGTH configured.
# The server will accept files of any size, attempting to load them into memory
# or spool them to disk, allowing attackers to exhaust server resources.

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', message="No file part", success=False)
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message="No selected file", success=False)
        
    if file and allowed_file(file.filename):
        # VULNERABILITY: We read the entire file into memory indiscriminately.
        # An attacker uploading a 5GB file will cause the process to crash (OOM).
        file_bytes = file.read()
        return render_template('index.html', message=f"File {file.filename} ({len(file_bytes)} bytes) successfully loaded into memory.", success=True)
    else:
        return render_template('index.html', message="Invalid file type.", success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"vulnerable\requirements.txt", """
Flask==2.3.2
""")

write_file(r"vulnerable\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# We limit memory inside the docker container to easily demonstrate OOM DoS
CMD ["python", "app.py"]
""")

write_file(r"vulnerable\docker-compose.yml", """
version: '3.8'
services:
  vulnerable-size-521:
    build: .
    ports:
      - "5000:5000"
    deploy:
      resources:
        limits:
          memory: 200M
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 5.2.1

This application fails to restrict the maximum size of uploaded files.

## Vulnerability
Because there is no file size limit enforced at the framework or web server level, the application blindly accepts any upload payload. The code then attempts to read the entire file into memory (`file.read()`). An attacker can easily launch a Denial of Service (DoS) attack by uploading a multi-gigabyte file, which will exhaust the server's RAM and cause an Out of Memory (OOM) crash.

*Note: In `docker-compose.yml`, the memory is deliberately capped at 200MB to make the OOM crash easier to demonstrate locally.*
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 5.2.1 (Oversized Files)

Failing to restrict file upload sizes opens the server to severe Resource Exhaustion and Denial of Service (DoS) attacks.

## The Attack
1. **Memory Exhaustion (OOM):** If an application reads uploaded files directly into RAM (e.g., to parse a CSV, resize an image, or calculate a hash), an attacker uploading a 5GB file will instantly consume 5GB of the server's RAM. If the server has less RAM available, the process crashes.
2. **Disk Exhaustion:** Even if the framework safely spools large uploads to temporary disk files (like Flask does by default for large files), an attacker can script thousands of concurrent 10GB uploads, rapidly filling the server's hard drive and taking down the entire database/OS.
3. **Bandwidth Exhaustion:** Large file uploads monopolize network connections and worker threads.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

You can use Burp Suite to manipulate the `Content-Length` or send genuinely large payloads to test the server's limits.

## Testing Steps
1. Intercept a legitimate file upload request.
2. Send it to Repeater.
3. To generate a large payload without freezing Burp Suite, you can use Burp's "Paste from file" feature or use Python scripts to generate a massive text string in the request body.
4. Send the request to the server.

## Evaluating Results
* **PASS (Secure App):** The server immediately responds with `413 Request Entity Too Large` and drops the connection, refusing to process the massive body.
* **FAIL (Vulnerable App):** The server accepts the data. It may take a long time to upload, eventually returning a `500 Internal Server Error` as the server runs out of memory, or returning a success message after processing the massive file.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

cURL is the easiest way to demonstrate this vulnerability by sending a genuinely large file.

## Testing Size Limits
We will generate a 250MB dummy file and attempt to upload it.

```bash
# Create a 250MB dummy file (Linux/macOS)
dd if=/dev/zero of=huge.txt bs=1M count=250

# Attempt upload
curl -F "file=@huge.txt" http://localhost:5000/upload
```

**Expected Result (Secure App):**
The connection terminates almost instantly with an HTTP 413 error.

**Expected Result (Vulnerable App):**
The file uploads entirely. If using the provided `docker-compose.yml` (which limits the container to 200MB RAM), the container will likely crash with an OOM (Out Of Memory) error and return a connection reset or 502 Bad Gateway.
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* The framework is explicitly configured with a maximum upload size.
* The web server actively monitors the incoming HTTP stream.
* If the stream exceeds the limit, the connection is aborted *before* the application logic parses the file.
* A clear `413 Payload Too Large` error is returned to the client.

## Vulnerable Implementation
* The server accepts the upload, allocating disk space or memory.
* The application logic triggers.
* The server runs out of resources, leading to performance degradation or a complete crash.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* While application frameworks (like Flask, Django, Express) offer configurations for max upload size, the **best practice** is to enforce file size limits at the reverse proxy/web server level (e.g., Nginx `client_max_body_size`, Apache `LimitRequestBody`, or AWS WAF/API Gateway).
* Enforcing it at the proxy layer drops the malicious connection before the payload even reaches your application runtime, saving CPU cycles.
* When testing locally without Nginx, setting `app.config['MAX_CONTENT_LENGTH']` in Flask is the correct approach.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To satisfy ASVS 5.2.1, you must prevent the application from processing oversized files.

1. **Framework Limits:** Configure your framework to reject large requests globally or per-route.
   * **Flask:** `app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024`
   * **Express (Multer):** `multer({ limits: { fileSize: 1000000 } })`
   * **Spring Boot:** `spring.servlet.multipart.max-file-size=10MB`
2. **Reverse Proxy Limits (Recommended):** Block large requests at the edge.
   * **Nginx:** Add `client_max_body_size 10M;` to the server block.
3. **Avoid In-Memory Processing:** Never use methods like `.read()` or `.getBytes()` on uploaded files unless you are absolutely certain the size limit is enforced. Use streaming APIs to process files in chunks.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 5.2.1

File uploads are fundamentally dangerous because they hand control over server resources directly to the end-user. 

When an HTTP request containing a file is sent, the server must buffer that request somewhere (memory or disk) before the application can parse the multipart form data and extract the file. If there are no limits, an attacker controls exactly how much memory or disk space the server consumes.

ASVS 5.2.1 targets the most basic layer of defense: ensuring the application explicitly defines and enforces what a "safe size" means for its specific business context.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
# Intercepting and modifying Content-Length manually is rarely effective because 
# frameworks parse the actual stream. Instead, use massive payloads.

POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Length: 5000000

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

[... 5 Megabytes of 'A' characters ...]
------WebKitFormBoundary7MA4YWxkTrZu0gW--
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE ---
HTTP/1.1 413 REQUEST ENTITY TOO LARGE
Content-Type: text/html; charset=utf-8
Content-Length: [length]
Connection: close

[...HTML Response containing "File exceeds the maximum allowed size of 1 MB."...]
""")

write_file(r"tests\curl.txt", """
# Test with a small safe file
echo "Hello World" > small.txt
curl -F "file=@small.txt" http://localhost:5000/upload

# Test with a large malicious file
dd if=/dev/zero of=huge.txt bs=1M count=10
curl -F "file=@huge.txt" http://localhost:5000/upload
""")

write_file(r"tests\payloads.txt", """
# Payload Generation for DoS Testing (Linux/macOS)

# Generate a 1MB file (Passes Secure App)
dd if=/dev/zero of=payload_1mb.txt bs=1M count=1

# Generate a 10MB file (Fails Secure App, Passes Vulnerable App)
dd if=/dev/zero of=payload_10mb.txt bs=1M count=10

# Generate a 300MB file (Will crash Vulnerable App due to 200MB Docker RAM limit)
dd if=/dev/zero of=payload_300mb.txt bs=1M count=300
""")
