from flask import Flask, render_template, request
import zipfile
import os

app = Flask(__name__)
# VULNERABILITY 1: Allowing large uploads just to accept the bomb (though even small ones can be deadly)
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
        
    try:
        # VULNERABILITY 2: Blindly extracting without checking uncompressed size or file count!
        with zipfile.ZipFile(file, 'r') as zf:
            extract_path = os.path.join("/tmp/extracted", file.filename)
            os.makedirs(extract_path, exist_ok=True)
            
            # Extract everything. A zip bomb will cause a massive CPU spike, fill the disk, or crash the process.
            zf.extractall(path=extract_path)
            
            return render_template('index.html', message=f"Archive blindly extracted to {extract_path}!", success=True)
            
    except zipfile.BadZipFile:
        return render_template('index.html', message="Invalid ZIP.", success=False)
    except Exception as e:
        return render_template('index.html', message=f"Extraction crashed (Likely Resource Exhaustion): {str(e)}", success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
