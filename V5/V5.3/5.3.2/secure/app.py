from flask import Flask, request, render_template, send_file, abort
from werkzeug.utils import secure_filename
import os
import uuid
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '/tmp/secure_uploads'
METADATA_FILE = os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w') as f:
        json.dump({}, f)

def load_metadata():
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)

def save_metadata(data):
    with open(METADATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    metadata = load_metadata()
    return render_template('index.html', title="Secure File Upload", files=metadata)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Secure File Upload", files=load_metadata())
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", title="Secure File Upload", files=load_metadata())
    
    # ASVS 5.3.2: Create file paths using internally generated values (UUID)
    # The original filename is sanitized and stored ONLY as metadata.
    safe_filename = secure_filename(file.filename)
    if not safe_filename:
        safe_filename = "unnamed_file"
        
    internal_id = str(uuid.uuid4())
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], internal_id)
    
    file.save(filepath)
    
    metadata = load_metadata()
    metadata[internal_id] = safe_filename
    save_metadata(metadata)
    
    return render_template('index.html', message="PASS: File uploaded securely using UUID.", title="Secure File Upload", files=metadata)

@app.route('/download')
def download():
    file_id = request.args.get('id')
    metadata = load_metadata()
    
    if not file_id or file_id not in metadata:
        abort(404)
        
    # We only use the internally generated UUID to fetch the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    
    if not os.path.exists(filepath):
        abort(404)
        
    # We can restore the original sanitized filename in the download prompt
    return send_file(filepath, as_attachment=True, download_name=metadata[file_id])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
