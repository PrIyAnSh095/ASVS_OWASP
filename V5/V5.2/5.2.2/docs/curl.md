# Testing with cURL

You can use cURL to quickly push mislabeled files to the server.

```bash
# 1. Create a fake image (actually text)
echo '<?php echo "Test"; ?>' > evil.jpg

# 2. Upload it to the server
curl -F "file=@evil.jpg" http://localhost:5000/upload
```

**Expected Result (Secure App):**
Rejects the file: `Magic Byte mismatch! Extension claims 'jpg' (image/jpeg), but content is 'text/plain' or 'text/x-php'.`

**Expected Result (Vulnerable App):**
Accepts the file successfully.
