# Expected Results

## PASS

- Request includes `X-Signature`.
- Signature is verified using HMAC-SHA256.
- Tampered payloads are rejected.
- Invalid signatures are rejected.
- Missing signatures are rejected.

## FAIL

- Missing signatures accepted.
- Invalid signatures accepted.
- Tampered requests processed.
- Request integrity not verified.
