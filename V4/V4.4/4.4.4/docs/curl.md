# Testing with cURL

You can use cURL to quickly verify if the token issuance endpoint requires an established HTTP session.

## Testing the Transition Endpoint

**Attempt without authentication:**
```bash
curl -i http://localhost:5000/api/ws-token
```
* **Secure App:** Returns `401 Unauthorized` (Must login first).
* **Vulnerable App:** Returns `200 OK` and a `{"token": "..."}`.

**Attempt with authentication (Secure App):**
```bash
# 1. Login and save the session cookie
curl -i -c cookies.txt -X POST -d "username=admin&password=password" http://localhost:5000/login

# 2. Use the cookie to get the WS token
curl -i -b cookies.txt http://localhost:5000/api/ws-token
```
