from flask import Flask, render_template, request
import os

app = Flask(__name__)
# Global system limit just to prevent immediate RAM crash in the lab
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 

# Per-User Config
LIMITS = {
    'max_files': 3,
    'max_storage': 100 * 1024 # 100 KB total storage per user
}

# In-memory mock database
db = {}

def get_user_quota(username):
    if username not in db:
        db[username] = {'file_count': 0, 'storage_used': 0}
    return db[username]

@app.route('/')
def index():
    username = request.args.get('username', 'user1')
    quota = get_user_quota(username)
    return render_template('index.html', username=username, quota=quota, limits=LIMITS)

@app.route('/upload', methods=['POST'])
def upload_file():
    username = request.form.get('username', 'user1')
    quota = get_user_quota(username)
    
    if 'file' not in request.files:
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message="No file part", success=False)
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message="No selected file", success=False)
        
    # Read file to determine exact size (or use seek/tell)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    # Validation 1: Max File Count
    if quota['file_count'] >= LIMITS['max_files']:
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message="Quota Exceeded: You have reached the maximum number of allowed files (3).", success=False)
        
    # Validation 2: Max Storage Limit
    if quota['storage_used'] + file_size > LIMITS['max_storage']:
        return render_template('index.html', username=username, quota=quota, limits=LIMITS, message=f"Quota Exceeded: Uploading this file ({file_size} bytes) would exceed your 100 KB limit.", success=False)
        
    # Validation 3: Individual File Size Limit (Implicitly covered by storage quota, but can be checked separately)
    # Passed all checks, update DB
    quota['file_count'] += 1
    quota['storage_used'] += file_size
    
    return render_template('index.html', username=username, quota=quota, limits=LIMITS, message=f"File {file.filename} uploaded successfully!", success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
