from flask import Flask, request, render_template
import os
import zipfile

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = '/tmp/vulnerable_extract'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', title="Vulnerable Archive Upload")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Vulnerable Archive Upload")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", title="Vulnerable Archive Upload")
    
    if not file.filename.endswith('.zip'):
        return render_template('index.html', error="Only ZIP files are allowed", title="Vulnerable Archive Upload")
        
    try:
        with zipfile.ZipFile(file, 'r') as z:
            # VULNERABILITY: Trusting the archive's internal filenames directly.
            # We mimic a vulnerable manual extraction process because Python's default extractall() 
            # strips absolute paths and parent directory traversals automatically.
            # In many other languages or using OS tools (like `unzip`), this manual extraction flaw is the default behavior.
            for info in z.infolist():
                # No validation!
                target_path = os.path.join(UPLOAD_FOLDER, info.filename)
                
                # If info.filename is '../../hacked.txt', os.path.join resolves it upward
                # We write the file directly.
                target_dir = os.path.dirname(target_path)
                if target_dir:
                    os.makedirs(target_dir, exist_ok=True)
                    
                if not info.is_dir():
                    with open(target_path, 'wb') as f:
                        f.write(z.read(info.filename))
            
            # Check if our specific test payload wrote outside the directory
            if os.path.exists('/tmp/hacked.txt'):
                return render_template('index.html', message="Archive extracted. (Vulnerable to Zip Slip! Detected /tmp/hacked.txt)", title="Vulnerable Archive Upload")
                
            return render_template('index.html', message="Archive extracted. (Vulnerable to Zip Slip!)", title="Vulnerable Archive Upload")
            
    except zipfile.BadZipFile:
        return render_template('index.html', error="Invalid ZIP archive", title="Vulnerable Archive Upload")
    except Exception as e:
        return render_template('index.html', error=f"Extraction error: {e}", title="Vulnerable Archive Upload")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
