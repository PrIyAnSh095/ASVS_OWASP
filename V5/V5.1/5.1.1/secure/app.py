from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # 2MB limit enforces the documented policy

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # In a real app, we would save to /tmp/uploads and trigger the documented malware scan
        return render_template('index.html', message=f"File {file.filename} uploaded and queued for malware scanning (simulated).", success=True)
    else:
        return render_template('index.html', message="Invalid file extension. Please review the File Upload Policy.", success=False)

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', message="File exceeds the documented 2MB maximum upload size.", success=False), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
