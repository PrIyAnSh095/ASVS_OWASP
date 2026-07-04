from flask import Flask, request, render_template, send_file, abort
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '/tmp/vulnerable_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    files = {}
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f)):
            files[f] = f
    return render_template('index.html', title="Vulnerable File Upload", files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Vulnerable File Upload")
    
    file = request.files['file']
    # Attacker can supply a custom filename via the form to bypass browser restrictions
    custom_filename = request.form.get('filename')
    
    filename = custom_filename if custom_filename else file.filename
    
    if not filename:
        return render_template('index.html', error="No selected file", title="Vulnerable File Upload")
    
    # VULNERABILITY: Trusting user-supplied filename directly for storage.
    # In Python, os.path.join('/tmp', '/etc/passwd') becomes '/etc/passwd'.
    # This allows arbitrary file write.
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
    except Exception as e:
        return render_template('index.html', error=f"Write error: {e}", title="Vulnerable File Upload")
        
    return render_template('index.html', message="File uploaded successfully (Vulnerable to Path Traversal!).", title="Vulnerable File Upload")

@app.route('/download')
def download():
    # VULNERABILITY: Trusting user-supplied filename directly for reading.
    # This allows Local File Inclusion (LFI) / Path Traversal reading.
    filename = request.args.get('id')
    if not filename:
        abort(400)
        
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
