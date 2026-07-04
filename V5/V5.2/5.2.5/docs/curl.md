# cURL Testing

You can use `curl` to test the archive upload functionality from the command line.

**Upload a normal ZIP:**
```bash
curl -F "file=@assets/sample-files/normal.zip" http://localhost:5000/upload
```

**Upload a symlink ZIP:**
```bash
curl -F "file=@assets/sample-files/symlink.zip" http://localhost:5000/upload
```

**Expected Results:**
- Vulnerable app: Accepts both files.
- Secure app: Rejects `symlink.zip`.
