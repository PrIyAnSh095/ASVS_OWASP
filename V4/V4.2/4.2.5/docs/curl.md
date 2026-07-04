# Testing with cURL

You can use `curl` to quickly test the application's handling of oversized inputs from the command line.

## Procedure

You can use Python or `printf` to generate a massively long string and pass it to `curl` as form data.

### Testing the Secure Application

```bash
# Generate a 10,000 character 'A' payload for the Authorization header
PAYLOAD=$(python3 -c "print('A' * 10000)")

curl -X POST http://localhost:5000/ \
     -d "uri=/api/data" \
     -d "cookie=session=123" \
     -d "auth=$PAYLOAD" \
     -d "custom_header=test"
```
**Expected Result:** The application should respond immediately with a validation error (e.g., "Authorization header length exceeds maximum allowed").

### Testing the Vulnerable Application

Using the same payload against the vulnerable endpoint:
```bash
curl -X POST http://localhost:5000/ \
     -d "uri=/api/data" \
     -d "cookie=session=123" \
     -d "auth=$PAYLOAD" \
     -d "custom_header=test"
```
**Expected Result:** The vulnerable application will attempt to send this 10,000-character header to the downstream service. The downstream service will likely reject it, causing a 500 Internal Server Error in the vulnerable app due to the downstream failure (e.g., connection reset or HTTP 431).
