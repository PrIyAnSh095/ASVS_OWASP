from flask import Flask, render_template, request
import zipfile
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # 5MB compressed max

MAX_UNCOMPRESSED_SIZE = 5 * 1024 * 1024 # 5 MB uncompressed max
MAX_FILES = 10 # Max files inside archive

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
        
    if not file.filename.endswith('.zip') and not file.filename.endswith('.docx'):
        return render_template('index.html', message="Only ZIP or DOCX allowed.", success=False)

    try:
        total_size = 0
        total_files = 0
        
        # Open the zip file to read headers ONLY. No extraction happens yet.
        with zipfile.ZipFile(file, 'r') as zf:
            for info in zf.infolist():
                total_files += 1
                total_size += info.file_size
                
                if total_files > MAX_FILES:
                    return render_template('index.html', message=f"Archive contains too many files (Limit: {MAX_FILES}). Rejected.", success=False)
                if total_size > MAX_UNCOMPRESSED_SIZE:
                    return render_template('index.html', message=f"Archive is too large when uncompressed (Limit: 5MB). Rejected to prevent Zip Bombs.", success=False)
            
            # If we get here, the archive is safe to extract.
            # zf.extractall(path="/tmp/extracted")
            return render_template('index.html', message=f"Archive validated successfully! Contains {total_files} files, {total_size} bytes uncompressed. (Extraction skipped for lab safety).", success=True)
            
    except zipfile.BadZipFile:
        return render_template('index.html', message="Corrupted or invalid ZIP archive.", success=False)
    except Exception as e:
        return render_template('index.html', message=f"Error: {str(e)}", success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
