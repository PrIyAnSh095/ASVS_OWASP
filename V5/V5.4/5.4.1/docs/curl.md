# cURL Testing

Test the download vulnerability from the command line:

**Attempt to download a sensitive file using Path Traversal:**
```bash
curl -i "http://localhost:5000/download?filename=../../../etc/passwd"
```

**Expected Results:**
- Vulnerable app: The HTTP headers (`-i` flag) will show the reflected `Content-Disposition: attachment; filename=../../../etc/passwd` and the body will contain the file contents.
- Secure app: Rejects the request, as it ignores arbitrary filename parameters and only accepts a valid UUID.
