# Solution

To securely handle file downloads according to ASVS 5.4.1:

1. Use an internal identifier (UUID or DB ID) to request the download, NOT the filename.
2. Maintain a server-side mapping of the ID to the safe filename.
3. Explicitly set the `Content-Disposition` header with the safe filename.

```python
@app.route('/download')
def download():
    file_id = request.args.get('id')
    # Lookup file metadata based on ID
    file_meta = get_metadata(file_id)
    if not file_meta:
        abort(404)
        
    # Safe internal path
    safe_path = os.path.join(UPLOAD_DIR, file_id)
    # Safe filename for Content-Disposition
    safe_filename = file_meta['original_name']
    
    return send_file(safe_path, as_attachment=True, download_name=safe_filename)
```
