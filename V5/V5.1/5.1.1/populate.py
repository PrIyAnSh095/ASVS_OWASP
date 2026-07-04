import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V5\V5.1\5.1.1"

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
    <title>ASVS 5.1.1 - File Handling Documentation</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; }
        .policy { background-color: #f9f9f9; padding: 10px; border-left: 4px solid #007bff; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>ASVS 5.1.1: File Upload Documentation</h1>
    {% block content %}{% endblock %}
</body>
</html>
"""

write_file(r"secure\templates\layout.html", layout_html)
write_file(r"vulnerable\templates\layout.html", layout_html)

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure Implementation: Fully Documented Uploads</h2>
    
    <div class="box policy">
        <h3>File Upload Policy (Documentation)</h3>
        <p>Before uploading a file, please review our strict file handling guidelines:</p>
        <ul>
            <li><strong>Permitted File Types (MIME):</strong> image/jpeg, image/png, application/pdf, text/plain</li>
            <li><strong>Expected Extensions:</strong> .jpg, .jpeg, .png, .pdf, .txt</li>
            <li><strong>Maximum Upload Size:</strong> 2 MB (2,097,152 bytes)</li>
            <li><strong>Archive Handling:</strong> ZIP or TAR archives are NOT permitted. (If they were, max extracted size would be strictly limited to 5 MB).</li>
            <li><strong>Storage Location:</strong> Files are stored temporarily in `/tmp/uploads` and are never executed.</li>
            <li><strong>Validation Process:</strong> The server checks the file extension, MIME type, and exact file size.</li>
            <li><strong>Malware Scanning:</strong> Uploaded files are asynchronously scanned by an internal antivirus engine. </li>
            <li><strong>Malicious File Behavior:</strong> If malware is detected, the file is immediately quarantined/deleted, and the user's account is flagged. A notification will be sent to the user.</li>
        </ul>
        <p><em>Note: This exhaustive documentation fulfills ASVS 5.1.1.</em></p>
    </div>

    <div class="box">
        <h3>Upload a File</h3>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload File</button>
        </form>
        
        <br>
        {% if message %}
            <div class="{% if success %}success{% else %}error{% endif %}">
                Result: {{ message }}
            </div>
        {% endif %}
    </div>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Vulnerable Implementation: Undocumented Uploads</h2>
    
    <div class="box policy" style="border-left-color: red;">
        <h3>File Upload Policy</h3>
        <p><em>(Missing)</em> No documentation is provided regarding what files are allowed, how large they can be, or what happens if malware is uploaded.</p>
        <p>This violates ASVS 5.1.1, as users (and developers) have no clear guidelines on the expected behavior of the upload feature.</p>
    </div>

    <div class="box">
        <h3>Upload a File</h3>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload File</button>
        </form>
        
        <br>
        {% if message %}
            <div class="{% if success %}success{% else %}error{% endif %}">
                Result: {{ message }}
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
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # 2MB limit enforces the documented policy

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # In a real app, we would save to /tmp/uploads and trigger the documented malware scan
        return render_template('index.html', message=f"File {file.filename} uploaded and queued for malware scanning (simulated).", success=True)
    else:
        return render_template('index.html', message="Invalid file extension. Please review the File Upload Policy.", success=False)

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', message="File exceeds the documented 2MB maximum upload size.", success=False), 413

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
  secure-upload-511:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 5.1.1

This application implements ASVS 5.1.1 by explicitly documenting the file handling policies directly in the user interface (and ideally in developer documentation).

## Implementation Details
* A clear policy lists allowed extensions (`.txt`, `.pdf`, `.png`, `.jpg`).
* It specifies the maximum file size (2 MB), which is enforced by Flask's `MAX_CONTENT_LENGTH`.
* It documents the backend behavior regarding malware scanning, informing users of what happens to malicious files.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
from flask import Flask, render_template, request
import os

app = Flask(__name__)
# VULNERABILITY: No documentation provided to the user or developer.
# The backend might arbitrarily enforce limits, but the lack of documentation violates ASVS 5.1.1.
# Here we just allow pretty much anything under 50MB without telling the user.
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 

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
        
    # Unclear policy: We silently reject .exe but don't tell the user.
    if file.filename.endswith('.exe'):
        return render_template('index.html', message="Upload failed.", success=False)
        
    return render_template('index.html', message="File uploaded successfully.", success=True)

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
CMD ["python", "app.py"]
""")

