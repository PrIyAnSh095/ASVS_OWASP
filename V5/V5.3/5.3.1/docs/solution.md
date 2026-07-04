# Solution

To securely serve user-uploaded files according to ASVS 5.3.1:

1. Never store uploaded files inside the web root if direct access is not required.
2. If direct HTTP access is required, serve the files via a dedicated endpoint that forces static delivery.
3. Use headers like `Content-Type: application/octet-stream` or `Content-Disposition: attachment` to prevent execution and inline rendering of active content.

```python
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # as_attachment=True forces download, preventing browser execution of HTML/JS
    # The framework ensures it is served statically, preventing server-side execution
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
```
