# Verification via Burp Suite

This document describes how to capture and test the upload workflow using Burp Suite to verify secure file quarantine controls.

## Intercepting File Uploads

1. Configure your browser to proxy HTTP traffic through Burp Suite (default: `127.0.0.1:8080`).
2. Navigate to the Secure Lab (`http://localhost:5000`) or Vulnerable Lab (`http://localhost:5001`).
3. Prepare a local test file containing the EICAR test string:
   `X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*`
4. Choose the file in the upload form, enable **Intercept On** in Burp Proxy, and submit.

### Upload Request:
```http
POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=---------------------------1234567890

-----------------------------1234567890
Content-Disposition: form-data; name="file"; filename="eicar.txt"
Content-Type: text/plain

X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
-----------------------------1234567890--
```

## Observing Results

### In Secure Lab (Port 5000):
The response redirecting back to `/` will trigger a flash message indicating:
`File Rejected! Threat identified: Malware Detected`

Check the clean downloads listing. The file `eicar.txt` is missing because it was intercepted in the Quarantine directory and securely purged after scanning.

### In Vulnerable Lab (Port 5001):
The response indicates success:
`File uploaded successfully: eicar.txt`

The file `eicar.txt` immediately appears in the public downloads zone, demonstrating a total failure of upload safety scanning.
