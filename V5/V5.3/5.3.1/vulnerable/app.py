from flask import Flask, request, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', title="Vulnerable File Upload", files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", title="Vulnerable File Upload", files=os.listdir(app.config['UPLOAD_FOLDER']))
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", title="Vulnerable File Upload", files=os.listdir(app.config['UPLOAD_FOLDER']))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return render_template('index.html', message="File uploaded successfully.", title="Vulnerable File Upload", files=os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # VULNERABILITY: Simulating an insecure web server configuration (like Apache + mod_php or CGI).
    # If a file has a .py extension, the server executes it instead of serving it as static data.
    if filename.endswith('.py'):
        try:
            # Simulate server-side execution
            result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=5)
            return f"<pre>Executing {filename}:\n\n{result.stdout}\n{result.stderr}</pre>"
        except Exception as e:
            return str(e)
            
    # For non-executable files, serve normally
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
