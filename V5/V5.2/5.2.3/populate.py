import os
import zipfile

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V5\V5.2\5.2.3"

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
    <title>ASVS 5.2.3 - Archive Validation</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
        .status { padding: 5px; border: 1px solid #000; display: inline-block; }
    </style>
</head>
<body>
    <h1>ASVS 5.2.3: Zip Bomb Prevention</h1>
    {% block content %}{% endblock %}
</body>
</html>
"""

write_file(r"secure\templates\layout.html", layout_html)
write_file(r"vulnerable\templates\layout.html", layout_html)

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure Implementation: Pre-Extraction Validation</h2>
    
    <div class="box">
        <p>This implementation reads the archive headers <strong>before</strong> extracting anything. It strictly enforces:</p>
        <ul>
            <li>Maximum 10 files allowed inside the archive.</li>
            <li>Maximum 5 MB total uncompressed size.</li>
        </ul>
        
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required accept=".zip,.docx">
            <button type="submit">Upload Archive</button>
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
                    <span style="color: green;">N/A (Valid archive)</span>
                {% else %}
                    <span style="color: green;">PASS (Malicious archive safely blocked before extraction)</span>
                {% endif %}
            </div>
        {% endif %}
    </div>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Vulnerable Implementation: Blind Extraction</h2>
    
    <div class="box">
        <p>This implementation uses <code>extractall()</code> without checking the uncompressed size or file count first. It is highly vulnerable to Zip Bombs.</p>
        
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required accept=".zip,.docx">
            <button type="submit">Upload Archive</button>
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
                    <span style="color: red;">FAIL (Archive extracted blindly!)</span>
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
import zipfile
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # 5MB compressed max

MAX_UNCOMPRESSED_SIZE = 5 * 1024 * 1024 # 5 MB uncompressed max
MAX_FILES = 10 # Max files inside archive

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
        
    if not file.filename.endswith('.zip') and not file.filename.endswith('.docx'):
        return render_template('index.html', message="Only ZIP or DOCX allowed.", success=False)

    try:
        total_size = 0
        total_files = 0
        
        # Open the zip file to read headers ONLY. No extraction happens yet.
        with zipfile.ZipFile(file, 'r') as zf:
            for info in zf.infolist():
                total_files += 1
                total_size += info.file_size
                
                if total_files > MAX_FILES:
                    return render_template('index.html', message=f"Archive contains too many files (Limit: {MAX_FILES}). Rejected.", success=False)
                if total_size > MAX_UNCOMPRESSED_SIZE:
                    return render_template('index.html', message=f"Archive is too large when uncompressed (Limit: 5MB). Rejected to prevent Zip Bombs.", success=False)
            
            # If we get here, the archive is safe to extract.
            # zf.extractall(path="/tmp/extracted")
            return render_template('index.html', message=f"Archive validated successfully! Contains {total_files} files, {total_size} bytes uncompressed. (Extraction skipped for lab safety).", success=True)
            
    except zipfile.BadZipFile:
        return render_template('index.html', message="Corrupted or invalid ZIP archive.", success=False)
    except Exception as e:
        return render_template('index.html', message=f"Error: {str(e)}", success=False)

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
  secure-zip-523:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 5.2.3

This application safely handles archive uploads by validating the contents *before* extraction.

## Security Controls
1. **Pre-Extraction Validation:** The `zipfile` module allows reading the central directory of the archive (`zf.infolist()`) without actually decompressing the data blocks.
2. **Uncompressed Size Limit:** We iterate through the file headers and sum `info.file_size`. If it exceeds our safety threshold (5MB), we instantly abort.
3. **File Count Limit:** We count the number of files. If an attacker submits an archive containing 100,000 empty files (Inode Exhaustion), we abort.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", """
from flask import Flask, render_template, request
import zipfile
import os

app = Flask(__name__)
# VULNERABILITY 1: Allowing large uploads just to accept the bomb (though even small ones can be deadly)
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
        
    try:
        # VULNERABILITY 2: Blindly extracting without checking uncompressed size or file count!
        with zipfile.ZipFile(file, 'r') as zf:
            extract_path = os.path.join("/tmp/extracted", file.filename)
            os.makedirs(extract_path, exist_ok=True)
            
            # Extract everything. A zip bomb will cause a massive CPU spike, fill the disk, or crash the process.
            zf.extractall(path=extract_path)
            
            return render_template('index.html', message=f"Archive blindly extracted to {extract_path}!", success=True)
            
    except zipfile.BadZipFile:
        return render_template('index.html', message="Invalid ZIP.", success=False)
    except Exception as e:
        return render_template('index.html', message=f"Extraction crashed (Likely Resource Exhaustion): {str(e)}", success=False)

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
# We limit disk space write logic or memory to observe crashes, but standard docker is fine.
CMD ["python", "app.py"]
""")

write_file(r"vulnerable\docker-compose.yml", """
version: '3.8'
services:
  vulnerable-zip-523:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 5.2.3

This application is highly vulnerable to Archive Bombs (Zip Bombs).

## Vulnerability
The server calls `zf.extractall()` immediately on any valid ZIP file uploaded. An attacker can craft a 42-kilobyte ZIP file that decompresses into 4.5 Petabytes of data (e.g., the infamous 42.zip). When the server attempts to extract this, it will consume 100% of the CPU and rapidly fill the entire hard drive, causing a complete Denial of Service.
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 5.2.3 (Zip Bombs)

Archives (like ZIP, GZ, and even DOCX, which are just ZIP files) use compression algorithms that look for repeated patterns.

## The Zip Bomb Attack
An attacker generates a file containing gigabytes of repeating zeroes. This file compresses extremely well (e.g., 10GB of zeroes compresses down to roughly 10MB).
1. The attacker uploads the 10MB ZIP. It passes the server's HTTP `Content-Length` restrictions.
2. The server blindly calls `extractall()`.
3. The server begins writing the 10GB of zeroes to the disk.
4. The server runs out of disk space, or the CPU maxes out processing the decompression, resulting in a Denial of Service.

## Inode Exhaustion
Instead of one massive file, the attacker creates an archive with 500,000 tiny 1-byte files. The extraction process creates half a million files on the filesystem, exhausting the filesystem's inodes. No further files can be created on the OS by any process.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

Since Zip Bombs rely on specific binary file structures, Burp Suite is best used merely to deliver the payload.

## Testing Steps
1. Generate the test archives using the provided `generate_tests.py` script.
2. In Burp Suite Repeater, upload `simulated-zip-bomb.zip` (100MB uncompressed).
3. Observe the response times and status.

## Evaluating Results
* **PASS (Secure App):** The server responds almost instantly with an error: "Archive is too large when uncompressed". The server CPU/Disk usage remains stable.
* **FAIL (Vulnerable App):** The request hangs for several seconds/minutes as the server spins its CPU extracting the bomb. It may return a 500 Error if the disk fills up.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

Upload the test files directly using cURL:

```bash
# Upload normal file
curl -F "file=@normal.zip" http://localhost:5000/upload

# Upload file with too many items
curl -F "file=@many-files.zip" http://localhost:5000/upload

# Upload simulated Zip Bomb
curl -F "file=@simulated-zip-bomb.zip" http://localhost:5000/upload
```
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* Reads the Zip Central Directory Headers *only*.
* Tallies up the `file_size` (uncompressed size) of all entries.
* Tallies up the total number of entries.
* Rejects the file without extracting a single byte if limits are exceeded.

## Vulnerable Implementation
* Instantiates extraction directly.
* Blindly relies on the decompression library, which will faithfully execute the extraction until the OS kills the process or the disk is full.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* **DOCX, XLSX, APK, JAR:** Remember that many modern file formats are literally just ZIP files with a different extension. If your application parses DOCX files using a library, that library is extracting an archive under the hood and must be hardened against Zip Bombs.
* **Recursive Zip Bombs:** The most devastating zip bombs contain zip files within zip files. Standard `extractall()` doesn't inherently recurse, but if your application logic extracts an archive, then looks inside it for other archives to extract, you must track the uncompressed size globally across all recursive operations.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To satisfy ASVS 5.2.3, implement pre-flight validation on all compressed formats:

1. **Python (zipfile):** Use `zf.infolist()` and check `info.file_size`.
2. **Java (java.util.zip):** Use `ZipInputStream.getNextEntry()` and track `entry.getSize()`.
3. **Node.js (yauzl):** Use the `entry` event to inspect `entry.uncompressedSize` before calling `.openReadStream()`.
4. **Limits to enforce:**
   * Max Total Uncompressed Size (e.g., 50MB)
   * Max Single File Uncompressed Size
   * Max Number of Files in the Archive
   * Max Compression Ratio (e.g., Uncompressed Size / Compressed Size > 100)
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 5.2.3

Compression algorithms are designed to trade CPU cycles for storage efficiency. In the context of a web server, an attacker weaponizes this efficiency. 

Because the web server's initial defense (`Content-Length` validation) only sees the highly efficient compressed size, the payload easily bypasses size restrictions. Once the payload crosses the threshold into the application logic, the decompression engine unpacks it into its true form, overwhelming the host infrastructure. 

Pre-flight inspection of archive headers is the only effective defense.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Content-Length: [length]

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="simulated-zip-bomb.zip"
Content-Type: application/zip

[... Binary Zip Data ...]
------WebKitFormBoundary--
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE ---
Archive is too large when uncompressed (Limit: 5MB). Rejected to prevent Zip Bombs.

--- VULNERABLE APPLICATION RESPONSE ---
[Hangs while extracting, eventually returns 500 Internal Server Error or Success if it survives]
""")

write_file(r"tests\curl.txt", """
# Run generate_tests.py first to create the zip files!
curl -F "file=@simulated-zip-bomb.zip" http://localhost:5000/upload
""")

write_file(r"tests\payloads.txt", """
Run the `generate_tests.py` script provided in this folder to generate the payloads locally!
""")

write_file(r"tests\generate_tests.py", '''
import zipfile
import os

print("Generating Test Archives for ASVS 5.2.3...")

# 1. Normal Zip
with zipfile.ZipFile("normal.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("test1.txt", "Hello World")
    zf.writestr("test2.txt", "Secure coding is fun.")
print("Created normal.zip (Passes both)")

# 2. Too Many Files Zip (Inode Exhaustion simulation)
with zipfile.ZipFile("many-files.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    for i in range(15): # Secure app limits to 10
        zf.writestr(f"file_{i}.txt", "tiny")
print("Created many-files.zip (Fails secure, Passes vulnerable)")

# 3. Simulated Zip Bomb (Large uncompressed size)
# Generates 15MB of zeroes, which compresses down to a few kilobytes.
# Secure app limits to 5MB uncompressed.
massive_data = b"0" * (15 * 1024 * 1024) 
with zipfile.ZipFile("simulated-zip-bomb.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("bomb.txt", massive_data)
print("Created simulated-zip-bomb.zip (Fails secure, Extracts 15MB blindly in vulnerable)")

print("Done!")
''')
