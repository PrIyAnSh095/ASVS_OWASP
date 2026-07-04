# curl Verification

Use curl to retrieve endpoints and inspect headers.

## Secure application

```bash
curl -i http://localhost:5000/json
curl -i http://localhost:5000/html
curl -i http://localhost:5000/xml
curl -i http://localhost:5000/text
```

## Vulnerable application

```bash
curl -i http://localhost:5001/json
curl -i http://localhost:5001/html
curl -i http://localhost:5001/xml
curl -i http://localhost:5001/text
```

## Expected output examples

Secure `json` response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
...
{ "status": "secure", "message": "application/json with charset=UTF-8" }
```

Vulnerable `json` response:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
...
{ "status": "vulnerable", "message": "JSON returned with text/html" }
```

Inspect the first response header line and confirm the `Content-Type` value matches the body format.
