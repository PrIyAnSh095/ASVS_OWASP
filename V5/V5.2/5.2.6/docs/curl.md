# cURL Testing

Test the image upload functionality from the command line:

**Upload a normal image:**
```bash
curl -F "file=@assets/sample-files/normal.jpg" http://localhost:5000/upload
```

**Upload an oversized dimension image:**
```bash
curl -F "file=@assets/sample-files/10000x10000.png" http://localhost:5000/upload
```

**Expected Results:**
- Vulnerable app: Processes the oversized image (may fail or take a long time).
- Secure app: Immediately rejects the oversized image.
