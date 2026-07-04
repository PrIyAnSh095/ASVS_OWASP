# ASVS 4.1.2 Theory

## HTTP, HTTPS, and TLS

HTTP is an application protocol used for web traffic. It sends requests and responses in plaintext, meaning anyone observing the network can read data, including sensitive credentials.

HTTPS is HTTP over TLS. TLS encrypts the request and response, protecting confidentiality and integrity. A secure browser connection begins with `https://`, and the server and client negotiate encryption before exchanging sensitive information.

## Redirects

A redirect is an HTTP response that tells the client to request a different URL. Common redirect status codes include `301`, `302`, and `307`.

For browser-based user-facing pages, redirects from `http://` to `https://` are acceptable because the user knows a secure page is intended. This is often used to improve usability while still encouraging secure access.

## Why browser redirects are acceptable

Browser pages such as `/` or other human-facing pages can safely redirect because the payload is not typically sensitive, and the browser can follow the redirect before user interaction continues.

## Why API redirects are discouraged

APIs are often used by automated clients, service integrations, or mobile applications. Redirecting API requests from HTTP to HTTPS is dangerous because:

- credentials and request bodies may already have been sent over HTTP
- the client does not expect an automatic protocol upgrade
- redirect semantics can change request methods or drop body content

APIs should instead reject HTTP requests and require clients to retry using HTTPS.

## Credential leakage

When a login endpoint automatically redirects from HTTP to HTTPS, the initial request with credentials may have already traversed the network unencrypted. The redirect does not remove that exposure.

## Real-world examples

- User-facing login pages may redirect to `https://` when users type `http://`.
- API clients should be configured to use `https://api.example.com` directly.
- A POST to `http://example.com/api/login` that returns `307` to `https://example.com/api/login` still exposes the original request data.

## Relevant RFCs

- RFC 7231: HTTP/1.1 Semantics and Content
- RFC 2817: Upgrading to TLS Within HTTP/1.1
- RFC 5785: Defining Well-Known URI Prefixes

ASVS 4.1.2 focuses on the difference between acceptable browser redirects and unacceptable API redirects to protect sensitive traffic.
