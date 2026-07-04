from flask import Flask, request, render_template
from PIL import Image, UnidentifiedImageError
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Secure limits
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB
MAX_WIDTH = 2048
MAX_HEIGHT = 2048
MAX_PIXELS = MAX_WIDTH * MAX_HEIGHT

@app.route('/')
def index():
    return render_template('index.html', title="Secure Image Upload")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Secure Image Upload")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", title="Secure Image Upload")
    
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file_length > MAX_FILE_SIZE:
        return render_template('index.html', error="File size exceeds limit", title="Secure Image Upload")

    try:
        # Pillow's Image.open reads metadata without fully decoding the image data
        # This is safe to do for checking dimensions
        img = Image.open(file)
        
        # ASVS 5.2.6: Verify pixel dimensions do not exceed configured maximum
        width, height = img.size
        total_pixels = width * height
        
        if width > MAX_WIDTH or height > MAX_HEIGHT or total_pixels > MAX_PIXELS:
            return render_template('index.html', 
                                   error=f"FAIL: Image dimensions ({width}x{height}) exceed the maximum allowed ({MAX_WIDTH}x{MAX_HEIGHT}).", 
                                   title="Secure Image Upload")
        
        # If dimensions are safe, proceed with processing/saving
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        # Note: We must reset the file pointer before saving or use the Image object
        img.save(filepath)
        return render_template('index.html', message=f"PASS: Image securely validated and saved. Dimensions: {width}x{height}", title="Secure Image Upload")

    except UnidentifiedImageError:
        return render_template('index.html', error="Invalid image format", title="Secure Image Upload")
    except Exception as e:
        return render_template('index.html', error=f"Error processing image: {str(e)}", title="Secure Image Upload")

if __name__ == '__main__':
    # Pillow config to prevent decompression bomb attacks intrinsically, but we handle it manually above as per ASVS requirements.
    Image.MAX_IMAGE_PIXELS = None # Disabled to demonstrate our custom check
    app.run(host='0.0.0.0', port=5000)
