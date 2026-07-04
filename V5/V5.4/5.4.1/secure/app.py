from flask import Flask, request, render_template, send_file, abort
import os
import uuid
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '/tmp/secure_downloads'
METADATA_FILE = os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Pre-populate some dummy files for downloading
if not os.path.exists(METADATA_FILE):
    metadata = {}
    
    id1 = str(uuid.uuid4())
    with open(os.path.join(app.config['UPLOAD_FOLDER'], id1), 'w') as f:
        f.write("This is a safe report.")
    metadata[id1] = "report.pdf"
    
    id2 = str(uuid.uuid4())
    with open(os.path.join(app.config['UPLOAD_FOLDER'], id2), 'w') as f:
        f.write("This is a safe invoice.")
    metadata[id2] = "invoice.pdf"
    
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)

def load_metadata():
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    metadata = load_metadata()
    return render_template('index.html', title="Secure File Download", files=metadata, secure=True)

@app.route('/download')
def download():
    # ASVS 5.4.1: Ignore user-supplied filenames. Use internal ID.
    file_id = request.args.get('id')
    metadata = load_metadata()
    
    if not file_id or file_id not in metadata:
        abort(404, description="Invalid file ID")
        
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    
    if not os.path.exists(filepath):
        abort(404, description="File not found")
        
    # ASVS 5.4.1: Specify safe filename using Content-Disposition
    # Flask's send_file with download_name automatically sets Content-Disposition safely
    safe_filename = metadata[file_id]
    return send_file(filepath, as_attachment=True, download_name=safe_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
