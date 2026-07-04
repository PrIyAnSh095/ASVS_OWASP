# Burp Suite Testing

To test for insecure download handling via Burp Suite:

1. **Intercept Download Request**: Click download and intercept the GET request.
2. **Modify Filename Parameter**: Change the `filename` parameter to `../../../../etc/passwd` or `../../../secret.txt`.
3. **Analyze Response**:
    - Vulnerable app: Returns the contents of `/etc/passwd`. The `Content-Disposition` header may also reflect the traversal payload.
    - Secure app: Ignores the user-supplied filename. Instead, it relies on an internal database ID or UUID, and sets the `Content-Disposition` header using a safe, server-side mapping.
