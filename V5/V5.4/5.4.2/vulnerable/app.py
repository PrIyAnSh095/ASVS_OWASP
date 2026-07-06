import os
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, send_file, Response, abort

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Root directory containing safe files to download
FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'files'))

@app.route('/')
def index():
    # Make sure target directory exists
    os.makedirs(FILES_DIR, exist_ok=True)
    files = os.listdir(FILES_DIR)
    return render_template('index.html', mode='Vulnerable', files=files)

@app.route('/download', methods=['GET', 'POST'])
def download():
    # Get user-supplied custom filename parameter or fall back
    filename_param = request.args.get('filename') or request.form.get('filename') or 'sample.pdf'
    
    # Locate actual source file to serve
    source_file = request.args.get('source') or request.form.get('source') or 'sample.pdf'
    
    # Locate target file path - use realpath containment check
    target_path = os.path.realpath(os.path.join(FILES_DIR, source_file))
    if not target_path.startswith(FILES_DIR + os.sep) and target_path != FILES_DIR:
        abort(403, "Access denied.")
    if not os.path.exists(target_path) or os.path.isdir(target_path):
        abort(404, "Requested file not found or access denied.")

    with open(target_path, 'rb') as f:
        file_content = f.read()

    # VULNERABLE: Direct string interpolation of the user-supplied parameter into Content-Disposition
    # This allows CRLF injection, response splitting, header injection, and malformed header structures.
    response = Response(file_content, mimetype='application/octet-stream')
    
    # Dangerous direct interpolation!
    # Under standard HTTP servers/libraries, this will output CRLF directly if the library permits,
    # or crash the header parser, or result in arbitrary headers being injected.
    response.headers['Content-Disposition'] = f"attachment; filename={filename_param}"
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
