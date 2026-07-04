from flask import Flask, request, render_template
import zipfile
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = '/tmp/uploads'
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
    
    if file and file.filename.endswith('.zip'):
        try:
            with zipfile.ZipFile(file) as z:
                # VULNERABILITY: Extracting without inspecting for symlinks.
                # In a real vulnerable scenario, developers might use shell commands like `unzip`
                # which preserve symlinks natively. For demonstration, we just extract.
                z.extractall(UPLOAD_FOLDER)
                return render_template('index.html', message="Archive extracted successfully (Vulnerable to symlinks!).", title="Vulnerable Archive Upload")
        except zipfile.BadZipFile:
            return render_template('index.html', error="Invalid ZIP file", title="Vulnerable Archive Upload")
    
    return render_template('index.html', error="Only ZIP files are allowed", title="Vulnerable Archive Upload")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
