# Command Line Testing with curl

The `curl` command-line tool is excellent for verifying how the server formats raw response headers and handles non-ASCII or malicious file parameters.

## Testing the Secure Implementation (Port 5000)

### 1. Basic Download Request
Request a standard filename:
```bash
curl -I "http://localhost:5000/download?source=sample.pdf&filename=normal.pdf"
```
**Expected Response:**
```http
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="normal.pdf"; filename*=UTF-8''normal.pdf
X-Content-Type-Options: nosniff
```

### 2. spaces and Quotes Payload
Request a filename containing spaces and quotes:
```bash
curl -I "http://localhost:5000/download?source=sample.pdf&filename=report%202025%22.pdf"
```
**Expected Response:**
```http
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="report 2025.pdf"; filename*=UTF-8''report%202025%22.pdf
```
*Note: The ASCII-fallback strip the quotes, and the `filename*` preserves the full URL-encoded UTF-8 string.*

### 3. CRLF Injection Attempt
Send a CRLF injection payload:
```bash
curl -I "http://localhost:5000/download?source=sample.pdf&filename=test%0d%0aX-Test:Injected"
```
**Expected Response:**
```http
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="testX-Test:Injected"; filename*=UTF-8''test%0D%0AX-Test%3AInjected
```
The raw CRLF sequence was stripped or escaped, ensuring it stays within the header body value. No new header called `X-Test` was created.

---

## Testing the Vulnerable Implementation (Port 5001)

### 1. Raw Payload
Send the CRLF payload to the vulnerable endpoint:
```bash
curl -I "http://localhost:5001/download?source=sample.pdf&filename=test%0d%0aX-Test:Injected"
```
**Observed Response:**
Depending on curl's HTTP parser tolerance, you will see the injected header explicitly listed:
```http
HTTP/1.1 200 OK
Content-Disposition: attachment; filename=test
X-Test: Injected
```
This confirms that the header structure has been broken and a new header was successfully injected.
