import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V5\V5.2\5.2.4"

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
    <title>ASVS 5.2.4 - Storage Quotas</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
        .quota { background: #eee; padding: 10px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>ASVS 5.2.4: Per-User File Quotas</h1>
    {% block content %}{% endblock %}
</body>
</html>
"""

write_file(r"secure\templates\layout.html", layout_html)
write_file(r"vulnerable\templates\layout.html", layout_html)

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure Implementation: Strict Storage Limits</h2>
    
    <div class="box">
        <form method="GET" action="/">
            <label>Current User:</label>
            <input type="text" name="username" value="{{ username }}" required>
            <button type="submit">Switch User</button>
        </form>
    </div>
    
    <div class="box quota">
        <h3>User Quota ({{ username }})</h3>
        <p><strong>Files Uploaded:</strong> {{ quota.file_count }} / {{ limits.max_files }}</p>
        <p><strong>Storage Used:</strong> {{ (quota.storage_used / 1024)|round(2) }} KB / {{ (limits.max_storage / 1024)|round(2) }} KB</p>
    </div>

    <div class="box">
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="hidden" name="username" value="{{ username }}">
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
    <h2>Vulnerable Implementation: Unrestricted Storage</h2>
    
    <div class="box">
        <form method="GET" action="/">
            <label>Current User:</label>
            <input type="text" name="username" value="{{ username }}" required>
            <button type="submit">Switch User</button>
        </form>
    </div>
    
    <div class="box quota" style="border-left: 4px solid red;">
        <h3>User Quota ({{ username }})</h3>
        <p><strong>Files Uploaded:</strong> {{ quota.file_count }} / (Unlimited)</p>
        <p><strong>Storage Used:</strong> {{ (quota.storage_used / 1024)|round(2) }} KB / (Unlimited)</p>
        <p><em>Warning: This user can exhaust the server's storage!</em></p>
    </div>

    <div class="box">
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="hidden" name="username" value="{{ username }}">
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
# Global system limit just to prevent immediate RAM crash in the lab
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 

# Per-User Config
LIMITS = {
    'max_files': 3,
    'max_storage': 100 * 1024 # 100 KB total storage per user
}

# In-memory mock database
db = {}

def get_user_quota(username):
    if username not in db:
        db[username] = {'file_count': 0, 'storage_used': 0}
    return db[username]

@app.route('/')
def index():
    username = request.args.get('username', 'user1')
    quota = get_user_quota(username)
    return render_template('index.html', username=username, quota=quota, limits=LIMITS)

@app.route('/upload', methods=['POST'])
def upload_file():
    username = request.form.get('username', 'user1')
    quota = get_user_quota(username)
    
    if 'file' not in request.files:
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message="No file part", success=False)
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message="No selected file", success=False)
        
    # Read file to determine exact size (or use seek/tell)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    # Validation 1: Max File Count
    if quota['file_count'] >= LIMITS['max_files']:
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message="Quota Exceeded: You have reached the maximum number of allowed files (3).", success=False)
        
    # Validation 2: Max Storage Limit
    if quota['storage_used'] + file_size > LIMITS['max_storage']:
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message=f"Quota Exceeded: Uploading this file ({file_size} bytes) would exceed your 100 KB limit.", success=False)
        
    # Validation 3: Individual File Size Limit (Implicitly covered by storage quota, but can be checked separately)
    # Passed all checks, update DB
    quota['file_count'] += 1
    quota['storage_used'] += file_size
    
    return render_template('index.html', username=username, quota=quota, limits=LIMITS, message=f"File {file.filename} uploaded successfully!", success=True)

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
  secure-quota-524:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 5.2.4

This application securely implements per-user quotas for file uploads.

## Security Controls
1. **File Count Enforcement:** The server tracks how many files `user1` has uploaded. If the count exceeds the configured limit (3), the server rejects the request.
2. **Storage Quota Enforcement:** The server tracks the total bytes `user1` is storing. If uploading a new file would push the user's total usage over their limit (100 KB), the upload is rejected.
3. **Prevention of Resource Exhaustion:** By binding storage directly to an authenticated user's identity, an attacker cannot write scripts to loop and fill the server's hard drive infinitely.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db = {}

def get_user_quota(username):
    if username not in db:
        db[username] = {'file_count': 0, 'storage_used': 0}
    return db[username]

@app.route('/')
def index():
    username = request.args.get('username', 'user1')
    quota = get_user_quota(username)
    return render_template('index.html', username=username, quota=quota)

@app.route('/upload', methods=['POST'])
def upload_file():
    username = request.form.get('username', 'user1')
    quota = get_user_quota(username)
    
    if 'file' not in request.files:
        return render_template('index.html', username=username, quota=quota, message="No file part", success=False)
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', username=username, quota=quota, message="No selected file", success=False)
        
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    # VULNERABILITY: No enforcement of quotas! 
    # An attacker can just spam this endpoint in a while loop.
    
    quota['file_count'] += 1
    quota['storage_used'] += file_size
    
    return render_template('index.html', username=username, quota=quota, message=f"File {file.filename} uploaded successfully!", success=True)

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
  vulnerable-quota-524:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 5.2.4

This application lacks any per-user upload quotas.

## Vulnerability
While it tracks how much data a user has uploaded, it never actually enforces a limit. This allows any single user (even a newly registered, free-tier attacker account) to upload millions of files and consume terabytes of storage, leading to a complete Denial of Service via Storage Exhaustion for the entire platform.
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 5.2.4 (Quota Exhaustion)

Unrestricted uploads lead directly to Resource Exhaustion.

## The "Free Tier" DoS Attack
1. An attacker registers a free account.
2. The attacker writes a simple Python loop that repeatedly uploads a 1MB file to the server.
3. Because the server only limits the *individual* file size (e.g., 5MB max), each individual upload succeeds.
4. Over a weekend, the attacker's script successfully uploads 500,000 files, consuming 500 GB of the server's hard drive.
5. The database crashes, OS logs cannot write, and legitimate users can no longer upload avatars or documents.

## Inode Exhaustion
An attacker can upload millions of 1-byte files. The hard drive might have 1TB of free space remaining, but the filesystem runs out of "inodes" (file pointers). The entire OS halts because it can no longer create any files. Enforcing a Maximum File Count quota prevents this.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

Burp Suite's Intruder is the perfect tool for testing quota enforcement.

## Testing Steps
1. Intercept a legitimate file upload request.
2. Send it to Burp Intruder.
3. Clear all payloads and select "Null payloads".
4. Set the payload count to `50` (to simulate uploading the same file 50 times rapidly).
5. Start the attack.

## Evaluating Results
* **PASS (Secure App):** The first 3 requests succeed (HTTP 200). The 4th request and all subsequent requests fail (e.g., returning HTTP 403 or an HTML page showing "Quota Exceeded").
* **FAIL (Vulnerable App):** All 50 requests succeed, and the server blindly stores 50 copies of the file for a single user.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

We can script cURL to test both the file count quota and the storage quota.

## 1. File Count Quota Test
```bash
echo "Tiny file" > tiny.txt
# Run 4 times in a row
for i in {1..4}; do curl -F "username=attacker" -F "file=@tiny.txt" http://localhost:5000/upload; done
```
*Secure App:* Accepts 3, rejects the 4th.

## 2. Storage Quota Test (100KB limit)
```bash
dd if=/dev/zero of=large.txt bs=1K count=150
curl -F "username=attacker2" -F "file=@large.txt" http://localhost:5000/upload
```
*Secure App:* Immediately rejects the 150KB upload because it exceeds the 100KB user quota.
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* Maintains state for every user's uploaded files (usually via Database records: `SELECT SUM(file_size) FROM uploads WHERE user_id = ?`).
* Before accepting a new upload, calculates: `Current Storage + New File Size <= Max Quota`.
* Calculates: `Current File Count + 1 <= Max File Count`.
* If either limit is breached, the transaction is rejected gracefully.

## Vulnerable Implementation
* The user logic and upload logic are completely decoupled.
* The system accepts files until the hard drive physically runs out of space, indiscriminately impacting all users on the platform.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* **Distributed Systems:** In microservice architectures (like AWS S3 + Lambda), quota enforcement is harder because uploads might go directly to S3 via Presigned URLs. To enforce quotas in this architecture, you must issue Presigned URLs with strict byte limits, and decrement the user's remaining quota in the central database *before* issuing the URL.
* **Race Conditions:** Naive `SELECT` followed by `INSERT` quota checks are vulnerable to Time-of-Check to Time-of-Use (TOCTOU) race conditions. If an attacker sends 50 concurrent uploads, they might all pass the `SELECT` check before any `INSERT` happens, bypassing the quota. (This lab keeps it simple, but production apps should use Database Locks or Redis Atomic counters).
""")

