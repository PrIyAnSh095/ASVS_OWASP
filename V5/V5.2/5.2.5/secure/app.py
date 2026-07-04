from flask import Flask, request, render_template
import zipfile
import os
import stat

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    
    if file and file.filename.endswith('.zip'):
        try:
            with zipfile.ZipFile(file) as z:
                # ASVS 5.2.5: Verify that the application does not allow uploading compressed files containing symbolic links.
                for info in z.infolist():
                    # Extract the upper 16 bits of external_attr to get the file type
                    mode = info.external_attr >> 16
                    if stat.S_ISLNK(mode):
                        return render_template('index.html', error="FAIL: Archive contains symbolic links which are not allowed.", title="Secure Archive Upload")
                
                # Safe to extract
                z.extractall(UPLOAD_FOLDER)
                return render_template('index.html', message="PASS: Archive safely extracted.", title="Secure Archive Upload")
        except zipfile.BadZipFile:
            return render_template('index.html', error="Invalid ZIP file", title="Secure Archive Upload")
    
    return render_template('index.html', error="Only ZIP files are allowed", title="Secure Archive Upload")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
