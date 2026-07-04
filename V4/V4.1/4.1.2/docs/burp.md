# Burp Suite Verification

## 1. Configure Burp Proxy

1. Open Burp Suite.
2. Go to Proxy > Options and confirm the listener is active on `127.0.0.1:8080`.
3. Configure your browser or curl to use Burp as the HTTP proxy.

## 2. Capture the request

1. In your browser, navigate to `http://localhost:5000/` for the secure lab.
2. Capture the request in Burp Proxy > HTTP history.
3. Repeat the same for `http://localhost:5000/api/profile`.

## 3. Send to Repeater

1. Right-click the captured request and choose `Send to Repeater`.
2. In Repeater, select the request and click Send.

## 4. Inspect the response

1. In Repeater, select the response tab.
2. Review the status code and headers.
3. For `/`, verify the response is a redirect and includes `Location: https://...`.
4. For `/api/profile`, verify the response is `403 Forbidden` and does not include a `Location` header.

## 5. Verify redirect status

Secure lab:

- `/` should return `302 Found` with `Location: https://...`
- `/api/*` should return `403 Forbidden`

Vulnerable lab:

- `/` should return `302 Found` with `Location: https://...`
- `/api/*` should return `307 Temporary Redirect` with `Location: https://...`

## 6. Compare secure vs vulnerable

1. Repeat the same requests against `http://localhost:5001`.
2. Compare the response codes and headers.
3. Confirm the vulnerable response sends API requests through a redirect.
