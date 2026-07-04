# Burp Suite Testing

To test for symlink vulnerabilities via Burp Suite:

1. **Create Malicious Archive**: Generate a ZIP file containing a symlink (on Linux/macOS: `ln -s /etc/passwd link.txt && zip --symlinks payload.zip link.txt`).
2. **Intercept Upload**: Upload `payload.zip` and intercept the POST request.
3. **Analyze Response**: 
    - If the server accepts and extracts it, attempt to access the extracted file. 
    - If it returns the contents of `/etc/passwd`, it's vulnerable (FAIL).
    - If the server rejects the upload stating "Symlinks are not allowed", it's secure (PASS).
