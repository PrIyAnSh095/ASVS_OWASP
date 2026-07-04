# Testing with cURL

cURL is the easiest way to demonstrate this vulnerability by sending a genuinely large file.

## Testing Size Limits
We will generate a 250MB dummy file and attempt to upload it.

```bash
# Create a 250MB dummy file (Linux/macOS)
dd if=/dev/zero of=huge.txt bs=1M count=250

# Attempt upload
curl -F "file=@huge.txt" http://localhost:5000/upload
```

**Expected Result (Secure App):**
The connection terminates almost instantly with an HTTP 413 error.

**Expected Result (Vulnerable App):**
The file uploads entirely. If using the provided `docker-compose.yml` (which limits the container to 200MB RAM), the container will likely crash with an OOM (Out Of Memory) error and return a connection reset or 502 Bad Gateway.
