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
