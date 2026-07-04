# Expected Results

## PASS criteria

| Endpoint | Secure behavior | Expected status | Expected header | Notes |
| --- | --- | --- | --- | --- |
| `/` | Redirects from HTTP to HTTPS | `302` | `Location: https://...` | Browser-facing page redirects correctly |
| `/api/login` | Rejects HTTP requests | `403` | no `Location` | Credentials are not auto-upgraded |
| `/api/profile` | Rejects HTTP requests | `403` | no `Location` | API requests require HTTPS explicitly |
| `/api/data` | Rejects HTTP requests | `403` | no `Location` | Automated API clients get an explicit failure |

## FAIL criteria

| Failure type | Vulnerable behavior | Why it fails |
| --- | --- | --- |
| API redirect | `POST /api/login` returns `307` to HTTPS | Credentials may already be sent over HTTP |
| Transparent upgrade | `/api/profile` redirects automatically | API clients are unaware of insecure transport |
| Mixed rules | API endpoints follow browser redirect logic | Secrets may leak before the redirect completes |
| Insecure assumptions | HTTP accepted then forwarded to HTTPS | Redirects do not remove the original exposure |

## What PASS looks like

- The browser page redirects to HTTPS.
- API endpoints return `403` on HTTP and do not send a `Location` header.
- Sensitive operations are explicitly denied over HTTP.

## What FAIL looks like

- API endpoints automatically redirect to HTTPS.
- Login and data endpoints send redirects after receiving HTTP requests.
- A `Location` header is present for API requests.
- The client is silently upgraded instead of failing.
