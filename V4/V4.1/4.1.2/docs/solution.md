# ASVS 4.1.2 Solution

## Secure implementation

The secure application follows the ASVS control by differentiating browser and API behavior.

- `/` redirects HTTP requests to `https://`.
- `/api/login` returns `403 Forbidden` for HTTP requests.
- `/api/profile` returns `403 Forbidden` for HTTP requests.
- `/api/data` returns `403 Forbidden` for HTTP requests.

API endpoints never perform transparent redirects. The secure app requires the client to retry using HTTPS.

## Vulnerable implementation

The vulnerable application intentionally fails ASVS 4.1.2.

- `/` redirects HTTP to HTTPS.
- `/api/login` redirects HTTP to HTTPS using `307 Temporary Redirect`.
- `/api/profile` redirects HTTP to HTTPS.
- `/api/data` redirects HTTP to HTTPS.

This demonstrates how API credentials or sensitive payloads can be transmitted over HTTP before the redirect completes.

## Verification

1. Request `http://localhost:5000/` and observe a browser redirect.
2. Request `http://localhost:5000/api/login` and observe `403 Forbidden`.
3. Request `http://localhost:5001/api/login` and observe a `307` redirect.
4. Compare the secure and vulnerable responses to see the difference in API handling.
