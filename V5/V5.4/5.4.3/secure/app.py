import os
import shutil
import logging
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'super_secret_secure_key_for_asvs_lab'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define storage directories
QUARANTINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'quarantine'))
DOWNLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'downloads'))

# Ensure paths exist
os.makedirs(QUARANTINE_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# EICAR signature prefix for detection
EICAR_SIGNATURE = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

def scan_file(file_path):
    """
    Simulates or performs antivirus scanning on the target file.
    Detects standard EICAR test signature to mimic real threat alerts.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            # Scan for EICAR signature anywhere in the file
            if EICAR_SIGNATURE in content or b"EICAR-STANDARD" in content:
                return False, "Malware Detected (EICAR Test Signature found)"
            
            # Simple content heuristic check for demo safety
            if b"VIRUS" in content.upper() or b"MALWARE" in content.upper():
                return False, "Threat detected by heuristic engine"
                
        return True, "Clean"
    except Exception as e:
        return False, f"Scan failed due to system error: {str(e)}"

@app.route('/')
def index():
    # List files available in the secure downloads directory
    files = os.listdir(DOWNLOADS_DIR)
    return render_template('index.html', mode='Secure', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part in request', 'error')
        return redirect(url_for('index'))
        
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    # Sanitize name
    filename = secure_filename(uploaded_file.filename)
    
    # Step 1: Move directly into Quarantine Zone
    quarantine_path = os.path.join(QUARANTINE_DIR, filename)
    uploaded_file.save(quarantine_path)
    logging.info(f"File quarantined: {filename} at {quarantine_path}")
    
    # Step 2: Trigger Antivirus scan on quarantined file
    is_clean, scan_message = scan_file(quarantine_path)
    
    if is_clean:
        # Step 3: Move to Clean Downloads zone
        destination_path = os.path.join(DOWNLOADS_DIR, filename)
        shutil.move(quarantine_path, destination_path)
        logging.info(f"File scanned clean. Moved to downloads: {filename}")
        flash(f"File uploaded successfully: {filename} (Status: CLEAN)", 'success')
    else:
        # Step 4: Keep in quarantine, flag as infected, and log detection
        logging.warning(f"SECURITY ALERT: Malicious file blocked: {filename}. Reason: {scan_message}")
        
        # Remove infected file immediately to ensure no accidental leaks
        try:
            os.remove(quarantine_path)
            logging.info(f"Infected file deleted from quarantine: {filename}")
        except OSError as e:
            logging.error(f"Failed to delete quarantined file: {e}")
            
        flash(f"File Rejected! Threat identified: {scan_message}", 'error')
        
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    # Only serve files from the verified clean downloads directory
    filename = secure_filename(filename)
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
