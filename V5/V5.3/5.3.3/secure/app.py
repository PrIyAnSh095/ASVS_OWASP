from flask import Flask, request, render_template
import os
import zipfile

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = os.path.abspath('/tmp/secure_extract')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_safe_path(basedir, path, follow_symlinks=True):
    # Resolves the absolute path and normalizes it
    if follow_symlinks:
        matchpath = os.path.realpath(path)
    else:
        matchpath = os.path.abspath(path)
    return basedir == matchpath or matchpath.startswith(basedir + os.sep)

@app.route('/')
def index():
    return render_template('index.html', title="Secure Archive Upload")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Secure Archive Upload")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", title="Secure Archive Upload")
    
    if not file.filename.endswith('.zip'):
        return render_template('index.html', error="Only ZIP files are allowed", title="Secure Archive Upload")
        
    try:
        with zipfile.ZipFile(file, 'r') as z:
            # ASVS 5.3.3: Validate all paths inside the archive before extraction
            for info in z.infolist():
                target_path = os.path.join(UPLOAD_FOLDER, info.filename)
                
                # Verify that the target path does not escape the upload folder
                if not is_safe_path(UPLOAD_FOLDER, target_path):
                    return render_template('index.html', 
                                           error=f"FAIL: Archive attempts Zip Slip (path traversal) with file: {info.filename}. Upload rejected.", 
                                           title="Secure Archive Upload")
                                           
            # Safe to extract
            z.extractall(UPLOAD_FOLDER)
            return render_template('index.html', message="PASS: Archive extracted safely within the boundaries of the extraction directory.", title="Secure Archive Upload")
            
    except zipfile.BadZipFile:
        return render_template('index.html', error="Invalid ZIP archive", title="Secure Archive Upload")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