write_file(r"docs\solution.md", """
# Solution Guide

To satisfy ASVS 5.2.4:

1. **Database Tracking:** Every uploaded file must be recorded in the database, associated with a specific User ID, tracking its size in bytes.
2. **Define Quotas:** Define strict Business Logic constraints (e.g., Free Tier: 50 Files, 100MB Total; Pro Tier: 5000 Files, 10GB Total).
3. **Enforce Before Save:** Calculate the user's current utilization. If `usage + incoming_file > quota`, reject.
4. **Handle Deletions:** When a user deletes a file, ensure the storage quota is accurately decremented so they can upload again.
5. **Race Condition Prevention:** Use atomic counters in a fast data store like Redis (e.g., `INCRBY user:123:storage 50000`) or database locking to prevent concurrent quota bypasses.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 5.2.4

Resource exhaustion is a fundamental category of Denial of Service (DoS). While Network DoS (DDoS) relies on flooding bandwidth, Application DoS relies on forcing the application to consume internal resources (Memory, CPU, Disk, Database Connections).

By failing to isolate user resources (a concept known as "Noisy Neighbor" in cloud computing), a vulnerable application allows a single malicious actor—or even just a buggy client script—to consume 100% of the shared storage pool. 

Implementing Quotas forces the application to implement "Tenant Isolation", ensuring that one user's excessive usage only impacts their own account, keeping the platform healthy for everyone else.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Content-Length: 200

------WebKitFormBoundary
Content-Disposition: form-data; name="username"

attacker_bob
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

A small file.
------WebKitFormBoundary--

(Send this request 5 times in Intruder)
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE (Request 1, 2, 3) ---
HTTP/1.1 200 OK
[...HTML...] File test.txt uploaded successfully!

--- SECURE APPLICATION RESPONSE (Request 4, 5) ---
HTTP/1.1 200 OK (Or 403)
[...HTML...] Quota Exceeded: You have reached the maximum number of allowed files.

--- VULNERABLE APPLICATION RESPONSE ---
HTTP/1.1 200 OK for all 5 requests.
""")

write_file(r"tests\curl.txt", """
# 1. Test File Count Quota (Run this repeatedly)
curl -F "username=testuser1" -F "file=@payloads.txt" http://localhost:5000/upload

# 2. Test Storage Size Quota
dd if=/dev/zero of=oversized.txt bs=1K count=150
curl -F "username=testuser2" -F "file=@oversized.txt" http://localhost:5000/upload
""")

write_file(r"tests\payloads.txt", """
# Payload Generation for DoS Testing (Linux/macOS)

# Small file for count testing
echo "Small payload" > small.txt

# 150KB file to instantly bust the 100KB secure quota
dd if=/dev/zero of=oversized.txt bs=1K count=150
""")
