import os
import re
from urllib.parse import quote
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, send_file, Response, abort
# pyrefly: ignore [missing-import]
from werkzeug.utils import safe_join

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Root directory containing safe files to download
FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'files'))

@app.route('/')
def index():
    # Make sure target directory exists
    os.makedirs(FILES_DIR, exist_ok=True)
    files = os.listdir(FILES_DIR)
    return render_template('index.html', mode='Secure', files=files)

@app.route('/download', methods=['GET', 'POST'])
def download():
    # Get user-supplied custom filename parameter or fall back
    filename_param = request.args.get('filename') or request.form.get('filename') or 'sample.pdf'
    
    # Locate actual source file to serve
    source_file = request.args.get('source') or request.form.get('source') or 'sample.pdf'
    
    # 1. Path Traversal Mitigation: Safe join to ensure target is within FILES_DIR
    target_path = safe_join(FILES_DIR, source_file)
    if not target_path or not os.path.exists(target_path) or os.path.isdir(target_path):
        abort(404, "Requested file not found or access denied.")

    # 2. Header Injection Mitigation (CRLF Mitigation):
    # Strip carriage returns and line feeds to prevent HTTP Response Splitting / Header Injection.
    sanitized_filename = re.sub(r'[\r\n]', '', filename_param)
    
    # 3. Filename Sanitization & RFC 6266 Encoding:
    # RFC 6266 defines filename* parameter using RFC 5987 encoding (UTF-8 URL-encoded).
    # We define a plain filename parameter with safe characters, and filename* for modern browsers.
    
    # Format fallback filename: Strip quotes, backslashes, and replace non-ASCII characters to avoid parser issues
    ascii_safe_filename = sanitized_filename.encode('ascii', errors='ignore').decode('ascii')
    ascii_safe_filename = ascii_safe_filename.replace('"', '').replace('\\', '_')
    if not ascii_safe_filename.strip():
        ascii_safe_filename = "download.pdf"
        
    # URL encode filename for filename* according to RFC 5987/6266
    utf8_encoded_filename = quote(sanitized_filename)
    
    # Build Content-Disposition header conforming to RFC 6266
    content_disposition = f"attachment; filename=\"{ascii_safe_filename}\"; filename*=UTF-8''{utf8_encoded_filename}"

    # Read binary file data and construct the response
    with open(target_path, 'rb') as f:
        file_content = f.read()

    response = Response(file_content, mimetype='application/octet-stream')
    response.headers['Content-Disposition'] = content_disposition
    
    # Ensure browsers don't sniff the content type
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
