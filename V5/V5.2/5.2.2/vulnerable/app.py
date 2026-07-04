from flask import Flask, render_template, request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    # VULNERABILITY: Only checking the string extension of the filename.
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

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
        
    # No magic byte check. No MIME verification. No content rewriting.
    if file and allowed_file(file.filename):
        # The file is accepted blindly!
        return render_template('index.html', message=f"File {file.filename} uploaded successfully.", success=True)
    else:
        return render_template('index.html', message="Invalid extension.", success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
