import os
import logging
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'super_secret_vulnerable_key_for_asvs_lab'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define storage directories
DOWNLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'downloads'))

# Ensure paths exist
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.route('/')
def index():
    # List all uploaded files (no validation, no scanning)
    files = os.listdir(DOWNLOADS_DIR)
    return render_template('index.html', mode='Vulnerable', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part in request', 'error')
        return redirect(url_for('index'))
        
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    # Sanitize name slightly to prevent path traversal
    filename = secure_filename(uploaded_file.filename)
    
    # VULNERABLE: Direct save to downloadable folder, no antivirus scan
    destination_path = os.path.join(DOWNLOADS_DIR, filename)
    uploaded_file.save(destination_path)
    
    logging.info(f"File uploaded (UNSCANNED): {filename} saved directly to public downloads.")
    flash(f"File uploaded successfully (No Scan performed): {filename}", 'success')
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    # Directly serving files, meaning malware uploaded by an attacker can be downloaded by everyone
    filename = secure_filename(filename)
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
