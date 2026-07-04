# Burp Suite Testing

## Capturing Responses

1. Enable Burp Proxy.
2. Navigate to `http://localhost:5000` (secure) or `http://localhost:5001` (vulnerable).
3. Click "Generate Response".
4. Inspect the response in Burp's Response tab.

## Inspecting Content-Length

1. In the Response tab, look for the `Content-Length` header.
2. Select the response body.
3. Burp shows the body byte count at the bottom.
4. Compare:
   - Declared Content-Length (in header)
   - Actual body length (shown by Burp)

## Secure Lab Verification

- Open Burp Repeater.
- Send a request to `http://localhost:5000/generate`.
- Inspect response headers.
- Content-Length matches body length exactly.
- Status: PASS

## Vulnerable Lab Verification

- Open Burp Repeater.
- Send a request to `http://localhost:5001/generate`.
- Inspect response headers.
- Content-Length does NOT match body length.
- Status: FAIL

## Side-by-side Comparison

Generate the same response type from both labs in Burp.
- Secure: Correct Content-Length
- Vulnerable: Incorrect Content-Length

This demonstrates why ASVS 4.2.2 compliance is mandatory.
