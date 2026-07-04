# Expected Results

## PASS (Secure)

- Content-Length is correct.
- Response body matches declared length.
- RFC 9112 compliant.
- No truncation.
- No extra bytes.
- Proxy can safely forward without desynchronization.

## FAIL (Vulnerable)

- Content-Length is incorrect.
- Response body does not match declared length.
- RFC 9112 non-compliant.
- Possible truncation or oversized declaration.
- Proxy becomes desynchronized.
- Risk of cache poisoning or request smuggling.
