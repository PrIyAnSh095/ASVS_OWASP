# Burp Suite Verification

Burp Suite can be used to manually verify the presence of CRLF and header injection vulnerabilities in the vulnerable application, as well as confirm defense-in-depth on the secure application.

## Intercepting the Request

1. Launch Burp Suite and configure your browser proxy to point to Burp (default `127.0.0.1:8080`).
2. Navigate to the vulnerable application page (e.g., `http://localhost:5001/`).
3. Click "Select" next to one of the sample files.
4. Input the following payload in the **Desired Filename Header Value** input box:
   `test`
5. Click **Download File** and intercept the request in the Burp Proxy tab.

The request will look like this:
```http
GET /download?source=sample.pdf&filename=test HTTP/1.1
Host: localhost:5001
User-Agent: Mozilla/5.0 ...
```

## Injecting Header via Repeater

Send the intercepted request to **Repeater** (`Ctrl + R`).

Modify the parameters in the request line to inject CRLF characters. In HTTP, we replace `test` with:
`test%0d%0aX-Injected-Header:+True`

Send the request.

### In Vulnerable Implementation (Port 5001):
Observe the raw response headers:
```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=test
X-Injected-Header: True
...
```
The application accepted the raw CRLF characters (`%0d%0a`), leading to response splitting where `X-Injected-Header` was successfully parsed as an independent HTTP header.

### In Secure Implementation (Port 5000):
Send the same payload to the secure application (Port 5000). The server output shows:
```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="testX-Injected-Header:_True"; filename*=UTF-8''testX-Injected-Header%3A%20True
...
```
CRLF characters are stripped or properly URL-encoded (using `%20`, `%3A` in the `filename*` parameter), preventing any response parsing confusion.