write_file(r"vulnerable\docker-compose.yml", """
version: '3.8'
services:
  vulnerable-upload-511:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 5.1.1

This application fails to document its file upload policies.

## Vulnerability
Users are presented with an upload button but given no guidance on allowed formats, file sizes, or security processes (like malware scanning). This lack of documentation makes the system unpredictable for users and makes it difficult for security engineers to audit whether the implementation matches the intended security architecture.
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 5.1.1 (Missing File Handling Documentation)

While missing documentation is not a direct exploit, it represents a severe architectural and operational vulnerability.

## The Risks of Undocumented Features
1. **Security Auditing Failures:** If developers do not explicitly document the maximum file size or allowed extensions, security testers cannot verify if the backend implementation is correct. A tester might assume a 10MB limit is intended when the business requirement was 1MB.
2. **Denial of Service (DoS):** Without documented (and enforced) limits on archive extraction sizes (e.g., zip bombs), systems are prone to CPU and disk exhaustion.
3. **Malware Handling Assumptions:** If the documentation does not explain how malware is handled, developers might assume a third-party gateway is scanning files, while the gateway assumes the application is doing it. This leads to gaps where malicious files are hosted and distributed.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

Testing for documentation completeness (ASVS 5.1.1) is largely a manual review process, but Burp Suite helps verify if the backend enforces the documented policies.

## Testing Steps
1. Review the application's help pages, upload UI, or API documentation (Swagger/OpenAPI). Check for:
   * Max file size
   * Allowed extensions/MIME types
   * Malware scanning behavior
2. Use Burp Suite Repeater to upload a file exactly at the documented size limit (e.g., 2MB). It should pass.
3. Modify the payload to exceed the limit (e.g., 2.1MB). The server should reject it.
4. Attempt to upload a disallowed extension (e.g., `.php` or `.exe`). It should be rejected with a clear message referencing the policy.

## Evaluating Results
* **PASS (Secure App):** The policy is clearly documented in the UI/Docs, and the backend perfectly enforces it.
* **FAIL (Vulnerable App):** There is no documentation. The backend accepts or rejects files arbitrarily without explaining why.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

You can use cURL to test if the backend enforces the documented file size limits.

## Testing Size Limits
Attempt to upload a 3MB file to an endpoint documented to only accept 2MB.

```bash
# Create a 3MB dummy file
dd if=/dev/zero of=large_file.txt bs=1M count=3

# Attempt upload
curl -F "file=@large_file.txt" http://localhost:5000/upload
```

**Expected Result (Secure App):** The server returns an HTTP 413 Payload Too Large, confirming the documented 2MB limit is enforced.
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* The user interface clearly displays the allowed file extensions, maximum size, and security policies (like malware scanning) before the user selects a file.
* Developer documentation (like API specs) contains the same strict definitions.
* The backend enforces these exact documented definitions.

## Vulnerable Implementation
* The upload form provides zero context or rules.
* The backend might arbitrarily reject certain files (like `.exe`) but fails to inform the user why.
* There is no documented consensus on how large files can be or what happens if a malicious file is uploaded.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* ASVS 5.1.1 is classified under "File Handling Documentation". It is a Level 1, 2, and 3 requirement.
* Documentation bridges the gap between Business Logic, Security Architecture, and User Experience.
* **Archive Files:** The requirement explicitly mentions "including unpacked size where applicable". If your application accepts `.zip` or `.tar.gz`, the documentation MUST state the maximum size of the uncompressed contents to prevent Zip Bomb attacks.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To satisfy ASVS 5.1.1:

1. **Write a File Upload Policy:** Create a standardized document or UI component that lists:
   * Permitted file extensions (e.g., `.jpg`, `.pdf`).
   * Permitted MIME types.
   * Maximum file size (e.g., 5 MB).
   * Maximum unpacked size (if archives are allowed).
2. **Document Malware Handling:** Explicitly state the system's behavior when malware is detected (e.g., "Files are scanned by ClamAV. Infected files are deleted and administrators are alerted.").
3. **Align Backend:** Ensure the backend code (e.g., Flask's `MAX_CONTENT_LENGTH`) exactly matches the documented numbers.
4. **API Documentation:** If building an API, include these limits in the OpenAPI/Swagger specification under the schema definition for the file upload endpoint.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 5.1.1

Security by obscurity does not work for file uploads. A robust security posture requires "Secure by Design," which starts with clear documentation.

When an application's file upload constraints are undocumented:
1. **Users get frustrated** because their files are rejected with generic "Upload Failed" messages.
2. **Developers make mistakes** because they don't know the intended constraints when refactoring or migrating the backend.
3. **Security analysts cannot audit** the application effectively because there is no baseline "truth" to test against.

By enforcing strict documentation (ASVS 5.1.1), organizations ensure that everyone understands the boundaries of the upload feature, making it significantly easier to implement the technical controls (like ASVS 5.1.2 and 5.1.3) correctly.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Length: 198

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

This is a test file.
------WebKitFormBoundary7MA4YWxkTrZu0gW--
""")

write_file(r"tests\burp_responses.txt", """
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: [length]

[...HTML Response containing "File test.txt uploaded and queued for malware scanning (simulated)."...]
""")

write_file(r"tests\curl.txt", """
# Standard Upload
curl -F "file=@test.txt" http://localhost:5000/upload

# Large File Upload (Should trigger 413 based on documented limits)
dd if=/dev/zero of=large.txt bs=1M count=3
curl -F "file=@large.txt" http://localhost:5000/upload
""")

write_file(r"tests\payloads.txt", """
# Documentation Review Checklist

[ ] Are allowed file types listed?
[ ] Are allowed extensions listed?
[ ] Is the maximum upload size stated?
[ ] Is the maximum extracted archive size stated (if applicable)?
[ ] Is the malware scanning and handling process explained?
""")
