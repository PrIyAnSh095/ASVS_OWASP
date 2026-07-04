from flask import Flask, request, render_template
from PIL import Image, UnidentifiedImageError
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Vulnerable: Validates ONLY file size
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB

@app.route('/')
def index():
    return render_template('index.html', title="Vulnerable Image Upload")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Vulnerable Image Upload")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", title="Vulnerable Image Upload")
    
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    # VULNERABILITY: Only checking file size, not image dimensions
    if file_length > MAX_FILE_SIZE:
        return render_template('index.html', error="File size exceeds limit", title="Vulnerable Image Upload")

    try:
        # VULNERABILITY: Fully decoding the image without checking dimensions first
        img = Image.open(file)
        img.load() # Force loading the image data into memory (simulating processing)
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        img.save(filepath)
        
        return render_template('index.html', message=f"Image processed successfully. (Vulnerable to Pixel Flood!)", title="Vulnerable Image Upload")
        
    except UnidentifiedImageError:
        return render_template('index.html', error="Invalid image format", title="Vulnerable Image Upload")
    except Exception as e:
        return render_template('index.html', error=f"Error processing image: {str(e)}", title="Vulnerable Image Upload")

if __name__ == '__main__':
    # Disable Pillow's internal decompression bomb protection to demonstrate the vulnerability
    Image.MAX_IMAGE_PIXELS = None 
    app.run(host='0.0.0.0', port=5000)
