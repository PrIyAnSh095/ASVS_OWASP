# curl Verification

## Secure lab commands

### Browser endpoint
curl -i http://localhost:5000/

Expected output:
- `HTTP/1.1 302 FOUND`
- `Location: https://localhost:5000/`

### API login
curl -i -X POST http://localhost:5000/api/login -H 'Content-Type: application/json' -d '{"username":"student"}'

Expected output:
- `HTTP/1.1 403 FORBIDDEN`
- no `Location` header
- JSON body explains HTTPS is required

### API profile
curl -i http://localhost:5000/api/profile

Expected output:
- `HTTP/1.1 403 FORBIDDEN`
- no redirect

### API data
curl -i http://localhost:5000/api/data

Expected output:
- `HTTP/1.1 403 FORBIDDEN`
- no redirect

## Vulnerable lab commands

### Browser endpoint
curl -i http://localhost:5001/

Expected output:
- `HTTP/1.1 302 FOUND`
- `Location: https://localhost:5001/`

### API login
curl -i -X POST http://localhost:5001/api/login -H 'Content-Type: application/json' -d '{"username":"student"}'

Expected output:
- `HTTP/1.1 307 TEMPORARY REDIRECT`
- `Location: https://localhost:5001/api/login`

### API profile
curl -i http://localhost:5001/api/profile

Expected output:
- `HTTP/1.1 307 TEMPORARY REDIRECT`
- `Location: https://localhost:5001/api/profile`

### API data
curl -i http://localhost:5001/api/data

Expected output:
- `HTTP/1.1 307 TEMPORARY REDIRECT`
- `Location: https://localhost:5001/api/data`
