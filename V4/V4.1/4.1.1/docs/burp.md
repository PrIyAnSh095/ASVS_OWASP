# Burp Suite Verification

## 1. Configure Burp Proxy

1. Open Burp Suite.
2. In Proxy > Options, confirm the listener is active on `127.0.0.1:8080`.
3. Configure your browser or system proxy to use `127.0.0.1:8080` for HTTP.

## 2. Capture the request

1. Open the browser and visit the secure endpoint:
   - `http://localhost:5000/json`
2. Ensure the request appears in Burp Proxy > HTTP history.

## 3. Send to Repeater

1. Right-click the request in HTTP history.
2. Choose `Send to Repeater`.
3. Switch to the Repeater tab.

## 4. Inspect the HTTP response

1. In Repeater, resend the request.
2. Select the response panel.
3. Review the response headers and payload.

## 5. Verify the Content-Type header

For the secure application, confirm:

- `Content-Type: application/json; charset=UTF-8`
- `Content-Type: text/html; charset=UTF-8`
- `Content-Type: application/xml; charset=UTF-8`
- `Content-Type: text/plain; charset=UTF-8`

For the vulnerable application, some responses should deliberately fail:

- JSON returned as `text/html`
- HTML returned as `text/plain`
- Missing `charset=UTF-8`
- Incorrect MIME type for XML

## 6. Compare secure vs vulnerable

1. Repeat the same request against `http://localhost:5001` for the vulnerable app.
2. Notice header differences in Repeater.
3. Confirm the vulnerable response bodies do not align with the declared `Content-Type`.
