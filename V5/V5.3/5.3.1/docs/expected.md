# Expected Results

### Vulnerable Implementation
- Simulates an insecure web server configuration (like a misconfigured Apache/PHP setup).
- If a `.py` file is requested from the `/uploads/` directory, the server executes the script and returns the output.
- This demonstrates a critical Remote Code Execution (RCE) vulnerability.

### Secure Implementation
- Stores files in a directory that explicitly lacks execution context.
- When any file is requested, the application forces a safe MIME type or uses `Content-Disposition: attachment` to ensure the browser treats it as data, not code.
- Executable files remain harmless data blobs.
