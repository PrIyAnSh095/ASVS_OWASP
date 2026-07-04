from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', title="Secure File Upload", files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Secure File Upload", files=os.listdir(app.config['UPLOAD_FOLDER']))
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", title="Secure File Upload", files=os.listdir(app.config['UPLOAD_FOLDER']))
    
    # Save the file. We do not restrict extensions here to prove the storage is secure.
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return render_template('index.html', message="PASS: File uploaded.", title="Secure File Upload", files=os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # ASVS 5.3.1: Verify files are never executed as server-side code.
    # Flask send_from_directory serves files statically.
    # We use as_attachment=True to ensure it's treated as data and downloaded,
    # preventing even client-side execution (XSS via HTML uploads).
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
