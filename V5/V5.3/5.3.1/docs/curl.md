# cURL Testing

Test the upload and execution functionality from the command line:

**Upload the payload:**
```bash
curl -F "file=@assets/sample-files/test.py" http://localhost:5000/upload
```

**Access the uploaded file:**
```bash
curl http://localhost:5000/uploads/test.py
```

**Expected Results:**
- Vulnerable app: You will see the executed output of the script.
- Secure app: You will see the raw source code of the script, or it will be downloaded.
