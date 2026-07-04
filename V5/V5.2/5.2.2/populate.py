import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V5\V5.2\5.2.2"

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
    <title>ASVS 5.2.2 - File Content Validation</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
        .status { padding: 5px; border: 1px solid #000; display: inline-block; }
    </style>
</head>
<body>
    <h1>ASVS 5.2.2: Verifying File Extensions and Magic Bytes</h1>
    {% block content %}{% endblock %}
</body>
</html>
"""

write_file(r"secure\templates\layout.html", layout_html)
write_file(r"vulnerable\templates\layout.html", layout_html)

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure Implementation: Deep Validation</h2>
    
    <div class="box">
        <p>This implementation validates the file extension against its internal magic bytes (MIME type). Furthermore, if it is an image, it safely parses and rewrites it to strip malicious payloads.</p>
        
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload File</button>
        </form>
        
        <br>
        {% if message %}
            <div class="{% if success %}success{% else %}error{% endif %}">
                Result: {{ message }}<br>
                {% if details %}
                <small>Validation Details: {{ details }}</small>
                {% endif %}
            </div>
            <br>
            <div class="status">
                <strong>PASS / FAIL:</strong>
                {% if success %}
                    <span style="color: green;">N/A (Valid File Processed)</span>
                {% else %}
                    <span style="color: green;">PASS (Malicious/Invalid file actively blocked!)</span>
                {% endif %}
            </div>
        {% endif %}
    </div>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Vulnerable Implementation: Extension-Only Validation</h2>
    
    <div class="box">
        <p>This implementation only checks if the file name ends in an allowed extension (e.g. `.jpg`). It does NOT check magic bytes or rewrite images.</p>
        
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
                    <span style="color: red;">FAIL (Check if you uploaded a disguised file!)</span>
                {% else %}
                    <span style="color: green;">N/A (Extension rejected)</span>
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
import magic
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Mapping allowed extensions to their expected MIME types
ALLOWED_TYPES = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'pdf': 'application/pdf',
    'txt': 'text/plain'
}

def secure_process_image(file_stream, ext):
    try:
        # Load the image using Pillow to verify its structure
        img = Image.open(file_stream)
        img.verify() # Verify it is an image
        
        # Reset stream pointer
        file_stream.seek(0)
        img = Image.open(file_stream)
        
        # Safely rewrite the image to an in-memory buffer, stripping malicious EXIF or trailing payloads
        out_stream = BytesIO()
        format = 'JPEG' if ext in ['jpg', 'jpeg'] else 'PNG'
        # Converting to RGB drops alpha channel/metadata in some formats
        img.convert('RGB').save(out_stream, format=format)
        out_stream.seek(0)
        return True, "Image safely rewritten."
    except Exception as e:
        return False, f"Image processing failed (Corrupted/Malicious): {str(e)}"

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
        
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    
    # 1. Extension Validation
    if ext not in ALLOWED_TYPES:
        return render_template('index.html', message="Extension not allowed.", success=False)
        
    # Read file content to check magic bytes
    file_bytes = file.read()
    file.seek(0) # Reset pointer for later use
    
    # 2. Magic Byte Validation (MIME type from content, not the header sent by the user)
    actual_mime = magic.from_buffer(file_bytes, mime=True)
    expected_mime = ALLOWED_TYPES[ext]
    
    if actual_mime != expected_mime:
        details = f"Magic Byte mismatch! Extension claims '{ext}' ({expected_mime}), but content is '{actual_mime}'."
        return render_template('index.html', message="File content does not match extension.", details=details, success=False)
        
    details = f"Magic Byte check passed ({actual_mime}). "
    
    # 3. Safe Rewriting / Content Validation
    if ext in ['jpg', 'jpeg', 'png']:
        success, img_details = secure_process_image(file, ext)
        details += img_details
        if not success:
            return render_template('index.html', message="Invalid Image Content.", details=details, success=False)
    
    return render_template('index.html', message="File safely uploaded and validated!", details=details, success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"secure\requirements.txt", """
Flask==2.3.2
python-magic==0.4.27
Pillow==10.0.0
""")

write_file(r"secure\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app

# Install libmagic required by python-magic
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
""")

