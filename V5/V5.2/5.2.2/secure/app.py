from flask import Flask, render_template, request
import magic
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Mapping allowed extensions to their expected MIME types
ALLOWED_TYPES = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'pdf': 'application/pdf',
    'txt': 'text/plain'
}

def secure_process_image(file_stream, ext):
    try:
        # Load the image using Pillow to verify its structure
        img = Image.open(file_stream)
        img.verify() # Verify it is an image
        
        # Reset stream pointer
        file_stream.seek(0)
        img = Image.open(file_stream)
        
        # Safely rewrite the image to an in-memory buffer, stripping malicious EXIF or trailing payloads
        out_stream = BytesIO()
        format = 'JPEG' if ext in ['jpg', 'jpeg'] else 'PNG'
        # Converting to RGB drops alpha channel/metadata in some formats
        img.convert('RGB').save(out_stream, format=format)
        out_stream.seek(0)
        return True, "Image safely rewritten."
    except Exception as e:
        return False, f"Image processing failed (Corrupted/Malicious): {str(e)}"

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
        
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    
    # 1. Extension Validation
    if ext not in ALLOWED_TYPES:
        return render_template('index.html', message="Extension not allowed.", success=False)
        
    # Read file content to check magic bytes
    file_bytes = file.read()
    file.seek(0) # Reset pointer for later use
    
    # 2. Magic Byte Validation (MIME type from content, not the header sent by the user)
    actual_mime = magic.from_buffer(file_bytes, mime=True)
    expected_mime = ALLOWED_TYPES[ext]
    
    if actual_mime != expected_mime:
        details = f"Magic Byte mismatch! Extension claims '{ext}' ({expected_mime}), but content is '{actual_mime}'."
        return render_template('index.html', message="File content does not match extension.", details=details, success=False)
        
    details = f"Magic Byte check passed ({actual_mime}). "
    
    # 3. Safe Rewriting / Content Validation
    if ext in ['jpg', 'jpeg', 'png']:
        success, img_details = secure_process_image(file, ext)
        details += img_details
        if not success:
            return render_template('index.html', message="Invalid Image Content.", details=details, success=False)
    
    return render_template('index.html', message="File safely uploaded and validated!", details=details, success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
