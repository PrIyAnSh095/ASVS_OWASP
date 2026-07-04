from flask import Flask, render_template, request
import os

app = Flask(__name__)
# VULNERABILITY: No documentation provided to the user or developer.
# The backend might arbitrarily enforce limits, but the lack of documentation violates ASVS 5.1.1.
# Here we just allow pretty much anything under 50MB without telling the user.
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 

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
        
    # Unclear policy: We silently reject .exe but don't tell the user.
    if file.filename.endswith('.exe'):
        return render_template('index.html', message="Upload failed.", success=False)
        
    return render_template('index.html', message="File uploaded successfully.", success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
