# Solution

## Secure implementation

- Uses HMAC-SHA256 to sign the request body.
- Rejects missing `X-Signature` with 401.
- Rejects invalid or mismatched signatures with 403.
- Calculates and compares signatures securely.
- Ensures modified request bodies do not pass verification.

## Vulnerable implementation

- Processes requests even without `X-Signature`.
- Accepts invalid signatures.
- Accepts modified request data.
- Skips message integrity verification.
