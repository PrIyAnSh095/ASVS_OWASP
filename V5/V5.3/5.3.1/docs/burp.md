# Burp Suite Testing

To test for executable upload vulnerabilities via Burp Suite:

1. **Upload Payload**: Create a payload (e.g., `test.py` containing `print("Hacked")`). Upload the file and intercept the request.
2. **Access the File**: Navigate to the uploaded file's URL (e.g., `/uploads/test.py`).
3. **Analyze Response**:
    - Vulnerable app: The server executes the script and returns the execution output ("Hacked").
    - Secure app: The server downloads the file, or serves it strictly as static text (e.g., `text/plain` with `Content-Disposition: attachment`), without executing it.
