# Burp Suite Testing

To test for Path Traversal vulnerabilities via Burp Suite:

1. **Upload Payload**: Attempt to upload a file but intercept the POST request.
2. **Modify Filename**: Change the `filename` parameter (or the custom filename field) to `../../../app.py`.
3. **Analyze Response**:
    - Vulnerable app: Accepts the path and overwrites `app.py`, or allows reading it if it's a download endpoint.
    - Secure app: Rejects the upload or sanitizes the filename to just `app.py` (or generates a random UUID), preventing traversal.
