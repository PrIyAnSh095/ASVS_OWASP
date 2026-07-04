# Burp Suite Testing

To test for Pixel Flood vulnerabilities via Burp Suite:

1. **Create Malicious Image**: Generate a PNG/JPG with extremely large dimensions but small file size.
2. **Intercept Upload**: Upload the image and intercept the POST request in Burp Suite.
3. **Analyze Response**:
    - Vulnerable app: Accepts the file, may hang, or eventually return an error after consuming excessive memory.
    - Secure app: Immediately returns a validation error such as "Image dimensions exceed the allowed maximum" without processing the image.