write_file(r"secure\docker-compose.yml", """
version: '3.8'
services:
  secure-content-522:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 5.2.2

This application validates file uploads by verifying the true identity of the file, rather than trusting the user-provided filename or `Content-Type` header.

## Security Controls
1. **Extension Validation:** Basic check to ensure the extension is allowed.
2. **Magic Byte Inspection:** Uses `python-magic` (libmagic) to analyze the file's raw binary signature and derive its actual MIME type. It compares this against the expected MIME type for the given extension.
3. **Safe Rewriting:** Uses the `Pillow` library to parse images and rewrite them to a new buffer, effectively stripping out trailing malicious payloads (like PHP code appended to a valid image) or Exif metadata exploits.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    # VULNERABILITY: Only checking the string extension of the filename.
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

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
        
    # No magic byte check. No MIME verification. No content rewriting.
    if file and allowed_file(file.filename):
        # The file is accepted blindly!
        return render_template('index.html', message=f"File {file.filename} uploaded successfully.", success=True)
    else:
        return render_template('index.html', message="Invalid extension.", success=False)

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
  vulnerable-content-522:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 5.2.2

This application fails to validate the actual content of uploaded files, relying entirely on the user-supplied filename.

## Vulnerability
Because the application only checks `filename.endswith('.jpg')`, an attacker can bypass the filter simply by renaming a malicious file. If the server later serves this file or passes it to a vulnerable backend process, it can lead to Remote Code Execution (RCE) or Cross-Site Scripting (XSS).
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 5.2.2 (Improper File Validation)

When an application relies solely on the filename extension or the `Content-Type` header (which is entirely controlled by the user), it becomes vulnerable to multiple file-based attacks.

## Polyglots and Disguised Files
1. **Renamed Executables:** An attacker renames an executable to `invoice.pdf`. If a downstream user downloads it and their OS hides file extensions, they might execute it.
2. **Web Shells:** An attacker uploads a PHP script renamed to `shell.jpg`. If the web server is misconfigured (e.g., Apache `AddHandler` misconfigurations), accessing `shell.jpg` might execute the PHP code.
3. **Image Polyglots:** An attacker creates a valid JPG file, but appends a script payload to the end of the binary data. The vulnerable app accepts it because the extension is `.jpg`. If the server is tricked into executing it, the valid image header is ignored, and the trailing script is executed.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

Burp Suite allows you to easily bypass front-end extension checks and manipulate the `Content-Type` header to test backend validation.

## Testing Steps
1. Create a dummy script file containing `<?php echo "Test"; ?>`. Save it as `shell.php`.
2. Intercept the file upload request.
3. In Burp Repeater, change `filename="shell.php"` to `filename="shell.jpg"`.
4. Change the `Content-Type` to `image/jpeg`.
5. Send the request.

## Evaluating Results
* **PASS (Secure App):** The server analyzes the binary content, sees the text (text/x-php), notices it doesn't match the `.jpg` extension expectation, and rejects it with an error.
* **FAIL (Vulnerable App):** The server looks at `.jpg`, ignores the actual content, and blindly saves the file.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

You can use cURL to quickly push mislabeled files to the server.

```bash
# 1. Create a fake image (actually text)
echo '<?php echo "Test"; ?>' > evil.jpg

# 2. Upload it to the server
curl -F "file=@evil.jpg" http://localhost:5000/upload
```

**Expected Result (Secure App):**
Rejects the file: `Magic Byte mismatch! Extension claims 'jpg' (image/jpeg), but content is 'text/plain' or 'text/x-php'.`

**Expected Result (Vulnerable App):**
Accepts the file successfully.
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* Reads the first few bytes of the file (Magic Bytes / File Signature) to determine its true MIME type (e.g., `FF D8 FF E0` for JPEG).
* Asserts that the detected MIME type matches the permitted list *and* matches the provided extension.
* For complex formats (Images, PDFs), it safely parses and rewrites the content using a trusted library (e.g., `Pillow` for Python) to strip out polyglot payloads.

## Vulnerable Implementation
* Splits the string filename by `.` and checks the last element against a hardcoded list.
* Implicitly trusts the `Content-Type` header sent by the HTTP client.
* Saves the raw byte stream directly to the disk without rewriting or scanning it.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* **Magic Bytes:** File signatures are much more reliable than extensions. Tools like `libmagic` (Python's `python-magic`) or `file` on Linux read these headers.
* **Safe Rewriting:** This is crucial. An attacker can create a file that possesses valid Magic Bytes (so it passes libmagic) but contains malicious code at the end (a Polyglot). By using a library like `Pillow` to read the image and save a *new* copy of it, you effectively sanitize the image, as the library will discard the trailing malicious code.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To satisfy ASVS 5.2.2:

1. **Ignore Client Headers:** Never trust the `Content-Type` header provided in the HTTP request.
2. **Verify Magic Bytes:** Use a library to read the file's binary signature and determine its true MIME type.
3. **Enforce Extension Match:** Ensure the detected MIME type logically matches the uploaded extension.
4. **Sanitize via Rewriting:** For media files (images, videos), pass them through a standard processing library (like ImageMagick, Pillow, FFmpeg) to transcode or rewrite them. This destroys hidden polyglot payloads.
5. **Use Trusted Libraries:** Never write your own file parsing logic. Rely on established libraries.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 5.2.2

The separation of a file's "Name" (Extension) and its "Content" (Data) is a frequent source of security vulnerabilities. Operating systems and web servers often use the extension to decide how to execute or render a file.

If an application enforces security based on the Name (e.g., "only allow .jpg"), but the web server executes based on Content, or vice versa, attackers can upload a file that passes the application's filter but is executed maliciously by the server or the end-user's operating system. 

Strictly tying the Extension, the Magic Bytes, and the actual parsed content together ensures the file is exactly what it claims to be.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Length: 172

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="evil.jpg"
Content-Type: image/jpeg

<?php echo "Test"; ?>
------WebKitFormBoundary7MA4YWxkTrZu0gW--
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE ---
[...HTML containing...]
Magic Byte mismatch! Extension claims 'jpg' (image/jpeg), but content is 'text/plain'.

--- VULNERABLE APPLICATION RESPONSE ---
[...HTML containing...]
File evil.jpg uploaded successfully.
""")

write_file(r"tests\curl.txt", """
# Test 1: Fake Extension (Text masquerading as JPG)
echo '<?php echo "Test"; ?>' > fake.jpg
curl -F "file=@fake.jpg" http://localhost:5000/upload

# Test 2: Text masquerading as PDF
echo 'Just some text' > fake.pdf
curl -F "file=@fake.pdf" http://localhost:5000/upload
""")

write_file(r"tests\payloads.txt", """
# Polyglot test (Requires hex editor or python script to generate)
# A true polyglot has valid JPEG headers but contains trailing text.
# The Magic Byte check will PASS this file!
# The "Safe Rewriting" step (Pillow) is required to stop it by stripping the text.

# To create a basic polyglot manually in Linux:
# 1. Download a valid tiny image `valid.jpg`
# 2. Append code: `echo '<?php echo "Test"; ?>' >> valid.jpg`
# 3. Upload `valid.jpg` to the Secure App. It will pass Magic Bytes, but the rewritten image saved by the app will no longer contain the PHP code!
""")
