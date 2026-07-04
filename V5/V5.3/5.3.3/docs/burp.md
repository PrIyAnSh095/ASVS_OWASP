# Burp Suite Testing

To test for Zip Slip vulnerabilities via Burp Suite:

1. **Craft Malicious Archive**: Create a zip file where one entry is named `../../../app.py`.
2. **Upload**: Intercept the upload of this archive.
3. **Analyze Response**:
    - Vulnerable app: Extracts the archive, overwriting `app.py` or another file outside the upload directory. The app might crash or execute the new payload on next run.
    - Secure app: Rejects the archive completely with an error indicating an invalid path.
