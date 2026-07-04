from flask import Flask, request, render_template, Response, abort
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '/tmp/vulnerable_downloads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Pre-populate dummy files
with open(os.path.join(app.config['UPLOAD_FOLDER'], 'report.pdf'), 'w') as f:
    f.write("This is a vulnerable report.")
with open(os.path.join(app.config['UPLOAD_FOLDER'], 'invoice.pdf'), 'w') as f:
    f.write("This is a vulnerable invoice.")
    
# Create a secret file outside the upload folder to demonstrate Path Traversal
with open('/tmp/secret.txt', 'w') as f:
    f.write("SUPER SECRET SERVER DATA")

@app.route('/')
def index():
    files = {
        'report.pdf': 'report.pdf',
        'invoice.pdf': 'invoice.pdf'
    }
    return render_template('index.html', title="Vulnerable File Download", files=files, secure=False)

@app.route('/download')
def download():
    # VULNERABILITY: Trusting user-supplied filename from URL parameter
    filename = request.args.get('filename')
    
    if not filename:
        abort(400)
        
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        abort(404, description="File not found")
        
    try:
        with open(filepath, 'rb') as f:
            file_data = f.read()
            
        # VULNERABILITY: Reflecting the user-supplied filename directly into the Content-Disposition header
        # without validation or sanitization.
        response = Response(file_data)
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Type'] = 'application/octet-stream'
        return response
        
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
