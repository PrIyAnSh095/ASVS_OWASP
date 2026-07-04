# Testing with cURL

You can use cURL to test if the backend enforces the documented file size limits.

## Testing Size Limits
Attempt to upload a 3MB file to an endpoint documented to only accept 2MB.

```bash
# Create a 3MB dummy file
dd if=/dev/zero of=large_file.txt bs=1M count=3

# Attempt upload
curl -F "file=@large_file.txt" http://localhost:5000/upload
```

**Expected Result (Secure App):** The server returns an HTTP 413 Payload Too Large, confirming the documented 2MB limit is enforced.
