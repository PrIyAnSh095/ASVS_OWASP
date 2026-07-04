# Burp Suite Testing

1. Capture a legitimate request to the secure app.
2. Send the request to Repeater.
3. Modify the request body fields such as `amount` or `recipient`.
4. Leave `X-Signature` unchanged.
5. Re-send the request.

Secure behavior:
- Request is rejected with `403 Forbidden` or `401 Unauthorized`.

Vulnerable behavior:
- Request is accepted and processed.

Repeat by removing the `X-Signature` header or replacing it with random data.
Secure app should reject the request; vulnerable app should still accept it.
