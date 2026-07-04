from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db = {}

def get_user_quota(username):
    if username not in db:
        db[username] = {'file_count': 0, 'storage_used': 0}
    return db[username]

@app.route('/')
def index():
    username = request.args.get('username', 'user1')
    quota = get_user_quota(username)
    return render_template('index.html', username=username, quota=quota)

@app.route('/upload', methods=['POST'])
def upload_file():
    username = request.form.get('username', 'user1')
    quota = get_user_quota(username)
    
    if 'file' not in request.files:
        return render_template('index.html', username=username, quota=quota, message="No file part", success=False)
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', username=username, quota=quota, message="No selected file", success=False)
        
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    # VULNERABILITY: No enforcement of quotas! 
    # An attacker can just spam this endpoint in a while loop.
    
    quota['file_count'] += 1
    quota['storage_used'] += file_size
    
    return render_template('index.html', username=username, quota=quota, message=f"File {file.filename} uploaded successfully!", success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
