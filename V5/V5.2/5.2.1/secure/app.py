from flask import Flask, render_template, request
import os

app = Flask(__name__)

# SECURE IMPLEMENTATION
# We strictly enforce a maximum upload size.
# Flask/Werkzeug intercepts the Content-Length header and the data stream.
# If the stream exceeds this limit, it aborts the upload and raises a 413 error
# before the application logic ever touches the file, protecting the server from DoS.
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1 MB Limit

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # We process the file safely here, knowing it is <= 1MB
        file_bytes = file.read()
        return render_template('index.html', message=f"File {file.filename} ({len(file_bytes)} bytes) successfully processed.", success=True)
    else:
        return render_template('index.html', message="Invalid file type.", success=False)

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', message="Validation Error: File exceeds the maximum allowed size of 1 MB.", success=False), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
