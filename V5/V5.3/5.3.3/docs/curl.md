# cURL Testing

Test the Zip Slip vulnerability from the command line:

**Upload a malicious Zip Slip archive:**
```bash
curl -F "file=@assets/sample-files/zip-slip.zip" http://localhost:5000/upload
```

**Expected Results:**
- Vulnerable app: The file extracts outside the `/tmp/uploads` directory. For demonstration, we track if a file was written to `/tmp/hacked.txt`.
- Secure app: The server rejects the archive with a validation message.
